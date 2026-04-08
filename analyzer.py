# analyzer.py

def analisar(dados: dict) -> dict:

    # 1. Valor Patrimonial por Ação (VPA)
    vpa   = dados["vpa"]
    preco = dados["cotacao"]
    vpa_ok = preco <= 1.5 * vpa

    # 2. Endividamento (Dívida Bruta / PL <= 3x)
    endividamento = dados["div_br_patrim"]
    endividamento_ok = endividamento <= 3.0

    # 3. Dividend Yield >= 6%
    dy = dados["div_yield"]
    dy_ok = dy >= 0.06

    # 4. ROE (Return on Equity) >= 15%
    roe = dados["roe"]
    roe_ok = roe >= 0.15

    # Recomendação final:
    # VPA é obrigatório e, além dele, pelo menos 2 dos 3 critérios restantes
    outros_criterios_ok = sum([endividamento_ok, dy_ok, roe_ok])
    comprar = vpa_ok and outros_criterios_ok >= 2

    return {
        "vpa":              vpa,
        "vpa_ok":           vpa_ok,
        "endividamento":    endividamento,
        "endividamento_ok": endividamento_ok,
        "dividend_yield":   dy,
        "dy_ok":            dy_ok,
        "roe":              roe,
        "roe_ok":           roe_ok,
        "comprar":          comprar,
        "recomendacao":     "✅ COMPRA" if comprar else "❌ NÃO RECOMENDADO",
    }
