import os

path = r"C:\Users\Felipe\Desktop\cblol9a0\cblol9a0\ui.py"

content = '''from __future__ import annotations

import reflex as rx

from .state import GameState, PlayerCard, Matchup, GameEvent

# Paleta — Broadcast eSports: azul marinho + dourado + branco
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
            # Draft progress bar — so no draft screen
            rx.cond(
                (GameState.screen == "draft"),
                rx.hstack(
                    rx.text(
                        (GameState.draft_round).to_string() + "/5",
                        font_size="0.8rem", font_weight="700", color=GOLD,
                    ),
                    rx.text("posicoes", font_size="0.7rem", color=GRAY),
                    gap="0.3rem",
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
                    font_size="0.7rem",
                    font_weight="600",
                    letter_spacing="0.05em",
                ),
                rx.box(),
            ),
            width="100%",
            align="center",
            px="2rem",
            py="0.55rem",
        ),
        bg=BG_DARK if False else BG,
        position="fixed",
        top="0",
        z_index="50",
        width="100%",
        height="56px",
        border_bottom="1px solid " + BORDER,
    )
'''

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Wrote {len(content)} chars")
