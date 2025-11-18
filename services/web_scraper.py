import requests
from bs4 import BeautifulSoup
from config.settings import URL_SITE

def coletar_texto_site(url=URL_SITE, limite=4000):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        html = resposta.text
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Erro ao acessar o site: {e}")
    soup = BeautifulSoup(html, "html.parser")
    texto_site = soup.get_text()
    return texto_site[:limite] 