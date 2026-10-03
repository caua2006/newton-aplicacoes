"""Fórmulas fechadas da ADO 2 (Leis de Newton e Aplicações).

Só física pura com NumPy: nenhuma interface e nenhuma integração numérica.
Cada função recebe os parâmetros e um vetor de tempo t (np.linspace) e devolve
um dicionário com as grandezas calculadas. Unidades do SI (kg, m, s, N, graus
apenas para o ângulo do plano).
"""
import numpy as np

G = 9.8  # m/s², aceleração da gravidade na Terra


# ---------------------------------------------------------------------------
# 3.1  Plano inclinado com atrito e tração (bloco m1 no plano, m2 pendurada)
# ---------------------------------------------------------------------------
def plano_inclinado(m1, m2, theta_graus, mu_s, mu_k, t, g=G):
    """Sentido positivo: m1 subindo o plano (m2 descendo)."""
    theta = np.radians(theta_graus)
    mu_k = min(mu_k, mu_s)  # fisicamente mu_k <= mu_s

    # Eixo perpendicular ao plano: sem aceleração => N = P_perp (2ª Lei)
    N = m1 * g * np.cos(theta)
    # Eixo ao longo do plano (soma das forças que não são atrito):
    # m2 puxa o fio para cima (m2*g), componente do peso de m1 puxa para baixo
    F_motriz = m2 * g - m1 * g * np.sin(theta)

    if abs(F_motriz) <= mu_s * N:
        # Atrito estático consegue segurar o sistema => equilíbrio
        a = 0.0
        estado = "EQUILÍBRIO ESTÁTICO"
    else:
        # 2ª Lei no sistema (m1 + m2): F_motriz - atrito_cinético = (m1+m2)*a
        # O atrito cinético se opõe ao sentido do movimento: sinal(F_motriz)
        a = (F_motriz - mu_k * N * np.sign(F_motriz)) / (m1 + m2)
        estado = "EM MOVIMENTO"

    T = m2 * (g - a)  # 2ª Lei em m2 (vertical): m2*g - T = m2*a
    x = 0.5 * a * t**2  # MRUV com x0 = 0 e v0 = 0: x = x0 + v0 t + a t²/2
    v = a * t           # MRUV: v = v0 + a t
    return dict(N=N, F_motriz=F_motriz, a=a, T=T, estado=estado,
                mu_critico=abs(F_motriz) / N if N > 0 else np.inf, x=x, v=v)


# ---------------------------------------------------------------------------
# 3.2  Força centrípeta (MCU)
# ---------------------------------------------------------------------------
def forca_centripeta(m, R, v, t):
    w = v / R                  # v = ω R
    Fc = m * v**2 / R          # 2ª Lei na direção radial: Fc = m ac = m v²/R
    x = R * np.cos(w * t)      # posição no MCU
    y = R * np.sin(w * t)
    return dict(w=w, Fc=Fc, periodo=2 * np.pi / w, x=x, y=y)


def carro_curva(mu_s, R, v, m, g=G):
    """Extensão: o atrito estático do pneu é a força centrípeta."""
    # Fc = m v²/R <= mu_s m g  =>  v_max = sqrt(mu_s g R)
    v_max = np.sqrt(mu_s * g * R)
    Fc = m * v**2 / R
    return dict(v_max=v_max, Fc=Fc, Fat_max=mu_s * m * g, derrapa=v > v_max)


# ---------------------------------------------------------------------------
# 3.3  Força de arrasto (queda vertical, sentido positivo para baixo)
# ---------------------------------------------------------------------------
def arrasto_linear(m, b, t, g=G):
    """F_arrasto = -b v  =>  m dv/dt = m g - b v (solução fechada)."""
    v_term = m * g / b
    tau = m / b
    v = v_term * (1 - np.exp(-t / tau))
    y = v_term * t - v_term * tau * (1 - np.exp(-t / tau))
    return dict(v_term=v_term, tau=tau, v=v, y=y)


def arrasto_quadratico(m, c, t, g=G):
    """F_arrasto = -c v|v|  =>  m dv/dt = m g - c v² (solução fechada)."""
    v_term = np.sqrt(m * g / c)
    u = g * t / v_term
    v = v_term * np.tanh(u)
    # ln(cosh u) calculado sem overflow: u + ln(1 + e^(-2u)) - ln 2
    y = (v_term**2 / g) * (u + np.log1p(np.exp(-2 * u)) - np.log(2))
    return dict(v_term=v_term, v=v, y=y)


def queda_livre(t, g=G):
    """Sem arrasto: MRUV com a = g."""
    return dict(v=g * t, y=0.5 * g * t**2)


def tempo_95(v_term, g=G, modo="linear"):
    """Tempo para atingir 95% de v_term (relatório, item 3)."""
    if modo == "linear":   # 1 - e^(-t/τ) = 0,95  => t = τ ln 20, τ = v_term/g
        return (v_term / g) * np.log(20)
    return (v_term / g) * np.arctanh(0.95)  # tanh(g t / v_term) = 0,95
