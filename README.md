# Ciclo de Commodities e ROE da Vale S.A. (2018–2024)

**Autor:** João Pedro da Rocha Costa Nascimento  
**GitHub:** github.com/jpn300300  
**Ferramentas:** Python · Pandas · NumPy · Matplotlib

---

## Objetivo

Analisar como o ciclo de preços do minério de ferro impacta o Retorno sobre Patrimônio Líquido (ROE) da Vale S.A., identificando:
- Pontos de inflexão no ROE ao longo do ciclo
- Defasagem entre o preço da ação e o desempenho financeiro
- Relação estatística entre retorno do ativo e resultado contábil

---

## Principais achados

| Métrica | Valor |
|---|---|
| ROE médio 2018–2024 | 13,8% |
| ROE no pico (jun/2021) | 52,3% |
| ROE no vale (Brumadinho, mar/2019) | -85,0% |
| Melhor defasagem (lag) | -4 trimestres |

### Interpretação

- O **pico do ciclo** ocorreu em jun/2021, impulsionado pela recuperação da demanda chinesa pós-pandemia e restrições de oferta australiana
- O **evento Brumadinho** (jan/2019) gerou o maior impacto negativo no ROE da história recente da empresa — queda de ~170 p.p. em 2 trimestres
- A análise de defasagem indica que **o preço da ação antecipa o ROE em ~1 trimestre**, confirmando a eficiência do mercado em precificar resultados futuros

---

## Como executar

```bash
pip install pandas numpy matplotlib
python analise_vale.py
```

O script gera automaticamente o painel de visualização `analise_vale_roe.png`.

---

## Estrutura do projeto

```
projeto_vale_commodities/
├── analise_vale.py       # Script principal
├── analise_vale_roe.png  # Visualização gerada
└── README.md             # Este arquivo
```

---

## Fontes

- Preços históricos: B3 / Yahoo Finance
- Dados de ROE: Relatórios de Resultados da Vale S.A. (Relações com Investidores)
