# Força de arrasto

## O que é

Um objeto de massa $m$ cai na vertical sob a gravidade e uma força de **arrasto** que se
opõe ao movimento. Ao contrário dos outros sistemas, a aceleração **não é constante**:
ela diminui conforme a velocidade aumenta, até o arrasto igualar o peso. Nesse ponto a
velocidade para de crescer, e é a **velocidade terminal**.

```
   |  F_arrasto (para cima, cresce com v)
   ●
   |  peso m·g (para baixo)
   ↓  v
```

## Equações

Sentido positivo: para baixo. A 2ª Lei dá $m\,\dfrac{dv}{dt} = mg - F_{arrasto}$. As
soluções já vêm prontas (fórmulas fechadas).

**Arrasto linear** ($F_{arrasto} = -bv$), mais adequado a velocidades baixas e fluidos
viscosos:

$$v_{term} = \frac{mg}{b} \quad \tau = \frac{m}{b} \quad v(t) = v_{term}\left(1 - e^{-t/\tau}\right)$$

$$y(t) = v_{term}\,t - v_{term}\,\tau\left(1 - e^{-t/\tau}\right)$$

**Arrasto quadrático** ($F_{arrasto} = -cv|v|$), mais realista para o ar:

$$v_{term} = \sqrt{\frac{mg}{c}} \quad v(t) = v_{term}\tanh\!\left(\frac{g t}{v_{term}}\right)$$

$$y(t) = \frac{v_{term}^2}{g}\ln\cosh\!\left(\frac{g t}{v_{term}}\right)$$

**Sem arrasto** (queda livre, para comparar): $v(t) = g t$ e $y(t) = \tfrac12 g t^2$.

**Tempo até 95% de $v_{term}$:**
linear $t_{95} = \tau\ln 20$; quadrático $t_{95} = \dfrac{v_{term}}{g}\,\mathrm{artanh}(0{,}95)$.

## Como usar no simulador

| Controle | O que muda |
|---|---|
| Modo linear / quadrático | modelo de arrasto usado |
| $m$ | massa |
| $b$ ou $c$ | coeficiente de arrasto |
| $g$ | gravidade (Lua, Terra, Júpiter...) |

O gráfico compara a queda com arrasto (curva que satura) e sem arrasto (reta $g\,t$),
e traça a linha da **velocidade terminal calculada pela fórmula**. Se a curva encosta
nessa linha, a implementação está certa.

## O que observar

- Valores padrão linear ($m=80$ kg, $b=10$): $v_{term} = 78{,}4$ m/s e
  $t_{95} \approx 23{,}97$ s.
- Com o mesmo $m$ e coeficiente 10 no modo quadrático: $v_{term} \approx 8{,}85$ m/s e
  $t_{95} \approx 1{,}66$ s.
- A forma é diferente porque, no linear, o arrasto cresce proporcional a $v$ e a curva
  se aproxima devagar do limite (exponencial). No quadrático o arrasto é desprezível no
  início e cresce rápido perto de $v_{term}$, dando a subida mais reta e a saturação mais
  abrupta (tangente hiperbólica).
- Aumentar $m$ aumenta $v_{term}$; aumentar o coeficiente diminui.

## Onde aparece na vida real

Paraquedismo (arrasto quadrático no ar), gotas de chuva, esferas caindo em óleo (arrasto
linear), projeto de carros e aviões.
