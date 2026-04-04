def analisar(dados: dict) -> dict:

    cotacao = dados["cotacao"]
    patrimonio = dados["patrimonio_liq"]
    num_acoes = dados["num_acoes"]
    div_br_patrim = dados["div_br_patrim"]
    dividend_yield = dados["div_yield"]

    # Valor patrimonial por ação
    vpa = patrimonio / num_acoes if num_acoes else 0

    # Endividamento
    endividamento = div_br_patrim

    # Regras
    vpa_ok = cotacao <= 1.5 * vpa
    endividamento_ok = endividamento <= 3
    dy_ok = dividend_yield >= 0.06

    comprar = vpa_ok and endividamento_ok and dy_ok

    if comprar:
        recomendacao = "Ação dentro dos critérios — possível oportunidade."
    else:
        recomendacao = "Ação não atende todos os critérios."

    return {
        "vpa": vpa,
        "vpa_ok": vpa_ok,
        "endividamento": endividamento,
        "endividamento_ok": endividamento_ok,
        "dividend_yield": dividend_yield,
        "dy_ok": dy_ok,
        "comprar": comprar,
        "recomendacao": recomendacao,
    }