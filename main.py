from services.web_scraper import coletar_texto_site
from services.gemini_service import configurar_gemini, gerar_resposta
from utils.prompt_builder import montar_prompt
from exceptions.custom_exceptions import SiteConnectionError, GeminiAPIError


def main():
    # Configura Gemini
    configurar_gemini()

    # Coleta o texto do site
    try:
        texto_site = coletar_texto_site()
    except ConnectionError as e:
        print(e)
        return

    # Loop de perguntas
    while True:
        pergunta = input("\nDigite sua pergunta sobre o programa Jovem Programador (ou 'sair' para encerrar): ")
        if pergunta.lower() == 'sair':
            print("Encerrando o Mentor Jovem AI. Até logo!")
            break

        prompt = montar_prompt(texto_site, pergunta)
        print(f"\nConsultando o Mentor Jovem AI...")
        try:
            resposta = gerar_resposta(prompt)
            print(f"\nResposta do Mentor Jovem AI:\n")
            print(resposta)
        except FileNotFoundError as e:
            print(f"\n❌ Erro: {e}")
            print("Por favor, verifique se sua API Key Gemini está correta e se o modelo escolhido é acessível para você.")
            print("Você pode tentar gerar uma nova API Key no Google AI Studio: https://aistudio.google.com/app/apikey")
        except ConnectionError as e:
            print(f"\n❌ {e}")
            print("Ocorreu um problema geral com a comunicação com a API Gemini.")
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main() 

