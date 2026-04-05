# 📊 Analisador Fundamentalista — B3

Aplicação web para análise fundamentalista de ações listadas na B3 (Bolsa de Valores do Brasil), desenvolvida como projeto de portfólio com foco em automação de dados e análise financeira.

---

## 🖥️ Demonstração

> Busca por nome de empresa ou código direto, análise dos 3 critérios fundamentalistas e gráfico interativo de preços dos últimos 6 meses.

---

## 💡 Motivação

Projeto desenvolvido para praticar integração de múltiplas fontes de dados financeiros, webscraping e construção de painéis analíticos interativos — aplicando conceitos de análise de valor (Value Investing) ao mercado brasileiro.

---

## 📐 Critérios de Análise

| Critério | Regra | Justificativa |
|---|---|---|
| **Valor Patrimonial (VPA)** | Cotação ≤ 1,5x o VPA | Ação não está sobrevalorizada em relação ao patrimônio contábil |
| **Endividamento** | Dívida Bruta ≤ 3x o Patrimônio Líquido | Empresa com alavancagem controlada |
| **Dividend Yield** | DY ≥ 6% | Boa distribuição de lucros aos acionistas |

A recomendação de **COMPRA** é emitida somente quando os 3 critérios são atendidos simultaneamente.

---

## 🛠️ Tecnologias

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — interface web interativa
- [yfinance](https://pypi.org/project/yfinance/) — dados fundamentalistas e histórico de preços
- [Selenium](https://selenium-python.readthedocs.io/) — busca de empresas por nome via Fundamentus
- [Plotly](https://plotly.com/python/) — gráfico interativo com zoom e seletor de período

---

## ⚙️ Como executar

**1. Clone o repositório**
```bash
git clone https://github.com/jprsouza87/BOVESPA_analyzer.git
cd BOVESPA_analyzer
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Execute a aplicação**
```bash
streamlit run app.py
```

Acesse em: `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
BOVESPA_analyzer/
├── app.py          # Painel Streamlit
├── scraper.py      # Coleta de dados (Selenium + yfinance)
├── analyzer.py     # Lógica de análise fundamentalista
└── requirements.txt
```

---

## ⚠️ Limitações conhecidas

- Indicadores de bancos e instituições financeiras podem apresentar dados ausentes por conta da estrutura de capital específica do setor
- O Dividend Yield do Yahoo Finance pode divergir levemente do Fundamentus em alguns casos
- A análise é baseada em critérios de valor simplificados e **não constitui recomendação financeira**

---

## 👤 Autor

João Paulo R. Souza — [github.com/jprsouza87](https://github.com/jprsouza87)

