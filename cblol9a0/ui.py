from __future__ import annotations

import reflex as rx

from .state import GameState, PlayerCard, LeagueRow, HeroMapIcon, Matchup, GameEvent

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

# Hero champions are now randomized via GameState.hero_map_icons


def tag_pill(tag: rx.Var) -> rx.Component:
    """Renderiza uma tag como pill. tag é um Var[str] vindo de rx.foreach."""
    bg = rx.match(
        tag,
        ("carry",             "#FEF3C7"),
        ("veteran",           "#EDE9FE"),
        ("forte_1v1",         "#FEE2E2"),
        ("teamplayer",        "#DBEAFE"),
        ("objective_control", "#D1FAE5"),
        ("playmaker",         "#FCE7F3"),
        ("early_game",        "#FEF9C3"),
        ("late_game",         "#F3E8FF"),
        ("jungle_ladrao",     "#FFEDD5"),
        ("jungle_agressivo",  "#FEE2E2"),
        ("clutch",            "#FDF4FF"),
        ("consistente",       "#F0FDF4"),
        ("internacional",     "#EFF6FF"),
        "#F3F4F6",
    )
    color = rx.match(
        tag,
        ("carry",             "#92400E"),
        ("veteran",           "#5B21B6"),
        ("forte_1v1",         "#991B1B"),
        ("teamplayer",        "#1E40AF"),
        ("objective_control", "#065F46"),
        ("playmaker",         "#9D174D"),
        ("early_game",        "#854D0E"),
        ("late_game",         "#6B21A8"),
        ("jungle_ladrao",     "#9A3412"),
        ("jungle_agressivo",  "#7F1D1D"),
        ("clutch",            "#701A75"),
        ("consistente",       "#14532D"),
        ("internacional",     "#1E3A5F"),
        "#374151",
    )
    label = rx.match(
        tag,
        ("carry",             "Carry"),
        ("veteran",           "Veteran"),
        ("forte_1v1",         "1v1"),
        ("teamplayer",        "Team Player"),
        ("objective_control", "Objetivos"),
        ("playmaker",         "Playmaker"),
        ("early_game",        "Early Game"),
        ("late_game",         "Late Game"),
        ("jungle_ladrao",     "Ladrão"),
        ("jungle_agressivo",  "Agressivo"),
        ("clutch",            "Clutch"),
        ("consistente",       "Consistente"),
        ("internacional",     "Internacional"),
        tag,
    )
    return rx.box(
        rx.text(label, font_size="0.65rem", font_weight="600", color=color),
        bg=bg,
        border_radius="99px",
        px="0.5rem",
        py="0.15rem",
        display="inline-block",
    )


def team_attr_pill(attr: rx.Var) -> rx.Component:
    """Renderiza um atributo de time como pill. attr é um Var[str]."""
    bg = rx.match(
        attr,
        ("botlane_forte",     "#FEF3C7"),
        ("toplane_dominante", "#FEE2E2"),
        ("jungle_pressao",    "#FFEDD5"),
        ("mid_carry",         "#F3E8FF"),
        ("stompa_early",      "#FEF9C3"),
        ("time_coeso",        "#DBEAFE"),
        ("star_player",       "#FEF3C7"),
        ("comunicacao_falha", "#FEE2E2"),
        ("time_veterano",     "#EDE9FE"),
        ("time_jovem",        "#D1FAE5"),
        "#F3F4F6",
    )
    color = rx.match(
        attr,
        ("botlane_forte",     "#92400E"),
        ("toplane_dominante", "#991B1B"),
        ("jungle_pressao",    "#9A3412"),
        ("mid_carry",         "#6B21A8"),
        ("stompa_early",      "#854D0E"),
        ("time_coeso",        "#1E40AF"),
        ("star_player",       "#78350F"),
        ("comunicacao_falha", "#7F1D1D"),
        ("time_veterano",     "#5B21B6"),
        ("time_jovem",        "#065F46"),
        "#374151",
    )
    label = rx.match(
        attr,
        ("botlane_forte",     "Bot Forte"),
        ("toplane_dominante", "Top Dominante"),
        ("jungle_pressao",    "Pressão JG"),
        ("mid_carry",         "Mid Carry"),
        ("stompa_early",      "Stompa Early"),
        ("time_coeso",        "Time Coeso"),
        ("star_player",       "Star Player"),
        ("comunicacao_falha", "Comm Falha"),
        ("time_veterano",     "Time Veterano"),
        ("time_jovem",        "Time Jovem"),
        attr,
    )
    return rx.box(
        rx.text(label, font_size="0.65rem", font_weight="700", color=color),
        bg=bg,
        border="1px solid " + color,
        border_radius="99px",
        px="0.6rem",
        py="0.2rem",
        display="inline-block",
    )


def _champion_pin(icon: HeroMapIcon, idx: int) -> rx.Component:
    """Pin simples pra home — sem clique, sem info."""
    return rx.box(
        rx.image(
            src=icon.icon_url,
            width="50px",
            height="50px",
            border_radius="50%",
            border="3px solid #52B788",
            box_shadow="0 0 14px rgba(82,183,136,0.7)",
        ),
        rx.text(
            icon.role,
            font_size="0.6rem",
            font_weight="700",
            color="#52B788",
            text_align="center",
            mt="2px",
            letter_spacing="0.05em",
        ),
        position="absolute",
        top=icon.pin_top,
        left=icon.pin_left,
        transform="translate(-50%, -50%)",
        z_index="10",
        display="flex",
        flex_direction="column",
        align_items="center",
    )


def _champion_pin_small(icon: HeroMapIcon, idx: int) -> rx.Component:
    """Pin clicavel pra league/playoffs — mostra card com info do jogador."""
    is_open = GameState.selected_pin_idx == idx
    player = rx.cond(
        GameState.drafted_players.length() > idx,
        GameState.drafted_players[idx],
        PlayerCard(),
    )
    return rx.box(
        rx.box(
            rx.image(
                src=icon.icon_url,
                width="42px",
                height="42px",
                border_radius="50%",
                border="3px solid " + GOLD,
                box_shadow="0 0 10px rgba(201,168,76,0.6)",
                cursor="pointer",
                on_click=GameState.toggle_pin_info(idx),
            ),
            # Card de info ao clicar
            rx.cond(
                is_open,
                rx.box(
                    rx.text(player.name, font_weight="700", font_size="0.75rem", color=WHITE),
                    rx.text(player.team, font_size="0.6rem", color=GRAY),
                    rx.hstack(
                        rx.text(player.year.to_string(), font_size="0.6rem", color=GRAY),
                        rx.text("·", font_size="0.6rem", color=GRAY_D),
                        rx.text("OVR " + player.overall.to_string(), font_size="0.65rem",
                                 font_weight="800", color=GOLD),
                        gap="0.2rem",
                        align="center",
                    ),
                    bg=BG_SURFACE,
                    border="1px solid " + BORDER,
                    border_radius="0px",
                    p="0.4rem 0.6rem",
                    position="absolute",
                    left="50px",
                    top="0px",
                    z_index="20",
                    min_width="140px",
                ),
                rx.box(),
            ),
            position="relative",
            display="inline-block",
        ),
        position="absolute",
        top=icon.pin_top,
        left=icon.pin_left,
        transform="translate(-50%, -50%)",
        z_index="10",
    )


def _draft_champion_pin(icon: HeroMapIcon, idx: int) -> rx.Component:
    """Pin clicavel pro draft — mostra card com info do jogador."""
    is_open = GameState.selected_pin_idx == idx
    player = rx.cond(
        GameState.drafted_players.length() > idx,
        GameState.drafted_players[idx],
        PlayerCard(),
    )
    return rx.box(
        rx.box(
            rx.image(
                src=icon.icon_url,
                width="45px",
                height="45px",
                border_radius="50%",
                border="3px solid " + GOLD,
                box_shadow="0 0 14px rgba(201,168,76,0.7)",
                cursor="pointer",
                on_click=GameState.toggle_pin_info(idx),
            ),
            # Card de info ao clicar
            rx.cond(
                is_open,
                rx.box(
                    rx.text(player.name, font_weight="700", font_size="0.75rem", color=WHITE),
                    rx.text(player.team, font_size="0.6rem", color=GRAY),
                    rx.hstack(
                        rx.text(player.year.to_string(), font_size="0.6rem", color=GRAY),
                        rx.text("·", font_size="0.6rem", color=GRAY_D),
                        rx.text("OVR " + player.overall.to_string(), font_size="0.65rem",
                                 font_weight="800", color=GOLD),
                        gap="0.2rem",
                        align="center",
                    ),
                    bg=BG_SURFACE,
                    border="1px solid " + BORDER,
                    border_radius="0px",
                    p="0.4rem 0.6rem",
                    position="absolute",
                    left="55px",
                    top="0px",
                    z_index="20",
                    min_width="140px",
                ),
                rx.box(),
            ),
            position="relative",
            display="inline-block",
        ),
        position="absolute",
        top=icon.pin_top,
        left=icon.pin_left,
        transform="translate(-50%, -50%)",
        z_index="10",
    )


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
            rx.link(
                rx.image(
                    src="/cblol9a0_logo_modern_horizontal.png",
                    height="90px",
                    width="auto",
                    filter="brightness(0) invert(1)",
                ),
                on_click=GameState.restart,
            ),
            rx.spacer(),
            rx.cond(
                GameState.screen == "draft",
                rx.hstack(
                    rx.text(
                        "DRAFT",
                        font_size="0.85rem", font_weight="600", color=WHITE,
                        letter_spacing="0.04em",
                    ),
                    rx.text("·", font_size="0.85rem", color=WHITE),
                    rx.text(
                        GameState.draft_round.to_string() + " / 5",
                        font_size="1.1rem", font_weight="800", color=GOLD,
                        text_align="center",
                    ),
                    gap="0.3rem",
                    align="center",
                ),
                rx.box(),
            ),
            rx.cond(
                GameState.screen == "league",
                rx.text(
                    "FASE DE LIGA",
                    font_size="0.85rem", font_weight="600", color=WHITE,
                    letter_spacing="0.04em",
                ),
                rx.box(),
            ),
            rx.spacer(),
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
        height="90px",
        border_bottom="1px solid " + BORDER,
    )


# ====== HOME VIEW ======

def _how_to_step(num: str, title: str) -> rx.Component:
    return rx.box(
        rx.text(num, font_size="2rem", font_weight="900", color=GOLD,
                 line_height="1", text_align="center"),
        rx.text(title, font_size="0.75rem", font_weight="600", color=WHITE,
                 text_align="center", mt="0.3rem"),
        text_align="center",
    )



def home_view() -> rx.Component:
    # Cores extra p/ esta view
    BG_DARK = "#1A1A2E"
    BG_LIGHT = "#F5F0E8"
    DARK_TEXT = "#111827"
    GREENAccent = "#2D6A4F"
    GREEN_L_ACCENT = "#52B788"
    BLUE_CHANCE = "#3B82F6"

    # Dados de raridade
    RARITY_CARDS = [
        {
            "label": "⭐ LEGENDARY",
            "color": GOLD,
            "border_top": "3px solid " + GOLD,
            "bg": "rgba(201,168,76,0.08)",
            "chance": "15% de chance",
            "desc": "Times campeões com histórico internacional marcante",
            "examples": "paiN 2015 • INTZ 2016 • LOUD 2022",
            "examples_color": GOLD,
        },
        {
            "label": "🔵 HISTORIC",
            "color": BLUE_CHANCE,
            "border_top": "3px solid " + BLUE_CHANCE,
            "bg": "rgba(59,130,246,0.08)",
            "chance": "35% de chance",
            "desc": "Todos os times campeões do CBLOL",
            "examples": "RED 2017 • KaBuM 2018 • paiN 2021",
            "examples_color": BLUE_CHANCE,
        },
        {
            "label": "⚪ COMMON",
            "color": "#9CA3AF",
            "border_top": "3px solid #9CA3AF",
            "bg": "rgba(156,163,175,0.08)",
            "chance": "50% de chance",
            "desc": "Finalistas e participantes marcantes do CBLOL",
            "examples": "Keyd 2021 • Fluxo 2023 • Vorax 2021",
            "examples_color": "#9CA3AF",
        },
    ]

    # Dados dos 5 steps
    HOW_STEPS = [
        ("1", "Escolha seu time", "Cada round sorteie um time histórico e escolha 1 jogador"),
        ("2", "Reroll estratégico", "Use seu reroll único para tentar um time melhor"),
        ("3", "Fase de liga", "7 partidas contra times históricos da CPU"),
        ("4", "Playoffs", "Top 4 avançam para semifinais e grande final"),
        ("5", "Seja campeão", "Vença a grande final e entre para a história"),
        ]

    return rx.box(
        # ===========================================================
        # SEÇÃO 1 — Hero (fundo escuro, duas colunas)
        # ===========================================================
        rx.box(
            rx.hstack(
                # ---------- Coluna esquerda (textual) ----------
                rx.box(
                    rx.text(
                                            "CBLOL 9A0",
                                            font_size="0.75rem",
                                            font_weight="600",
                                            color=GREEN_L,
                                            letter_spacing="0.15em",
                                        ),
                                        rx.box(
                                            rx.text(
                                                "MONTE O TIME",
                                                font_size="clamp(2.8rem, 5vw, 4.5rem)",
                                                font_weight="900",
                                                color=WHITE,
                                                line_height="1.05",
                                            ),
                                            rx.text(
                                                "DOS SONHOS",
                                                font_size="clamp(2.8rem, 5vw, 4.5rem)",
                                                font_weight="900",
                                                color=GOLD,
                                                line_height="1.05",
                                            ),
                                        ),
                                        rx.text(
                                            "Drafte uma seleção histórica: sai um time e uma liga. Escale um craque que esteve lá, complete o elenco e dispute — seu time faz 9A0?",
                                            font_size="1.05rem",
                                            color="#9CA3AF",
                                            max_width="440px",
                                            mt="1rem",
                                            line_height="1.5",
                                        ),
                    # Stats pills — removido
                    # CTA Button
                    rx.button(
                        "COMEÇAR DRAFT →",
                        on_click=GameState.init_draft,
                        bg=WHITE,
                        color=BG_DARK,
                        font_size="1.3rem",
                        font_weight="800",
                        letter_spacing="0.06em",
                        padding="1.2rem 3rem",
                        border_radius="0px",
                        mt="2rem",
                        cursor="pointer",
                        _hover={
                            "bg": GOLD,
                            "color": BG_DARK,
                            "transform": "scale(1.04)",
                        },
                    ),
                    flex="1",
                    padding="4rem 3rem",
                    display="flex",
                    flex_direction="column",
                    justify_content="center",
                    align_items="flex-start",
                    min_width="280px",
                ),
                # ---------- Coluna direita (mapa) ----------
                                rx.box(
                                    rx.box(
                                        rx.image(
                                            src="/summoners_rift_modern.png",
                                            width="100%",
                                            border_radius="12px",
                                            opacity="0.9",
                                        ),
                                                                                rx.foreach(
                                            GameState.hero_map_icons,
                                            _champion_pin,
                                        ),
                                        position="relative",
                                        bg="rgba(255,255,255,0.04)",
                                        border="1px solid rgba(255,255,255,0.08)",
                                        border_radius="20px",
                                        padding="1.5rem",
                                    ),
                                    width="480px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    min_width="280px",
                                ),
                gap="2rem",
                align="center",
                justify_content="center",
                width="100%",
                max_width="1100px",
                margin_x="auto",
                flex_wrap="wrap",
            ),
            bg=BG_DARK,
            min_height="calc(100vh - 90px)",
            padding_top="90px",
            width="100%",
        ),

        # ===========================================================
                # SEÇÃO 2 — Como Funciona (padrão visual do site)
                # ===========================================================
                rx.box(
                    rx.text(
                        "COMO FUNCIONA",
                        font_size="0.7rem",
                        font_weight="700",
                        color=GRAY_D,
                        text_align="center",
                        letter_spacing="0.1em",
                        mb="0.5rem",
                    ),
                    rx.text(
                        "5 rounds de draft. 7 partidas. Um campeão.",
                        font_size="1rem",
                        color=GRAY,
                        text_align="center",
                        margin_bottom="2.5rem",
                    ),
                    rx.flex(
                        *[
                            rx.box(
                                rx.text(
                                    step[0],
                                    font_size="1.8rem",
                                    font_weight="900",
                                    color=GOLD,
                                    line_height="1",
                                    text_align="center",
                                ),
                                rx.text(
                                    step[1],
                                    font_size="0.7rem",
                                    font_weight="600",
                                    color=WHITE,
                                    text_align="center",
                                    mt="0.4rem",
                                ),
                                rx.text(
                                    step[2],
                                    font_size="0.6rem",
                                    color=GRAY_D,
                                    text_align="center",
                                    margin_top="0.2rem",
                                    line_height="1.3",
                                ),
                                width="100%",
                                padding="1rem 0.75rem",
                                bg=BG_CARD,
                                border="1px solid " + BORDER,
                                border_radius="10px",
                                _hover={
                                    "bg": BG_SURFACE,
                                    "border_color": GOLD,
                                    "transition": "all 0.15s",
                                },
                            )
                            for step in HOW_STEPS
                        ],
                        flex_wrap="nowrap",
                        justify_content="center",
                        gap="0.75rem",
                        width="100%",
                        max_width="750px",
                        margin_x="auto",
                    ),
                    bg=BG_DARK,
                    padding="3rem 2rem",
                    width="100%",
                ),

                footer(),

        width="100%",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("CBLOL", font_weight="800", color=WHITE, font_size="0.9rem"),
            rx.text("9A0", font_size="0.65rem", font_weight="800", color=BG,
                     bg=GOLD, px="0.3rem", py="0.05rem", border_radius="0px"),
            gap="0.2rem",
            align="center",
        ),
        rx.text(
            "Jogo de draft histórico do cenário brasileiro de League of Legends.",
            font_size="0.7rem", color=GRAY_D, mt="0.4rem",
            text_align="center",
        ),
        rx.text(
            "2025 CBLOL 9A0. League of Legends é propriedade da Riot Games.",
            font_size="0.65rem", color=GRAY_D, mt="0.3rem",
            text_align="center",
        ),
        bg=BG_CARD,
        width="100%",
        py="2rem",
        px="2rem",
        display="flex",
        flex_direction="column",
        align_items="center",
        text_align="center",
        border_top="1px solid " + BORDER,
    )



# ====== DRAFT VIEW ======

def _draft_player_card(p: PlayerCard, idx: int) -> rx.Component:
    """Card vertical de jogador disponível para seleção."""
    role_taken = GameState.drafted_roles.contains(p.role)
    disabled = role_taken | GameState.selected_from_current_team

    return rx.box(
        rx.vstack(
            rx.spacer(),
            # Champion icon
            rx.box(
                rx.image(
                    src=p.icon_url,
                    width="60px",
                    height="60px",
                    object_fit="cover",
                    border_radius="0px",
                    border="2px solid " + rx.cond(disabled, GRAY_D, GOLD),
                    opacity=rx.cond(disabled, "0.4", "1"),
                ),
                display="flex",
                justify_content="center",
                width="100%",
            ),
            # Nome
            rx.text(p.name, font_weight="700", font_size="0.85rem",
                     color=rx.cond(disabled, GRAY_D, WHITE),
                     text_align="center", truncate=True,
                     px="0.15rem", mt="0.3rem"),
            # Campeão
            rx.text(p.champion, font_size="0.65rem",
                     color=rx.cond(disabled, GRAY_D, GRAY),
                     text_align="center", truncate=True,
                     px="0.15rem"),
            # Role badge
            rx.text(
                p.role,
                font_size="0.6rem", font_weight="700",
                color=rx.cond(disabled, GRAY_D, GOLD),
                mt="0.2rem",
            ),
            # Tags
            rx.flex(
                rx.foreach(p.tags, tag_pill),
                flex_wrap="wrap",
                gap="0.15rem",
                justify="center",
                px="0.1rem",
            ),
            # Overall
            rx.text(
                p.overall.to_string(),
                font_weight="900",
                font_size="1.3rem",
                color=rx.cond(disabled, GRAY_D, GOLD),
                text_align="center",
                mt="0.2rem",
            ),
            rx.spacer(),
            gap="0.05rem",
            align_items="center",
            width="100%",
            height="100%",
        ),
        p="0rem",
        bg=rx.cond(disabled, BG_CARD, BG_SURFACE),
        border="2px solid " + rx.cond(disabled, BORDER, BORDER_L),
        border_top="4px solid " + rx.cond(disabled, GRAY_D, GOLD),
        border_radius="0px",
        opacity=rx.cond(disabled, "0.5", "1"),
        cursor=rx.cond(disabled, "not-allowed", "pointer"),
        on_click=rx.cond(disabled, rx.noop(), GameState.select_player(p)),
        _hover=rx.cond(disabled, {}, {"bg": "#1E2D4A", "border_color": GOLD, "transition": "all 0.12s"}),
        aspect_ratio="3/5",
        width="100%",
    )


def _draft_team_header() -> rx.Component:
    team = GameState.current_draft_team
    return rx.vstack(
        rx.text(team.display_name, font_weight="900", font_size="1.5rem", color=WHITE,
                 text_align="center", width="100%"),
        rx.hstack(
            rx.text(team.year.to_string(), font_size="0.7rem", color=GRAY),
            rx.text("·", font_size="0.7rem", color=GRAY_D),
            rx.text(team.rarity, font_size="0.65rem", font_weight="700",
                     color=GOLD),
            rx.text("·", font_size="0.7rem", color=GRAY_D),
            rx.text(
                "OVR " + team.overall.to_string().split(".")[0],
                font_weight="900", font_size="0.75rem", color=GOLD,
            ),
            gap="0.4rem",
            align="center",
            justify="center",
            width="100%",
        ),
        align_items="center",
        width="100%",
        mb="0.5rem",
    )


def _draft_my_team_slot(p: PlayerCard, role: str) -> rx.Component:
    """Slot da lista Meu Time."""
    filled = p.name != ""
    return rx.box(
        rx.hstack(
            rx.cond(
                filled,
                rx.image(
                    src=p.icon_url,
                    width="32px", height="32px",
                    border_radius="0px",
                    border="2px solid " + GOLD,
                ),
                rx.box(
                    width="32px", height="32px",
                    border_radius="0px",
                    bg=BG_SURFACE,
                    border="1px dashed " + GRAY_D,
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
            ),
            rx.box(
                rx.text(
                    rx.cond(filled, p.name, role),
                    font_size="0.75rem",
                    font_weight=rx.cond(filled, "700", "500"),
                    color=rx.cond(filled, WHITE, GRAY_D),
                ),
                rx.cond(
                    filled,
                    rx.text(
                        p.champion + " · OVR " + p.overall.to_string(),
                        font_size="0.6rem",
                        color=GRAY,
                    ),
                    rx.text("--", font_size="0.6rem", color=GRAY_D),
                ),
                flex="1",
            ),
            rx.text(
                role,
                font_size="0.6rem",
                font_weight="600",
                color=GRAY_D,
                bg=BG_SURFACE,
                px="0.35rem",
                py="0.1rem",
                border_radius="3px",
            ),
            gap="0.5rem",
            align="center",
            width="100%",
        ),
        p="0.4rem 0.6rem",
        bg=rx.cond(filled, BG_SURFACE, BG_CARD),
        border="1px solid " + rx.cond(filled, BORDER_L, BORDER),
        border_radius="0px",
        width="100%",
    )


def draft_view() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                # ===== COLUNA ESQUERDA (maior) — Time sorteado =====
                rx.vstack(
                    # Team header
                    _draft_team_header(),
                    # Players cards
                    rx.box(
                        rx.box(
                            rx.foreach(
                                GameState.current_draft_team.players,
                                lambda p, i: _draft_player_card(p, i),
                            ),
                            gap="0.5rem",
                            display="grid",
                            grid_template_columns="repeat(5, 1fr)",
                            width="100%",
                            max_width="650px",
                        ),
                        display="flex",
                        justify_content="center",
                        width="100%",
                    ),
                    # Action buttons
                    rx.box(
                        rx.cond(
                            GameState.draft_complete,
                            rx.vstack(
                                rx.hstack(
                                    rx.input(
                                        value=GameState.team_name_input,
                                        on_change=GameState.set_team_name,
                                        placeholder="Nome do seu time",
                                        font_size="0.9rem",
                                        font_weight="600",
                                        color=WHITE,
                                        bg=BG_SURFACE,
                                        border="1px solid " + BORDER,
                                        border_radius="0px",
                                        padding="0.6rem 1rem",
                                        height="44px",
                                        width="240px",
                                        _placeholder={"color": GRAY_D},
                                    ),
                                    rx.button(
                                        "INICIAR LIGA →",
                                        on_click=GameState.init_league,
                                        bg=GOLD,
                                        color=BG,
                                        font_weight="800",
                                        font_size="1rem",
                                        padding="0.9rem 3rem",
                                        border_radius="0px",
                                        letter_spacing="0.06em",
                                        _hover={"bg": GOLD_L, "transform": "scale(1.02)"},
                                        disabled=GameState.team_name_input == "",
                                    ),
                                    gap="0.75rem",
                                    align="center",
                                ),
                            ),
                            rx.hstack(
                                rx.button(
                                    rx.cond(GameState.reroll_used, "REROLL USADO", "REROLL"),
                                    on_click=GameState.reroll,
                                    disabled=GameState.reroll_used,
                                    bg=rx.cond(GameState.reroll_used, BG_CARD, "transparent"),
                                    color=rx.cond(GameState.reroll_used, GRAY_D, GOLD),
                                    border="1px solid " + rx.cond(GameState.reroll_used, BORDER, GOLD),
                                    font_weight="700",
                                    font_size="0.8rem",
                                    padding="0.6rem 1.5rem",
                                    border_radius="0px",
                                    letter_spacing="0.04em",
                                    cursor=rx.cond(GameState.reroll_used, "not-allowed", "pointer"),
                                    _hover={"bg": rx.cond(GameState.reroll_used, BG_CARD, "rgba(201,168,76,0.1)")},
                                ),
                                rx.button(
                                    "PRÓXIMO TIME →",
                                    on_click=GameState.next_team,
                                    bg=GOLD,
                                    color=BG,
                                    font_weight="800",
                                    font_size="0.9rem",
                                    padding="0.6rem 2rem",
                                    border_radius="0px",
                                    letter_spacing="0.05em",
                                    _hover={"bg": GOLD_L, "transform": "scale(1.02)"},
                                ),
                                gap="0.75rem",
                                justify="center",
                                width="100%",
                            ),
                        ),
                        width="100%",
                        display="flex",
                        justify_content="center",
                        mt="1rem",
                    ),
                    flex="3",
                    min_w="380px",
                ),
                # ===== COLUNA DIREITA (menor) — Mapa + Meu Time =====
                rx.vstack(
                    # Map
                    rx.box(
                        rx.box(
                            rx.image(
                                src="/summoners_rift_modern.png",
                                width="100%",
                                border_radius="0px",
                                opacity="0.85",
                            ),
                            rx.foreach(
                                GameState.draft_map_icons,
                                _draft_champion_pin,
                            ),
                            position="relative",
                            border_radius="0px",
                        ),
                        width="100%",
                        max_w="264px",
                    ),
                    # Meu Time
                    rx.box(
                        rx.text("MEU TIME", font_size="0.65rem", font_weight="700",
                                 color=GRAY_D, letter_spacing="0.08em", mb="0.35rem"),
                        # Atributos do time
                        rx.cond(
                            GameState.draft_round > 0,
                            rx.flex(
                                rx.foreach(GameState.player_team_attributes, team_attr_pill),
                                flex_wrap="wrap",
                                gap="0.25rem",
                                mb="0.5rem",
                            ),
                            rx.box(),
                        ),
                        rx.vstack(
                            _draft_my_team_slot(GameState.drafted_slots[0], "Top"),
                            _draft_my_team_slot(GameState.drafted_slots[1], "Jungle"),
                            _draft_my_team_slot(GameState.drafted_slots[2], "Mid"),
                            _draft_my_team_slot(GameState.drafted_slots[3], "ADC"),
                            _draft_my_team_slot(GameState.drafted_slots[4], "Support"),
                            gap="0.3rem",
                            width="100%",
                        ),
                        width="100%",
                        max_w="264px",
                        mt="0.75rem",
                    ),
                    align_items="flex-start",
                    min_w="220px",
                    flex="1",
                    pb="3rem",
                ),
                align="stretch",
                width="100%",
                max_width="1100px",
                mx="auto",
                mb="2rem",
            ),
            display="flex",
            justify_content="center",
            width="100%",
            px="2rem",
        ),
        rx.box(height="3rem"),
        footer(),
        bg=BG,
        min_height="100vh",
        padding_top="90px",
    )


# ====== LEAGUE VIEW ======

def _league_table_row(entry: LeagueRow, idx: int) -> rx.Component:
    is_player = entry.is_player
    return rx.box(
        rx.hstack(
            rx.text(idx + 1, font_weight="800", font_size="0.85rem",
                     color=rx.cond(is_player, BG, GRAY_D), min_w="2rem", text_align="center"),
            rx.text(entry.name, font_weight=rx.cond(is_player, "800", "600"),
                     font_size="0.9rem",
                     color=rx.cond(is_player, BG, WHITE), flex="1", truncate=True),
            rx.text(entry.wins.to_string(), font_weight="700", font_size="0.9rem",
                     color=rx.cond(is_player, BG, GREEN_L), min_w="2rem", text_align="center"),
            rx.text(entry.losses.to_string(), font_weight="700", font_size="0.9rem",
                     color=rx.cond(is_player, BG, RED), min_w="2rem", text_align="center"),
            gap="0.35rem",
            align="center",
            width="100%",
        ),
        p="0.6rem 0.8rem",
        bg=rx.cond(is_player, GOLD, BG_CARD),
        border="1px solid " + rx.cond(is_player, GOLD, BORDER),
        border_radius="0px",
        width="100%",
    )


def _league_team_slot(p: PlayerCard, role: str) -> rx.Component:
    filled = p.name != ""
    return rx.box(
        rx.hstack(
            rx.image(
                src=p.icon_url,
                width="28px", height="28px",
                border_radius="0px",
                border="2px solid " + GOLD,
            ),
            rx.box(
                rx.text(p.name, font_weight="600", font_size="0.65rem", color=WHITE, truncate=True),
                rx.text(p.champion, font_size="0.55rem", color=GRAY, truncate=True),
                flex="1",
            ),
            rx.text(role, font_size="0.5rem", font_weight="600", color=GRAY_D),
            rx.text(p.overall.to_string(), font_weight="800", font_size="0.7rem", color=GOLD),
            gap="0.3rem",
            align="center",
            width="100%",
        ),
        p="0.3rem 0.5rem",
        bg=BG_SURFACE,
        border="1px solid " + BORDER_L,
        border_radius="0px",
        width="100%",
    )


def league_view() -> rx.Component:
    return rx.box(
        rx.box(
            rx.hstack(
                # ===== COLUNA ESQUERDA (maior) — Classificação =====
                rx.vstack(
                    # Tabela
                    rx.box(
                        # Header da tabela
                        rx.hstack(
                            rx.text("#", font_size="0.55rem", font_weight="700", color=GRAY_D,
                                     min_w="1.5rem", text_align="center"),
                            rx.text("TIME", font_size="0.55rem", font_weight="700", color=GRAY_D,
                                     flex="1"),
                            rx.text("V", font_size="0.55rem", font_weight="700", color=GRAY_D,
                                     min_w="1.5rem", text_align="center"),
                            rx.text("D", font_size="0.55rem", font_weight="700", color=GRAY_D,
                                     min_w="1.5rem", text_align="center"),
                            gap="0.25rem",
                            align="center",
                            width="100%",
                            pb="0.25rem",
                        ),
                        rx.foreach(
                            GameState.league_table,
                            _league_table_row,
                        ),
                        gap="0.2rem",
                        display="flex",
                        flex_direction="column",
                        width="480px",
                        mx="auto",
                    ),
                    rx.box(height="3rem"),
                    # Próximo adversário + botão
                    rx.cond(
                        GameState.league_complete,
                        rx.button(
                            "IR PARA PLAYOFFS →",
                            on_click=GameState.init_playoffs,
                            bg=GOLD,
                            color=BG,
                            font_weight="800",
                            font_size="0.9rem",
                            padding="0.7rem 2.5rem",
                            border_radius="0px",
                            letter_spacing="0.05em",
                            mt="2rem",
                            _hover={"bg": GOLD_L, "transform": "scale(1.02)"},
                        ),
                        rx.box(
                            rx.box(
                                rx.text("PRÓXIMO ADVERSÁRIO", font_size="0.55rem",
                                         font_weight="700", color=GRAY_D,
                                         letter_spacing="0.06em", mb="0.3rem"),
                                rx.text(GameState.next_opponent, font_size="1rem",
                                         font_weight="800", color=WHITE),
                                border_radius="0px",
                                p="0.6rem 1rem",
                                width="240px",
                            ),
                            rx.button(
                                "JOGAR PRÓXIMA PARTIDA",
                                on_click=GameState.start_match,
                                bg=GOLD,
                                color=BG,
                                font_weight="800",
                                font_size="0.9rem",
                                padding="0.7rem 2.5rem",
                                border_radius="0px",
                                letter_spacing="0.05em",
                                mt="0.75rem",
                                disabled=GameState.match_in_progress,
                                _hover={"bg": GOLD_L, "transform": "scale(1.02)"},
                            ),
                            display="flex",
                            flex_direction="column",
                            align_items="center",
                            mt="2rem",
                            width="100%",
                        ),
                    ),
                    flex="2",
                    min_w="300px",
                    align_items="center",
                ),
                # ===== COLUNA DIREITA — Mapa + Time =====
                rx.vstack(
                    # Map
                    rx.box(
                        rx.box(
                            rx.image(
                                src="/summoners_rift_modern.png",
                                width="100%",
                                border_radius="0px",
                                opacity="0.85",
                            ),
                            rx.foreach(
                                GameState.draft_map_icons,
                                _champion_pin_small,
                            ),
                            position="relative",
                            border_radius="0px",
                        ),
                        width="100%",
                        max_w="264px",
                    ),
                    # Nome do time + OVR
                    rx.box(
                        rx.text(GameState.player_team_name, font_weight="800", font_size="0.85rem",
                                 color=WHITE, text_align="center"),
                        rx.text("OVR " + GameState.team_overall.to_string(), font_weight="900",
                                 font_size="1.2rem", color=GOLD, text_align="center"),
                        rx.flex(
                            rx.foreach(GameState.player_team_attributes, team_attr_pill),
                            flex_wrap="wrap",
                            gap="0.25rem",
                            justify="center",
                            mt="0.3rem",
                        ),
                        bg=BG_SURFACE,
                        border="1px solid " + BORDER,
                        border_radius="0px",
                        p="0.5rem 1rem",
                        width="100%",
                        max_w="264px",
                        mt="0.75rem",
                    ),
                    # Lista do time
                    rx.box(
                        rx.text("TIME", font_size="0.6rem", font_weight="700",
                                 color=GRAY_D, letter_spacing="0.06em", mb="0.35rem"),
                        rx.vstack(
                            _league_team_slot(GameState.drafted_slots[0], "Top"),
                            _league_team_slot(GameState.drafted_slots[1], "Jungle"),
                            _league_team_slot(GameState.drafted_slots[2], "Mid"),
                            _league_team_slot(GameState.drafted_slots[3], "ADC"),
                            _league_team_slot(GameState.drafted_slots[4], "Support"),
                            gap="0.2rem",
                            width="100%",
                        ),
                        width="100%",
                        max_w="264px",
                        mt="0.75rem",
                    ),
                    align_items="flex-start",
                    min_w="220px",
                    flex="1",
                    pb="3rem",
                ),
                align="stretch",
                width="100%",
                max_width="1100px",
                mx="auto",
                mb="2rem",
            ),
            display="flex",
            justify_content="center",
            width="100%",
            px="2rem",
        ),
        rx.box(height="3rem"),
        footer(),
        bg=BG,
        min_height="100vh",
        padding_top="90px",
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
            # Atributos do time (se venceu)
            rx.cond(
                is_win,
                rx.flex(
                    rx.foreach(GameState.player_team_attributes, team_attr_pill),
                    flex_wrap="wrap",
                    gap="0.3rem",
                    justify="center",
                    mt="0.5rem",
                ),
                rx.box(),
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
        min_height="calc(100vh - 90px)",
        bg=BG,
        padding_top="90px",
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
                rx.cond(
                    GameState.champion_team == GameState.player_team_name,
                    rx.flex(
                        rx.foreach(GameState.player_team_attributes, team_attr_pill),
                        flex_wrap="wrap",
                        gap="0.3rem",
                        justify="center",
                        mt="0.5rem",
                    ),
                    rx.box(),
                ),
                bg=BG_SURFACE,
                p="2rem",
                border_radius="0px",
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
