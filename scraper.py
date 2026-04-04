from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup


def _criar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    return driver


def buscar_dados(ticker: str) -> dict:
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker.upper()}"

    driver = _criar_driver()
    driver.get(url)

    tds = driver.find_elements(By.TAG_NAME, "td")

    if not any("Cotação" in td.text for td in tds):
        driver.quit()
        raise ValueError(f"Ticker '{ticker}' não encontrado no Fundamentus.")

    campos = {
        "cotacao": "Cotação",
        "patrimonio_liq": "Patrim. Líq",
        "num_acoes": "Nro. Ações",
        "div_br_patrim": "Div Br/ Patrim",
        "div_yield": "Div. Yield",
    }

    dados_brutos = {}

    for chave, label in campos.items():
        for td in tds:
            if label in td.text:
                valor = td.find_element(By.XPATH, "./following-sibling::td[1]").text
                dados_brutos[chave] = valor.strip()
                break

    driver.quit()

    return _limpar_dados(dados_brutos)


def _limpar_dados(d: dict):

    def to_float(s: str):
        s = s.replace("R$", "").replace("%", "").strip()

        if s in ("-", "", "N/A", "?"):
            return 0.0

        s = s.replace(".", "").replace(",", ".")
        return float(s)

    return {
        "cotacao": to_float(d["cotacao"]),
        "patrimonio_liq": to_float(d["patrimonio_liq"]),
        "num_acoes": to_float(d["num_acoes"]),
        "div_br_patrim": to_float(d["div_br_patrim"]),
        "div_yield": to_float(d["div_yield"]) / 100,
    }


def buscar_por_nome(termo: str):

    driver = _criar_driver()

    url = "https://www.fundamentus.com.br/buscaavancada.php"

    driver.get(url)

    campo = driver.find_element(By.NAME, "papel")
    campo.send_keys(termo)

    botao = driver.find_element(By.XPATH, "//input[@type='image']")
    botao.click()

    # espera a tabela carregar
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

            resultados.append({"papel": papel, "nome": nome})

    driver.quit()

    return resultados


if __name__ == "__main__":
    dados = buscar_dados("PETR4")
    print(dados)