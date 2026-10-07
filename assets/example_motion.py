"""RSD (desligamento rápido) — motion explicativo, só texto na tela, Ynvest Solar.
Conteúdo-base: explicação de @infinitienergybrasil / @joao.growsolar (reescrita, sem áudio nem imagem deles).
Estilo: referências de motion limpo (fundo claro, 1 cor de marca, cards, tipografia cinética) + diagramas de
sistema solar com fluxo CC/CA e mudança de estado.
"""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path.home() / ".claude" / "skills" / "reels-editor" / "scripts"))
from motion_lib import *  # noqa

# ============================================================ ROTEIRO (texto = narração)
TXT = dict(
    A="As placas transformam a luz do sol em energia.",
    B="Essa energia desce até o inversor…",
    C="…e segue para a casa e para a rede.",
    D="Agora imagine um foco de incêndio.",
    E="O bombeiro desliga o inversor.",
    F="Mas a energia vem de cima para baixo: o telhado continua energizado.",
    G="Cada placa gera cerca de 40 V.",
    H="10 placas em série somam 400 V no telhado.",
    I="O RSD fica embaixo de cada placa.",
    J="No desligamento, ele corta a energia placa por placa.",
    K="A tensão não se soma. Telhado seguro.",
)
HL = dict(A={"sol": GOLD}, B={"inversor…": INK}, F={"energizado": DANGER, "cima": DANGER, "baixo": DANGER},
          G={"40": DC, "v": DC}, H={"400": DANGER, "v": DANGER}, I={"rsd": GOLD}, J={"placa": SAFE},
          K={"seguro": SAFE})
# timeline: hook, title, then one window per sentence (reading time), then claim cards and CTA
T0 = {}; t = 8.0
for k in "ABCDEFGHIJK":
    T0[k] = (t + .2, t + .2 + read_time(TXT[k])); t = T0[k][1]
    if k in "CFHK": t += .2                                   # small breath between chapters
S1, S2 = (0.0, 4.3), (4.3, 8.0)
OUT = T0["K"][1]                                              # diagram leaves
L0, M0, CTA0 = OUT + .3, OUT + 3.7, OUT + 7.6
DUR = CTA0 + 4.6
A0, B0, C0, D0, E0, F0, G0, H0, I0, J0, K0 = (T0[k][0] for k in "ABCDEFGHIJK")
INV_OFF, RSD_CUT = E0 + 1.1, J0 + 1.2                         # the two switch moments

# ============================================================ LAYOUT (8-px grid, inside the safe area)
PLX, PLY, PLW, PLH = 540, 519, 904, 378                       # panels card = the roof (full width, 88-px margins)
PW, PH, PGAP = 152, 88, 20                                    # module size
PCOLS = [88 + 32 + PW // 2 + i * (PW + PGAP) for i in range(5)]
PROWS = [450, 600]
INVX, INVY, INVW = 540, 854, 620
CASAX, REDEX, LOADY, LOADW = 300, 780, 1076, 400
TXTY = 1310
P_DC = dense([(540, 708), (540, 780)], r=0)
P_AC1 = dense([(540, 928), (540, 965), (CASAX, 965), (CASAX, 1002)])
P_AC2 = dense([(540, 928), (540, 965), (REDEX, 965), (REDEX, 1002)])
WIRES = Wires((80, 700, 1000, 1010))
WHITE_ = (255, 255, 255, 255)


def diagram(ov, t):
    inv_on = t < INV_OFF; hot = F0 <= t < RSD_CUT; cut = eo(prog(t, RSD_CUT, .5)); off = eo(prog(t, INV_OFF, .4))
    # ---- wires (under the cards)
    WIRES.begin()
    pdc = eo(prog(t, B0, .7))
    if pdc > 0:
        col = lerp(lerp(DC, DANGER, eo(prog(t, F0, .4))), HAIR, cut)
        wdt = 11 + (4 * (0.5 + 0.5 * math.sin((t - F0) * 9)) if hot else 0)
        WIRES.line(P_DC, col, wdt, 0, pdc)
        if pdc >= 1 and cut < 1: WIRES.dots(P_DC, t, col, n=1, speed=120, r=11, a=1 - cut)
    pac = eo(prog(t, C0, .7))
    if pac > 0:
        col = lerp(AC, HAIR, off)
        for pth in (P_AC1, P_AC2):
            WIRES.line(pth, col, 11, 0, pac)
            if pac >= 1 and off < 1: WIRES.dots(pth, t, AC, n=2, speed=160, r=11, a=1 - off)
    WIRES.end(ov)
    # ---- panels card (the roof): sun + label on the left of the header, rapid-shutdown switch on the right
    if card(ov, PLX, PLY, PLW, PLH, t, A0):
        ps = prog(t, A0 + .3, .5)
        if ps > 0: paste(ov, g_sun(64), 148, 368, (.5 + .5 * eback(ps)) * (1 + .04 * math.sin(t * 2.2)), eo(ps))
        label(ov, "PLACAS  ·  TELHADO" if t < J0 else "TELHADO", 190, 368, ts("xs"), ax=0, a=eo(prog(t, A0 + .2, .3)))
        if t >= J0:
            pj = eo(prog(t, J0, .35)); label(ov, "DESLIGAMENTO RÁPIDO", 836, 368, ts("xs"), INK, a=pj, ax=1)
            if pj > 0: toggle(ov, 906, 368, cut, on=SAFE, w=92, h=48)
        for r, y in enumerate(PROWS):
            for c, x in enumerate(PCOLS):
                i = r * 5 + c; p = prog(t, A0 + .15 + i * .04, .35)
                if p <= 0: continue
                paste(ov, g_panel(PW, PH, "hot" if hot else "on"), x, y, .6 + .4 * eback(p), eo(p))
                if c < 4 and cut < 1 and p >= 1:                      # series link to the next module
                    paste(ov, RR(PGAP, 8, 4, DANGER if hot else DC), x + (PW + PGAP) / 2, y, a=1 - cut)
                pv = prog(t, G0 + .15 + i * .07, .3)                    # "40 V" on each module
                if pv > 0: label(ov, "40 V", x, y, ts("xs"), WHITE_, a=eo(pv))
                pr = prog(t, I0 + .2 + i * .07, .35)                    # RSD under each module
                if pr > 0:
                    cy = y + PH / 2 + 8 + 18
                    paste(ov, RR(PW, 36, 10, lerp(GOLD, SAFE, cut)), x, cy, .5 + .5 * eback(pr), eo(pr))
                    label(ov, "RSD", x, cy, ts("xs"), INK, a=eo(pr))
    # ---- inverter card (glyph + state on the left, its switch on the right from the "bombeiro" sentence on)
    if card(ov, INVX, INVY, INVW, 148, t, B0 - .25):
        paste(ov, g_inverter(84, 96, inv_on), INVX - 236, INVY)
        label(ov, "INVERSOR", INVX - 170, INVY - 22, ts("xs"), ax=0)
        label(ov, "ligado" if inv_on else "desligado", INVX - 170, INVY + 22, ts("sm"), SAFE if inv_on else MUTE, "Bold", ax=0)
        if t >= E0:
            if eo(prog(t, E0, .35)) > 0: toggle(ov, INVX + 226, INVY, 1 - off, on=SAFE)
    # ---- house + grid
    for x, g, name in ((CASAX, g_house, "CASA"), (REDEX, g_tower, "REDE")):
        if card(ov, x, LOADY, LOADW, 148, t, C0 - .25):
            paste(ov, g(92), x - 128, LOADY); label(ov, name, x - 62, LOADY - 22, ts("xs"), ax=0)
            label(ov, "sem energia" if off >= 1 else "recebendo", x - 62, LOADY + 22, ts("sm"), MUTE if off >= 1 else AC, "Bold", ax=0)
    pf = prog(t, D0 + .25, .4)
    if pf > 0: paste(ov, g_flame(96), CASAX + 150, LOADY - 70, (.4 + .6 * eback(pf)) * (1 + .06 * math.sin(t * 13)), eo(pf))
    # ---- state tags on the roof-to-inverter stretch
    if F0 + .3 <= t < RSD_CUT:
        p = prog(t, F0 + .3, .35); pill(ov, 306, 744, "ENERGIZADO", ts("sm"), DANGER, WHITE_, "bolt", s=.6 + .4 * eback(p), a=eo(p))
    if t >= RSD_CUT + .3:
        p = prog(t, RSD_CUT + .3, .35); pill(ov, 330, 744, "SEGURO", ts("sm"), SAFE, WHITE_, "check", s=.6 + .4 * eback(p), a=eo(p))
    if H0 + .2 <= t < RSD_CUT:                                          # the sum
        p = prog(t, H0 + .2, .35); v = int(round(400 * eo(prog(t, H0 + .5, .9)) / 40) * 40)
        pill(ov, 786, 744, f"10 × 40 V = {v} V", ts("sm"), INK, WHITE_, s=.6 + .4 * eback(p), a=eo(p))
    if t >= RSD_CUT + .45:
        p = prog(t, RSD_CUT + .45, .35); pill(ov, 778, 744, "40 V por placa", ts("sm"), INK, WHITE_, s=.6 + .4 * eback(p), a=eo(p))


CHAPTERS = (("COMO FUNCIONA", A0, T0["C"][1]), ("O PROBLEMA", D0, T0["F"][1]), ("A CONTA", G0, T0["H"][1]), ("A SOLUÇÃO", I0, T0["K"][1]))


def draw(ov, t):
    # 1. hook
    ktext(ov, t, .2, S1[1], "Desligou o inversor.", 800, ts("2xl"), weight="Bold", maxw=900)
    b = ktext(ov, t, 1.5, S1[1], "O telhado continua energizado?", 940, ts("xl"), MUTE, "SemiBold", {"energizado?": DANGER})
    # 2. title
    if S2[0] <= t < S2[1]:
        out = eo(prog(t, S2[1] - .28, .28)); p = prog(t, S2[0] + .1, .45)
        paste(ov, T("RSD", ts("3xl"), INK, "Black", shadow=False), W / 2, 760 - 22 * out, .7 + .3 * eback(p), eo(p) * (1 - out))
    ktext(ov, t, S2[0] + .5, S2[1], "Rapid Shutdown", 852, ts("md"), MUTE, "Medium")
    ktext(ov, t, S2[0] + 1.0, S2[1], "desligamento rápido", 940, ts("xl"), INK, "Bold")
    chip(ov, t, S2[0] + 1.7, S2[1], "ITEM DE SEGURANÇA", W / 2, 1050, GOLD, INK, ts("sm"))
    # 3-6. the system
    if A0 - .1 <= t < OUT + .5:
        ex = eo(prog(t, OUT, .45))
        if ex > 0:
            lay = Image.new("RGBA", (W, H)); diagram(lay, t)
            lay.putalpha(lay.getchannel("A").point(lambda v: int(v * (1 - ex)))); ov.alpha_composite(lay, (0, int(-30 * ex)))
        else:
            diagram(ov, t)
    for name, a, b in CHAPTERS: chip(ov, t, a, b, name, W / 2, 296, INK, (255, 255, 255, 255), ts("xs"))
    for k in "ABCDEFGHIJK": ktext(ov, t, T0[k][0], T0[k][1], TXT[k], TXTY, ts("lg"), INK, "SemiBold", HL.get(k), maxw=880)
    pk = prog(t, K0 + 1.2, .35)
    if 0 < pk and t < OUT: paste(ov, g_check(56), W / 2, TXTY + 96, .5 + .5 * eback(pk), eo(pk) * (1 - eo(prog(t, OUT - .28, .28))))
    # 7. claims (as stated in the base video — the brand confirms the normative basis)
    b = ktext(ov, t, L0, M0, "Hoje, instalar o RSD é obrigatório.", 800, ts("2xl"), INK, "Bold", {"obrigatório.": INK}, maxw=860)
    if b and t < M0 - .3:                                    # circle only the last line ("é obrigatório.")
        lw = text_w("é", ts("2xl"), "Bold") + ts("2xl") * .28 + text_w("obrigatório.", ts("2xl"), "Bold"); ly = b[3] - ts("2xl") * 1.24 / 2
        ring(ov, t, L0 + 1.1, (W / 2 - lw / 2, ly - 40, W / 2 + lw / 2, ly + 44), GOLD, pad=(36, 10))
    if M0 <= t < CTA0:
        if card(ov, W / 2, 800, 880, 300, t, M0, a=1 - eo(prog(t, CTA0 - .28, .28))):
            pass
    ktext(ov, t, M0 + .15, CTA0, "Sem ele, a seguradora pode recusar a cobertura.", 800, ts("lg"), INK, "SemiBold",
          {"recusar": DANGER, "cobertura.": DANGER}, maxw=760)
    # 8. CTA
    ktext(ov, t, CTA0 + .1, DUR + 1, "Seu sistema tem RSD?", 760, ts("2xl"), INK, "Bold", {"rsd?": GOLD})
    p = prog(t, CTA0 + 1.1, .4)
    if p > 0:
        pulse = 1 + .025 * math.sin(max(0, t - CTA0 - 1.6) * 6)
        pill(ov, W / 2, 900, "Fale com a Ynvest Solar", ts("md"), GOLD, INK, s=(.6 + .4 * eback(p)) * pulse, a=eo(p))
    p = prog(t, CTA0 + 1.6, .4)
    if p > 0: label(ov, "@ynvestsolar", W / 2, 1000, ts("sm"), MUTE, "SemiBold", a=eo(p))


if __name__ == "__main__":
    print(f"duração {DUR:.1f}s · inversor off {INV_OFF:.1f}s · RSD {RSD_CUT:.1f}s · saída {OUT:.1f}s") if len(sys.argv) > 1 and sys.argv[1] == "times" else None
    Motion(draw, DUR, BG).cli() if not (len(sys.argv) > 1 and sys.argv[1] == "times") else print({k: tuple(round(x, 1) for x in v) for k, v in T0.items()})
