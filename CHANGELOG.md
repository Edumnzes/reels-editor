# Changelog

## 2.0.0 — em desenvolvimento (branch `v2`)
- **Perfil da marca como primeiro passo**: briefing curto + análise somente leitura dos Reels e Insights
  do Instagram (login feito pela pessoa), salvo em `~/instagram-legendas/<arroba>/` e reaproveitado.
- Pasta compartilhada com a skill `legendas-instagram` (`perfil.md`), mais `video.md`, `marca.json` e `videos.md`.
- `scripts/brand.py` (list/show/init/log e `load_brand()` para o project.py) e `assets/marca_template.json`.
- `references/onboarding.md`: roteiro do briefing, o que ler no Instagram, regras de segurança e modelos.
- O perfil passa a definir termos da transcrição, direção visual, cores, CTA e duração alvo.
- Termos de uso: seção sobre acesso ao Instagram e dados do perfil.

## 1.0.0 — 2026-09-29
Primeira versão no GitHub (uso privado).

- Análise: transcrição com tempo por palavra (faster-whisper), mapa de energia, detecção de rostos (YuNet).
- Corte automático de pausas com verificação por re-transcrição; `cuts.json` com cortes exatos por quadro.
- Câmera virtual com decisão LOCK/TRACK por trecho, zoom só nos cortes e relatório `motion`.
- Legendas palavra por palavra em 3 estilos (hormozi, minimal, cinematic).
- Motion graphics com posicionamento fora do rosto (`slot()`), escala tipográfica fixa e animações de texto (`fx.py`).
- Ajustes de cor com comparação lado a lado (`looks`); ajustes personalizados por projeto.
- Integração com Adobe Podcast Enhance Speech via conector Adobe; mixagem e normalização a −14 LUFS.
- Efeitos sonoros a partir de biblioteca local licenciada (`~/reels-sfx`).
- Documentação: README, fluxo completo, licença proprietária, termos de uso e avisos de terceiros.
