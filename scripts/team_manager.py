#!/usr/bin/env python3
"""
Gerenciador de Times e Jogadores — CBLOL 9A0

Gera o arquivo data.py com times e jogadores a partir de dados JSON salvos.
Totalmente independente do jogo, só serve para atualizar data.py.

Uso:
    python scripts/team_manager.py          # modo interativo
    python scripts/team_manager.py build    # gera data.py do JSON salvo

Dados salvos em: scripts/teams_data.json
Saída gerada:    cblol9a0/data.py
"""

import json
import os
import shutil
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional

# ─── Caminhos ────────────────────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "cblol9a0", "data.py")
JSON_PATH = os.path.join(BASE_DIR, "scripts", "teams_data.json")
BACKUP_PATH = os.path.join(BASE_DIR, "scripts", "teams_data_backup.json")

# ─── Modelos de dados (cópia simplificada dos do data.py) ───────────────

VALID_ROLES = ["Top", "Jungle", "Mid", "ADC", "Support"]
VALID_RARITIES = ["Common", "Historic", "Legendary"]

VALID_TAGS = [
    "carry", "veteran", "forte_1v1", "teamplayer", "objective_control",
    "playmaker", "early_game", "late_game", "jungle_ladrao",
    "jungle_agressivo", "clutch", "consistente", "internacional",
]


@dataclass
class PlayerData:
    name: str = ""
    role: str = ""
    champion: str = ""
    overall: int = 50
    team: str = ""
    year: int = 2020
    nationality: str = "BR"
    tags: list[str] = field(default_factory=list)


@dataclass
class TeamData:
    name: str = ""
    year: int = 2020
    region: str = "BR"
    rarity: str = "Common"
    display_name: str = ""
    description: str = ""
    players: list[PlayerData] = field(default_factory=list)


# ─── Utilitários ─────────────────────────────────────────────────────────

def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def _input_int(prompt: str, default: int = 0, lo: int = 0, hi: int = 999) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            v = int(raw)
            return _clamp(v, lo, hi)
        except ValueError:
            print(f"  Número inválido. Digite entre {lo} e {hi}.")


def _input_str(prompt: str, default: str = "") -> str:
    raw = input(prompt).strip()
    if not raw and default:
        return default
    return raw


def _input_choice(prompt: str, options: list[str], default: str = "") -> str:
    while True:
        raw = input(prompt).strip().lower()
        if not raw and default:
            return default
        for opt in options:
            if opt.lower().startswith(raw):
                return opt
        print(f"  Opções: {', '.join(options)}")


# ─── IO JSON ─────────────────────────────────────────────────────────────

def load_teams() -> list[dict]:
    if not os.path.exists(JSON_PATH):
        return []
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_teams(teams: list[dict]):
    # Backup
    if os.path.exists(JSON_PATH):
        shutil.copy2(JSON_PATH, BACKUP_PATH)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(teams, f, ensure_ascii=False, indent=2)
    print(f"  ✅ Dados salvos em {JSON_PATH}")


# ─── Geração do data.py ─────────────────────────────────────────────────

def _escape(s: str) -> str:
    """Escapa string para código Python."""
    return json.dumps(s, ensure_ascii=False)


def build_data_py(teams: list[dict]) -> str:
    """Gera o conteúdo completo de cblol9a0/data.py a partir da lista de times."""
    lines = []
    lines.append('from dataclasses import dataclass, field')
    lines.append('from typing import Optional')
    lines.append('import random')
    lines.append('')

    # Player dataclass
    lines.append('')
    lines.append('')
    lines.append('@dataclass')
    lines.append('class Player:')
    lines.append('    name: str')
    lines.append('    role: str  # "Top" | "Jungle" | "Mid" | "ADC" | "Support"')
    lines.append('    champion: str')
    lines.append('    overall: int  # 1–99')
    lines.append('    team: str')
    lines.append('    year: int')
    lines.append('    nationality: str = "BR"')
    lines.append('    tags: list[str] = field(default_factory=list)')
    lines.append('')

    # Team dataclass
    lines.append('')
    lines.append('@dataclass')
    lines.append('class Team:')
    lines.append('    name: str')
    lines.append('    year: int')
    lines.append('    region: str')
    lines.append('    rarity: str  # "Common" | "Historic" | "Legendary"')
    lines.append('    players: list[Player]')
    lines.append('    description: str = ""')
    lines.append('')
    lines.append('    @property')
    lines.append('    def overall(self) -> float:')
    lines.append('        return sum(p.overall for p in self.players) / len(self.players)')
    lines.append('')
    lines.append('    @property')
    lines.append('    def display_name(self) -> str:')
    lines.append('        return f"{self.name} ({self.year})"')
    lines.append('')

    # ALL_TEAMS
    lines.append('')
    lines.append('# ====== TIMES ======')
    lines.append('')
    lines.append('ALL_TEAMS: list[Team] = [')
    lines.append('')

    for td in teams:
        name = td.get("name", "Time")
        year = td.get("year", 2020)
        region = td.get("region", "BR")
        rarity = td.get("rarity", "Common")
        desc = td.get("description", "")
        players = td.get("players", [])

        lines.append(f'    Team(')
        lines.append(f'        name={_escape(name)},')
        lines.append(f'        year={year},')
        lines.append(f'        region={_escape(region)},')
        lines.append(f'        rarity={_escape(rarity)},')
        lines.append(f'        description={_escape(desc)},')
        lines.append(f'        players=[')
        for p in players:
            p_name = p.get("name", "")
            p_role = p.get("role", "Mid")
            p_champ = p.get("champion", "Ahri")
            p_ovr = p.get("overall", 50)
            p_year = p.get("year", year)
            p_nat = p.get("nationality", "BR")
            p_tags = p.get("tags", [])
            tags_str = ", ".join(_escape(t) for t in p_tags)
            lines.append(f'            Player(')
            lines.append(f'                name={_escape(p_name)},')
            lines.append(f'                role={_escape(p_role)},')
            lines.append(f'                champion={_escape(p_champ)},')
            lines.append(f'                overall={p_ovr},')
            lines.append(f'                team={_escape(name)},')
            lines.append(f'                year={p_year},')
            lines.append(f'                nationality={_escape(p_nat)},')
            lines.append(f'                tags=[{tags_str}],')
            lines.append(f'            ),')
        lines.append(f'        ],')
        lines.append(f'    ),')
        lines.append('')

    lines.append(']')
    lines.append('')

    # Funções auxiliares
    lines.append('')
    lines.append('# ====== FUNÇÕES AUXILIARES ======')
    lines.append('')
    lines.append('')
    lines.append('def champion_icon_url(champion: str) -> str:')
    lines.append('    """Retorna a URL do ícone do campeão na DDragon."""')
    lines.append('    return f"https://ddragon.leagueoflegends.com/cdn/14.10.1/img/champion/{champion}.png"')
    lines.append('')
    lines.append('')
    lines.append('TEAM_POOL: list[Team] = []')
    lines.append('')
    lines.append('')
    lines.append('def draw_random_team() -> Team:')
    lines.append('    global TEAM_POOL')
    lines.append('    if not TEAM_POOL:')
    lines.append('        TEAM_POOL = list(ALL_TEAMS)')
    lines.append('    idx = random.randint(0, len(TEAM_POOL) - 1)')
    lines.append('    return TEAM_POOL.pop(idx)')
    lines.append('')
    lines.append('')
    lines.append('def reset_pool():')
    lines.append('    """Reseta o pool de times para o início."""')
    lines.append('    global TEAM_POOL')
    lines.append('    TEAM_POOL = list(ALL_TEAMS)')
    lines.append('')
    lines.append('')
    lines.append('def get_team_power(team_name: str) -> float:')
    lines.append('    for t in ALL_TEAMS:')
    lines.append('        if t.display_name == team_name:')
    lines.append('            return t.overall')
    lines.append('    return 50.0')
    lines.append('')
    lines.append('')
    lines.append('def get_team_by_display_name(display_name: str) -> Optional[Team]:')
    lines.append('    for t in ALL_TEAMS:')
    lines.append('        if t.display_name == display_name:')
    lines.append('            return t')
    lines.append('    return None')
    lines.append('')

    # _calc_player_team_attrs
    lines.append('')
    lines.append('def _calc_player_team_attrs(players: list[Player]) -> list[str]:')
    lines.append('    """Calcula atributos do time baseado nos jogadores selecionados."""')
    lines.append('    attrs = []')
    lines.append('    if not players:')
    lines.append('        return attrs')
    lines.append('    by_role = {p.role: p for p in players}')
    lines.append('')
    lines.append('    adc = by_role.get("ADC")')
    lines.append('    supp = by_role.get("Support")')
    lines.append('    if adc and supp and adc.overall >= 80 and supp.overall >= 80:')
    lines.append('        attrs.append("botlane_forte")')
    lines.append('')
    lines.append('    top = by_role.get("Top")')
    lines.append('    if top and top.overall >= 85:')
    lines.append('        attrs.append("toplane_dominante")')
    lines.append('')
    lines.append('    mid = by_role.get("Mid")')
    lines.append('    if mid and mid.overall >= 85:')
    lines.append('        attrs.append("mid_carry")')
    lines.append('')
    lines.append('    teams = set(p.team for p in players)')
    lines.append('    if len(teams) == 1:')
    lines.append('        attrs.append("time_coeso")')
    lines.append('')
    lines.append('    avg_year = sum(2025 - p.year for p in players) / len(players)')
    lines.append('    if avg_year >= 4:')
    lines.append('        attrs.append("time_veterano")')
    lines.append('    if avg_year < 2:')
    lines.append('        attrs.append("time_jovem")')
    lines.append('')
    lines.append('    if any(p.overall >= 90 for p in players):')
    lines.append('        attrs.append("star_player")')
    lines.append('')
    lines.append('    avg_ovr = sum(p.overall for p in players) / len(players)')
    lines.append('    if avg_ovr >= 82:')
    lines.append('        attrs.append("stompa_early")')
    lines.append('')
    lines.append('    jg = by_role.get("Jungle")')
    lines.append('    if jg and jg.overall >= 82:')
    lines.append('        attrs.append("jungle_pressao")')
    lines.append('')
    lines.append('    return attrs')
    lines.append('')

    return "\n".join(lines)


def write_data_py(content: str):
    """Escreve o conteúdo gerado em data.py com backup."""
    backup = DATA_PATH + ".bak"
    if os.path.exists(DATA_PATH):
        shutil.copy2(DATA_PATH, backup)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ {DATA_PATH} atualizado ({len(content)} bytes)")
    print(f"  💾 Backup salvo em {backup}")


# ─── Modo Interativo ─────────────────────────────────────────────────────

def interactive():
    teams = load_teams()

    while True:
        print("\n" + "=" * 50)
        print("  GERENCIADOR DE TIMES - CBLOL 9A0")
        print("=" * 50)
        print(f"  Times cadastrados: {len(teams)}")
        print()
        print("  1) Listar times")
        print("  2) Adicionar time")
        print("  3) Remover time")
        print("  4) Editar time")
        print("  5) Gerenciar jogadores de um time")
        print("  6) Gerar data.py")
        print("  7) Sair")
        print()
        opt = input("  Escolha: ").strip()

        if opt == "1":
            _list_teams(teams)
        elif opt == "2":
            _add_team(teams)
        elif opt == "3":
            _remove_team(teams)
        elif opt == "4":
            _edit_team(teams)
        elif opt == "5":
            _manage_players(teams)
        elif opt == "6":
            content = build_data_py(teams)
            write_data_py(content)
        elif opt == "7":
            print("  Até mais!")
            break
        else:
            print("  Opção inválida.")


def _list_teams(teams: list[dict]):
    if not teams:
        print("  Nenhum time cadastrado.")
        return
    print(f"\n  {'#':>3}  {'Time':<30} {'Ano':>4} {'Raridade':<12} {'Jogadores':>5}")
    print("  " + "-" * 62)
    for i, t in enumerate(teams):
        n = len(t.get("players", []))
        print(f"  {i+1:>3}) {t.get('name','?'):<30} {t.get('year',0):>4} {t.get('rarity','?'):<12} {n:>5}")


def _pick_team(teams: list[dict]) -> Optional[int]:
    _list_teams(teams)
    if not teams:
        return None
    while True:
        raw = input("  Número do time (Enter cancela): ").strip()
        if not raw:
            return None
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(teams):
                return idx
        except ValueError:
            pass
        print("  Número inválido.")


def _add_team(teams: list[dict]):
    print("\n  ── Novo Time ──")
    name = _input_str("  Nome do time: ")
    if not name:
        print("  Cancelado.")
        return
    year = _input_int("  Ano (ex: 2015): ", default=2020, lo=2010, hi=2030)
    region = _input_str("  Região (BR): ", default="BR") or "BR"
    rarity = _input_choice("  Raridade (Common/Historic/Legendary): ", VALID_RARITIES, default="Common")
    desc = _input_str("  Descrição (opcional): ")

    team = {
        "name": name,
        "year": year,
        "region": region,
        "rarity": rarity,
        "description": desc,
        "players": [],
    }
    teams.append(team)
    print(f"  ✅ Time '{name}' adicionado!")

    # Pergunta se quer adicionar jogadores agora
    add_players = input("  Adicionar jogadores agora? (S/n): ").strip().lower()
    if add_players in ("", "s", "sim"):
        _add_players_to_team(team)
    save_teams(teams)


def _remove_team(teams: list[dict]):
    idx = _pick_team(teams)
    if idx is None:
        return
    t = teams[idx]
    confirm = input(f"  Remover '{t['name']}' ({t['year']})? (s/N): ").strip().lower()
    if confirm in ("s", "sim"):
        removed = teams.pop(idx)
        save_teams(teams)
        print(f"  🗑️  '{removed['name']}' removido.")
    else:
        print("  Cancelado.")


def _edit_team(teams: list[dict]):
    idx = _pick_team(teams)
    if idx is None:
        return
    t = teams[idx]
    print(f"\n  Editando: {t['name']} ({t['year']})")
    print("  Enter = manter valor atual")
    name = _input_str(f"  Nome [{t['name']}]: ", default=t['name'])
    year = _input_int(f"  Ano [{t['year']}]: ", default=t['year'], lo=2010, hi=2030)
    region = _input_str(f"  Região [{t['region']}]: ", default=t['region']) or t['region']
    rarity = _input_choice(f"  Raridade ({'/'.join(VALID_RARITIES)}) [{t['rarity']}]: ", VALID_RARITIES, default=t['rarity'])
    desc = _input_str(f"  Descrição [{t.get('description','')}]: ", default=t.get('description', ''))

    t['name'] = name
    t['year'] = year
    t['region'] = region
    t['rarity'] = rarity
    t['description'] = desc
    save_teams(teams)
    print("  ✅ Time atualizado!")


def _manage_players(teams: list[dict]):
    idx = _pick_team(teams)
    if idx is None:
        return
    team = teams[idx]

    while True:
        players = team.get("players", [])
        print(f"\n  ── Jogadores de {team['name']} ({len(players)}) ──")
        for i, p in enumerate(players):
            tags_str = ", ".join(p.get("tags", []))
            print(f"  {i+1:>3}) {p.get('name','?'):<20} {p.get('role','?'):<8} "
                  f"{p.get('champion','?'):<12} OVR {p.get('overall',0):>2}  [{tags_str}]")
        print()
        print("  1) Adicionar jogador")
        print("  2) Editar jogador")
        print("  3) Remover jogador")
        print("  4) Voltar")
        opt = input("  Escolha: ").strip()

        if opt == "1":
            _add_players_to_team(team, single=True)
            save_teams(teams)
        elif opt == "2":
            _edit_player(players)
            save_teams(teams)
        elif opt == "3":
            _remove_player(players)
            save_teams(teams)
        elif opt == "4":
            break


def _add_players_to_team(team: dict, single: bool = False):
    """Adiciona um ou mais jogadores ao time."""
    while True:
        print(f"\n  ── Novo Jogador ({team['name']}) ──")
        name = _input_str("  Nome: ")
        if not name:
            if single:
                return
            break

        role = _input_choice(f"  Role ({'/'.join(VALID_ROLES)}): ", VALID_ROLES)
        champion = _input_str("  Campeão: ")
        overall = _input_int("  Overall (1-99): ", default=50, lo=1, hi=99)
        nationality = _input_str("  Nacionalidade (BR): ", default="BR") or "BR"

        print("  Tags disponíveis:")
        print(f"    {', '.join(VALID_TAGS)}")
        tags_raw = _input_str("  Tags (separadas por vírgula, opcional): ")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip() in VALID_TAGS]

        player = {
            "name": name,
            "role": role,
            "champion": champion,
            "overall": overall,
            "year": team.get("year", 2020),
            "nationality": nationality,
            "tags": tags,
        }
        team.setdefault("players", []).append(player)
        print(f"  ✅ Jogador '{name}' adicionado!")

        if single:
            break
        again = input("  Adicionar outro? (S/n): ").strip().lower()
        if again not in ("", "s", "sim"):
            break


def _edit_player(players: list[dict]):
    if not players:
        print("  Nenhum jogador.")
        return
    while True:
        raw = input("  Número do jogador (Enter cancela): ").strip()
        if not raw:
            return
        try:
            idx = int(raw) - 1
            if not (0 <= idx < len(players)):
                print("  Número inválido.")
                continue
        except ValueError:
            print("  Número inválido.")
            continue
        break

    p = players[idx]
    print(f"  Editando: {p['name']}")
    print("  Enter = manter valor atual")
    name = _input_str(f"  Nome [{p['name']}]: ", default=p['name'])
    role = _input_choice(f"  Role ({'/'.join(VALID_ROLES)}) [{p['role']}]: ", VALID_ROLES, default=p['role'])
    champion = _input_str(f"  Campeão [{p['champion']}]: ", default=p['champion'])
    overall = _input_int(f"  Overall [{p['overall']}]: ", default=p['overall'], lo=1, hi=99)
    nat = _input_str(f"  Nacionalidade [{p.get('nationality','BR')}]: ", default=p.get('nationality', 'BR'))

    print(f"  Tags atuais: {', '.join(p.get('tags', []))}")
    print(f"  Tags disp:   {', '.join(VALID_TAGS)}")
    tags_raw = _input_str("  Tags (separadas por vírgula, Enter mantém): ")
    tags = [t.strip() for t in tags_raw.split(",") if t.strip() in VALID_TAGS] if tags_raw else p.get("tags", [])

    p['name'] = name
    p['role'] = role
    p['champion'] = champion
    p['overall'] = overall
    p['nationality'] = nat
    p['tags'] = tags
    print("  ✅ Jogador atualizado!")


def _remove_player(players: list[dict]):
    if not players:
        print("  Nenhum jogador.")
        return
    while True:
        raw = input("  Número do jogador (Enter cancela): ").strip()
        if not raw:
            return
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(players):
                removed = players.pop(idx)
                print(f"  🗑️  '{removed['name']}' removido.")
                return
        except ValueError:
            pass
        print("  Número inválido.")


# ─── Build (modo script) ────────────────────────────────────────────────

def build():
    teams = load_teams()
    if not teams:
        print("  ❌ Nenhum time encontrado em", JSON_PATH)
        print("  Use 'python scripts/team_manager.py' no modo interativo primeiro.")
        sys.exit(1)
    content = build_data_py(teams)
    write_data_py(content)


# ─── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    else:
        interactive()
