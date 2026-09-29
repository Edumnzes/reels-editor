# Reels Editor — skill para Claude Code

Transforma vídeos brutos gravados no celular em **Reels / TikTok / Shorts prontos (1080×1920)**:
corta pausas e respirações, coloca legendas dinâmicas palavra por palavra, faz zooms suaves
acompanhando o rosto, adiciona motion graphics explicativos, corrige a cor e limpa a voz
com o Adobe Podcast Enhance Speech.

> **Uso privado.** Este repositório é proprietário — veja [LICENSE.md](LICENSE.md) e
> [TERMOS_DE_USO.md](TERMOS_DE_USO.md).

---

## Índice
1. [O que a skill faz](#o-que-a-skill-faz)
2. [Requisitos](#requisitos)
3. [Instalação](#instalação)
4. [Como usar](#como-usar)
5. [Estrutura do repositório](#estrutura-do-repositório)
6. [Comandos do projeto](#comandos-do-projeto)
7. [Efeitos sonoros](#efeitos-sonoros)
8. [Áudio com Adobe Podcast](#áudio-com-adobe-podcast)
9. [Limitações](#limitações)
10. [Solução de problemas](#solução-de-problemas)
11. [Documentação detalhada](#documentação-detalhada)

---

## O que a skill faz

| Etapa | Resultado |
|---|---|
| Análise | Transcrição com tempo de cada palavra, mapa de pausas, detecção de rostos, resumo do vídeo |
| Corte | Remove silêncio, respirações, "éé", falsas largadas e repetições; verifica o corte transcrevendo de novo |
| Câmera virtual | Zooms leves só nos cortes, enquadramento fixo (tripé) ou acompanhamento suave do rosto |
| Legendas | Palavra por palavra, 3 estilos (Hormozi, minimal/autoridade, cinematográfico), palavras-chave destacadas |
| Motion graphics | Selos, cards, listas, contadores, gráficos e chamada final — posicionados fora do rosto |
| Cor | Ajustes prontos (natural, clean_warm, teal_orange, moody, vivid_day) com comparação lado a lado |
| Áudio | Voz tratada pelo Adobe Podcast + ambiente dosado + volume no padrão do Instagram (−14 LUFS) |
| Entrega | `Downloads/<nome>_reels_final.mp4` + resumo do que foi feito e pontos para conferir |

O fluxo completo, passo a passo, está em [docs/FLUXO.md](docs/FLUXO.md).

## Requisitos

- **Claude Code** (app desktop, CLI ou extensão de IDE) com suporte a skills.
- **Python 3.10+** instalado no sistema (só para criar o ambiente; o resto é automático).
- ~2 GB livres (modelo de transcrição Whisper baixado no primeiro uso).
- Windows, macOS ou Linux. Testado principalmente no Windows 11.
- Opcional: **conector Adobe for creativity** no Claude, para o tratamento de voz.
- Opcional: arquivos de efeitos sonoros licenciados (veja [Efeitos sonoros](#efeitos-sonoros)).

Não é preciso instalar ffmpeg: a skill usa o binário do pacote `imageio-ffmpeg`.

## Instalação

```bash
git clone https://github.com/Edumnzes/reels-editor.git ~/.claude/skills/reels-editor
```

```bash
python ~/.claude/skills/reels-editor/scripts/setup_env.py
```

O segundo comando cria o ambiente Python em `~/reelsenv` (caminho curto de propósito — caminhos
longos quebram o `venv` no Windows) e instala as dependências de [requirements.txt](requirements.txt).
Ele imprime o caminho do Python e do ffmpeg que a skill vai usar.

Para atualizar depois:

```bash
git -C ~/.claude/skills/reels-editor pull
```

## Como usar

No Claude Code, anexe o vídeo e chame a skill:

```
@"C:\Users\voce\Downloads\VIDEO.MOV"
/reels-editor
```

Ou simplesmente peça em linguagem natural: *"edita esse vídeo para Reels, corta as pausas e
coloca legenda"*. A skill também é acionada por pedidos parciais (só legendas, só o corte, só o áudio).

O Claude vai:
1. analisar o vídeo e mostrar o mapa (tempo | plano | fala | tratamento sugerido);
2. perguntar o que só você sabe (nome do evento, @, estilo);
3. cortar, montar o projeto, conferir prévias e renderizar;
4. entregar o arquivo final em `Downloads` com um resumo.

Cada vídeo ganha uma pasta de trabalho em `~/reels/<nome-do-video>/`. Ela é mantida para que
ajustes (texto, cor, tempo) sejam rápidos — basta pedir.

## Estrutura do repositório

```
reels-editor/
├── SKILL.md                  # instruções que o Claude segue (ponto de entrada da skill)
├── README.md                 # este arquivo
├── LICENSE.md                # licença proprietária
├── TERMOS_DE_USO.md          # termos de uso e privacidade
├── THIRD_PARTY_NOTICES.md    # licenças de terceiros (fontes, modelo, bibliotecas)
├── CHANGELOG.md
├── requirements.txt
├── docs/
│   └── FLUXO.md              # o fluxo completo, do vídeo bruto à entrega
├── scripts/
│   ├── setup_env.py          # cria ~/reelsenv e instala dependências
│   ├── transcribe.py         # transcrição com faster-whisper (tempo por palavra)
│   ├── energy.py             # mapa de energia do áudio (pausas)
│   ├── faces.py              # detecção de rostos (YuNet) + folha de miniaturas
│   ├── plan_cut.py           # remove pausas dentro das frases escolhidas
│   ├── cut.py                # renderiza o corte (+ cuts.json com o início de cada trecho)
│   ├── detect_cuts.py        # confere os cortes visíveis na imagem
│   ├── mix_audio.py          # mixa voz + ambiente + SFX e normaliza (−14 LUFS)
│   ├── reels_lib.py          # motor: câmera, legendas, cor, B-roll, SFX, QA, render
│   └── fx.py                 # animações de texto e fundos (inspiradas no React Bits)
├── references/
│   ├── style-guide.md        # números e regras: ritmo, zoom, proporção, legendas
│   ├── visual-references.md  # direções visuais, cor, SFX, bancos de assets
│   └── reactbits.md          # catálogo de animações
└── assets/
    ├── example_project.py    # projeto completo de exemplo (copiar e adaptar)
    ├── *.ttf + OFL.txt       # fontes (SIL Open Font License)
    └── yunet.onnx            # modelo de detecção de rosto (MIT)
```

## Comandos do projeto

Dentro da pasta do vídeo (`~/reels/<nome>/`), com o Python do ambiente (`~/reelsenv/Scripts/python`
no Windows, `~/reelsenv/bin/python` no macOS/Linux):

| Comando | Para quê |
|---|---|
| `python project.py preview 1 5.7 19.3 --debug` | Quadros-chave renderizados (com zonas de segurança) |
| `python project.py check` | Texto sobre o rosto / fora da área segura |
| `python project.py cuts` | Em cada corte: zoom ou não, e por quê |
| `python project.py motion` | Velocidade de pan/zoom e tremidas — deve dar **SMOOTH** |
| `python project.py strip 5.2 6.2` | Quadros consecutivos para julgar suavidade |
| `python project.py looks 12` | O mesmo quadro em todos os ajustes de cor |
| `python project.py full render.mp4` | Render final (+ `final_sheet.jpg` para conferência) |

## Efeitos sonoros

A skill marca um som para cada evento visual (pop, whoosh, click, ding, flash…), mas **não
baixa sons sozinha**. Salve arquivos licenciados em:

```
~/reels-sfx/pop_01.wav
~/reels-sfx/whoosh_01.wav
~/reels-sfx/click_01.wav
~/reels-sfx/ding_01.wav
```

O nome precisa começar pela categoria. Fontes gratuitas com uso comercial permitido: **Mixkit**
e **Pixabay**. Se a pasta não existir, o vídeo sai sem SFX e o render avisa quais categorias faltam.

## Áudio com Adobe Podcast

Com o conector **Adobe for creativity** ativo no Claude, só a trilha de voz é enviada ao Adobe
(a imagem nunca sai do computador). O resultado volta em faixas separadas (voz limpa, ambiente,
reverb) e é mixado localmente. Sem o conector, a skill normaliza o áudio original.

> No app desktop (aba Code), o resultado do Adobe chega por um painel que pode demorar a aparecer.
> Alternativa manual: enviar `voice.wav` em podcast.adobe.com/enhance e devolver o arquivo tratado.

## Limitações

- Texto atrás da pessoa, texto "preso" no cenário em 3D e máscara do sujeito exigem Premiere,
  After Effects ou CapCut.
- A câmera virtual só simula ângulos (zoom/enquadramento); ângulos reais exigem outra gravação.
- LUTs `.cube` e templates `.mogrt/.aep` não são aplicados pelo motor.

## Solução de problemas

| Sintoma | Causa / solução |
|---|---|
| Erro de SSL ao baixar o modelo | Antivírus/proxy — a skill já usa `truststore`; rode de novo |
| `venv` falha no Windows | Caminho longo demais — mantenha o ambiente em `~/reelsenv` |
| Palavra cortada no meio | Alargar o limite daquele corte em 0,1–0,2 s e renderizar de novo |
| Rosto pequeno não é seguido | Baixar `min_face` para ~28 no `project.py` |
| Legenda com texto errado | Corrigir no `FIX` do projeto ou direto no `words.json` |

## Documentação detalhada

- [docs/FLUXO.md](docs/FLUXO.md) — tudo o que acontece do vídeo à entrega, e as ferramentas usadas
- [SKILL.md](SKILL.md) — as instruções que o Claude segue
- [references/style-guide.md](references/style-guide.md) — regras de ritmo, zoom, proporção e legendas
- [references/visual-references.md](references/visual-references.md) — estilos, cor, SFX e bancos de assets
