# Formatos de vídeo (templates)

Escolhidos pelo dono da skill a partir de referências validadas no Instagram (@cybnutri "5 formatos de posts
virais", @sala.criativa "Formatos virais de 2026", @allankevin.r "3 formatos criativos", @eder.tapias
"como gravo os formatos virais"). Padrões de máquina em `assets/formatos.json`; motions em `scripts/formats.py`;
montagens com mais de uma fonte em `scripts/compose.py`. As regras do `manual-edicao.md` valem para todos.

**Como escolher (passo B do SKILL.md):** depois do perfil da marca, recomende **3 formatos** para este vídeo
(pelo material gravado + objetivo + o que funciona na marca em `video.md`) e deixe ver a lista toda.
Se o material não serve ao formato escolhido (ex.: Clone sem câmera fixa), diga e entregue o guia de gravação.
"O melhor formato é o que deu certo na rotina e na comunicação da marca" — valide um, repita e adapte.

| id | Formato | Grupo | Precisa de | Montagem |
|---|---|---|---|---|
| `fala_popups` | Fala para câmera + pop-ups | fala | 1 vídeo falando | corte normal |
| `dicas_rapidas` | Dicas rápidas / copiar e colar | fala | 1 vídeo com 3–7 dicas | corte normal |
| `historia` | História / narrativa | fala | 1 vídeo contando uma história | corte normal |
| `depoimento` | Depoimento de cliente | prova | vídeo do cliente (+ B-roll) | corte normal |
| `react` | React (tela dividida) | prova | vídeo de referência + reação | `compose.py split` |
| `clone` | Clone | prova | 2 takes com câmera fixa | `compose.py clone` |
| `frase_identificacao` | Vídeo curto + frase de identificação | imagem | 1 clipe sem fala | `compose.py assemble` |
| `conteudo_legenda` | Conteúdo na legenda | imagem | 1 clipe do dia a dia | `compose.py assemble` |
| `voiceover` | Voiceover | imagem | clipes + narração | `compose.py assemble --audio` |
| `serie` | Série com episódios | visual | episódio em qualquer formato | corte normal + identidade da série |
| `gancho_visual` | Gancho visual forte / Dia X | visual | muitos clipes curtos | `compose.py assemble` |
| `multitarefa` | Multitarefa | visual | 1 vídeo falando enquanto faz algo | corte normal |

---

## fala_popups — Fala para câmera + pop-ups
- **Quando:** explicar, opinar, anunciar (é o formato padrão da skill até aqui).
- **Estrutura:** gancho → contexto → desenvolvimento → prova → conclusão → CTA.
- **Edição:** corte de pausas sem função, zoom só em jump cut visível, legenda por grupo; pop-ups (selo,
  card, gráfico) só onde explicam, provam ou situam. 20–60 s.
- **Motions:** `hook_title`/pill no gancho, cards do projeto, `cta_follow`.
- **Gravar:** celular na vertical na altura dos olhos, luz de frente (janela), lapela; falar em frases curtas
  e deixar 1 s de silêncio entre ideias (facilita o corte). Um B-roll de 3–5 s do assunto ajuda muito.

## dicas_rapidas — Dicas rápidas / "copiar e colar"
- **Quando:** conteúdo salvável ("6 regras…", "3 erros…"). Um dos formatos mais fáceis de viralizar.
- **Estrutura:** gancho com número ("3 sinais de que…") → dica 1 → dica 2 → dica 3 → resumo → CTA salvar.
- **Edição:** ritmo rápido, cada dica entra num corte; sem introdução. 15–45 s.
- **Motions:** `tip_card(n, total, texto)` na entrada de cada dica + `tip_progress` no topo; `cta_save` no fim.
  A legenda continua; o card traz a dica resumida em ≤ 8 palavras.
- **Gravar:** uma dica por take; comece cada take já pela dica ("Dois: …"). Liste as dicas antes de gravar.

## historia — História / narrativa
- **Quando:** caso real, bastidor com tensão, "como tudo começou". Prende pela curiosidade ("preciso saber o final").
- **Estrutura:** cold open com a tensão (a frase mais forte do meio, 1–3 s) → contexto → conflito → virada →
  desfecho → aprendizado → CTA. Nunca contar o final no início.
- **Edição:** ritmo variável — mais lento na virada (pausa com função mantida), mais rápido no contexto.
  B-roll ilustrando cada etapa. 30–90 s. Zoom editorial só na virada.
- **Motions:** `chapter_label` discreto ("O PROBLEMA", "A VIRADA") quando a história é longa; `quote_card`
  na frase-chave (esconda a legenda nesse trecho com `hide_captions`). Poucos gráficos: a história é o foco.
- **Gravar:** conte em ordem, com detalhes concretos (lugar, número, nome); grave a frase de impacto 2×.

## depoimento — Depoimento de cliente
- **Quando:** prova social — "terror da concorrência". Quem fala é o cliente, não a marca.
- **Estrutura:** resultado primeiro (a melhor frase do cliente) → quem é → como era antes → decisão →
  depois com números → CTA.
- **Edição:** limpar pausas mas manter a naturalidade (não "robotizar" o cliente); B-roll do projeto/local
  enquanto ele fala do resultado. 20–60 s.
- **Motions:** `name_card(nome, empresa/cidade)` nos primeiros segundos em que ele aparece; `before_after`
  (ex.: conta R$ 890 → R$ 49) quando o número é dito; `quote_card` opcional na frase-chave.
- **Gravar:** entreviste (pergunte, não peça texto decorado): "como era antes?", "o que mudou?",
  "quanto você pagava e quanto paga?". Cliente olhando levemente para o lado de quem pergunta. Autorização
  de uso de imagem do cliente é obrigatória (TERMOS §2).

## react — React (tela dividida)
- **Quando:** aproveitar um vídeo que já está circulando e trazer a opinião do especialista.
- **Estrutura:** trecho da referência (o gancho vem dela) → reação → opinião/correção do especialista → CTA.
- **Montagem:** `compose.py split REFERENCIA.mp4 REACAO.MOV raw.mp4 --top-ss X --dur D` (referência em
  cima com áudio −14 dB, reação embaixo centrada no rosto). Depois o fluxo normal. 15–45 s.
- **Edição:** `cap_y=960` (legenda na emenda), `ZOOM` 1.0, `RANGES` sem acompanhar rosto (None).
- **Motions:** `react_label` na emenda nos primeiros segundos; `cta_follow` no fim.
- **Direitos:** só use referência sua, licenciada ou um trecho curto com comentário e crédito ao autor na
  tela e na legenda. Registre a origem em `decisoes.json`. O Instagram pode silenciar ou limitar.
- **Gravar:** assista à referência enquanto grava a reação (fone de ouvido), reaja de verdade nos primeiros
  segundos, depois fale para a câmera.

## clone — Clone
- **Quando:** diálogo "eu cético × eu especialista", objeção × resposta, pergunta × solução. Chama atenção pelo efeito.
- **Estrutura:** clone A pergunta/objeta → clone B responde → nova objeção → solução → CTA.
- **Montagem:** `compose.py clone TAKE_A.MOV TAKE_B.MOV raw.mp4 --seam 0.5 [--b-offset s]`. A = pessoa no lado
  esquerdo, B = lado direito. O script avisa se a câmera mexeu. Depois o fluxo normal; `ZOOM` 1.0.
- **Motions:** `speaker_tag("EU CÉTICO", "left")` / `speaker_tag("EU ESPECIALISTA", "right")` na primeira fala
  de cada um; roupa ou acessório diferente ajuda a distinguir.
- **Gravar (obrigatório):** celular no **tripé, sem mexer** entre os takes, mesma luz, mesmo enquadramento.
  Marque no chão os dois lugares. Grave o take A inteiro deixando silêncio onde B fala, depois o B com o
  roteiro do A tocando no fone. Ninguém cruza a metade do quadro.

## frase_identificacao — Vídeo curto + frase de identificação
- **Quando:** gerar identificação/compartilhamento ("Nossa, sou eu") com pouco esforço de gravação.
- **Estrutura:** um único momento: imagem "rolando" + uma frase. 5–12 s (o loop conta a favor).
- **Montagem:** `compose.py assemble clips.json raw.mp4` (1 clipe, ou 2–3 curtos). Sem legenda de fala.
- **Edição:** Ken Burns leve (1.0→1.06), cor da marca, frase no meio da tela; nada mais.
- **Motions:** `big_phrase(frase, destaques)` do início ao fim (entra em 0,5 s). Frase ≤ 18 palavras.
- **Música:** ainda não configurada na skill — oriente a pessoa a escolher o áudio no app do Instagram ao postar.
- **Gravar:** 10–15 s de uma cena simples e bonita da rotina (obra, cliente, equipe, pôr do sol na usina).

## conteudo_legenda — Conteúdo na legenda
- **Quando:** o conteúdo é texto (lista, passo a passo, história escrita); o vídeo só prende o olhar.
- **Estrutura:** imagem rolando → gancho curto na tela → "Leia a legenda".
- **Montagem:** `compose.py assemble` com 1 clipe (6–15 s). Sem legenda de fala.
- **Motions:** `big_phrase(gancho)` + `read_caption()` apontando para a legenda.
- **Legenda do post:** é o conteúdo principal — use a skill `legendas-instagram` para escrevê-la.
- **Gravar:** clipe do dia a dia com movimento suave (trabalhando no notebook, vistoria, equipe na obra).

## voiceover — Voiceover
- **Quando:** quem fala não quer aparecer, ou as imagens explicam melhor que o rosto (obra, processo, lugar).
- **Estrutura:** gancho → contexto → desenvolvimento → conclusão → CTA (na narração).
- **Montagem:** `compose.py assemble clips.json raw.mp4 --audio narracao.wav [--loop]` — a narração define a
  duração; clipes trocam a cada 2–4 s. Depois o fluxo normal (a transcrição da narração vira legenda).
- **Edição:** cada clipe mostra o que está sendo dito (B-roll semântico — manual §4). 15–60 s.
- **Motions:** pills/cards pontuais, `cta_follow`.
- **Gravar:** narração num lugar silencioso, celular a um palmo da boca (ou lapela); grave os clipes
  pensando em cada frase do roteiro.

## serie — Série com episódios
- **Quando:** conteúdo recorrente com identidade fixa ("Obra da semana", "Dúvida da semana"). Cria hábito
  e retorno ("no próximo episódio…").
- **Estrutura:** vinheta/selo da série → gancho do episódio → conteúdo (em qualquer outro formato) →
  gancho do próximo episódio.
- **Edição:** o formato de base vem de `fala_popups`, `dicas_rapidas`, `voiceover`… A série só acrescenta a
  identidade fixa: mesmas cores, mesmo selo, mesma posição, mesma frase de fechamento.
- **Motions:** `series_badge(nome, episodio)` no início; `next_episode(teaser)` no fim.
- **Guardar:** nome, número do último episódio e identidade em `marca.json → series` para manter a sequência.

## gancho_visual — Gancho visual forte / "Dia X"
- **Quando:** a imagem prende antes da fala — transformação, processo, desafio com contagem ("Dia 12").
- **Estrutura:** imagem que para a rolagem (o melhor/mais estranho momento) → título "dia X / testando…" →
  processo em cortes → resultado → CTA.
- **Montagem:** `compose.py assemble` com muitos clipes curtos (troca a cada ~3 s) ou corte normal se houver fala.
- **Motions:** `day_title(dia, subtitulo)` no primeiro segundo; pills pontuais no processo.
- **Gravar:** registre o processo inteiro em clipes de 3–5 s (antes, durante, depois), sempre do mesmo ângulo
  para o antes/depois bater.

## multitarefa — Multitarefa (fala enquanto faz)
- **Quando:** autenticidade e bastidor — explicar enquanto instala, confere, cozinha, trabalha.
- **Estrutura:** gancho → explicação durante a tarefa → resultado da tarefa → CTA.
- **Edição:** corte das pausas da fala, mas mantendo a ação contínua (não cortar no meio de um gesto);
  legenda por grupo; poucos pop-ups (a ação já é o visual). 20–60 s.
- **Motions:** pills pontuais, `cta_follow`.
- **Gravar:** celular fixo (tripé) com a pessoa e a tarefa no quadro; lapela obrigatória (as mãos estão ocupadas
  e o barulho da tarefa atrapalha).
