"""Simulador interativo - ADO 2 Física (Leis de Newton e Aplicações).

Todas as fórmulas estão em formulas.py; aqui fica só a interface (matplotlib.widgets).
Execute:  python3 simulador.py

Comparação automática: ao soltar um slider, os valores anteriores ficam no gráfico como
linhas tracejadas (a mais recente em laranja) e o painel de resultados mostra
"antes" x "agora".
"""
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from matplotlib.animation import FuncAnimation

import formulas as f

# --- Nomes dos sistemas e modos ---------------------------------------------
PLANO = "Plano inclinado com atrito e tração"
CENTRIPETA = "Força centrípeta"
ARRASTO = "Força de arrasto"
SISTEMAS = [PLANO, CENTRIPETA, ARRASTO]

CIRCULO, CARRO = "Círculo (MCU)", "Carro na curva"
LINEAR, QUADRATICO = "Arrasto linear (−b·v)", "Arrasto quadrático (−c·v|v|)"
MODOS = {CENTRIPETA: [CIRCULO, CARRO], ARRASTO: [LINEAR, QUADRATICO]}

# (chave, rótulo, mínimo, máximo, padrão, símbolo curto)
SLIDERS = {
    PLANO: [("m1", "Massa do bloco m1 (kg)", 0.5, 20, 5, "m1"),
            ("m2", "Massa pendurada m2 (kg)", 0.5, 20, 4, "m2"),
            ("theta", "Ângulo θ do plano (°)", 0, 80, 30, "θ"),
            ("mu_s", "Atrito estático μs", 0, 1, 0.3, "μs"),
            ("mu_k", "Atrito cinético μk", 0, 1, 0.2, "μk")],
    CENTRIPETA: [("R", "Raio R (m)", 1, 100, 20, "R"),
                 ("v", "Velocidade v (m/s)", 1, 40, 10, "v"),
                 ("m", "Massa m (kg)", 1, 2000, 100, "m"),
                 ("mu", "Atrito pneu-pista μ (carro)", 0.1, 1.2, 0.7, "μ")],
    ARRASTO: [("m", "Massa m (kg)", 1, 200, 80, "m"),
              ("k", "Coef. de arrasto (b ou c)", 0.05, 20, 10, "b/c"),
              ("g", "Gravidade g (m/s²)", 1.6, 24.8, 9.8, "g")],
}

# --- Cores -------------------------------------------------------------------
FUNDO, CARTAO, DESTAQUE = "#f3f5fa", "#ffffff", "#2563eb"
TEXTO, APAGADO, BORDA = "#1f2937", "#6b7280", "#e5e7eb"
COR_RECENTE, COR_ANTIGA, COR_ALERTA, COR_OK = "#f59e0b", "#9ca3af", "#dc2626", "#16a34a"

estado = {"sistema": PLANO, "modo": None}
valores_salvos = {}          # últimos valores de cada sistema (ao trocar de menu)
comparacao = {"ref": None, "historico": []}   # valores anteriores (fantasmas)
ctl = {"axes": [], "sliders": {}, "radio": None, "extras": []}
anim = {"ponto": None, "t0": time.perf_counter()}

# --- Janela e painel esquerdo ------------------------------------------------
fig = plt.figure(figsize=(14, 8), facecolor=FUNDO)
try:
    fig.canvas.manager.set_window_title("Simulador - Leis de Newton e Aplicações")
except Exception:
    pass

ax_cartao = fig.add_axes([0.015, 0.012, 0.31, 0.976], facecolor=CARTAO)
ax_cartao.set_xticks([]); ax_cartao.set_yticks([])
for s in ax_cartao.spines.values():
    s.set_color(BORDA)

fig.text(0.035, 0.95, "Leis de Newton e Aplicações", fontsize=16, weight="bold", color=TEXTO)
fig.text(0.035, 0.925, "ADO 2 · Física · simulador interativo", fontsize=9, color=APAGADO)
fig.text(0.035, 0.885, "1. ESCOLHA O SISTEMA", fontsize=8, weight="bold", color=DESTAQUE)
fig.text(0.035, 0.625, "3. AJUSTE OS PARÂMETROS", fontsize=8, weight="bold", color=DESTAQUE)
fig.text(0.035, 0.022, "Dica: ao soltar um slider, o valor anterior fica tracejado no gráfico.",
         fontsize=7.5, color=APAGADO)
texto_modo = fig.text(0.035, 0.745, "", fontsize=8, weight="bold", color=DESTAQUE)

ax_sis = fig.add_axes([0.03, 0.775, 0.28, 0.10], facecolor=CARTAO)
radio_sistema = RadioButtons(ax_sis, SISTEMAS, activecolor=DESTAQUE,
                             radio_props={"s": 70})
ax_info = fig.add_axes([0.03, 0.05, 0.28, 0.255], facecolor="#f9fafb")
ax_a = fig.add_axes([0.41, 0.56, 0.56, 0.36])
ax_b = fig.add_axes([0.41, 0.09, 0.56, 0.36])


def estilizar_radio(radio, ax):
    for s in ax.spines.values():
        s.set_visible(False)
    for lab in radio.labels:
        lab.set_fontsize(10); lab.set_color(TEXTO)


estilizar_radio(radio_sistema, ax_sis)


# --- Cálculo (só chama formulas.py) -----------------------------------------
def calcular(sis, modo, p):
    """Devolve as séries para os gráficos e a lista de resultados do painel."""
    if sis == PLANO:
        t = np.linspace(0, 10, 300)
        r = f.plano_inclinado(p["m1"], p["m2"], p["theta"], p["mu_s"], p["mu_k"], t)
        movendo = r["estado"] == "EM MOVIMENTO"
        info = [("Situação", "Em movimento" if movendo else "Equilíbrio", None),
                ("Aceleração a", f"{r['a']:.3f} m/s²", r["a"]),
                ("Tração no fio T", f"{r['T']:.2f} N", r["T"]),
                ("Normal N", f"{r['N']:.2f} N", r["N"]),
                ("Força motriz", f"{r['F_motriz']:.2f} N", r["F_motriz"]),
                ("μs crítico (|F|/N)", f"{r['mu_critico']:.3f}", r["mu_critico"])]
        if p["mu_k"] > p["mu_s"]:
            info.append(("Aviso", "μk limitado a μs", None))
        return dict(t=t, x=r["x"], v=r["v"], info=info)

    if sis == CENTRIPETA:
        t = np.linspace(0, 10, 400)
        r = f.forca_centripeta(p["m"], p["R"], p["v"], t)
        ang = np.linspace(0, 2 * np.pi, 200)
        info = [("Força centrípeta Fc", f"{r['Fc']:.1f} N", r["Fc"]),
                ("Velocidade angular ω", f"{r['w']:.3f} rad/s", r["w"]),
                ("Período", f"{r['periodo']:.2f} s", r["periodo"])]
        derrapa = False
        if modo == CARRO:
            c = f.carro_curva(p["mu"], p["R"], p["v"], p["m"])
            derrapa = bool(c["derrapa"])
            info += [("v máx sem derrapar", f"{c['v_max']:.2f} m/s", c["v_max"]),
                     ("Atrito máximo", f"{c['Fat_max']:.0f} N", c["Fat_max"]),
                     ("Resultado", "Derrapa!" if derrapa else "Faz a curva", None)]
        return dict(t=t, x=r["x"], y=r["y"], cx=p["R"] * np.cos(ang),
                    cy=p["R"] * np.sin(ang), R=p["R"], derrapa=derrapa, info=info)

    g, linear = p["g"], modo == LINEAR
    vt = p["m"] * g / p["k"] if linear else np.sqrt(p["m"] * g / p["k"])
    t = np.linspace(0, 5 * vt / g, 300)  # 5 constantes de tempo (τ = v_term/g)
    r = f.arrasto_linear(p["m"], p["k"], t, g) if linear \
        else f.arrasto_quadratico(p["m"], p["k"], t, g)
    q = f.queda_livre(t, g)
    t95 = f.tempo_95(r["v_term"], g, "linear" if linear else "quad")
    info = [("Modelo", "Linear" if linear else "Quadrático", None),
            ("v terminal (fórmula)", f"{r['v_term']:.2f} m/s", r["v_term"]),
            ("v no fim do gráfico", f"{r['v'][-1]:.2f} m/s", r["v"][-1]),
            ("Tempo até 95% de v_term", f"{t95:.2f} s", t95)]
    return dict(t=t, v=r["v"], y=r["y"], vq=q["v"], yq=q["y"], vt=r["v_term"], info=info)


# --- Controles (reconstruídos a cada troca de sistema) ----------------------
def params_atuais():
    return {k: s.val for k, s in ctl["sliders"].items()}


def salvar_valores():
    if ctl["sliders"]:
        valores_salvos[estado["sistema"]] = params_atuais()


def montar_controles(padrao=False):
    for ax in ctl["axes"]:
        fig.delaxes(ax)
    ctl.update(axes=[], sliders={}, radio=None)
    sis = estado["sistema"]

    modos = MODOS.get(sis)
    texto_modo.set_text("2. ESCOLHA O MODO" if modos else "")
    if modos:
        ax = fig.add_axes([0.03, 0.665, 0.28, 0.075], facecolor=CARTAO)
        radio = RadioButtons(ax, modos, active=modos.index(estado["modo"]),
                             activecolor=DESTAQUE, radio_props={"s": 70})
        estilizar_radio(radio, ax)
        radio.on_clicked(trocar_modo)
        ctl["axes"].append(ax); ctl["radio"] = radio

    salvos = {} if padrao else valores_salvos.get(sis, {})
    for i, (chave, rotulo, lo, hi, v0, _) in enumerate(SLIDERS[sis]):
        ax = fig.add_axes([0.175, 0.58 - 0.05 * i, 0.10, 0.022], facecolor=BORDA)
        span = hi - lo
        fmt = "%.0f" if span >= 60 else "%.1f" if span >= 5 else "%.2f"
        s = Slider(ax, rotulo, lo, hi, valinit=salvos.get(chave, v0), valfmt=fmt,
                   color=DESTAQUE, initcolor="none")
        s.label.set_fontsize(8.5); s.label.set_color(TEXTO)
        s.valtext.set_fontsize(8.5); s.valtext.set_color(TEXTO)
        s.on_changed(lambda _: desenhar())
        ctl["axes"].append(ax); ctl["sliders"][chave] = s


def reiniciar_comparacao():
    comparacao["ref"] = params_atuais()
    comparacao["historico"] = []


def trocar_sistema(rotulo):
    salvar_valores()
    estado["sistema"] = rotulo
    estado["modo"] = MODOS[rotulo][0] if rotulo in MODOS else None
    montar_controles()
    reiniciar_comparacao()
    desenhar()


def trocar_modo(rotulo):
    estado["modo"] = rotulo
    reiniciar_comparacao()
    desenhar()


def limpar_comparacoes(_=None):
    reiniciar_comparacao()
    desenhar()


def restaurar_padrao(_=None):
    montar_controles(padrao=True)
    reiniciar_comparacao()
    desenhar()


def ao_soltar_mouse(_):
    """Ao soltar um slider, o valor anterior vira um 'fantasma' de comparação."""
    p = params_atuais()
    if comparacao["ref"] is not None and comparacao["ref"] != p:
        comparacao["historico"] = (comparacao["historico"] + [comparacao["ref"]])[-3:]
        comparacao["ref"] = p
        desenhar()


def fantasmas(p):
    """Lista (calc, rótulo, cor, espessura) dos valores anteriores, do mais antigo ao mais novo."""
    antigos = list(comparacao["historico"])
    if comparacao["ref"] is not None and comparacao["ref"] != p:
        antigos.append(comparacao["ref"])
    antigos = antigos[-4:]
    simbolos = {c[0]: c[5] for c in SLIDERS[estado["sistema"]]}
    saida = []
    for i, gp in enumerate(antigos):
        mudou = [f"{simbolos[k]}={gp[k]:.4g}" for k in p if gp[k] != p[k]]
        rotulo = "antes: " + ", ".join(mudou) if mudou else "antes"
        recente = i == len(antigos) - 1
        saida.append((calcular(estado["sistema"], estado["modo"], gp), rotulo,
                      COR_RECENTE if recente else COR_ANTIGA, 2.0 if recente else 1.4))
    return saida


# --- Desenho -----------------------------------------------------------------
def estilizar_eixo(ax, titulo, xlabel, ylabel):
    ax.clear()
    ax.set_facecolor(CARTAO)
    ax.set_title(titulo, fontsize=11, color=TEXTO, loc="left", pad=8)
    ax.set_xlabel(xlabel, fontsize=9, color=APAGADO)
    ax.set_ylabel(ylabel, fontsize=9, color=APAGADO)
    ax.grid(True, color=BORDA, lw=0.8)
    ax.tick_params(colors=APAGADO, labelsize=8.5)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(BORDA)
    ax.set_aspect("auto")


def desenhar_resultados(atual, fant):
    ax_info.clear()
    ax_info.set_xticks([]); ax_info.set_yticks([])
    for s in ax_info.spines.values():
        s.set_color(BORDA)
    ax_info.text(0.04, 0.93, "Resultados", fontsize=10, weight="bold", color=TEXTO, va="center")
    antes = fant[-1][0]["info"] if fant else None
    if antes:
        ax_info.text(0.62, 0.93, "antes", fontsize=8, color=COR_RECENTE, ha="right", va="center")
    ax_info.text(0.96, 0.93, "agora", fontsize=8, color=DESTAQUE, ha="right", va="center")
    for i, (rotulo, texto, _num) in enumerate(atual["info"]):
        y = 0.80 - 0.115 * i
        ax_info.text(0.04, y, rotulo, fontsize=8.5, color=APAGADO, va="center")
        if antes and i < len(antes):
            ax_info.text(0.62, y, antes[i][1], fontsize=8.5, color=COR_RECENTE,
                         ha="right", va="center")
        cor = COR_ALERTA if texto in ("Derrapa!",) else COR_OK if texto == "Faz a curva" else TEXTO
        ax_info.text(0.96, y, texto, fontsize=9, weight="bold", color=cor,
                     ha="right", va="center")


def desenhar():
    sis, modo, p = estado["sistema"], estado["modo"], params_atuais()
    atual = calcular(sis, modo, p)
    fant = fantasmas(p)
    anim["ponto"] = None

    if sis == PLANO:
        estilizar_eixo(ax_a, "Posição de m1 ao longo do plano (positivo = subindo)", "t (s)", "x (m)")
        estilizar_eixo(ax_b, "Velocidade de m1", "t (s)", "v (m/s)")
        for calc, rot, cor, lw in fant:
            ax_a.plot(calc["t"], calc["x"], "--", color=cor, lw=lw, label=rot)
            ax_b.plot(calc["t"], calc["v"], "--", color=cor, lw=lw, label=rot)
        ax_a.plot(atual["t"], atual["x"], color=DESTAQUE, lw=2.6, label="agora")
        ax_b.plot(atual["t"], atual["v"], color=DESTAQUE, lw=2.6, label="agora")
        ax_a.axhline(0, color=APAGADO, lw=0.8)
        ax_b.axhline(0, color=APAGADO, lw=0.8)

    elif sis == CENTRIPETA:
        estilizar_eixo(ax_a, "Vista de cima: trajetória circular", "x (m)", "y (m)")
        estilizar_eixo(ax_b, "Posição x(t) = R·cos(ωt)  —  mais rápido = mais oscilações",
                       "t (s)", "x (m)")
        raio_max = max([atual["R"]] + [c["R"] for c, *_ in fant])
        for calc, rot, cor, lw in fant:
            ax_a.plot(calc["cx"], calc["cy"], "--", color=cor, lw=lw, label=rot)
            ax_b.plot(calc["t"], calc["x"], "--", color=cor, lw=lw, label=rot)
        cor_atual = COR_ALERTA if atual["derrapa"] else DESTAQUE
        ax_a.plot(atual["cx"], atual["cy"], color=cor_atual, lw=2.6, label="agora")
        ax_a.plot([0], [0], "+", color=APAGADO)
        anim["ponto"], = ax_a.plot([atual["R"]], [0], "o", color=cor_atual, ms=12)
        ax_a.set_aspect("equal")
        ax_a.set_xlim(-1.15 * raio_max, 1.15 * raio_max)
        ax_a.set_ylim(-1.15 * raio_max, 1.15 * raio_max)
        ax_b.plot(atual["t"], atual["x"], color=cor_atual, lw=2.6, label="agora")

    else:
        estilizar_eixo(ax_a, "Velocidade da queda: com arrasto x sem arrasto", "t (s)", "v (m/s)")
        estilizar_eixo(ax_b, "Distância percorrida", "t (s)", "y (m)")
        for calc, rot, cor, lw in fant:
            ax_a.plot(calc["t"], calc["v"], "--", color=cor, lw=lw, label=rot)
            ax_b.plot(calc["t"], calc["y"], "--", color=cor, lw=lw, label=rot)
        ax_a.plot(atual["t"], atual["vq"], ":", color=APAGADO, lw=1.8, label="sem arrasto (g·t)")
        ax_b.plot(atual["t"], atual["yq"], ":", color=APAGADO, lw=1.8, label="sem arrasto")
        ax_a.axhline(atual["vt"], color=COR_OK, ls="-.", lw=1.3, label="v terminal (fórmula)")
        ax_a.plot(atual["t"], atual["v"], color=DESTAQUE, lw=2.6, label="agora")
        ax_b.plot(atual["t"], atual["y"], color=DESTAQUE, lw=2.6, label="agora")
        vt_max = max([atual["vt"]] + [c["vt"] for c, *_ in fant])
        t_max = max([atual["t"][-1]] + [c["t"][-1] for c, *_ in fant])
        ax_a.set_ylim(0, 1.5 * vt_max)
        ax_a.set_xlim(0, t_max); ax_b.set_xlim(0, t_max)

    for ax in (ax_a, ax_b):
        ax.legend(loc="best", fontsize=8, frameon=True, framealpha=0.9, edgecolor=BORDA)
    desenhar_resultados(atual, fant)
    fig.canvas.draw_idle()


def animar(_):
    """Move o ponto no círculo com x(t) = R cos(ωt), y(t) = R sen(ωt) em tempo real."""
    if anim["ponto"] is None or estado["sistema"] != CENTRIPETA:
        return
    p = params_atuais()
    t = time.perf_counter() - anim["t0"]
    w = p["v"] / p["R"]
    anim["ponto"].set_data([p["R"] * np.cos(w * t)], [p["R"] * np.sin(w * t)])


# --- Botões e eventos --------------------------------------------------------
def criar_botao(pos, texto, acao):
    ax = fig.add_axes(pos)
    b = Button(ax, texto, color=BORDA, hovercolor="#d1d5db")
    b.label.set_fontsize(8.5); b.label.set_color(TEXTO)
    b.on_clicked(acao)
    return b


botao_limpar = criar_botao([0.03, 0.325, 0.135, 0.035], "Limpar comparações", limpar_comparacoes)
botao_padrao = criar_botao([0.175, 0.325, 0.135, 0.035], "Restaurar padrão", restaurar_padrao)
radio_sistema.on_clicked(trocar_sistema)
fig.canvas.mpl_connect("button_release_event", ao_soltar_mouse)

montar_controles()
reiniciar_comparacao()
desenhar()
animacao = FuncAnimation(fig, animar, interval=30, cache_frame_data=False)

if __name__ == "__main__":
    plt.show()
