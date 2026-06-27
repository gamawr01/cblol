# Home Screen Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reformular a home screen com layout de 2 colunas (texto + mapa), navbar com logo horizontal, seção "como funciona" minimalista e footer simplificado.

**Architecture:** Modificações concentradas em `cblol9a0/ui.py`. A navbar ganha o logo horizontal em vez do texto. A `home_view()` é reescrita com layout flex de 2 colunas. As funções auxiliares `_hero_champion()` e `_step_card()` são removidas, substituídas por `_how_to_step()` minimalista. Footer é simplificado para logo + copyright.

**Tech Stack:** Python, Reflex (rx), assets em `assets/`

---

### Task 1: Atualizar a navbar com o logo horizontal

**Files:**
- Modify: `cblol9a0/ui.py:57-114`

- [ ] **Step 1: Substituir o texto "CBLOL" + badge "9A0" pelo logo horizontal na navbar**

No arquivo `cblol9a0/ui.py`, na função `navbar()`, substituir:

```python
rx.hstack(
    rx.text("CBLOL", font_size="1.05rem", font_weight="800", color=WHITE,
             letter_spacing="0.02em"),
    rx.text("9A0", font_size="0.7rem", font_weight="900", color=BG,
             bg=GOLD, px="0.35rem", py="0.1rem", border_radius="4px"),
    gap="0.3rem",
    align="center",
),
```

Por:

```python
rx.image(
    src="/assets/cblol9a0_logo_modern_horizontal.png",
    height="30px",
    width="auto",
),
```

- [ ] **Step 2: Verificar visualmente no browser**

Acessar `http://localhost:3000` e confirmar que o logo aparece na navbar no lugar do texto, mantendo alinhamento correto.

- [ ] **Step 3: Commit**

```bash
git add cblol9a0/ui.py
git commit -m "feat: substituir texto por logo horizontal na navbar"
```

---

### Task 2: Reescrever a hero section com layout de 2 colunas

**Files:**
- Modify: `cblol9a0/ui.py:118-214` (função `home_view()`)
- Remove: funções `_hero_champion()` (linhas 119-132) e `_step_card()` (linhas 135-148) — serão removidas no Task 3

- [ ] **Step 1: Escrever a nova hero section**

Substituir a hero section atual (linhas 153-214) por:

```python
# Hero — 2 colunas: texto + mapa
rx.flex(
    # Coluna esquerda — textual
    rx.box(
        rx.text(
            "FANTASY GAME",
            font_size="0.75rem",
            font_weight="700",
            color=GRAY,
            letter_spacing="0.12em",
            text_transform="uppercase",
        ),
        rx.text(
            "MONTE O TIME",
            font_size="min(4.5rem, 8vw)",
            font_weight="900",
            color=WHITE,
            line_height="1.05",
            letter_spacing="-0.02em",
            mt="0.4rem",
        ),
        rx.text(
            "DOS SONHOS",
            font_size="min(4.5rem, 8vw)",
            font_weight="900",
            color=GOLD,
            line_height="1.05",
            letter_spacing="-0.02em",
        ),
        rx.text(
            "Drafte jogadores historicos do CBLOL e dispute a liga.",
            font_size="1rem",
            color=GRAY_D,
            mt="1.2rem",
            line_height="1.5",
            max_w="420px",
        ),
        rx.button(
            "INICIAR DRAFT",
            on_click=GameState.init_draft,
            bg=GOLD,
            color=BG,
            font_weight="800",
            font_size="1.1rem",
            px="3rem",
            py="1rem",
            border_radius="10px",
            mt="2rem",
            cursor="pointer",
            letter_spacing="0.05em",
            _hover={
                "bg": GOLD_L,
                "transform": "translateY(-2px)",
                "box_shadow": "0 8px 24px rgba(201, 168, 76, 0.25)",
            },
        ),
        flex="1",
        min_w="280px",
    ),
    # Coluna direita — mapa
    rx.box(
        rx.image(
            src="/assets/summoners_rift_modern.png",
            width="100%",
            height="auto",
            border_radius="12px",
            border="1px solid " + BORDER,
            box_shadow="0 0 40px rgba(201, 168, 76, 0.08)",
        ),
        flex="1",
        min_w="280px",
        display="flex",
        align_items="center",
        justify_content="center",
    ),
    gap="3rem",
    align="center",
    justify="center",
    width="100%",
    max_w="1100px",
    mx="auto",
    flex_wrap="wrap",
    py="6rem",
    px="2rem",
),
```

- [ ] **Step 2: Verificar visualmente no browser**

Confirmar que a home mostra:
- Tag "FANTASY GAME" no topo
- Título "MONTE O TIME" (branco) + "DOS SONHOS" (dourado) em duas linhas
- Subtítulo descritivo
- Botão "INICIAR DRAFT" estilizado
- Mapa de Summoner's Rift à direita
- Em telas menores, o mapa vai para baixo do texto

- [ ] **Step 3: Commit**

```bash
git add cblol9a0/ui.py
git commit -m "feat: nova hero section com layout de 2 colunas e mapa"
```

---

### Task 3: Substituir "Como Funciona" por versão minimalista

**Files:**
- Modify: `cblol9a0/ui.py:216-234`
- Remove: `_hero_champion()` (linhas 119-132) e `_step_card()` (linhas 135-148)

- [ ] **Step 1: Remover funções auxiliares antigas**

Remover `_hero_champion()` (linhas 119-132) e `_step_card()` (linhas 135-148) do arquivo.

- [ ] **Step 2: Criar nova função auxiliar `_how_to_step`**

Adicionar antes de `home_view()`:

```python
def _how_to_step(num: str, title: str) -> rx.Component:
    return rx.box(
        rx.text(num, font_size="2rem", font_weight="900", color=GOLD,
                 line_height="1", text_align="center"),
        rx.text(title, font_size="0.75rem", font_weight="600", color=WHITE,
                 text_align="center", mt="0.3rem"),
        text_align="center",
    )
```

- [ ] **Step 3: Substituir a seção "Como Funciona" na home_view**

Substituir o bloco atual (linhas 216-234) por:

```python
# How it works — minimalista
rx.box(
    rx.text("COMO FUNCIONA", font_size="0.7rem", font_weight="700", color=GRAY_D,
             text_align="center", letter_spacing="0.1em", mb="2rem"),
    rx.flex(
        _how_to_step("1", "Escolha"),
        _how_to_step("2", "Reroll"),
        _how_to_step("3", "Liga"),
        _how_to_step("4", "Playoffs"),
        _how_to_step("5", "Titulo"),
        gap="3rem",
        justify="center",
        flex_wrap="wrap",
    ),
    py="4rem",
    px="2rem",
    bg=BG,
    border_top="1px solid " + BORDER,
),
```

- [ ] **Step 4: Verificar visualmente no browser**

Confirmar que os 5 passos aparecem em linha horizontal:
- Número grande dourado
- Nome do passo em branco
- Sem cards, sem bordas, sem descrições longas

- [ ] **Step 5: Commit**

```bash
git add cblol9a0/ui.py
git commit -m "feat: secao como funciona minimalista sem cards"
```

---

### Task 4: Simplificar o footer

**Files:**
- Modify: `cblol9a0/ui.py:236-291` (footer dentro de `home_view()`)

- [ ] **Step 1: Substituir o footer atual por versão simplificada**

Substituir o bloco do footer (linhas 236-291) por:

```python
# Footer simplificado
rx.box(
    rx.hstack(
        rx.text("CBLOL", font_weight="800", color=WHITE, font_size="0.9rem"),
        rx.text("9A0", font_size="0.65rem", font_weight="800", color=BG,
                 bg=GOLD, px="0.3rem", py="0.05rem", border_radius="3px"),
        gap="0.2rem",
        align="center",
    ),
    rx.text(
        "Jogo de draft historico do cenario brasileiro de League of Legends.",
        font_size="0.7rem", color=GRAY_D, mt="0.4rem",
    ),
    rx.text(
        "2025 CBLOL 9A0. League of Legends e propriedade da Riot Games.",
        font_size="0.65rem", color=GRAY_D, mt="0.3rem",
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
),
```

- [ ] **Step 2: Verificar visualmente no browser**

Confirmar que o footer mostra:
- Logo "CBLOL 9A0" centralizado
- Texto descritivo
- Copyright
- Sem colunas de links (JOGO, RARIDADES, CREDITOS)

- [ ] **Step 3: Commit**

```bash
git add cblol9a0/ui.py
git commit -m "feat: footer simplificado com logo e copyright"
```

---

### Task 5: Teste funcional completo

**Files:**
- No file changes — verification only

- [ ] **Step 1: Testar fluxo completo de navegação**

No browser (`http://localhost:3000`):

1. Home carrega com novo design
2. Clicar "INICIAR DRAFT" → navega para tela de draft
3. Preencher os 5 slots de draft
4. Verificar que a liga funciona corretamente
5. Jogar partida, verificar resultado
6. Navegar playoffs
7. Clicar "REINICIAR" → volta para home com novo design
8. Confirmar que navbar mostra indicador de draft durante o draft
9. Confirmar que botão "REINICIAR" aparece durante draft/league/match

- [ ] **Step 2: Commit final (se necessário)**

Se houver ajustes, commitá-los:

```bash
git add cblol9a0/ui.py
git commit -m "fix: ajustes finos na home screen redesign"
```

---

### Task 6: Push para o remote

- [ ] **Step 1: Push**

```bash
git push origin main
```
