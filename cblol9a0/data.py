from dataclasses import dataclass, field
from typing import Optional
import random


@dataclass
class Player:
    name: str
    role: str  # "Top" | "Jungle" | "Mid" | "ADC" | "Support"
    champion: str
    overall: int  # 1–99
    team: str
    year: int
    nationality: str = "BR"
    tags: list[str] = field(default_factory=list)


@dataclass
class Team:
    name: str
    year: int
    region: str
    rarity: str  # "Common" | "Historic" | "Legendary"
    players: list[Player]
    description: str = ""

    @property
    def overall(self) -> float:
        return sum(p.overall for p in self.players) / len(self.players)

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.year})"


RARITY_WEIGHTS = {"Common": 50, "Historic": 35, "Legendary": 15}

# Special champion names that differ from URL format
SPECIAL_CHAMPIONS = {
    "Kai'Sa": "Kaisa",
    "Kai'sa": "Kaisa",
    "K'Sante": "KSante",
    "K'sante": "KSante",
    "Cho'Gath": "Chogath",
    "Kha'Zix": "Khazix",
    "LeBlanc": "Leblanc",
    "Vel'Koz": "Velkoz",
    "Bel'Veth": "Belveth",
    "Wukong": "MonkeyKing",
    "Rek'Sai": "RekSai",
    "Rek'sai": "RekSai",
}


def champion_icon_url(champion: str) -> str:
    clean = SPECIAL_CHAMPIONS.get(champion, champion)
    clean = clean.replace(" ", "")
    clean = clean.replace("'", "")
    clean = clean.replace(".", "")
    clean = clean.replace("_", "")
    return (
        f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{clean}.png"
    )


# --- LEGENDARY TEAMS (5) ---

LEGENDARY_TEAMS = [
    Team(
        name="paiN Gaming",
        year=2015,
        region="BR",
        rarity="Legendary",
        players=[
            Player("Mylon", "Top", "Gnar", 86, "paiN Gaming", 2015),
            Player("SirT", "Jungle", "Elise", 85, "paiN Gaming", 2015),
            Player("Kami", "Mid", "Cassiopeia", 91, "paiN Gaming", 2015),
            Player("brTT", "ADC", "Tristana", 93, "paiN Gaming", 2015),
            Player("Dioud", "Support", "Alistar", 87, "paiN Gaming", 2015, nationality="FR"),
        ],
        description="Campeões do CBLOL 2015 1º Split, representaram o Brasil no MSI 2015.",
    ),
    Team(
        name="INTZ",
        year=2016,
        region="BR",
        rarity="Legendary",
        players=[
            Player("Yang", "Top", "Gnar", 84, "INTZ", 2016),
            Player("Revolta", "Jungle", "Lee Sin", 91, "INTZ", 2016),
            Player("Tockers", "Mid", "Viktor", 86, "INTZ", 2016),
            Player("micaO", "ADC", "Jinx", 88, "INTZ", 2016),
            Player("Jockster", "Support", "Thresh", 83, "INTZ", 2016),
        ],
        description="Campeões do CBLOL 2016 1º Split. Revolta foi MVP da final.",
    ),
    Team(
        name="KaBuM! e-Sports",
        year=2014,
        region="BR",
        rarity="Legendary",
        players=[
            Player("LEP", "Top", "Shyvana", 82, "KaBuM! e-Sports", 2014),
            Player("Danagorn", "Jungle", "Vi", 80, "KaBuM! e-Sports", 2014),
            Player("tinowns", "Mid", "Zed", 88, "KaBuM! e-Sports", 2014),
            Player("Minerva", "ADC", "Caitlyn", 81, "KaBuM! e-Sports", 2014),
            Player("dans", "Support", "Annie", 78, "KaBuM! e-Sports", 2014),
        ],
        description="Campeões do CBLOL 2014 2º Split. Primeiro título do tinowns.",
    ),
    Team(
        name="LOUD",
        year=2022,
        region="BR",
        rarity="Legendary",
        players=[
            Player("Robo", "Top", "Gwen", 90, "LOUD", 2022),
            Player("Croc", "Jungle", "Viego", 88, "LOUD", 2022, nationality="KR"),
            Player("tinowns", "Mid", "Azir", 92, "LOUD", 2022),
            Player("Brance", "ADC", "Zeri", 87, "LOUD", 2022, nationality="KR"),
            Player("Ceos", "Support", "Nautilus", 86, "LOUD", 2022),
        ],
        description="Campeões do CBLOL 2022 2º Split. Primeira LOUD campeã.",
    ),
    Team(
        name="LOUD",
        year=2023,
        region="BR",
        rarity="Legendary",
        players=[
            Player("Robo", "Top", "K'Sante", 91, "LOUD", 2023),
            Player("Croc", "Jungle", "Maokai", 89, "LOUD", 2023, nationality="KR"),
            Player("tinowns", "Mid", "Syndra", 93, "LOUD", 2023),
            Player("Route", "ADC", "Jinx", 90, "LOUD", 2023, nationality="KR"),
            Player("Ceos", "Support", "Lulu", 87, "LOUD", 2023),
        ],
        description="Bicampeã do CBLOL 2023. Dinastia LOUD no auge.",
    ),
]

# --- HISTORIC TEAMS (16) ---

HISTORIC_TEAMS = [
    Team(
        name="vTi Ignis",
        year=2012,
        region="BR",
        rarity="Historic",
        players=[
            Player("Mylon", "Top", "Malphite", 72, "vTi Ignis", 2012),
            Player("rafes", "Jungle", "Nunu", 70, "vTi Ignis", 2012),
            Player("Snowlz", "Mid", "Anivia", 71, "vTi Ignis", 2012),
            Player("manajj", "ADC", "Caitlyn", 73, "vTi Ignis", 2012),
            Player("Alocs", "Support", "Soraka", 69, "vTi Ignis", 2012),
        ],
        description="Primeiros campeões do cenário brasileiro. Season 2.",
    ),
    Team(
        name="paiN Gaming",
        year=2013,
        region="BR",
        rarity="Historic",
        players=[
            Player("Venon", "Top", "Shen", 76, "paiN Gaming", 2013),
            Player("SirT", "Jungle", "Vi", 80, "paiN Gaming", 2013),
            Player("Kami", "Mid", "Zed", 83, "paiN Gaming", 2013),
            Player("brTT", "ADC", "Caitlyn", 87, "paiN Gaming", 2013),
            Player("Espeon", "Support", "Thresh", 77, "paiN Gaming", 2013),
        ],
        description="Primeira line-up histórica da paiN com Kami e brTT.",
    ),
    Team(
        name="Keyd Stars",
        year=2014,
        region="BR",
        rarity="Historic",
        players=[
            Player("Mylon", "Top", "Shyvana", 81, "Keyd Stars", 2014),
            Player("Winged", "Jungle", "Lee Sin", 84, "Keyd Stars", 2014, nationality="KR"),
            Player("SuNo", "Mid", "Orianna", 82, "Keyd Stars", 2014, nationality="KR"),
            Player("brTT", "ADC", "Lucian", 89, "Keyd Stars", 2014),
            Player("Loop", "Support", "Annie", 78, "Keyd Stars", 2014),
        ],
        description="Time com core coreana + brTT. Finalistas CBLOL 2014.",
    ),
    Team(
        name="INTZ",
        year=2015,
        region="BR",
        rarity="Historic",
        players=[
            Player("Yang", "Top", "Maokai", 82, "INTZ", 2015),
            Player("Revolta", "Jungle", "Rek'Sai", 88, "INTZ", 2015),
            Player("Tockers", "Mid", "Viktor", 84, "INTZ", 2015),
            Player("micaO", "ADC", "Sivir", 86, "INTZ", 2015),
            Player("Jockster", "Support", "Alistar", 81, "INTZ", 2015),
        ],
        description="Pré-história da INTZ campeã. Revolta em ascensão.",
    ),
    Team(
        name="RED Canids",
        year=2017,
        region="BR",
        rarity="Historic",
        players=[
            Player("Robo", "Top", "Camille", 87, "RED Canids", 2017),
            Player("Nappon", "Jungle", "Kha'Zix", 83, "RED Canids", 2017),
            Player("Tockers", "Mid", "Orianna", 84, "RED Canids", 2017),
            Player("brTT", "ADC", "Jhin", 91, "RED Canids", 2017),
            Player("Dioud", "Support", "Thresh", 85, "RED Canids", 2017, nationality="FR"),
        ],
        description="RED Canids campeã do CBLOL 2017 1º Split.",
    ),
    Team(
        name="Team oNe",
        year=2017,
        region="BR",
        rarity="Historic",
        players=[
            Player("VVert", "Top", "Renekton", 80, "Team oNe", 2017),
            Player("4LaN", "Jungle", "Graves", 79, "Team oNe", 2017),
            Player("Brucer", "Mid", "Taliyah", 81, "Team oNe", 2017),
            Player("Absolut", "ADC", "Tristana", 83, "Team oNe", 2017),
            Player("RedBert", "Support", "Rakan", 82, "Team oNe", 2017),
        ],
        description="Primeira line-up da Team oNe no CBLOL.",
    ),
    Team(
        name="KaBuM! e-Sports",
        year=2018,
        region="BR",
        rarity="Historic",
        players=[
            Player("Zantins", "Top", "Urgot", 82, "KaBuM! e-Sports", 2018),
            Player("Ranger", "Jungle", "Nidalee", 84, "KaBuM! e-Sports", 2018),
            Player("dyNquedo", "Mid", "Yasuo", 86, "KaBuM! e-Sports", 2018),
            Player("TitaN", "ADC", "Kai'Sa", 90, "KaBuM! e-Sports", 2018),
            Player("Riyev", "Support", "Braum", 80, "KaBuM! e-Sports", 2018),
        ],
        description="KaBuM! com TitaN e dyNquedo. Semi-finalistas CBLOL 2018.",
    ),
    Team(
        name="Flamengo eSports",
        year=2019,
        region="BR",
        rarity="Historic",
        players=[
            Player("Tay", "Top", "Jayce", 84, "Flamengo eSports", 2019),
            Player("Shini", "Jungle", "Jarvan IV", 83, "Flamengo eSports", 2019),
            Player("Goku", "Mid", "Zoe", 86, "Flamengo eSports", 2019),
            Player("brTT", "ADC", "Xayah", 90, "Flamengo eSports", 2019),
            Player("Luci", "Support", "Thresh", 82, "Flamengo eSports", 2019, nationality="KR"),
        ],
        description="Flamengo campeão do CBLOL 2019 1º Split com brTT.",
    ),
    Team(
        name="INTZ",
        year=2019,
        region="BR",
        rarity="Historic",
        players=[
            Player("Tay", "Top", "Urgot", 85, "INTZ", 2019),
            Player("Shini", "Jungle", "Sejuani", 82, "INTZ", 2019),
            Player("Envy", "Mid", "Lissandra", 83, "INTZ", 2019),
            Player("Mills", "ADC", "Xayah", 81, "INTZ", 2019),
            Player("RedBert", "Support", "Thresh", 84, "INTZ", 2019),
        ],
        description="INTZ campeã do CBLOL 2019 2º Split.",
    ),
    Team(
        name="KaBuM! e-Sports",
        year=2020,
        region="BR",
        rarity="Historic",
        players=[
            Player("Tay", "Top", "Gangplank", 84, "KaBuM! e-Sports", 2020),
            Player("Buggax", "Jungle", "Gragas", 82, "KaBuM! e-Sports", 2020),
            Player("dyNquedo", "Mid", "Orianna", 85, "KaBuM! e-Sports", 2020),
            Player("TitaN", "ADC", "Ashe", 88, "KaBuM! e-Sports", 2020),
            Player("Ceos", "Support", "Thresh", 83, "KaBuM! e-Sports", 2020),
        ],
        description="KaBuM! vice-campeã do CBLOL 2020 1º Split.",
    ),
    Team(
        name="INTZ",
        year=2020,
        region="BR",
        rarity="Historic",
        players=[
            Player("Tay", "Top", "Fiora", 86, "INTZ", 2020),
            Player("Shini", "Jungle", "Lee Sin", 84, "INTZ", 2020),
            Player("Envy", "Mid", "Corki", 85, "INTZ", 2020),
            Player("micaO", "ADC", "Caitlyn", 87, "INTZ", 2020),
            Player("RedBert", "Support", "Leona", 85, "INTZ", 2020),
        ],
        description="INTZ campeã do CBLOL 2020 2º Split. Tay e Shini bicampeões.",
    ),
    Team(
        name="paiN Gaming",
        year=2021,
        region="BR",
        rarity="Historic",
        players=[
            Player("Robo", "Top", "Gnar", 88, "paiN Gaming", 2021),
            Player("CarioK", "Jungle", "Hecarim", 86, "paiN Gaming", 2021),
            Player("tinowns", "Mid", "Twisted Fate", 90, "paiN Gaming", 2021),
            Player("brTT", "ADC", "Kai'Sa", 91, "paiN Gaming", 2021),
            Player("Luci", "Support", "Alistar", 83, "paiN Gaming", 2021, nationality="KR"),
        ],
        description="paiN campeã do CBLOL 2021 1º Split. brTT octacampeão.",
    ),
    Team(
        name="RED Canids",
        year=2021,
        region="BR",
        rarity="Historic",
        players=[
            Player("TitaN", "Top", "Renekton", 85, "RED Canids", 2021),
            Player("JoJo", "Jungle", "Jarvan IV", 82, "RED Canids", 2021),
            Player("Grevthar", "Mid", "Viktor", 83, "RED Canids", 2021),
            Player("Aegis", "ADC", "Aphelios", 84, "RED Canids", 2021),
            Player("Guigo", "Support", "Thresh", 81, "RED Canids", 2021),
        ],
        description="RED Canids vice-campeã do CBLOL 2021 2º Split.",
    ),
    Team(
        name="RED Canids",
        year=2022,
        region="BR",
        rarity="Historic",
        players=[
            Player("TitaN", "Top", "Gangplank", 87, "RED Canids", 2022),
            Player("JoJo", "Jungle", "Viego", 84, "RED Canids", 2022),
            Player("Grevthar", "Mid", "Ahri", 85, "RED Canids", 2022),
            Player("Aegis", "ADC", "Jinx", 86, "RED Canids", 2022),
            Player("Guigo", "Support", "Lulu", 83, "RED Canids", 2022),
        ],
        description="RED Canids campeã do CBLOL 2022 1º Split.",
    ),
    Team(
        name="LOUD",
        year=2024,
        region="BR",
        rarity="Historic",
        players=[
            Player("Robo", "Top", "K'Sante", 91, "LOUD", 2024),
            Player("Croc", "Jungle", "Vi", 88, "LOUD", 2024, nationality="KR"),
            Player("tinowns", "Mid", "Corki", 92, "LOUD", 2024),
            Player("Route", "ADC", "Jinx", 90, "LOUD", 2024, nationality="KR"),
            Player("RedBert", "Support", "Nautilus", 87, "LOUD", 2024),
        ],
        description="LOUD tetracampeã do CBLOL 2024 2º Split.",
    ),
    Team(
        name="paiN Gaming",
        year=2024,
        region="BR",
        rarity="Historic",
        players=[
            Player("Wizer", "Top", "Renekton", 86, "paiN Gaming", 2024),
            Player("Cariok", "Jungle", "Xin Zhao", 85, "paiN Gaming", 2024),
            Player("tinowns", "Mid", "Azir", 89, "paiN Gaming", 2024),
            Player("brTT", "ADC", "Jinx", 90, "paiN Gaming", 2024),
            Player("Luci", "Support", "Lulu", 83, "paiN Gaming", 2024, nationality="KR"),
        ],
        description="paiN Gaming campeã do CBLOL 2024 1º Split. brTT nonacampeão.",
    ),
]

# --- COMMON TEAMS (13) ---

COMMON_TEAMS = [
    Team(
        name="CNB e-Sports",
        year=2013,
        region="BR",
        rarity="Common",
        players=[
            Player("Leko", "Top", "Renekton", 74, "CNB e-Sports", 2013),
            Player("Revolta", "Jungle", "Lee Sin", 78, "CNB e-Sports", 2013),
            Player("takeshi", "Mid", "Karthus", 76, "CNB e-Sports", 2013),
            Player("manajj", "ADC", "Caitlyn", 73, "CNB e-Sports", 2013),
            Player("Alocs", "Support", "Thresh", 72, "CNB e-Sports", 2013),
        ],
        description="Primeira equipe profissional do Revolta.",
    ),
    Team(
        name="CNB e-Sports",
        year=2016,
        region="BR",
        rarity="Common",
        players=[
            Player("LEP", "Top", "Fiora", 79, "CNB e-Sports", 2016),
            Player("Minerva", "Jungle", "Graves", 77, "CNB e-Sports", 2016),
            Player("tinowns", "Mid", "Azir", 84, "CNB e-Sports", 2016),
            Player("pbo", "ADC", "Sivir", 74, "CNB e-Sports", 2016),
            Player("Wos", "Support", "Karma", 72, "CNB e-Sports", 2016),
        ],
        description="CNB com o jovem tinowns no meio.",
    ),
    Team(
        name="Vivo Keyd",
        year=2018,
        region="BR",
        rarity="Common",
        players=[
            Player("Yang", "Top", "Gangplank", 83, "Vivo Keyd", 2018),
            Player("Revolta", "Jungle", "Camille", 89, "Vivo Keyd", 2018),
            Player("Tockers", "Mid", "Azir", 85, "Vivo Keyd", 2018),
            Player("micaO", "ADC", "Kog'Maw", 87, "Vivo Keyd", 2018),
            Player("Jockster", "Support", "Braum", 82, "Vivo Keyd", 2018),
        ],
        description="Keyd com Revolta e micaO. Semi-finalistas CBLOL 2018.",
    ),
    Team(
        name="Flamengo eSports",
        year=2018,
        region="BR",
        rarity="Common",
        players=[
            Player("Tay", "Top", "Irelia", 82, "Flamengo eSports", 2018),
            Player("Shini", "Jungle", "Xin Zhao", 81, "Flamengo eSports", 2018),
            Player("Goku", "Mid", "Akali", 84, "Flamengo eSports", 2018),
            Player("brTT", "ADC", "Lucian", 90, "Flamengo eSports", 2018),
            Player("Luci", "Support", "Thresh", 80, "Flamengo eSports", 2018, nationality="KR"),
        ],
        description="Primeiro Flamengo no CBLOL com brTT.",
    ),
    Team(
        name="Rensga eSports",
        year=2021,
        region="BR",
        rarity="Common",
        players=[
            Player("Guigo", "Top", "Gnar", 81, "Rensga eSports", 2021),
            Player("Aegis", "Jungle", "Lee Sin", 80, "Rensga eSports", 2021),
            Player("tinowns", "Mid", "Ryze", 85, "Rensga eSports", 2021),
            Player("Absolut", "ADC", "Aphelios", 82, "Rensga eSports", 2021),
            Player("RedBert", "Support", "Leona", 83, "Rensga eSports", 2021),
        ],
        description="Rensga com tinowns como destaque.",
    ),
    Team(
        name="paiN Gaming",
        year=2022,
        region="BR",
        rarity="Common",
        players=[
            Player("Wizer", "Top", "Gnar", 84, "paiN Gaming", 2022),
            Player("CarioK", "Jungle", "Viego", 85, "paiN Gaming", 2022),
            Player("tinowns", "Mid", "Corki", 88, "paiN Gaming", 2022),
            Player("brTT", "ADC", "Jinx", 89, "paiN Gaming", 2022),
            Player("Luci", "Support", "Nautilus", 82, "paiN Gaming", 2022, nationality="KR"),
        ],
        description="paiN vice-campeã do CBLOL 2022 1º Split.",
    ),
    Team(
        name="Fluxo",
        year=2023,
        region="BR",
        rarity="Common",
        players=[
            Player("Guigo", "Top", "Jax", 82, "Fluxo", 2023),
            Player("Ayu", "Jungle", "Vi", 80, "Fluxo", 2023),
            Player("Cortezy", "Mid", "Akali", 84, "Fluxo", 2023),
            Player("Goot", "ADC", "Xayah", 82, "Fluxo", 2023),
            Player("Kuri", "Support", "Lulu", 79, "Fluxo", 2023),
        ],
        description="Fluxo estreando no CBLOL 2023.",
    ),
    Team(
        name="FURIA",
        year=2023,
        region="BR",
        rarity="Common",
        players=[
            Player("Tay", "Top", "Fiora", 83, "FURIA", 2023),
            Player("Shini", "Jungle", "Hecarim", 81, "FURIA", 2023),
            Player("Tutsz", "Mid", "Azir", 84, "FURIA", 2023),
            Player("Goot", "ADC", "Jinx", 82, "FURIA", 2023),
            Player("RedBert", "Support", "Thresh", 85, "FURIA", 2023),
        ],
        description="FURIA com a experiência de Tay, Shini e RedBert.",
    ),
    Team(
        name="RED Canids",
        year=2023,
        region="BR",
        rarity="Common",
        players=[
            Player("TitaN", "Top", "Renekton", 85, "RED Canids", 2023),
            Player("Buggax", "Jungle", "Vi", 81, "RED Canids", 2023),
            Player("Grevthar", "Mid", "Viktor", 82, "RED Canids", 2023),
            Player("Absolut", "ADC", "Jinx", 83, "RED Canids", 2023),
            Player("Guigo", "Support", "Nautilus", 80, "RED Canids", 2023),
        ],
        description="RED Canids no CBLOL 2023.",
    ),
    Team(
        name="Keyd Stars",
        year=2021,
        region="BR",
        rarity="Common",
        players=[
            Player("Guigo", "Top", "Gangplank", 81, "Keyd Stars", 2021),
            Player("Aegis", "Jungle", "Hecarim", 79, "Keyd Stars", 2021),
            Player("tinowns", "Mid", "Lucian", 86, "Keyd Stars", 2021),
            Player("aspas", "ADC", "Tristana", 90, "Keyd Stars", 2021),
            Player("RedBert", "Support", "Rakan", 83, "Keyd Stars", 2021),
        ],
        description="Keyd Stars com aspas no ADC antes de migrar pro VALORANT.",
    ),
    Team(
        name="Los Grandes",
        year=2023,
        region="BR",
        rarity="Common",
        players=[
            Player("Wizer", "Top", "Jax", 80, "Los Grandes", 2023),
            Player("Ranger", "Jungle", "Viego", 82, "Los Grandes", 2023),
            Player("Tutsz", "Mid", "Syndra", 83, "Los Grandes", 2023),
            Player("Goot", "ADC", "Xayah", 81, "Los Grandes", 2023),
            Player("Kuri", "Support", "Lulu", 78, "Los Grandes", 2023),
        ],
        description="Los Grandes no CBLOL 2023.",
    ),
    Team(
        name="Liberty",
        year=2022,
        region="BR",
        rarity="Common",
        players=[
            Player("Damage", "Top", "Gnar", 78, "Liberty", 2022),
            Player("Yampi", "Jungle", "Lee Sin", 77, "Liberty", 2022),
            Player("Vert", "Mid", "Orianna", 76, "Liberty", 2022),
            Player("Lobo", "ADC", "Jinx", 75, "Liberty", 2022),
            Player("Banggu", "Support", "Thresh", 74, "Liberty", 2022, nationality="KR"),
        ],
        description="Liberty no CBLOL 2022.",
    ),
    Team(
        name="Vorax",
        year=2021,
        region="BR",
        rarity="Common",
        players=[
            Player("Tay", "Top", "Renekton", 79, "Vorax", 2021),
            Player("Reven", "Jungle", "Jarvan IV", 77, "Vorax", 2021),
            Player("Envy", "Mid", "Viktor", 81, "Vorax", 2021),
            Player("Titan", "ADC", "Aphelios", 80, "Vorax", 2021),
            Player("Banggu", "Support", "Thresh", 75, "Vorax", 2021, nationality="KR"),
        ],
        description="Vorax no CBLOL 2021.",
    ),
]

ALL_TEAMS = LEGENDARY_TEAMS + HISTORIC_TEAMS + COMMON_TEAMS
TEAM_POOL: list[Team] = []
"""Temporary pool of teams not yet drawn this draft session."""


def draw_random_team() -> Team:
    """Sorteia 1 time aleatório do pool, respeitando os pesos de raridade.

    Se o pool estiver vazio, recria a partir de ALL_TEAMS.
    """
    global TEAM_POOL
    if not TEAM_POOL:
        TEAM_POOL = list(ALL_TEAMS)

    # Group teams by rarity with weights
    weighted = []
    for team in TEAM_POOL:
        weight = RARITY_WEIGHTS.get(team.rarity, 50)
        weighted.extend([team] * weight)

    chosen = random.choice(weighted)

    # Remove all instances of chosen team from pool (prevent repeat)
    TEAM_POOL = [t for t in TEAM_POOL if t.display_name != chosen.display_name]

    return chosen


def get_team_power(team_display_name: str) -> float:
    """Retorna o overall de um time pelo display_name. Fallback: 70.0."""
    for team in ALL_TEAMS:
        if team.display_name == team_display_name:
            return team.overall
    return 70.0


def get_team_by_display_name(name: str) -> Optional[Team]:
    """Encontra um time pelo display_name."""
    for team in ALL_TEAMS:
        if team.display_name == name:
            return team
    return None


def reset_pool():
    """Reseta o pool de times para o início."""
    global TEAM_POOL
    TEAM_POOL = list(ALL_TEAMS)


def _calc_player_team_attrs(players: list[Player]) -> list[str]:
    """Calcula atributos do time baseado nos jogadores selecionados.
    Retorna lista de strings com os atributos (ex: 'botlane_forte', 'star_player')."""
    attrs = []
    if not players:
        return attrs

    # Mapeia jogadores por role
    by_role = {p.role: p for p in players}

    # Bot lane forte: ADC e Support ambos overall >= 80
    adc = by_role.get("ADC")
    supp = by_role.get("Support")
    if adc and supp and adc.overall >= 80 and supp.overall >= 80:
        attrs.append("botlane_forte")

    # Top dominante: Top overall >= 85
    top = by_role.get("Top")
    if top and top.overall >= 85:
        attrs.append("toplane_dominante")

    # Mid carry: Mid overall >= 85
    mid = by_role.get("Mid")
    if mid and mid.overall >= 85:
        attrs.append("mid_carry")

    # Time coeso: todos os jogadores do mesmo time original
    teams = set(p.team for p in players)
    if len(teams) == 1:
        attrs.append("time_coeso")

    # Time veterano: media de anos dos players >= 3 (contando de 2025)
    avg_year = sum(2025 - p.year for p in players) / len(players)
    if avg_year >= 4:
        attrs.append("time_veterano")

    # Time jovem: media de anos < 2
    if avg_year < 2:
        attrs.append("time_jovem")

    # Star player: alguem com overall >= 90
    if any(p.overall >= 90 for p in players):
        attrs.append("star_player")

    # Stompa early: media overall >= 82
    avg_ovr = sum(p.overall for p in players) / len(players)
    if avg_ovr >= 82:
        attrs.append("stompa_early")

    # Pressao JG: Jungle overall >= 82
    jg = by_role.get("Jungle")
    if jg and jg.overall >= 82:
        attrs.append("jungle_pressao")

    return attrs
