from __future__ import annotations

import reflex as rx

from .state import GameState, PlayerCard, Matchup, GameEvent

# Paleta - Broadcast eSports: azul marinho + dourado + branco
BG = "#0B1121"
BG_CARD = "#131B2F"
BG_SURFACE = "#1A2540"
GOLD = "#C9A84C"
GOLD_L = "#E0C76E"
WHITE = "#FFFFFF"
GRAY = "#8B93A5"
GRAY_D = "#5A6378"
GREEN = "#2D6A4F"
GREEN_L = "#3CB371"
RED = "#DC2626"
BLUE_ACC = "#3B82F6"
BORDER = "#1E2D4A"
BORDER_L = "#263554"

ROLE_ICONS = {
    "Top": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/spell/SummonerTeleport.png",
    "Jungle": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/spell/SummonerSmite.png",
    "Mid": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/spell/SummonerDot.png",
    "ADC": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/perk-images/StatMods/StatModsAttackSpeedIcon.png",
    "Support": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/spell/SummonerGuardian.png",
}

HERO_CHAMPIONS = {
    "Top": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Garen.png",
    "Jungle": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/LeeSin.png",
    "Mid": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Syndra.png",
    "ADC": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Jinx.png",
    "Support": "https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/Thresh.png",
}

RARITY_COLORS = {
    "Legendary": ("#3D2E0A", "#F59E0B", "#FEF3C7"),
    "Historic": ("#1E3A5F", "#3B82F6", "#DBEAFE"),
    "Common": ("#1F2937", "#9CA3AF", "#F3F4F6"),
}

PHASE_COLORS = {
    "early": "#3B82F6",
    "mid": "#F59E0B",
    "late": "#F97316",
    "finish": GOLD,
}

ROLE_ORDER = ["Top", "Jungle", "Mid", "ADC", "Support"]


# ====== NAVBAR ======

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.text("CBLOL", font_size="1.05rem", font_weight="800", color=WHITE,
                         letter_spacing="0.02em"),
                rx.text("9A0", font_size="0.7rem", font_weight="900", color=BG,
                         bg=GOLD, px="0.35rem", py="0.1rem", border_radius="4px"),
                gap="0.3rem",
                align="center",
            ),
            rx.spacer(),
            rx.cond(
                GameState.screen == "draft",
                rx.hstack(
                    rx.text(
                        GameState.draft_round.to_string(),
                        font_size="0.85rem", font_weight="800", color=GOLD,
                    ),
                    rx.text("/5 preenchidas", font_size="0.7rem", color=GRAY),
                    gap="0.25rem",
                    align="center",
                    bg=BG_SURFACE,
                    px="0.7rem",
                    py="0.3rem",
                    border_radius="6px",
                ),
                rx.box(),
            ),
            rx.spacer(),
            rx.cond(
                GameState.screen != "home",
                rx.button(
                    "REINICIAR",
                    on_click=GameState.restart,
                    variant="outline",
                    size="1",
                    color=GRAY_D,
                    bg="transparent",
                    font_size="0.65rem",
                    font_weight="700",
                    letter_spacing="0.04em",
                ),
                rx.box(),
            ),
            width="100%",
            align="center",
            px="2rem",
            py="0.55rem",
        ),
        bg=BG,
        position="fixed",
        top="0",
        z_index="50",
        width="100%",
        height="56px",
        border_bottom="1px solid " + BORDER,
    )


# ====== HOME VIEW ======

def _hero_champion(role: str, url: str) -> rx.Component:
    return rx.flex(
        rx.image(
            src=url,
            width="56px",
            height="56px",
            border_radius="50%",
            border="2px solid " + GOLD,
        ),
        rx.text(role, font_size="0.65rem", color=GRAY_D, font_weight="600", mt="0.3rem",
                 letter_spacing="0.03em", text_transform="uppercase"),
        direction="column",
        align="center",
    )


def _step_card(num: str, title: str, desc: str) -> rx.Component:
    return rx.box(
        rx.text(num, font_size="2.2rem", font_weight="900", color=GOLD,
                 line_height="1"),
        rx.text(title, font_weight="700", font_size="0.9rem", color=WHITE, mt="0.4rem",
                 letter_spacing="0.01em"),
        rx.text(desc, font_size="0.72rem", color=GRAY_D, mt="0.2rem", line_height="1.4"),
        bg=BG_CARD,
        border="1px solid " + BORDER,
        border_radius="10px",
        p="1.25rem",
        width="190px",
        min_h="155px",
    )


def home_view() -> rx.Component:
    return rx.box(
        # Hero
        rx.box(
            rx.text(
                "MONTE O TIME DOS",
                font_weight="400",
                font_size="0.85rem",
                color=GRAY,
                text_align="center",
                letter_spacing="0.1em",
            ),
            rx.text(
                "SONHOS DO CBLOL",
                font_weight="900",
                font_size="3rem",
                color=GOLD,
                text_align="center",
                line_height="1.1",
                letter_spacing="-0.01em",
            ),
            rx.text(
                "Drafte jogadores historicos, dispute a liga e seja campeao",
                font_size="0.85rem",
                color=GRAY_D,
                text_align="center",
                mt="0.8rem",
            ),
            rx.flex(
                _hero_champion("Top", HERO_CHAMPIONS["Top"]),
                _hero_champion("Jungle", HERO_CHAMPIONS["Jungle"]),
                _hero_champion("Mid", HERO_CHAMPIONS["Mid"]),
                _hero_champion("ADC", HERO_CHAMPIONS["ADC"]),
                _hero_champion("Support", HERO_CHAMPIONS["Support"]),
                gap="1.8rem",
                justify="center",
                mt="2.5rem",
                flex_wrap="wrap",
            ),
            rx.button(
                "INICIAR DRAFT",
                on_click=GameState.init_draft,
                bg=GOLD,
                color=BG,
                font_weight="800",
                font_size="0.9rem",
                px="2.5rem",
                py="0.9rem",
                border_radius="8px",
                mt="2.5rem",
                cursor="pointer",
                letter_spacing="0.04em",
                _hover={"bg": GOLD_L, "transform": "translateY(-1px)"},
            ),
            py="5rem",
            px="2rem",
            display="flex",
            flex_direction="column",
            align_items="center",
            bg=BG,
            padding_top="120px",
            padding_bottom="80px",
            border_bottom="1px solid " + BORDER,
        ),
        # How it works
        rx.box(
            rx.text("COMO FUNCIONA", font_size="0.75rem", font_weight="700", color=GRAY_D,
                     text_align="center", letter_spacing="0.08em", mb="2rem"),
            rx.flex(
                _step_card("1", "Escolha", "5 rounds de draft. Escolha qualquer jogador do time sorteado."),
                _step_card("2", "Reroll", "Use seu reroll unico para trocar de time."),
                _step_card("3", "Liga", "Enfrente 7 adversarios na fase de pontos."),
                _step_card("4", "Playoffs", "Top 4 avancam para o mata-mata."),
                _step_card("5", "Titulo", "Venca a Grande Final!"),
                gap="1rem",
                justify="center",
                flex_wrap="wrap",
                max_w="1050px",
                mx="auto",
            ),
            py="4rem",
            px="2rem",
            bg=BG,
        ),
        # Footer
        rx.box(
            rx.flex(
                rx.box(
                    rx.hstack(
                        rx.text("CBLOL", font_weight="800", color=WHITE, font_size="0.9rem"),
                        rx.text("9A0", font_size="0.65rem", font_weight="800", color=BG,
                                 bg=GOLD, px="0.3rem", py="0.05rem", border_radius="3px"),
                        gap="0.2rem",
                        align="center",
                    ),
                    rx.text("Jogo de draft historico do cenario brasileiro de League of Legends.",
                             font_size="0.7rem", color=GRAY_D, mt="0.4rem", line_height="1.5"),
                    flex="1.5",
                    min_w="180px",
                ),
                rx.box(
                    rx.text("JOGO", font_weight="600", color=WHITE, font_size="0.72rem",
                             letter_spacing="0.04em"),
                    rx.text("Draft", font_size="0.7rem", color=GRAY_D, mt="0.3rem"),
                    rx.text("Liga", font_size="0.7rem", color=GRAY_D),
                    rx.text("Playoffs", font_size="0.7rem", color=GRAY_D),
                    min_w="80px",
                ),
                rx.box(
                    rx.text("RARIDADES", font_weight="600", color=WHITE, font_size="0.72rem",
                             letter_spacing="0.04em"),
                    rx.text("Legendary", font_size="0.7rem", color=GRAY_D, mt="0.3rem"),
                    rx.text("Historic", font_size="0.7rem", color=GRAY_D),
                    rx.text("Common", font_size="0.7rem", color=GRAY_D),
                    min_w="80px",
                ),
                rx.box(
                    rx.text("CREDITOS", font_weight="600", color=WHITE, font_size="0.72rem",
                             letter_spacing="0.04em"),
                    rx.text("CBLOL 2012-2024", font_size="0.7rem", color=GRAY_D, mt="0.3rem"),
                    rx.text("Data Dragon CDN", font_size="0.7rem", color=GRAY_D),
                    rx.text("Reflex Framework", font_size="0.7rem", color=GRAY_D),
                    min_w="80px",
                ),
                gap="2rem",
                flex_wrap="wrap",
                max_w="900px",
                mx="auto",
                py="2.5rem",
                px="2rem",
            ),
            rx.box(
                rx.text("2025 CBLOL 9A0. League of Legends e propriedade da Riot Games.",
                         font_size="0.65rem", color=GRAY_D, text_align="center"),
                border_top="1px solid " + BORDER,
                mt="1.5rem",
                pt="1.25rem",
            ),
            bg=BG_CARD,
            width="100%",
        ),
        width="100%",
    )


# ====== DRAFT VIEW ======

def _draft_role_slot(role: str, idx: int) -> rx.Component:
    is_filled = GameState.draft_round > idx
    is_current = GameState.draft_round == idx
    empty = PlayerCard()

    drafted = rx.cond(is_filled, GameState.drafted_players[idx], empty)

    return rx.box(
        rx.flex(
            rx.image(
                src=rx.cond(is_filled, drafted.icon_url, ROLE_ICONS.get(role, "")),
                width="28px",
                height="28px",
                border_radius="6px",
            ),
            rx.box(
                rx.text(
                    rx.cond(is_filled, drafted.name, role),
                    font_size="0.78rem",
                    font_weight=rx.cond(is_filled, "700", "500"),
                    color=rx.cond(is_filled, WHITE, GRAY),
                ),
                rx.cond(
                    is_filled,
                    rx.text(
                        drafted.champion + "  OVR " + drafted.overall.to_string(),
                        font_size="0.65rem",
                        color=GRAY_D,
                    ),
                    rx.text(
                        rx.cond(is_current, "disponivel", "aguardando"),
                        font_size="0.65rem",
                        color=rx.cond(is_current, GOLD, GRAY_D),
                    ),
                ),
                flex="1",
            ),
            rx.cond(
                is_filled,
                rx.text("OK", font_size="0.7rem", font_weight="800", color=GREEN_L),
                rx.box(),
            ),
            gap="0.5rem",
            align="center",
            width="100%",
        ),
        p="0.55rem 0.7rem",
        bg=rx.cond(is_filled, BG_SURFACE, rx.cond(is_current, "#1A2540", BG_CARD)),
        border="1px solid " + rx.cond(is_current, GOLD, rx.cond(is_filled, BORDER_L, BORDER)),
        border_radius="8px",
        width="100%",
    )


def _draft_player_row(p: PlayerCard, idx: int) -> rx.Component:
    role = p.role
    # Check if this role is already filled — compare role string to each drafted player's role
    is_filled = GameState.draft_round > idx
    is_current = GameState.draft_round == idx

    return rx.box(
        rx.flex(
            rx.image(
                src=p.icon_url,
                width="36px",
                height="36px",
                border_radius="8px",
                border="2px solid " + rx.cond(is_current, GOLD, "transparent"),
            ),
            rx.box(
                rx.text(
                    p.name,
                    font_weight="700",
                    font_size="0.85rem",
                    color=rx.cond(is_filled, GRAY_D, WHITE),
                ),
                rx.text(
                    p.champion,
                    font_size="0.7rem",
                    color=rx.cond(is_filled, GRAY_D, GRAY),
                ),
                flex="1",
            ),
            rx.box(
                rx.text(p.role, font_size="0.65rem", font_weight="700", color=rx.cond(is_filled, GRAY_D, GRAY),
                         text_align="center",
                         bg=rx.cond(is_filled, BG_SURFACE, BG),
                         px="0.4rem", py="0.15rem", border_radius="4px"),
                min_w="70px",
            ),
            rx.text(
                p.overall.to_string(),
                font_weight="900",
                font_size="1rem",
                color=rx.cond(is_filled, GRAY_D, GOLD),
            ),
            gap="0.6rem",
            align="center",
            width="100%",
        ),
        p="0.55rem 0.7rem",
        bg=rx.cond(is_filled, BG_CARD, rx.cond(is_current, BG_SURFACE, BG_CARD)),
        border_radius="6px",
        opacity=rx.cond(is_filled, "0.35", "1"),
        cursor=rx.cond(is_filled, "not-allowed", rx.cond(is_current, "pointer", "default")),
        on_click=rx.cond(is_current, GameState.select_player(p), rx.noop()),
        border_left="3px solid " + rx.cond(is_current, GOLD, "transparent"),
        width="100%",
    )


def _team_card_view() -> rx.Component:
    team = GameState.current_draft_team
    rarity_info = RARITY_COLORS.get("Common", ("#1F2937", "#9CA3AF", "#F3F4F6"))
    r_bg = rarity_info[0]
    r_text = rarity_info[1] if len(rarity_info) > 1 else "#9CA3AF"

    return rx.box(
        # Header
        rx.box(
            rx.flex(
                rx.box(
                    rx.text(team.display_name, font_weight="800", font_size="1.1rem", color=WHITE),
                    rx.text(
                        team.rarity,
                        font_size="0.6rem",
                        font_weight="700",
                        color=r_text,
                        bg=r_bg,
                        px="0.4rem",
                        py="0.1rem",
                        border_radius="3px",
                        letter_spacing="0.04em",
                    ),
                    gap="0.4rem",
                    align="center",
                ),
                rx.text(
                    rx.text("OVR", font_size="0.6rem", color=GRAY_D, letter_spacing="0.05em"),
                    rx.text(
                        team.overall.to_string().split(".")[0],
                        font_weight="900",
                        font_size="1.6rem",
                        color=GOLD,
                        line_height="1",
                    ),
                    gap="0.1rem",
                    display="flex",
                    flex_direction="column",
                    align_items="flex-end",
                ),
                justify="between",
                align="start",
                width="100%",
            ),
            bg=BG_SURFACE,
            p="0.8rem 1rem",
            border_radius="8px 8px 0 0",
        ),
        # Candidates
        rx.box(
            rx.foreach(
                team.players,
                lambda p, i: _draft_player_row(p, i),
            ),
            bg=BG_CARD,
            p="0.4rem 0.5rem",
            gap="0.25rem",
            display="flex",
            flex_direction="column",
        ),
        # Footer — reroll
        rx.box(
            rx.flex(
                rx.button(
                    rx.cond(
                        GameState.reroll_used,
                        "REROLL USADO",
                        "REROLL",
                    ),
                    on_click=GameState.reroll,
                    disabled=GameState.reroll_used,
                    bg=rx.cond(GameState.reroll_used, BG_CARD, BG_SURFACE),
                    color=rx.cond(GameState.reroll_used, GRAY_D, GOLD),
                    font_weight="700",
                    font_size="0.75rem",
                    size="2",
                    border_radius="6px",
                    letter_spacing="0.03em",
                    cursor=rx.cond(GameState.reroll_used, "not-allowed", "pointer"),
                ),
                rx.text(
                    "Escolha qualquer jogador disponivel",
                    font_size="0.7rem",
                    color=GRAY_D,
                ),
                justify="between",
                align="center",
                width="100%",
            ),
            bg=BG_CARD,
            p="0.6rem 1rem",
            border_radius="0 0 8px 8px",
            border_top="1px solid " + BORDER,
        ),
        border_radius="8px",
        overflow="hidden",
        width="100%",
    )


def draft_view() -> rx.Component:
    return rx.flex(
        # Left sidebar — slots
        rx.box(
            rx.text("SEU TIME", font_size="0.65rem", font_weight="700", color=GRAY_D,
                     letter_spacing="0.08em", mb="0.8rem"),
            rx.flex(
                _draft_role_slot("Top", 0),
                _draft_role_slot("Jungle", 1),
                _draft_role_slot("Mid", 2),
                _draft_role_slot("ADC", 3),
                _draft_role_slot("Support", 4),
                direction="column",
                gap="0.4rem",
                width="100%",
            ),
            width="280px",
            bg=BG_CARD,
            border_right="1px solid " + BORDER,
            p="1.25rem",
            height="calc(100vh - 56px)",
            position="sticky",
            top="56px",
        ),
        # Right — team card
        rx.box(
            _team_card_view(),
            flex="1",
            p="1.5rem",
            max_w="560px",
        ),
        width="100%",
        bg=BG,
        padding_top="56px",
        min_height="100vh",
    )


# ====== LEAGUE VIEW ======

def _league_match_row(m: Matchup, idx: int) -> rx.Component:
    is_win = m.winner == GameState.player_team_name
    is_loss = m.played & (m.winner != GameState.player_team_name)

    bg_row = rx.cond(
        is_win, "#0D3320",
        rx.cond(is_loss, "#3B1010", BG_CARD),
    )
    bl = rx.cond(
        is_win, "3px solid " + GREEN,
        rx.cond(is_loss, "3px solid " + RED, "3px solid " + BORDER),
    )

    return rx.box(
        rx.flex(
            rx.text(m.team_a, font_weight="600", font_size="0.8rem", color=WHITE,
                     text_align="right", flex="1"),
            rx.box(
                rx.cond(
                    m.played,
                    rx.text(
                        m.score_a.to_string() + " - " + m.score_b.to_string(),
                        font_weight="800",
                        font_size="1rem",
                        color=GOLD,
                        text_align="center",
                    ),
                    rx.text("VS", font_size="0.7rem", color=GRAY_D, font_weight="600",
                             text_align="center", letter_spacing="0.06em"),
                ),
                min_w="4rem",
                text_align="center",
            ),
            rx.text(m.team_b, font_weight="600", font_size="0.8rem", color=WHITE,
                     text_align="left", flex="1"),
            gap="0.6rem",
            align="center",
            width="100%",
        ),
        p="0.7rem 1rem",
        bg=bg_row,
        border_radius="8px",
        border_left=bl,
        width="100%",
    )


def league_view() -> rx.Component:
    return rx.box(
        rx.text("FASE DE LIGA", font_size="0.7rem", font_weight="700", color=GRAY_D,
                 text_align="center", letter_spacing="0.08em", mb="0.3rem"),
        rx.text(
            GameState.player_team_name,
            font_size="1.3rem",
            font_weight="800",
            color=GOLD,
            text_align="center",
        ),
        # W/L counter
        rx.flex(
            rx.box(
                rx.text("V", font_size="0.6rem", color=GRAY_D, letter_spacing="0.06em"),
                rx.text(GameState.league_wins.to_string(), font_size="1.4rem", font_weight="900", color=GREEN_L),
                text_align="center",
                flex="1",
                bg=BG_CARD,
                border_radius="8px",
                p="0.6rem",
            ),
            rx.box(
                rx.text("D", font_size="0.6rem", color=GRAY_D, letter_spacing="0.06em"),
                rx.text(GameState.league_losses.to_string(), font_size="1.4rem", font_weight="900", color=RED),
                text_align="center",
                flex="1",
                bg=BG_CARD,
                border_radius="8px",
                p="0.6rem",
            ),
            gap="1rem",
            max_w="250px",
            mx="auto",
            mt="0.8rem",
            mb="1.5rem",
        ),
        # Schedule
        rx.box(
            rx.foreach(GameState.league_schedule, lambda m, i: _league_match_row(m, i)),
            gap="0.4rem",
            display="flex",
            flex_direction="column",
            width="100%",
            max_w="550px",
            mx="auto",
        ),
        rx.flex(
            rx.cond(
                GameState.league_complete,
                rx.button(
                    "IR PARA PLAYOFFS",
                    on_click=GameState.init_playoffs,
                    bg=GOLD,
                    color=BG,
                    font_weight="800",
                    font_size="0.8rem",
                    size="3",
                    border_radius="8px",
                    letter_spacing="0.04em",
                ),
                rx.button(
                    "JOGAR PROXIMA PARTIDA",
                    on_click=GameState.start_match,
                    bg=GREEN,
                    color=WHITE,
                    font_weight="800",
                    font_size="0.8rem",
                    size="3",
                    border_radius="8px",
                    letter_spacing="0.04em",
                    disabled=GameState.match_in_progress,
                ),
            ),
            justify="center",
            mt="1.5rem",
            width="100%",
        ),
        max_w="700px",
        mx="auto",
        p="1.5rem",
        bg=BG,
        min_height="100vh",
        padding_top="72px",
    )


# ====== MATCH VIEW ======

def _match_event_row(ev: GameEvent) -> rx.Component:
    pc = PHASE_COLORS.get(ev.phase, GRAY)
    return rx.box(
        rx.flex(
            rx.box(
                rx.text(ev.time, font_size="0.65rem", font_weight="700", color=pc),
                bg=BG_SURFACE,
                px="0.4rem",
                py="0.1rem",
                border_radius="4px",
                min_w="38px",
                text_align="center",
            ),
            rx.box(
                rx.text(ev.phase.upper(), font_size="0.55rem", font_weight="700", color=pc,
                         letter_spacing="0.05em"),
                bg="rgba(0,0,0,0.2)",
                px="0.3rem",
                py="0.08rem",
                border_radius="3px",
            ),
            rx.text(ev.description, font_size="0.75rem", color=GRAY, flex="1"),
            gap="0.5rem",
            align="center",
            width="100%",
        ),
        p="0.5rem 0.7rem",
        bg=BG_CARD,
        border_radius="6px",
        border_left="3px solid " + pc,
        width="100%",
    )


def match_view() -> rx.Component:
    return rx.box(
        # Scoreboard
        rx.box(
            rx.flex(
                rx.box(
                    rx.text(GameState.current_match_team_a, font_weight="700", font_size="0.9rem",
                             color=WHITE, text_align="center"),
                    flex="1",
                ),
                rx.box(
                    rx.text(
                        GameState.current_match_score_a.to_string() + " x " + GameState.current_match_score_b.to_string(),
                        font_weight="900",
                        font_size="2.2rem",
                        color=GOLD,
                        text_align="center",
                        line_height="1",
                    ),
                    rx.cond(
                        GameState.match_in_progress,
                        rx.text("AO VIVO", font_size="0.55rem", font_weight="700", color=RED,
                                 letter_spacing="0.1em", text_align="center"),
                        rx.box(),
                    ),
                    min_w="6rem",
                    text_align="center",
                ),
                rx.box(
                    rx.text(GameState.current_match_team_b, font_weight="700", font_size="0.9rem",
                             color=WHITE, text_align="center"),
                    flex="1",
                ),
                align="center",
                width="100%",
                gap="1rem",
            ),
            bg=BG_SURFACE,
            p="1.5rem",
            border_radius="10px",
            max_w="550px",
            mx="auto",
            mb="1.2rem",
        ),
        # Controls
        rx.flex(
            rx.cond(
                GameState.match_in_progress,
                rx.flex(
                    rx.button(
                        "1x",
                        on_click=GameState.set_speed(1),
                        size="1",
                        variant="soft",
                        bg=rx.cond(GameState.match_speed == 1, GOLD, BG_SURFACE),
                        color=rx.cond(GameState.match_speed == 1, BG, GRAY),
                        font_weight="700",
                    ),
                    rx.button(
                        "2x",
                        on_click=GameState.set_speed(2),
                        size="1",
                        variant="soft",
                        bg=rx.cond(GameState.match_speed == 2, GOLD, BG_SURFACE),
                        color=rx.cond(GameState.match_speed == 2, BG, GRAY),
                        font_weight="700",
                    ),
                    rx.button(
                        "3x",
                        on_click=GameState.set_speed(3),
                        size="1",
                        variant="soft",
                        bg=rx.cond(GameState.match_speed == 3, GOLD, BG_SURFACE),
                        color=rx.cond(GameState.match_speed == 3, BG, GRAY),
                        font_weight="700",
                    ),
                    gap="0.25rem",
                ),
                rx.button(
                    "INICIAR PARTIDA",
                    on_click=GameState.run_match_simulation,
                    bg=GREEN,
                    color=WHITE,
                    font_weight="800",
                    font_size="0.8rem",
                    size="3",
                    border_radius="8px",
                    letter_spacing="0.04em",
                ),
            ),
            justify="center",
            mb="1.2rem",
            gap="0.5rem",
        ),
        # Events feed
        rx.box(
            rx.cond(
                GameState.match_in_progress | (GameState.events_shown > 0),
                rx.box(
                    rx.foreach(
                        GameState.match_events[:GameState.events_shown],
                        lambda ev: _match_event_row(ev),
                    ),
                    gap="0.35rem",
                    display="flex",
                    flex_direction="column",
                    width="100%",
                ),
                rx.box(),
            ),
            max_w="550px",
            mx="auto",
            width="100%",
        ),
        rx.cond(
            GameState.match_in_progress,
            rx.text("Partida em andamento...", font_size="0.7rem", color=GRAY_D,
                     text_align="center", mt="0.5rem"),
            rx.box(),
        ),
        max_w="700px",
        mx="auto",
        p="1.5rem",
        bg=BG,
        min_height="100vh",
        padding_top="72px",
    )


# ====== RESULT VIEW ======

def result_view() -> rx.Component:
    is_win = GameState.last_match_winner == GameState.player_team_name
    return rx.box(
        rx.flex(
            rx.text(
                rx.cond(is_win, "TROFEU", "X"),
                font_size="4rem",
            ),
            rx.text(
                rx.cond(is_win, "VITORIA", "DERROTA"),
                font_size="3.5rem",
                font_weight="900",
                color=rx.cond(is_win, GOLD, RED),
                letter_spacing="-0.01em",
            ),
            rx.text(
                GameState.last_match_winner,
                font_size="1.1rem",
                font_weight="600",
                color=WHITE,
                mt="0.3rem",
            ),
            rx.text(
                rx.cond(is_win, "Seu time venceu a partida!", "Seu time foi derrotado."),
                font_size="0.8rem",
                color=GRAY_D,
                mt="0.4rem",
            ),
            rx.flex(
                rx.cond(
                    GameState.league_complete,
                    rx.button(
                        "IR PARA PLAYOFFS",
                        on_click=GameState.init_playoffs,
                        bg=GOLD,
                        color=BG,
                        font_weight="800",
                        font_size="0.8rem",
                        size="3",
                        border_radius="8px",
                        letter_spacing="0.04em",
                    ),
                    rx.button(
                        "VOLTAR A LIGA",
                        on_click=GameState.go_to_league,
                        bg=GREEN,
                        color=WHITE,
                        font_weight="800",
                        font_size="0.8rem",
                        size="3",
                        border_radius="8px",
                        letter_spacing="0.04em",
                    ),
                ),
                rx.button(
                    "REINICIAR",
                    on_click=GameState.restart,
                    variant="outline",
                    color=GRAY_D,
                    size="2",
                    border_radius="8px",
                ),
                justify="center",
                gap="0.6rem",
                mt="1.5rem",
            ),
            direction="column",
            align="center",
            p="2rem",
            bg=rx.cond(is_win, "#0D3320", "#3B1010"),
            border_radius="12px",
            max_w="420px",
            width="100%",
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        flex_direction="column",
        min_height="calc(100vh - 56px)",
        bg=BG,
        padding_top="56px",
    )


# ====== PLAYOFFS VIEW ======

def _po_card(m: Matchup, idx: int) -> rx.Component:
    title = rx.cond(idx == 2, "GRANDE FINAL", "SEMIFINAL " + (idx + 1).to_string())
    return rx.box(
        rx.text(title, font_size="0.6rem", font_weight="700", color=GRAY_D,
                 letter_spacing="0.06em", text_align="center", mb="0.5rem"),
        rx.flex(
            rx.text(m.team_a, font_weight=rx.cond(m.played & (m.winner == m.team_a), "700", "500"),
                     font_size="0.8rem",
                     color=rx.cond(m.played & (m.winner == m.team_a), GOLD, WHITE),
                     flex="1", text_align="right"),
            rx.box(
                rx.cond(
                    m.played,
                    rx.text(
                        m.score_a.to_string() + " x " + m.score_b.to_string(),
                        font_weight="800",
                        font_size="0.95rem",
                        color=GOLD,
                    ),
                    rx.text("VS", font_size="0.65rem", color=GRAY_D, font_weight="600",
                             letter_spacing="0.05em"),
                ),
                min_w="3rem",
                text_align="center",
            ),
            rx.text(m.team_b, font_weight=rx.cond(m.played & (m.winner == m.team_b), "700", "500"),
                     font_size="0.8rem",
                     color=rx.cond(m.played & (m.winner == m.team_b), GOLD, WHITE),
                     flex="1", text_align="left"),
            gap="0.5rem",
            align="center",
            width="100%",
        ),
        rx.cond(
            m.played,
            rx.text("Vencedor: " + m.winner, font_size="0.65rem", color=GREEN_L, font_weight="600",
                     text_align="center", mt="0.3rem"),
            rx.button(
                "DISPUTAR",
                on_click=GameState.play_playoff_match(idx),
                bg=GREEN,
                color=WHITE,
                font_weight="700",
                font_size="0.7rem",
                size="2",
                border_radius="6px",
                mt="0.5rem",
                letter_spacing="0.03em",
                disabled=GameState.match_in_progress,
            ),
        ),
        p="1rem",
        bg=BG_CARD,
        border="1px solid " + BORDER,
        border_radius="10px",
        min_w="260px",
        width="100%",
    )


def playoffs_view() -> rx.Component:
    return rx.box(
        rx.cond(
            GameState.champion_team != "",
            # Champion celebration
            rx.box(
                rx.text("CAMPEAO", font_size="0.7rem", font_weight="700", color=GOLD,
                         text_align="center", letter_spacing="0.08em"),
                rx.text(GameState.champion_team, font_size="1.8rem", font_weight="900", color=WHITE,
                         text_align="center", mt="0.3rem"),
                bg=BG_SURFACE,
                p="2rem",
                border_radius="12px",
                border="2px solid " + GOLD,
                max_w="500px",
                mx="auto",
                mb="2rem",
            ),
            # Bracket
            rx.box(
                rx.text("PLAYOFFS", font_size="0.75rem", font_weight="700", color=GRAY_D,
                         text_align="center", letter_spacing="0.08em", mb="1.2rem"),
                rx.flex(
                    rx.foreach(
                        GameState.playoff_bracket,
                        lambda m, i: rx.box(
                            _po_card(m, i),
                            flex="1",
                            min_w="260px",
                        ),
                    ),
                    gap="1rem",
                    justify="center",
                    flex_wrap="wrap",
                    width="100%",
                    max_w="850px",
                    mx="auto",
                ),
                width="100%",
            ),
        ),
        rx.cond(
            GameState.champion_team != "",
            rx.button(
                "JOGAR NOVAMENTE",
                on_click=GameState.restart,
                bg=GOLD,
                color=BG,
                font_weight="800",
                font_size="0.8rem",
                size="3",
                border_radius="8px",
                letter_spacing="0.04em",
                display="block",
                mx="auto",
            ),
            rx.box(),
        ),
        bg=BG,
        min_height="100vh",
        padding_top="72px",
        p="1.5rem",
    )


# ====== MAIN INDEX ======

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.cond(GameState.screen == "home", home_view(), rx.box()),
        rx.cond(GameState.screen == "draft", draft_view(), rx.box()),
        rx.cond(GameState.screen == "league", league_view(), rx.box()),
        rx.cond(GameState.screen == "match", match_view(), rx.box()),
        rx.cond(GameState.screen == "result", result_view(), rx.box()),
        rx.cond(GameState.screen == "playoffs", playoffs_view(), rx.box()),
        font_family="'Plus Jakarta Sans', sans-serif",
        bg=BG,
        min_height="100vh",
    )
