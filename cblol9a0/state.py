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


class TeamCard(BaseModel):
    name: str = ""
    year: int = 0
    rarity: str = ""
    description: str = ""
    overall: float = 0.0
    display_name: str = ""
    players: list[PlayerCard] = []


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


def _build_schedule(player_team_name: str) -> list[Matchup]:
    """Gera 7 partidas da fase de liga contra times aleatórios."""
    opponent_names = [t.display_name for t in ALL_TEAMS if t.display_name != player_team_name]
    chosen = random.sample(opponent_names, min(7, len(opponent_names)))
    schedule = []
    for opp in chosen:
        schedule.append(Matchup(team_a=player_team_name, team_b=opp))
    return schedule


class GameState(rx.State):
    screen: str = "home"

    # Draft
    current_draft_team: TeamCard = TeamCard()
    drafted_players: list[PlayerCard] = []
    draft_round: int = 0
    reroll_used: bool = False
    roles_order: list[str] = ["Top", "Jungle", "Mid", "ADC", "Support"]

    # League
    player_team_name: str = "Meu Time"
    league_schedule: list[Matchup] = []

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

    # --- Draft Handlers ---

    def _draw_next_team(self):
        t = draw_random_team()
        self.current_draft_team = _team_to_card(t)

    def start_game(self):
        self.screen = "home"

    def init_draft(self):
        self.drafted_players = []
        self.draft_round = 0
        self.reroll_used = False
        reset_pool()
        self._draw_next_team()
        self.screen = "draft"

    def select_player(self, player: PlayerCard):
        # Aceita qualquer role que ainda nao foi preenchida
        if self.draft_round >= 5:
            return
        # Verifica se a role ja foi preenchida
        already_taken = [p.role for p in self.drafted_players]
        if player.role in already_taken:
            return

        self.drafted_players.append(player)
        self.draft_round += 1

        if self.draft_round >= 5:
            self.init_league()
        else:
            self._draw_next_team()

    def reroll(self):
        if self.reroll_used:
            return
        self.reroll_used = True
        self._draw_next_team()

    # --- League Handlers ---

    def init_league(self):
        # Build team name from drafted players
        team_names = set(p.team for p in self.drafted_players)
        if len(team_names) > 1:
            self.player_team_name = "Misto All-Stars"
        elif len(team_names) == 1:
            self.player_team_name = list(team_names)[0]
        else:
            self.player_team_name = "Meu Time"

        self.league_schedule = _build_schedule(self.player_team_name)
        self.playoff_bracket = []
        self.playoff_round = 0
        self.champion_team = ""
        self.screen = "league"

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
        self.screen = "home"
        self.current_draft_team = TeamCard()
        self.drafted_players = []
        self.draft_round = 0
        self.reroll_used = False
        self.player_team_name = "Meu Time"
        self.league_schedule = []
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
