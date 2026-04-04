# 📊 Analisador Fundamentalista — B3


https://b3analyzer.streamlit.app/

Aplicação web para análise fundamentalista de ações listadas na B3 (Bolsa de Valores do Brasil).
Busca dados reais diretamente do [Fundamentus](https://www.fundamentus.com.br/) via web scraping e aplica critérios de valor para recomendar ou não a compra de uma ação.

---

## 🖥️ Interface

- Busca de empresa por nome com seleção do papel
- Entrada direta pelo código da ação (ex: PETR4)
- Painel com indicadores fundamentalistas
- Recomendação automática de compra

---

## 📐 Critérios de Análise

| Critério | Regra | Justificativa |
|---|---|---|
| **Valor Patrimonial (VPA)** | Cotação ≤ 1,5x o VPA | Ação não está sobrevalorizada em relação ao patrimônio |
| **Endividamento** | Dívida Bruta ≤ 3x o Patrimônio Líquido | Empresa com alavancagem controlada |
| **Dividend Yield** | DY ≥ 6% | Boa distribuição de lucros aos acionistas |

A recomendação de **COMPRA** é emitida somente quando os 3 critérios são atendidos simultaneamente.

---

## 🛠️ Tecnologias

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — interface web

---

## 📁 Estrutura do Projeto

BOVESPA_analyzer/
├── app.py          # Painel Streamlit
├── scraper.py      # Web scraping 
├── analyzer.py     # Lógica de análise fundamentalista
└── requirements.txt

---

## ⚠️ Limitações conhecidas

- Indicadores de bancos e instituições financeiras (ex: ITUB4) podem apresentar campos ausentes no Fundamentus — tratados como zero
- Os dados dependem da disponibilidade do site Fundamentus
- A análise é baseada em critérios de valor simplificados e **não constitui recomendação financeira**

---

## 👤 Autor

João Paulo — [github.com/jprsouza87](https://github.com/jprsouza87)
