# Mentor Jovem AI

Um assistente inteligente que responde dúvidas sobre o programa Jovem Programador, utilizando a API Gemini do Google e informações do site oficial.

## Estrutura do Projeto

- `main.py`: ponto de entrada do sistema.
- `config/settings.py`: configurações gerais (API Key, URL do site).
- `services/web_scraper.py`: coleta e trata o texto do site.
- `services/gemini_service.py`: integra com a API Gemini.
- `utils/prompt_builder.py`: monta o prompt para a IA.
- `exceptions/custom_exceptions.py`: exceções customizadas.

## Como usar

1. Instale as dependências:
   ```bash
   pip install bs4
   pip install requests  
   pip install google-generativeai
   ```
2. Configure sua chave da API Gemini em `config/settings.py`.
3. Execute o sistema:
   ```bash
   python main.py
   ```

## Observações
- Certifique-se de que sua chave da API Gemini está correta e ativa.
- O sistema limita as respostas a 1000 caracteres e utiliza apenas o conteúdo do site Jovem Programador. 