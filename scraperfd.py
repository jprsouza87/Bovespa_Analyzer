from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _criar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


def buscar_por_nome(termo: str) -> list:
    driver = _criar_driver()
    try:
        driver.get("https://www.fundamentus.com.br/buscaavancada.php")
        campo = driver.find_element(By.NAME, "papel")
        campo.send_keys(termo)
        botao = driver.find_element(By.XPATH, "//input[@type='image']")
        botao.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
        )
        linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        resultados = []
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) >= 3:
                papel = colunas[0].text.strip()
                nome  = colunas[2].text.strip()
                if papel and nome:
                    resultados.append({"papel": papel, "nome": nome})
        return resultados
    finally:
        driver.quit()


def buscar_dados(ticker: str) -> dict:
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker.upper()}"
    driver = _criar_driver()
    try:
        driver.get(url)
        tds = driver.find_elements(By.TAG_NAME, "td")

        if not any("Cotação" in td.text for td in tds):
            raise ValueError(f"Ticker '{ticker}' não encontrado no Fundamentus.")

        campos = {
            "cotacao":       "Cotação",
            "patrimonio_liq": "Patrim. Líq",
            "num_acoes":     "Nro. Ações",
            "div_br_patrim": "Div Br/ Patrim",
            "div_yield":     "Div. Yield",
            "vpa":           "VPA",
            "roe":           "ROE",
        }

        dados_brutos = {}
        for chave, label in campos.items():
            for td in tds:
                if label in td.text and td.text.strip() == label:
                    valor = td.find_element(By.XPATH, "./following-sibling::td[1]").text
                    dados_brutos[chave] = valor.strip()
                    break

        return _limpar_dados(dados_brutos)
    finally:
        driver.quit()


def buscar_historico(ticker: str):
    # mantém yfinance só para o gráfico — menos requisições, sem problema
    import yfinance as yf
    t = yf.Ticker(f"{ticker.upper()}.SA")
    return t.history(period="12mo")


def _limpar_dados(d: dict) -> dict:
    def to_float(s: str) -> float:
        s = s.replace("R$", "").replace("%", "").strip()
        if s in ("-", "", "N/A", "?"):
            return 0.0
        s = s.replace(".", "").replace(",", ".")
        return float(s)

    return {
        "cotacao":        to_float(d.get("cotacao", "0")),
        "vpa":            to_float(d.get("vpa", "0")),
        "patrimonio_liq": to_float(d.get("patrimonio_liq", "0")),
        "num_acoes":      to_float(d.get("num_acoes", "0")),
        "div_br_patrim":  to_float(d.get("div_br_patrim", "0")),
        "div_yield":      to_float(d.get("div_yield", "0")) / 100,
        "roe":            to_float(d.get("roe", "0")) / 100,
    }