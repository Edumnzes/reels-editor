"""Editorial decision log + 0-5 scorecard (manual 17 and 19), one decisoes.json per project.

Usage (inside the project folder):
    python decisions.py init <video> [--handle <arroba>]    # create decisoes.json (brand guidelines pre-filled)
    python decisions.py check                               # every required field filled? scores valid?
    python decisions.py report                              # markdown summary for the delivery message
    python decisions.py archive <handle> <name>             # copy to ~/instagram-legendas/<handle>/decisoes/<name>.json

Fields follow the manual's training-data format (input_video, objective, platform, audience, duration_target,
brand_guidelines, editorial_strategy, cut_decisions, b_roll_decisions, caption_style, audio_strategy,
color_strategy, motion_strategy, final_output, qa_result) plus kept_pauses, sfx_strategy,
rejected_errors_check and scores. Every cut/motion/SFX entry carries its REASON: the log must explain the edit.
"""
import json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "decisoes_template.json"
DIMS = {  # manual 17: 0-1 / 2-3 / 4-5
    "narrativa": ("confusa/desconectada", "compreensível", "clara e bem estruturada"),
    "ritmo": ("cansativo/confuso", "adequado", "preciso e intencional"),
    "audio": ("prejudica a compreensão", "aceitável", "limpo e bem mixado"),
    "texto": ("ilegível/excessivo", "funcional", "legível e hierárquico"),
    "motion": ("distrai/quebra", "funcional", "reforça a informação"),
    "cor": ("inconsistente", "aceitável", "consistente/intencional"),
    "composicao": ("mal enquadrada", "funcional", "clara e equilibrada"),
    "plataforma": ("formato inadequado", "publicável", "otimizado para o destino"),
    "acessibilidade": ("ignorada", "parcial", "bem implementada"),
    "objetivo": ("não atende", "atende parcialmente", "atende claramente"),
}
REJECT = [  # manual 21: errors the editor must reject - each one answered true (avoided) / false + why
    "transicoes_em_excesso", "zoom_em_todas_as_frases", "sfx_em_todos_os_cortes", "legenda_gigante_cobrindo_rosto",
    "texto_baixo_contraste", "musica_mais_alta_que_fala", "grading_exagerado", "cortes_rapidos_demais",
    "broll_sem_relacao", "imagem_gerada_incorreta", "cta_antes_do_beneficio", "tendencia_sem_objetivo",
    "introducao_longa", "mesmo_estilo_para_todo_nicho",
]
REQUIRED = ["input_video", "formato", "objective", "audience", "duration_target", "editorial_strategy", "cut_decisions",
            "caption_style", "audio_strategy", "color_strategy", "motion_strategy", "final_output", "qa_result"]
P = Path("decisoes.json")


def load(): return json.loads(P.read_text(encoding="utf-8"))
def save(d): P.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def init(video, handle=None):
    d = json.loads(TEMPLATE.read_text(encoding="utf-8")); d["input_video"] = video
    d["rejected_errors_check"] = {k: None for k in REJECT}
    if handle:
        sys.path.insert(0, str(HERE)); from brand import load_brand
        b = load_brand(handle); d["handle"] = b["handle"]
        d["brand_guidelines"] = {k: b.get(k) for k in ("cores", "fontes", "logo", "cta", "edicao")}
        d["duration_target"] = d["duration_target"] or "%s-%s s" % tuple(b["edicao"]["duracao_alvo_s"])
    if P.exists(): print("decisoes.json já existe - nada alterado"); return
    save(d); print("criado", P.resolve())


def band(n): return 0 if n <= 1 else 1 if n <= 3 else 2


def check(d=None):
    d = d or load(); probs = []
    for k in REQUIRED:
        if d.get(k) in (None, "", [], {}): probs.append(f"campo vazio: {k}")
    for c in d.get("cut_decisions", []):
        if not c.get("motivo"): probs.append(f"corte sem motivo: {c}")
    for m in d.get("motion_strategy", []):
        if not m.get("funcao"): probs.append(f"motion sem função: {m.get('elemento', m)}")
    for k in DIMS:
        sc = d.get("scores", {}).get(k, {}); n = sc.get("nota")
        if not isinstance(n, (int, float)) or not 0 <= n <= 5: probs.append(f"nota inválida: {k}")
        elif n <= 3 and not sc.get("nota_texto"): probs.append(f"nota {n} em {k} precisa de justificativa")
    for k, v in d.get("rejected_errors_check", {}).items():
        if v is None: probs.append(f"erro a rejeitar não verificado: {k}")
    for p in probs: print("  -", p)
    print("decisões:", "COMPLETAS" if not probs else f"{len(probs)} pendência(s)")
    return probs


def report():
    d = load(); sc = d.get("scores", {}); rows = []
    for k, labels in DIMS.items():
        n = sc.get(k, {}).get("nota")
        if isinstance(n, (int, float)):
            rows.append(f"| {k.capitalize()} | {n} | {labels[band(n)]} | {sc[k].get('nota_texto', '')} |")
    notas = [sc[k]["nota"] for k in DIMS if isinstance(sc.get(k, {}).get("nota"), (int, float))]
    print("| Dimensão | Nota | Nível | Observação |\n|---|---|---|---|\n" + "\n".join(rows))
    if notas: print(f"\nMédia: {sum(notas) / len(notas):.1f} / 5 · menor: {min(notas)}")
    es = d.get("editorial_strategy", {})
    print(f"\nEstrutura: {es.get('estrutura', '')} · Mensagem: {es.get('mensagem_central', '')}")
    print(f"Cortes registrados: {len(d.get('cut_decisions', []))} · pausas mantidas: {len(d.get('kept_pauses', []))} · "
          f"motions: {len(d.get('motion_strategy', []))} · QA: {d.get('qa_result', {}).get('veredito', '-')}")


def archive(handle, name):
    sys.path.insert(0, str(HERE)); from brand import folder
    dst = folder(handle) / "decisoes"; dst.mkdir(parents=True, exist_ok=True)
    out = dst / f"{name}.json"; shutil.copy(P, out); print("arquivado em", out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a: print(__doc__)
    elif a[0] == "init": init(a[1], a[a.index("--handle") + 1] if "--handle" in a else None)
    elif a[0] == "check": sys.exit(1 if check() else 0)
    elif a[0] == "report": report()
    elif a[0] == "archive": archive(a[1], a[2])
    else: print(__doc__)
