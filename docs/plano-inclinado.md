# Plano inclinado com atrito e tração

## O que é

Um bloco de massa $m_1$ está sobre um plano inclinado (ângulo $\theta$) com atrito. Um fio
inextensível passa por uma polia sem atrito no topo e prende o bloco a uma segunda massa
$m_2$, pendurada na vertical. A massa $m_2$ puxa o bloco para cima do plano e o peso de
$m_1$ puxa para baixo.

```
           polia
      ____ o
     /  m1\  |
    /  []  \ |
   /        \| fio
  /  θ       [] m2
 /____________
```

## Diagrama de corpo livre

- **Bloco $m_1$:** peso $m_1 g$ (componentes $m_1 g\cos\theta$ perpendicular e
  $m_1 g\sin\theta$ ao longo do plano), normal $N$, tração $T$ (para cima do plano) e
  atrito $f$ (contra o movimento).
- **Massa $m_2$:** peso $m_2 g$ (para baixo) e tração $T$ (para cima).

## Equações

Sentido positivo: $m_1$ subindo o plano.

$$N = m_1 g\cos\theta \qquad F_{motriz} = m_2 g - m_1 g\sin\theta$$

- Se $|F_{motriz}| \le \mu_s N$: $a = 0$ (**equilíbrio estático**).
- Senão (**movimento**):

$$a = \frac{F_{motriz} - \mu_k N\,\mathrm{sinal}(F_{motriz})}{m_1 + m_2}$$

Como $a$ é constante, vale o MRUV:

$$x(t) = x_0 + v_0 t + \tfrac12 a t^2 \qquad v(t) = v_0 + a t$$

Tração no fio (2ª Lei em $m_2$): $T = m_2 (g - a)$.

## Derivação de $a$

1. Em $m_1$, perpendicular ao plano: $N - m_1 g\cos\theta = 0$.
2. Em $m_1$, ao longo do plano: $T - m_1 g\sin\theta - f = m_1 a$.
3. Em $m_2$, na vertical: $m_2 g - T = m_2 a$.
4. Somando 2 e 3, $T$ se cancela: $m_2 g - m_1 g\sin\theta - f = (m_1 + m_2)\,a$.
5. Com $f = \mu_k N$ oposto ao movimento, sai a fórmula de $a$ acima.

## Como usar no simulador

| Slider | O que muda |
|---|---|
| $m_1$, $m_2$ | massas do bloco e da massa pendurada |
| $\theta$ | ângulo do plano (0° a 80°) |
| $\mu_s$ | atrito estático (decide se o sistema sai do lugar) |
| $\mu_k$ | atrito cinético (vale só depois que o sistema se move; o simulador limita $\mu_k \le \mu_s$) |

O painel mostra a situação (em movimento ou equilíbrio), $a$, $T$, $N$, $F_{motriz}$ e
o **$\mu_s$ crítico**, $|F_{motriz}|/N$.

## O que observar

- Com os valores padrão ($m_1=5$ kg, $m_2=4$ kg, $\theta=30°$, $\mu_s=0{,}3$, $\mu_k=0{,}2$):
  $a \approx 0{,}690$ m/s², $T \approx 36{,}44$ N e $\mu_s$ crítico $\approx 0{,}346$.
- Suba $\mu_s$ até passar de $0{,}346$: o sistema vira equilíbrio e as curvas ficam em zero.
- Aumente $\theta$: o peso de $m_1$ ao longo do plano cresce e $F_{motriz}$ diminui (pode
  até mudar de sinal, e o bloco passa a descer).

## Onde aparece na vida real

Guinchos e esteiras inclinadas, vagonetes de mina, elevadores de carga em rampa e a
máquina de Atwood com rampa.
