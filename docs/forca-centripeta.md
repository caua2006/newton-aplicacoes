# Força centrípeta

## O que é

Uma massa $m$ presa a um fio de comprimento $R$ gira em um círculo horizontal com
velocidade tangencial $v$ constante (movimento circular uniforme, MCU). A velocidade muda
de direção o tempo todo, então há aceleração, sempre apontando para o centro. A força que
a causa é a **força centrípeta**.

```
        v ↑
          o───→ trajetória
         /
   centro ● ← Fc (aponta pro centro)
```

## Equações

$$\omega = \frac{v}{R} \qquad x(t) = R\cos(\omega t) \qquad y(t) = R\sin(\omega t)$$

$$F_c = \frac{m v^2}{R} = m\omega^2 R \qquad T_{período} = \frac{2\pi}{\omega}$$

Elas vêm da 2ª Lei de Newton na direção radial: $F_c = m\,a_c$ com $a_c = v^2/R$.

## Extensão: carro fazendo uma curva plana

No modo **Carro na curva**, o atrito estático entre pneu e pista é quem fornece a força
centrípeta. O atrito estático máximo é $\mu m g$, então:

$$\frac{m v^2}{R} \le \mu m g \;\Rightarrow\; v_{max} = \sqrt{\mu g R}$$

Acima de $v_{max}$ o carro **derrapa** (o simulador avisa em vermelho). A massa $m$ não
entra em $v_{max}$.

## Como usar no simulador

| Slider | O que muda |
|---|---|
| $R$ | raio da trajetória |
| $v$ | velocidade tangencial |
| $m$ | massa |
| $\mu$ | atrito pneu-pista (só no modo carro) |

O painel mostra $F_c$, $\omega$, o período e, no modo carro, $v_{max}$, o atrito máximo
e se o carro derrapa.

## O que observar

- Valores padrão ($R=20$ m, $v=10$ m/s, $m=100$ kg): $F_c = 500$ N e
  $\omega = 0{,}5$ rad/s.
- Dobrar $v$ **quadruplica** $F_c$ (depende de $v^2$); dobrar $R$ divide $F_c$ por 2.
- No modo carro, com $\mu=0{,}7$ e $R=20$ m: $v_{max} \approx 11{,}71$ m/s. Passando disso,
  aparece "Derrapa!". Diminua $\mu$ (pista molhada) e $v_{max}$ cai.

## Onde aparece na vida real

Carros e trens em curvas, satélites em órbita, centrífugas, rotores e brinquedos de
parque (carrossel, roda-gigante).
