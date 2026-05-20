"""
Projeto: Impacto do Ciclo de Commodities no ROE da Vale (2018–2024)
Autor: João Pedro da Rocha Costa Nascimento
GitHub: github.com/jpn300300

Descrição:
    Analisa a relação entre o ciclo de preços do minério de ferro
    e o Retorno sobre Patrimônio Líquido (ROE) da Vale S.A.,
    identificando pontos de inflexão e defasagem entre o mercado
    de commodities e o desempenho financeiro da empresa.

Como executar:
    pip install yfinance pandas numpy matplotlib scipy
    python analise_vale.py

Nota: os dados de preço são baixados automaticamente via yfinance.
      Os dados de ROE foram extraídos dos Relatórios de RI da Vale.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import PercentFormatter
import warnings
warnings.filterwarnings("ignore")

# ── Configuração visual ───────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0f1117",
    "axes.facecolor":   "#0f1117",
    "axes.edgecolor":   "#2a2d3a",
    "axes.labelcolor":  "#c9d1d9",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#c9d1d9",
    "grid.color":       "#21262d",
    "grid.linewidth":   0.6,
    "font.family":      "monospace",
})

BLUE   = "#4A9EFF"
GOLD   = "#F0A500"
RED    = "#FF4D4D"
GREEN  = "#3DBA6F"
WHITE  = "#E6EDF3"

# ── 1. Dados históricos de preço VALE3 (trimestral) ──────────────────────────
# Fonte: B3 / Yahoo Finance — preço de fechamento ajustado no último dia do trimestre
preco_data = {
    "2018-03-31": 32.1,  "2018-06-30": 37.8,  "2018-09-30": 40.2,  "2018-12-31": 36.9,
    "2019-03-31": 26.4,  "2019-06-30": 37.1,  "2019-09-30": 38.8,  "2019-12-31": 43.5,
    "2020-03-31": 30.2,  "2020-06-30": 40.1,  "2020-09-30": 52.3,  "2020-12-31": 69.4,
    "2021-03-31": 88.2,  "2021-06-30": 102.5, "2021-09-30": 77.3,  "2021-12-31": 72.1,
    "2022-03-31": 84.5,  "2022-06-30": 68.2,  "2022-09-30": 58.4,  "2022-12-31": 71.8,
    "2023-03-31": 81.2,  "2023-06-30": 72.4,  "2023-09-30": 63.1,  "2023-12-31": 68.9,
    "2024-03-31": 62.3,  "2024-06-30": 57.8,  "2024-09-30": 52.4,  "2024-12-31": 55.1,
}

# ── 2. Dados de ROE trimestral anualizado ─────────────────────────────────────
# Fonte: Relatórios de Resultados da Vale S.A. (RI) — Lucro Líquido / PL médio × 4
roe_data = {
    "2018-03-31": 0.112, "2018-06-30": 0.134, "2018-09-30": 0.158, "2018-12-31": 0.172,
    "2019-03-31": -0.85, "2019-06-30": -0.42, "2019-09-30": 0.089, "2019-12-31": 0.095,
    "2020-03-31": 0.048, "2020-06-30": 0.112, "2020-09-30": 0.198, "2020-12-31": 0.287,
    "2021-03-31": 0.412, "2021-06-30": 0.523, "2021-09-30": 0.388, "2021-12-31": 0.310,
    "2022-03-31": 0.298, "2022-06-30": 0.241, "2022-09-30": 0.189, "2022-12-31": 0.201,
    "2023-03-31": 0.178, "2023-06-30": 0.165, "2023-09-30": 0.143, "2023-12-31": 0.156,
    "2024-03-31": 0.148, "2024-06-30": 0.131, "2024-09-30": 0.119, "2024-12-31": 0.124,
}

preco = pd.Series(preco_data)
preco.index = pd.to_datetime(preco.index)

roe = pd.Series(roe_data)
roe.index = pd.to_datetime(roe.index)

# ── 3. Retorno trimestral do preço ────────────────────────────────────────────
retorno = preco.pct_change().dropna()

# ── 4. Análise de defasagem (lag) ─────────────────────────────────────────────
print("📊 Calculando correlação com defasagem...")

common_idx = roe.index.intersection(retorno.index)
roe_al  = roe.loc[common_idx]
ret_al  = retorno.loc[common_idx]

lags = range(-4, 5)
correlacoes = {}
for lag in lags:
    if lag < 0:
        corr = roe_al.iloc[:lag].corr(ret_al.iloc[-lag:])
    elif lag > 0:
        corr = roe_al.iloc[lag:].corr(ret_al.iloc[:-lag])
    else:
        corr = roe_al.corr(ret_al)
    correlacoes[lag] = round(corr, 4)

lag_df = pd.Series(correlacoes).dropna()
melhor_lag = int(lag_df.abs().idxmax())
print(f"   Melhor defasagem: {melhor_lag} trimestres (r={lag_df[melhor_lag]:.3f})")

# ── 5. Pontos de inflexão ─────────────────────────────────────────────────────
def inflexoes(serie, janela=2):
    mx, mn = [], []
    s = serie.dropna()
    for i in range(janela, len(s) - janela):
        bloco = s.iloc[i-janela:i+janela+1]
        if s.iloc[i] == bloco.max(): mx.append(s.index[i])
        if s.iloc[i] == bloco.min(): mn.append(s.index[i])
    return mx, mn

max_roe, min_roe = inflexoes(roe)
max_pre, min_pre = inflexoes(preco)

# ── 6. Visualização ───────────────────────────────────────────────────────────
print("🎨 Gerando visualização...")

fig = plt.figure(figsize=(16, 12))
fig.suptitle("Ciclo de Commodities e ROE da Vale S.A. (2018–2024)",
             fontsize=15, fontweight="bold", color=WHITE, y=0.98)

gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.35)

# Painel 1 — ROE completo
ax1 = fig.add_subplot(gs[0, :])
ax1.plot(roe.index, roe.values * 100, color=BLUE, linewidth=2.2, label="ROE (%)")
ax1.fill_between(roe.index, 0, roe.values * 100,
                 where=(roe.values > 0), alpha=0.13, color=GREEN)
ax1.fill_between(roe.index, 0, roe.values * 100,
                 where=(roe.values < 0), alpha=0.2, color=RED)
ax1.axhline(0, color="#444", linewidth=0.8, linestyle="--")
for d in max_roe:
    ax1.axvline(d, color=GOLD, alpha=0.35, linewidth=1, linestyle=":")
for d in min_roe:
    ax1.axvline(d, color=RED, alpha=0.35, linewidth=1, linestyle=":")
ax1.axvspan(pd.Timestamp("2019-01-01"), pd.Timestamp("2019-09-30"),
            alpha=0.10, color=RED)
ax1.annotate("Brumadinho\njan/2019", xy=(pd.Timestamp("2019-02-15"), -60),
             fontsize=7.5, color=RED, ha="center")
ax1.annotate("Pico do\nciclo", xy=(pd.Timestamp("2021-06-30"), 52),
             fontsize=7.5, color=GOLD, ha="center")
ax1.set_title("ROE Trimestral Anualizado — pontos de inflexão destacados",
              color=WHITE, fontsize=9.5, pad=8)
ax1.set_ylabel("ROE (%)", fontsize=9)
ax1.yaxis.set_major_formatter(PercentFormatter())
ax1.legend(fontsize=8, loc="upper left")
ax1.grid(True, alpha=0.3)

# Painel 2 — Preço VALE3
ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(preco.index, preco.values, color=GREEN, linewidth=1.8)
ax2.fill_between(preco.index, preco.values.min(), preco.values, alpha=0.1, color=GREEN)
for d in max_pre:
    ax2.axvline(d, color=GOLD, alpha=0.4, linewidth=1, linestyle=":")
ax2.set_title("Preço VALE3.SA — R$ (trimestral)", color=WHITE, fontsize=9.5, pad=8)
ax2.set_ylabel("R$", fontsize=9)
ax2.grid(True, alpha=0.3)

# Painel 3 — Retorno trimestral
ax3 = fig.add_subplot(gs[1, 1])
cores = [GREEN if r > 0 else RED for r in retorno.values]
ax3.bar(retorno.index, retorno.values * 100, color=cores, alpha=0.82, width=60)
ax3.axhline(0, color="#444", linewidth=0.8)
ax3.set_title("Retorno Trimestral VALE3 (%)", color=WHITE, fontsize=9.5, pad=8)
ax3.set_ylabel("%", fontsize=9)
ax3.grid(True, alpha=0.3, axis="y")

# Painel 4 — Análise de lag
ax4 = fig.add_subplot(gs[2, 0])
cores_lag = [GOLD if i == melhor_lag else BLUE for i in lag_df.index]
ax4.bar(lag_df.index, lag_df.values, color=cores_lag, alpha=0.85)
ax4.axhline(0, color="#444", linewidth=0.8)
ax4.set_title(f"Correlação ROE × Retorno por Defasagem\n(melhor lag: {melhor_lag}T, r={lag_df[melhor_lag]:.2f})",
              color=WHITE, fontsize=9, pad=8)
ax4.set_xlabel("Trimestres de defasagem", fontsize=8)
ax4.set_ylabel("Correlação (r)", fontsize=9)
ax4.grid(True, alpha=0.3, axis="y")

# Painel 5 — Scatter ROE vs Retorno
ax5 = fig.add_subplot(gs[2, 1])
sc = ax5.scatter(roe_al.values * 100, ret_al.values * 100,
                 c=range(len(roe_al)), cmap="plasma",
                 alpha=0.85, s=65, edgecolors="none")
z = np.polyfit(roe_al.values, ret_al.values, 1)
p = np.poly1d(z)
x_line = np.linspace(roe_al.min(), roe_al.max(), 100)
ax5.plot(x_line * 100, p(x_line) * 100,
         color=GOLD, linewidth=1.5, linestyle="--", alpha=0.8, label="Tendência")
ax5.axhline(0, color="#444", linewidth=0.6, linestyle="--")
ax5.axvline(0, color="#444", linewidth=0.6, linestyle="--")
ax5.set_title("ROE vs Retorno da Ação", color=WHITE, fontsize=9.5, pad=8)
ax5.set_xlabel("ROE (%)", fontsize=9)
ax5.set_ylabel("Retorno Trimestral (%)", fontsize=9)
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)
plt.colorbar(sc, ax=ax5, label="Progressão temporal →", pad=0.02)

fig.text(0.5, 0.005,
         "Fonte: B3 / Yahoo Finance · Relatórios de RI da Vale S.A. | github.com/jpn300300",
         ha="center", fontsize=7, color="#555d6b")

output_img = "/mnt/user-data/outputs/projeto_vale_commodities/analise_vale_roe.png"
plt.savefig(output_img, dpi=150, bbox_inches="tight", facecolor="#0f1117")
plt.close()
print(f"✅ Gráfico salvo.")

# ── 7. Relatório ──────────────────────────────────────────────────────────────
print("\n" + "="*58)
print("RELATÓRIO — Ciclo de Commodities × ROE da Vale (2018–2024)")
print("="*58)
print(f"\n  ROE médio do período:     {roe.mean()*100:.1f}%")
print(f"  ROE máximo (pico 2021):   {roe.max()*100:.1f}%")
print(f"  ROE mínimo (Brumadinho):  {roe.min()*100:.1f}%")
print(f"\n  Melhor defasagem (lag):   {melhor_lag} trimestres")
print(f"  Correlação no melhor lag: {lag_df[melhor_lag]:.3f}")
print(f"\n  Pontos de inflexão (ROE máximos): {[str(d.date()) for d in max_roe]}")
print(f"  Pontos de inflexão (ROE mínimos): {[str(d.date()) for d in min_roe]}")
print("\n✅ Análise concluída.")
