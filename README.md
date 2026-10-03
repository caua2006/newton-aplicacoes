# Simulador Interativo — Leis de Newton e Aplicações

Atividade ADO 2 — Física - Práticas Extensivas.

**Grupo:**
- Cauã Carvalho de Oliveira
- Pedro Henrique Patricio
- João Pedro Moz
- Rafael Pascual

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 simulador.py
```

A janela do matplotlib abre sozinha. Não há integração numérica: tudo usa as fórmulas
fechadas avaliadas sobre um vetor `t = np.linspace(...)`.

## O que a interface oferece

1. Menu para escolher o sistema: **Plano inclinado com atrito e tração**, **Força centrípeta**
   e **Força de arrasto**.
2. Modo (centrípeta: círculo ou carro na curva; arrasto: linear ou quadrático).
3. Sliders dos parâmetros; o gráfico e os resultados atualizam em tempo real.

**Comparação automática:** ao soltar um slider, os valores anteriores ficam no gráfico como
linhas tracejadas (a mais recente em laranja), com o que mudou na legenda. O painel
"Resultados" mostra as colunas **antes** e **agora**. O botão "Limpar comparações" apaga os
tracejados e "Restaurar padrão" volta os sliders ao valor inicial.

| Sistema | Sliders | Mostra na tela |
|---|---|---|
| Plano inclinado com atrito e tração | m1, m2, θ, μ estático, μ cinético | situação, aceleração, tração no fio, normal, μ crítico |
| Força centrípeta (+ modo **carro na curva**, extensão) | R, v, m, μ | Fc, ω, período, v máx. antes de derrapar |
| Força de arrasto (linear ou quadrático) | m, coeficiente b ou c, g | v terminal, v no fim do gráfico, tempo até 95% |

## Documentação dos sistemas

Explicação de cada sistema (diagrama, equações, derivação, o que observar e aplicações):

- [Plano inclinado com atrito e tração](docs/plano-inclinado.md)
- [Força centrípeta](docs/forca-centripeta.md)
- [Força de arrasto](docs/forca-arrasto.md)

## Estrutura do código

- `formulas.py`: todas as fórmulas (física pura com NumPy), comentadas com a lei de origem.
- `simulador.py`: interface (RadioButtons, Sliders, Buttons, gráficos), só chama `formulas.py`.
- `docs/`: explicação em Markdown de cada sistema.
- `relatorio.md`: relatório da atividade.
