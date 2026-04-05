import requests
from bs4 import BeautifulSoup
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADERS = {"User-Agent": "Mozilla/5.0"}


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
    t = yf.Ticker(f"{ticker.upper()}.SA")
    info = t.info
    hist = t.history(period="1d")

    if hist.empty:
        raise ValueError(f"Ticker '{ticker}' não encontrado.")

    cotacao    = hist["Close"].iloc[-1]
    book_value = info.get("bookValue")
    shares     = info.get("sharesOutstanding")
    total_debt = info.get("totalDebt", 0) or 0
    div_yield  = info.get("dividendYield", 0) or 0

    if not book_value or not shares:
        raise ValueError(f"Dados insuficientes para '{ticker}'.")

    patrimonio_liq = book_value * shares
    div_br_patrim  = total_debt / patrimonio_liq if patrimonio_liq > 0 else 0

    return {
        "cotacao":        cotacao,
        "vpa":            book_value,
        "patrimonio_liq": patrimonio_liq,
        "num_acoes":      shares,
        "div_br_patrim":  div_br_patrim,
        "div_yield":      div_yield / 100 if div_yield > 1 else div_yield,
    }


def buscar_historico(ticker: str):
    t = yf.Ticker(f"{ticker.upper()}.SA")
    return t.history(period="6mo")