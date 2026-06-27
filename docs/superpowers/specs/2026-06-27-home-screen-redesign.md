# Home Screen Redesign — Spec

> **Date:** 2026-06-27
> **App:** CBLOL 9A0 (Reflex)
> **Goal:** Reformular a home screen com design minimalista, foco em tipografia forte, assets visuais e clareza.

---

## 1. Contexto

Projeto Reflex com tema broadcast eSports (azul marinho `#0B1121` + dourado `#C9A84C`). A home atual tem hero section, 5 cards de passos "como funciona" e footer completo. O usuário quer algo mais limpo, direto ao ponto, com o mapa de Summoner's Rift como destaque visual e o logo horizontal na navbar.

**Assets disponíveis:**
- `assets/cblol9a0_logo_modern_horizontal.png` — logo horizontal para navbar
- `assets/cblol9a0_logo_modern_square.png` — logo quadrado
- `assets/summoners_rift_modern.png` — mapa de Summoner's Rift

---

## 2. Design

### 2.1 Navbar

Substituir o atual texto "CBLOL" + badge "9A0" pelo logo horizontal.

- Imagem: `cblol9a0_logo_modern_horizontal.png`
- Altura: ~30px, ajuste proporcional
- Alinhamento: vertical centrado na barra de 56px
- Manter: indicador de draft ("X/5 preenchidas") e botão "REINICIAR"

### 2.2 Hero Section (Home View)

Layout em **duas colunas** (flexbox) centralizadas verticalmente na viewport.

#### Coluna Esquerda (textual)
- **Tag label:** `"FANTASY GAME"` — font-size `0.75rem`, weight 700, color `GRAY`, letter-spacing `0.12em`, text-transform uppercase
- **Título principal:** `"MONTE O TIME DOS SONHOS"` — font-size clamp(`2.5rem`, `5vw`, `4.5rem`), weight 900, color `WHITE`, line-height 1.05, letter-spacing `-0.02em`
- **Subtítulo:** `"Drafte jogadores históricos do CBLOL e dispute a liga"` — font-size `1rem`, color `GRAY_D`, margin-top `1rem`
- **Botão:** `"INICIAR DRAFT"` — bg `GOLD`, color `BG`, font-size `1.1rem`, weight 800, padding `1rem 3rem`, border-radius `10px`, letter-spacing `0.05em`, margin-top `2rem`
  - Hover: bg `GOLD_L`, `transform: translateY(-2px)`, `box-shadow: 0 8px 24px rgba(201, 168, 76, 0.25)`
- **Alinhamento:** vertical centrado, ocupando ~55% da largura

#### Coluna Direita (visual)
- Imagem: `summoners_rift_modern.png`
- Largura: ~380px (ou 40% da viewport, com max-width)
- border-radius: `12px`
- border: `1px solid BORDER`
- box-shadow sutil com glow dourado: `0 0 40px rgba(201, 168, 76, 0.08)`

#### Comportamento responsivo
- `flex_wrap="wrap"` para empilhar em telas menores
- Quando empilhado: mapa vai para baixo do texto, centralizado

### 2.3 "Como Funciona" (estilo minimalista, sem cards)

- **Título:** `"COMO FUNCIONA"` — font-size `0.7rem`, weight 700, color `GRAY_D`, letter-spacing `0.1em`, text-align center, margin-bottom `2rem`
- **5 passos em linha horizontal:**
  - Cada passo: número grande dourado + nome do passo
  - Número: font-size `2rem`, weight 900, color `GOLD`, line-height 1
  - Nome: font-size `0.75rem`, weight 600, color `WHITE`, margin-top `0.3rem`
  - Sem descrições textuais extras
  - Sem cards, sem border, sem background
  - Gap entre passos: `3rem`
  - Separador opcional: linha vertical sutil `BORDER` entre passos

### 2.4 Footer (simplificado)

- Logo "CBLOL 9A0" + texto descritivo (1 linha)
- Copyright: `"2025 CBLOL 9A0. League of Legends é propriedade da Riot Games."`
- Remover as 3 colunas de links (JOGO, RARIDADES, CREDITOS)
- Reduzir padding vertical

---

## 3. Implementação

### Arquivos afetados
- **Modificar:** `cblol9a0/ui.py` — funções `navbar()`, `home_view()`, remover `_hero_champion()`, `_step_card()`, simplificar footer

### O que remover
- `_hero_champion()` — ícones de campeões por role (não estarão mais na home)
- `_step_card()` — cards com número + título + descrição (substituídos por texto puro)
- Seção footer com 3 colunas de links
- Ícones de papel de parede / círculos de campeão da hero section

### O que criar
- Nova função helper `_how_to_step(number, title)` — renderiza um passo minimalista

### O que modificar
- `navbar()` — trocar texto pelo logo horizontal
- `home_view()` — reescrever completamente o layout
- Footer dentro de `home_view()` — simplificar

### Paleta de cores (mantida)
```python
BG = "#0B1121"
BG_CARD = "#131B2F"
BG_SURFACE = "#1A2540"
GOLD = "#C9A84C"
GOLD_L = "#E0C76E"
WHITE = "#FFFFFF"
GRAY = "#8B93A5"
GRAY_D = "#5A6378"
BORDER = "#1E2D4A"
```

### Constantes mantidas
- `ROLE_ICONS`, `HERO_CHAMPIONS` — não usadas na home, mas mantidas para outras views
- `RARITY_COLORS`, `PHASE_COLORS`, `ROLE_ORDER` — mantidas

---

## 4. Critérios de Sucesso

- [ ] Home renderiza com layout de 2 colunas (texto + mapa)
- [ ] Logo horizontal aparece na navbar substituindo o texto "CBLOL 9A0"
- [ ] Navbar mantém funcionalidade de indicador de draft e botão REINICIAR
- [ ] Botão "INICIAR DRAFT" inicia o fluxo de jogo (`GameState.init_draft`)
- [ ] Seção "COMO FUNCIONA" mostra 5 passos em linha, sem cards, sem hover
- [ ] Footer simplificado com apenas logo + copyright
- [ ] Layout responsivo empilha em telas menores
- [ ] Navegação entre views (home/draft/league/match/result/playoffs) continua funcionando
- [ ] Cores e tipografia seguem a paleta temática existente
