from __future__ import annotations
import asyncio
import random
from typing import Optional

import reflex as rx
from pydantic import BaseModel

from .data import (
    Player,
    Team,
    ALL_TEAMS,
    draw_random_team,
    get_team_power,
    get_team_by_display_name,
    champion_icon_url,
    reset_pool,
)


class PlayerCard(BaseModel):
    name: str = ""
    role: str = ""
    champion: str = ""
    overall: int = 0
    team: str = ""
    year: int = 0
    icon_url: str = ""


class LeagueRow(BaseModel):
    name: str = ""
    wins: int = 0
    losses: int = 0
    is_player: bool = False


class TeamCard(BaseModel):
    name: str = ""
    year: int = 0
    rarity: str = ""
    description: str = ""
    overall: float = 0.0
    display_name: str = ""
    players: list[PlayerCard] = []


class HeroMapIcon(BaseModel):
    name: str = ""
    role: str = ""
    champion: str = ""
    icon_url: str = ""
    pin_top: str = "50%"
    pin_left: str = "50%"


class Matchup(BaseModel):
    team_a: str = ""
    team_b: str = ""
    score_a: int = 0
    score_b: int = 0
    played: bool = False
    winner: str = ""


class GameEvent(BaseModel):
    time: str = ""
    description: str = ""
    phase: str = ""  # "early" | "mid" | "late" | "finish"


def _player_to_card(p: Player) -> PlayerCard:
    return PlayerCard(
        name=p.name,
        role=p.role,
        champion=p.champion,
        overall=p.overall,
        team=p.team,
        year=p.year,
        icon_url=champion_icon_url(p.champion),
    )


def _team_to_card(t: Team) -> TeamCard:
    return TeamCard(
        name=t.name,
        year=t.year,
        rarity=t.rarity,
        description=t.description,
        overall=t.overall,
        display_name=t.display_name,
        players=[_player_to_card(p) for p in t.players],
    )


def _build_schedule(player_team_name: str) -> tuple[list[Matchup], list[list[Matchup]]]:
    """
    Retorna:
      - 7 partidas do jogador (sem resultado)
      - rodadas de confrontos entre outros times (sem resultado ainda)
    """
    opponent_names = [t.display_name for t in ALL_TEAMS if t.display_name != player_team_name]
    chosen = random.sample(opponent_names, min(7, len(opponent_names)))

    player_matches = []
    for opp in chosen:
        player_matches.append(Matchup(team_a=player_team_name, team_b=opp))

    # Round-robin entre os 7 outros times → 6 rodadas
    teams = list(chosen)
    n = len(teams)
    fixed = teams[0]
    rotating = teams[1:]
    rounds = []

    for _ in range(n - 1):
        matches = []
        matches.append((fixed, rotating[0]))
        for i in range(1, (n - 1) // 2 + 1):
            if i < len(rotating) - i:
                matches.append((rotating[i], rotating[len(rotating) - i]))
        rotating = [rotating[-1]] + rotating[:-1]

        round_list = []
        for a, b in matches:
            round_list.append(Matchup(team_a=a, team_b=b))
        rounds.append(round_list)

    return player_matches, rounds


class GameState(rx.State):
    screen: str = "home"

    # Home hero map — keyed by ddragon URL-safe champion name
    HERO_CHAMPIONS_BY_ROLE: dict[str, list[str]] = {
        "Top": ["Garen", "Darius", "Renekton", "Camille", "Fiora", "Illaoi", "Sett", "Mordekaiser", "Aatrox", "Shen", "Jax", "Riven", "Volibear", "Quinn", "Malphite", "Yasuo", "Poppy", "Udyr"],
        "Jungle": ["LeeSin", "Elise", "JarvanIV", "RekSai", "Viego", "XinZhao", "Graves", "Nidalee", "Ekko", "Hecarim", "Rammus", "Warwick", "Nocturne", "Shaco", "Khazix", "Kindred", "Zac", "Amumu", "Kayn", "MasterYi"],
        "Mid": ["Syndra", "Orianna", "Ahri", "Azir", "Leblanc", "Cassiopeia", "Viktor", "Zed", "Corki", "Ryze", "Lux", "Diana", "Annie", "TwistedFate", "Veigar", "Akali", "Qiyana", "Sylas", "Galio", "Malzahar"],
        "ADC": ["Jinx", "Ezreal", "Vayne", "Lucian", "Varus", "Tristana", "Ashe", "Kaisa", "Xayah", "Caitlyn", "Draven", "MissFortune", "Sivir", "Aphelios", "Kalista", "Senna", "Zeri", "Samira", "Twitch", "KogMaw"],
        "Support": ["Thresh", "Leona", "Nautilus", "Lulu", "Blitzcrank", "Alistar", "Morgana", "Janna", "Soraka", "Braum", "Rakan", "Karma", "Nami", "Zyra", "Yuumi", "Rell", "Renata", "Taric", "Sona", "Pyke"],
    }
    HERO_PIN_POSITIONS: dict[str, tuple[str, str]] = {
        "Top": ("22%", "25%"),
        "Jungle": ("32%", "41%"),
        "Mid": ("49%", "47%"),
        "ADC": ("70%", "67%"),
        "Support": ("81%", "58%"),
    }
    SMALL_PIN_POSITIONS: dict[str, tuple[str, str]] = {
        "Top": ("20%", "23%"),
        "Jungle": ("28%", "40%"),
        "Mid": ("48%", "46%"),
        "ADC": ("72%", "69%"),
        "Support": ("84%", "59%"),
    }
    LEAGUE_PIN_POSITIONS: dict[str, tuple[str, str]] = {
        "Top": ("16%", "23%"),
        "Jungle": ("29%", "40%"),
        "Mid": ("48%", "46%"),
        "ADC": ("72%", "69%"),
        "Support": ("84%", "59%"),
    }
    hero_map_icons: list[HeroMapIcon] = []

    def _randomize_hero_map(self):
        icons = []
        for role, champions in self.HERO_CHAMPIONS_BY_ROLE.items():
            champ = random.choice(champions)
            pos = self.HERO_PIN_POSITIONS.get(role, ("50%", "50%"))
            icons.append(HeroMapIcon(
                name=champ,
                role=role,
                champion=champ,
                icon_url=f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{champ}.png",
                pin_top=pos[0],
                pin_left=pos[1],
            ))
        self.hero_map_icons = icons

    def on_load(self):
        """Called on page load — randomize hero map champions."""
        self._randomize_hero_map()

    # Draft
    current_draft_team: TeamCard = TeamCard()
    drafted_players: list[PlayerCard] = []
    draft_round: int = 0
    reroll_used: bool = False
    selected_from_current_team: bool = False
    roles_order: list[str] = ["Top", "Jungle", "Mid", "ADC", "Support"]
    draft_map_icons: list[HeroMapIcon] = []
    selected_pin_idx: int = -1
    team_name_input: str = "Meu Time"

    # League
    player_team_name: str = "Meu Time"
    league_schedule: list[Matchup] = []
    league_rounds: list[list[Matchup]] = []
    league_round_index: int = 0

    # Match
    match_events: list[GameEvent] = []
    events_shown: int = 0
    match_in_progress: bool = False
    match_speed: int = 1
    current_match_team_a: str = ""
    current_match_team_b: str = ""
    current_match_score_a: int = 0
    current_match_score_b: int = 0

    # Playoffs
    playoff_bracket: list[Matchup] = []
    playoff_round: int = 0
    champion_team: str = ""

    # --- Computed Vars ---

    @rx.var
    def draft_complete(self) -> bool:
        return self.draft_round >= 5

    @rx.var
    def drafted_roles(self) -> list[str]:
        """Roles que ja foram preenchidas."""
        return [p.role for p in self.drafted_players]

    @rx.var
    def drafted_slots(self) -> list[PlayerCard]:
        """5 slots ordenados por role (Top, Jungle, Mid, ADC, Support)."""
        mapping = {p.role: p for p in self.drafted_players}
        order = ["Top", "Jungle", "Mid", "ADC", "Support"]
        return [mapping.get(r, PlayerCard()) for r in order]

    @rx.var
    def team_overall(self) -> str:
        """Overall medio do time draftado."""
        if not self.drafted_players:
            return "0"
        total = sum(p.overall for p in self.drafted_players)
        return str(round(total / len(self.drafted_players)))

    @rx.var
    def league_wins(self) -> int:
        return sum(1 for m in self.league_schedule if m.played and m.winner == self.player_team_name)

    @rx.var
    def league_losses(self) -> int:
        return sum(1 for m in self.league_schedule if m.played and m.winner != "" and m.winner != self.player_team_name)

    @rx.var
    def league_complete(self) -> bool:
        return all(m.played for m in self.league_schedule) and len(self.league_schedule) > 0

    @rx.var
    def last_match_winner(self) -> str:
        if not self.league_schedule:
            return ""
        for m in reversed(self.league_schedule):
            if m.played:
                return m.winner
        return ""

    @rx.var
    def next_opponent(self) -> str:
        """Proximo adversario nao jogado."""
        for m in self.league_schedule:
            if not m.played:
                opp = m.team_b if m.team_a == self.player_team_name else m.team_a
                return opp
        return ""

    @rx.var
    def league_table(self) -> list[LeagueRow]:
        """Tabela de classificacao: 10 times ordenados por vitorias."""
        all_teams = set()
        all_teams.add(self.player_team_name)
        for m in self.league_schedule:
            all_teams.add(m.team_a)
            all_teams.add(m.team_b)

        table = []
        for team_name in all_teams:
            wins = 0
            losses = 0
            for m in self.league_schedule:
                if not m.played:
                    continue
                if m.winner == team_name:
                    wins += 1
                elif team_name in (m.team_a, m.team_b):
                    losses += 1
            table.append(LeagueRow(
                name=team_name,
                wins=wins,
                losses=losses,
                is_player=team_name == self.player_team_name,
            ))

        table.sort(key=lambda x: x.wins, reverse=True)
        return table

    # --- Draft Handlers ---

    def _draw_next_team(self):
        t = draw_random_team()
        self.current_draft_team = _team_to_card(t)

    def start_game(self):
        self._randomize_hero_map()
        self.screen = "home"

    def init_draft(self):
        self.drafted_players = []
        self.draft_round = 0
        self.reroll_used = False
        self.selected_from_current_team = False
        self.selected_pin_idx = -1
        self.draft_map_icons = []
        self.team_name_input = "Meu Time"
        reset_pool()
        self._draw_next_team()
        self.screen = "draft"

    def select_player(self, player: PlayerCard):
        # Só pode selecionar 1 jogador por time sorteado
        if self.selected_from_current_team:
            return
        if self.draft_round >= 5:
            return
        already_taken = [p.role for p in self.drafted_players]
        if player.role in already_taken:
            return

        self.drafted_players.append(player)
        self.draft_round += 1
        self.selected_from_current_team = True

        # Adiciona pin no mapa do draft
        champ_name = player.champion
        pos = self.SMALL_PIN_POSITIONS.get(player.role, ("50%", "50%"))
        new_icon = HeroMapIcon(
            name=player.name,
            role=player.role,
            champion=champ_name,
            icon_url=f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{champ_name}.png",
            pin_top=pos[0],
            pin_left=pos[1],
        )
        self.draft_map_icons = self.draft_map_icons + [new_icon]

        if self.draft_round >= 5:
            # Não chama init_league automaticamente, aguarda o botão
            pass

    def next_team(self):
        """Sorteia o próximo time (acionado pelo botão PRÓXIMO TIME)."""
        if self.draft_round >= 5:
            return
        self.selected_from_current_team = False
        self.selected_pin_idx = -1
        self._draw_next_team()

    def reroll(self):
        if self.reroll_used:
            return
        self.reroll_used = True
        self.selected_from_current_team = False
        self.selected_pin_idx = -1
        self._draw_next_team()

    def toggle_pin_info(self, idx: int):
        if self.selected_pin_idx == idx:
            self.selected_pin_idx = -1
        else:
            self.selected_pin_idx = idx

    def set_team_name(self, name: str):
        self.team_name_input = name

    # --- League Handlers ---

    def init_league(self):
        # Usa o nome digitado pelo jogador ou fallback
        name = self.team_name_input.strip()
        if not name:
            name = "Meu Time"
        self.player_team_name = name

        player_matches, rounds = _build_schedule(self.player_team_name)
        self.league_schedule = player_matches
        self.league_rounds = rounds
        self.league_round_index = 0
        # Recalcula pins com posições da liga
        league_icons = []
        for p in self.drafted_players:
            champ_name = p.champion
            pos = self.LEAGUE_PIN_POSITIONS.get(p.role, ("50%", "50%"))
            league_icons.append(HeroMapIcon(
                name=p.name,
                role=p.role,
                champion=champ_name,
                icon_url=f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{champ_name}.png",
                pin_top=pos[0],
                pin_left=pos[1],
            ))
        self.draft_map_icons = league_icons
        self.playoff_bracket = []
        self.playoff_round = 0
        self.champion_team = ""
        self.screen = "league"

    def _reveal_round(self):
        """Revela a proxima rodada de confrontos entre outros times com resultados."""
        if self.league_round_index >= len(self.league_rounds):
            return
        round_matches = self.league_rounds[self.league_round_index]
        self.league_round_index += 1
        for m in round_matches:
            winner = m.team_a if random.random() < 0.5 else m.team_b
            score_a = 1 if winner == m.team_a else 0
            score_b = 1 if winner == m.team_b else 0
            self.league_schedule.append(Matchup(
                team_a=m.team_a, team_b=m.team_b,
                score_a=score_a, score_b=score_b,
                played=True, winner=winner,
            ))

    def start_match(self):
        # Find first unplayed matchup
        for m in self.league_schedule:
            if not m.played:
                self.current_match_team_a = m.team_a
                self.current_match_team_b = m.team_b
                self.current_match_score_a = 0
                self.current_match_score_b = 0
                self.match_events = []
                self.events_shown = 0
                self.match_speed = 1
                self.match_in_progress = False
                self.screen = "match"
                return

    @rx.event(background=True)
    async def run_match_simulation(self):
        async with self:
            self.match_in_progress = True

        # Calculate probabilities
        power_a = get_team_power(self.current_match_team_a)
        power_b = get_team_power(self.current_match_team_b)
        total = power_a + power_b
        prob_a = power_a / total

        # Generate events
        events = []
        minutes = [3, 8, 12, 18, 22, 28, 32]

        # Early game (first blood, ganks)
        if random.random() < 0.7:
            killer = "A" if random.random() < prob_a else "B"
            events.append(GameEvent(
                time="3:00",
                description=f"First Blood! {'Seu time' if killer == 'A' else 'Time adversário'} abriu o placar!",
                phase="early",
            ))
        else:
            events.append(GameEvent(
                time="5:00",
                description="Laning phase tranquila, sem kills até o momento.",
                phase="early",
            ))

        # Mid game (objectives, team fights)
        mid_events_count = random.randint(2, 3)
        for i in range(mid_events_count):
            winner = "A" if random.random() < prob_a else "B"
            team_name = "Seu time" if winner == "A" else "Time adversário"
            events.append(GameEvent(
                time=f"{minutes[2 + i]}:00",
                description=f"{team_name} venceu uma team fight e garantiu objetivo!",
                phase="mid",
            ))

        # Late game (baron, decisive fights)
        late_winner = "A" if random.random() < prob_a else "B"
        late_name = "Seu time" if late_winner == "A" else "Time adversário"
        events.append(GameEvent(
            time="28:00",
            description=f"{late_name} abateu o Barão Nashor!",
            phase="late",
        ))

        # Determine final winner
        final_winner = "A" if random.random() < prob_a else "B"
        final_name = "Seu time" if final_winner == "A" else "Time adversário"
        score_a = 0
        score_b = 0
        if final_winner == "A":
            score_a = 1
        else:
            score_b = 1

        events.append(GameEvent(
            time="35:00",
            description=f"{final_name} destruiu o Nexus e venceu a partida!",
            phase="finish",
        ))

        async with self:
            self.match_events = events

        # Reveal events one by one
        speed_map = {1: 1.2, 2: 0.6, 3: 0.2}
        delay = speed_map.get(self.match_speed, 1.2)

        for i in range(len(events)):
            await asyncio.sleep(delay)
            async with self:
                self.events_shown = i + 1
                # Update scores progressively
                if events[i].phase == "finish":
                    self.current_match_score_a = score_a
                    self.current_match_score_b = score_b

        # Final update to league schedule
        async with self:
            winner_name = (
                self.current_match_team_a if final_winner == "A"
                else self.current_match_team_b
            )
            # Update the corresponding matchup
            new_schedule = []
            for m in self.league_schedule:
                if not m.played and m.team_a == self.current_match_team_a and m.team_b == self.current_match_team_b:
                    new_schedule.append(Matchup(
                        team_a=m.team_a,
                        team_b=m.team_b,
                        score_a=score_a,
                        score_b=score_b,
                        played=True,
                        winner=winner_name,
                    ))
                else:
                    new_schedule.append(m)
            self.league_schedule = new_schedule
            self._reveal_round()
            self.match_in_progress = False
            self.screen = "result"

    def set_speed(self, speed: int):
        self.match_speed = speed

    def go_to_league(self):
        self.screen = "league"

    # --- Playoffs ---

    def init_playoffs(self):
        # Top 3 opponents by power + player team
        opponents = []
        for m in self.league_schedule:
            opp_name = m.team_b if m.team_a == self.player_team_name else m.team_a
            if opp_name not in opponents and opp_name != self.player_team_name:
                opponents.append(opp_name)

        # Sort by team power descending, take top 3
        opponents.sort(key=lambda name: get_team_power(name), reverse=True)
        top_3 = opponents[:3]
        all_teams = [self.player_team_name] + top_3
        random.shuffle(all_teams)

        self.playoff_bracket = [
            Matchup(team_a=all_teams[0], team_b=all_teams[1]),
            Matchup(team_a=all_teams[2], team_b=all_teams[3]),
        ]
        self.playoff_round = 0
        self.champion_team = ""
        self.screen = "playoffs"

    @rx.event(background=True)
    async def play_playoff_match(self, idx: int):
        async with self:
            if idx >= len(self.playoff_bracket):
                return
            matchup = self.playoff_bracket[idx]
            if matchup.played:
                return
            self.match_in_progress = True
            self.current_match_team_a = matchup.team_a
            self.current_match_team_b = matchup.team_b
            self.current_match_score_a = 0
            self.current_match_score_b = 0

        power_a = get_team_power(matchup.team_a)
        power_b = get_team_power(matchup.team_b)
        total = power_a + power_b
        prob_a = power_a / total

        winner = "A" if random.random() < prob_a else "B"
        score_a = 1 if winner == "A" else 0
        score_b = 1 if winner == "B" else 0
        winner_name = matchup.team_a if winner == "A" else matchup.team_b

        await asyncio.sleep(1.5)

        async with self:
            new_bracket = list(self.playoff_bracket)
            new_bracket[idx] = Matchup(
                team_a=matchup.team_a,
                team_b=matchup.team_b,
                score_a=score_a,
                score_b=score_b,
                played=True,
                winner=winner_name,
            )
            self.playoff_bracket = new_bracket
            self.match_in_progress = False

            # Check if both semis done
            semi_done = all(m.played for m in self.playoff_bracket[:2])
            if semi_done and len(self.playoff_bracket) == 2:
                # Create final
                final_a = self.playoff_bracket[0].winner
                final_b = self.playoff_bracket[1].winner
                self.playoff_bracket.append(Matchup(team_a=final_a, team_b=final_b))
                self.playoff_round = 1
            elif semi_done and len(self.playoff_bracket) == 3:
                # Final was just played
                self.champion_team = winner_name

    # --- Reset ---

    def restart(self):
        self._randomize_hero_map()
        self.screen = "home"
        self.current_draft_team = TeamCard()
        self.drafted_players = []
        self.draft_round = 0
        self.reroll_used = False
        self.selected_from_current_team = False
        self.selected_pin_idx = -1
        self.draft_map_icons = []
        self.team_name_input = "Meu Time"
        self.player_team_name = "Meu Time"
        self.league_schedule = []
        self.league_rounds = []
        self.league_round_index = 0
        self.match_events = []
        self.events_shown = 0
        self.match_in_progress = False
        self.match_speed = 1
        self.current_match_team_a = ""
        self.current_match_team_b = ""
        self.current_match_score_a = 0
        self.current_match_score_b = 0
        self.playoff_bracket = []
        self.playoff_round = 0
        self.champion_team = ""
        reset_pool()
