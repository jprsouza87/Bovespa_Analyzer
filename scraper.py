from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import re
import asyncio


def buscar_dados(ticker: str) -> dict:
    url = f"https://www.fundamentus.com.br/detalhes.php?papel={ticker.upper()}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Verifica se o ticker existe (página inválida não tem a célula 'Cotação')
        if page.locator("td").filter(has_text="Cotação").count() == 0:
            browser.close()
            raise ValueError(f"Ticker '{ticker}' não encontrado no Fundamentus.")

        campos = {
            "cotacao":        "Cotação",
            "patrimonio_liq": "Patrim. Líq",
            "num_acoes":      "Nro. Ações",
            "div_br_patrim":  "Div Br/ Patrim",
            "div_yield":      "Div. Yield",
        }

        dados_brutos = {}
        for chave, label in campos.items():
            try:
                celula = page.locator("td").filter(has_text=label).first
                valor = celula.locator("xpath=following-sibling::td[1]").inner_text()
                dados_brutos[chave] = valor.strip()
            except Exception as e:
                raise RuntimeError(f"Erro ao extrair '{label}': {e}")

        browser.close()

    return _limpar_dados(dados_brutos)


def _limpar_dados(d: dict) -> dict:
    def to_float(s: str) -> float:
        s = s.replace("R$", "").replace("%", "").strip()
        if s in ("-", "", "N/A", "?"):
            return 0.0  # valor ausente → trata como zero
        s = s.replace(".", "").replace(",", ".")
        return float(s)

    return {
        "cotacao":        to_float(d["cotacao"]),
        "patrimonio_liq": to_float(d["patrimonio_liq"]),
        "num_acoes":      to_float(d["num_acoes"]),
        "div_br_patrim":  to_float(d["div_br_patrim"]),
        "div_yield":      to_float(d["div_yield"]) / 100,
    }

async def _buscar_nome_async(termo: str) -> list:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(
            "https://www.fundamentus.com.br/buscaavancada.php",
            wait_until="domcontentloaded"
        )

        await page.locator("input[name='papel']").fill(termo)
        await page.locator("input[type='image']").first.click()
        await page.wait_for_load_state("domcontentloaded")

        linhas = await page.locator("table tbody tr").all()
        resultados = []
        for linha in linhas:
            colunas = await linha.locator("td").all()
            if len(colunas) >= 3:
                papel   = (await colunas[0].inner_text()).strip()
                nome    = (await colunas[2].inner_text()).strip()
                resultados.append({"papel": papel, "nome": nome})

        await browser.close()
    return resultados


def buscar_por_nome(termo: str) -> list:
    import sys
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    return asyncio.run(_buscar_nome_async(termo))


# Teste rápido
if __name__ == "__main__":
    dados = buscar_dados("PETR4")
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")