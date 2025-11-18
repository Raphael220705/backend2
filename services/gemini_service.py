import google.api_core.exceptions
import google.generativeai as genai
from config.settings import GEMINI_API_KEY


def configurar_gemini():
    genai.configure(api_key=GEMINI_API_KEY)


def gerar_resposta(prompt, temperature=0.2, max_output_tokens=150, modelo= "models/gemini-2.0-flash"):
    try:
        model = genai.GenerativeModel(modelo)
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        }

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        #  Verificar se há conteúdo antes de acessar .text
        if not response.candidates:
            raise ValueError("Nenhum candidato de resposta foi retornado pela API Gemini.")

        candidate = response.candidates[0]

        #  Verificar motivo de finalização
        finish_reason = getattr(candidate, "finish_reason", None)
        if finish_reason == 2:
            raise RuntimeError("A geração foi bloqueada por razões de segurança.")
        elif finish_reason != 0:
            print(f"⚠️ Aviso: geração interrompida (finish_reason={finish_reason})")

        # Verificar partes de texto
        if not candidate.content or not candidate.content.parts:
            raise ValueError("A resposta não contém partes de texto válidas.")

        #  Retornar o texto com segurança
        return response.text.strip()

    except google.api_core.exceptions.NotFound as e:
        raise FileNotFoundError(f"O modelo '{modelo}' não foi encontrado ou não está disponível para sua API Key/região. Detalhes: {e}")

    except google.api_core.exceptions.GoogleAPIError as e:
        raise ConnectionError(f"Erro da API Gemini: {e}")

    except Exception as e:
        #  Captura erros inesperados com contexto
        raise RuntimeError(f"Erro inesperado: {e}")


