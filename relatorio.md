# Relatório — Leis de Newton e Aplicações (ADO 2)

**Grupo:** Cauã Carvalho de Oliveira, Pedro Henrique Patricio, João Pedro Moz, Rafael Pascual

## Introdução

Nesta atividade construímos um simulador interativo em Python, usando `matplotlib.widgets`
(menu, sliders e botões), para três sistemas clássicos da Segunda Lei de Newton (ΣF = m·a):
o plano inclinado com atrito e tração, a força centrípeta e a força de arrasto. Todos os
sistemas têm solução em forma fechada, então nenhum método de integração numérica foi
necessário: as fórmulas, que estão no arquivo `formulas.py`, são avaliadas diretamente sobre
um vetor de tempo criado com `np.linspace`. A interface, em `simulador.py`, permite escolher
o sistema, alterar os parâmetros pelos sliders e acompanhar os gráficos e os valores
calculados em tempo real. Além dos três sistemas, implementamos a extensão opcional do carro
fazendo uma curva plana.

## 1. Plano inclinado com atrito e tração

Um bloco de massa m1 está sobre um plano com ângulo θ e coeficientes de atrito μs (estático)
e μk (cinético). Um fio inextensível passa por uma polia sem atrito no topo e liga o bloco a
uma massa m2 pendurada na vertical. Adotamos como sentido positivo o de m1 subindo o plano.

**Equações usadas**

- N = m1·g·cosθ
- F_motriz = m2·g − m1·g·sinθ
- Se |F_motriz| ≤ μs·N, então a = 0 (equilíbrio estático)
- Caso contrário, a = (F_motriz − μk·N·sinal(F_motriz)) / (m1 + m2)
- x(t) = ½·a·t² e v(t) = a·t (MRUV, com x0 = 0 e v0 = 0)
- Tração no fio: T = m2·(g − a)

**Derivação de a a partir do diagrama de corpo livre.** Em m1 atuam o peso (com componentes
m1·g·cosθ perpendicular e m1·g·sinθ ao longo do plano), a normal N, a tração T e o atrito;
em m2 atuam o peso e a tração. Perpendicular ao plano, m1 não acelera, então
N = m1·g·cosθ. Ao longo do plano, a Segunda Lei para m1 dá T − m1·g·sinθ − f_at = m1·a. Na
vertical, para m2, temos m2·g − T = m2·a. Somando as duas últimas equações, a tração se
cancela e fica m2·g − m1·g·sinθ − f_at = (m1 + m2)·a. O atrito cinético vale f_at = μk·N e
se opõe ao movimento, e é por isso que aparece o sinal(F_motriz) na fórmula: se o bloco sobe,
o atrito aponta para baixo, e se o bloco desce, aponta para cima. Isolando a, chegamos à
expressão acima.

**Resultado e valor crítico.** Com m1 = 5 kg, m2 = 4 kg, θ = 30°, μs = 0,3, μk = 0,2 e
g = 9,8 m/s², obtemos N = 42,44 N e F_motriz = 14,70 N. Como μs·N = 12,73 N é menor que
F_motriz, o sistema se move, com a ≈ 0,690 m/s² e T ≈ 36,44 N. Para encontrar o valor crítico
variamos o coeficiente de atrito na interface (com μs = μk = μ) até o sistema deixar de se
mover: com μ = 0,34 ele ainda se move e com μ = 0,35 passa para equilíbrio estático. A teoria
prevê que o sistema para quando |F_motriz| = μs·N, ou seja, μ = 14,70 / 42,44 ≈ 0,346, que
está dentro do intervalo encontrado no simulador. Vale notar que quem decide se o sistema sai
do lugar é o atrito estático μs; o μk só influencia a aceleração depois que o movimento
começa.

## 2. Força centrípeta

Uma massa m presa a um fio de comprimento R gira em um círculo horizontal com velocidade
tangencial v constante (movimento circular uniforme). A velocidade muda de direção o tempo
todo, então há uma aceleração apontando para o centro, e a força que a produz é a força
centrípeta (no caso, a tração do fio).

**Equações usadas**

- ω = v/R
- x(t) = R·cos(ωt) e y(t) = R·sen(ωt)
- Fc = m·v²/R = m·ω²·R

Essas equações vêm da Segunda Lei na direção radial, com aceleração centrípeta v²/R. No
simulador, as posições x(t) e y(t) são calculadas sobre o vetor de tempo e usadas para
desenhar o círculo e animar o ponto. Com R = 20 m, v = 10 m/s e m = 100 kg, o painel mostra
ω = 0,5 rad/s e Fc = 500 N; dobrando a velocidade, Fc quadruplica, pois depende de v².

**Extensão: carro em curva plana.** Nesse modo, a força centrípeta é fornecida pelo atrito
estático entre o pneu e a pista, cujo valor máximo é μ·m·g. Impondo m·v²/R ≤ μ·m·g, chegamos
à velocidade máxima antes de derrapar, v_max = √(μ·g·R), que não depende da massa. Com
μ = 0,7 e R = 20 m, v_max ≈ 11,71 m/s; acima disso o simulador indica que o carro derrapa, e
diminuir μ (pista molhada) reduz esse limite.

## 3. Força de arrasto

Um objeto de massa m cai na vertical sob a ação do peso e de uma força de arrasto que se opõe
ao movimento. Diferente dos outros sistemas, a aceleração não é constante: ela diminui à
medida que a velocidade aumenta, até que o arrasto iguale o peso e a velocidade pare de
crescer (velocidade terminal).

**Equações usadas**

- Arrasto linear (F = −b·v): v_term = m·g/b, τ = m/b,
  v(t) = v_term·(1 − e^(−t/τ)) e y(t) = v_term·t − v_term·τ·(1 − e^(−t/τ))
- Arrasto quadrático (F = −c·v|v|): v_term = √(m·g/c),
  v(t) = v_term·tanh(g·t/v_term) e y(t) = (v_term²/g)·ln cosh(g·t/v_term)
- Queda livre, usada como comparação: v(t) = g·t

No simulador, o gráfico mostra a curva com arrasto, a queda livre e uma linha com a
velocidade terminal calculada pela fórmula. A curva satura exatamente nessa linha, o que
confirma que a implementação está correta, e a diferença para a queda livre cresce com o
tempo.

**Tempo até 95% da velocidade terminal.** Com m = 80 kg e coeficiente igual a 10 nos dois
modelos, o arrasto linear tem v_term = 78,4 m/s e atinge 95% em
t = (v_term/g)·ln 20 ≈ 23,97 s. Já o quadrático tem v_term ≈ 8,85 m/s e atinge 95% em
t = (v_term/g)·artanh(0,95) ≈ 1,66 s.

**Por que a forma da curva é diferente.** No arrasto linear, a força cresce na mesma
proporção da velocidade, então a taxa com que v se aproxima de v_term é proporcional ao que
ainda falta para chegar nele (dv/dt = (v_term − v)/τ). Isso resulta em uma exponencial, que
se aproxima do limite de forma suave e lenta. No arrasto quadrático, a força cresce com v²:
no início ela é quase desprezível e a curva sobe como a queda livre, mas perto de v_term o
arrasto cresce muito e freia o objeto com força. O resultado é a tangente hiperbólica, que
sobe quase reta no começo e satura de forma mais abrupta. Nesse exemplo, o quadrático chega a
95% bem antes principalmente porque a sua velocidade terminal é bem menor com o mesmo valor
numérico do coeficiente.

## 4. Aplicações reais

O plano inclinado com polia aparece em guinchos, esteiras inclinadas, vagonetes de mina e
elevadores de carga em rampa, em que uma massa sobe puxada por outra que desce, e o atrito
decide se o conjunto se move. A força centrípeta está presente em carros e trens fazendo
curvas, em satélites em órbita e em centrífugas; o modo carro mostra bem por que a
velocidade máxima numa curva diminui em pista molhada. A força de arrasto é essencial no
paraquedismo e na queda de gotas de chuva (arrasto quadrático no ar), no movimento de esferas
em óleo (arrasto linear) e no projeto de carros e aviões.

## Dificuldades encontradas

A principal dificuldade física foi o sinal do atrito cinético, que sempre se opõe ao
movimento e por isso depende do sinal de F_motriz. No arrasto quadrático, o cálculo de
ln cosh(u) estoura para tempos grandes, e resolvemos reescrevendo como
u + ln(1 + e^(−2u)) − ln 2. Na interface, o desafio foi ter sliders e menus diferentes para
cada sistema na mesma janela, recriando os controles a cada troca.
