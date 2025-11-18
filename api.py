from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.web_scraper import coletar_texto_site
from services.gemini_service import configurar_gemini, gerar_resposta
from utils.prompt_builder import montar_prompt
from exceptions.custom_exceptions import SiteConnectionError, GeminiAPIError
import uvicorn

# Inicializar FastAPI
app = FastAPI(title="Mentor IA API", version="1.0.0")

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique o domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para requisições
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

# Configurar Gemini na inicialização
configurar_gemini()

@app.get("/")
async def root():
    return {"message": "Mentor IA API está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Mentor IA API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Validar se a mensagem não está vazia
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")
        
        # Coletar texto do site
        try:
            texto_site = coletar_texto_site()
        except ConnectionError as e:
            raise HTTPException(status_code=503, detail=f"Erro ao acessar site de referência: {str(e)}")
        
        # Montar prompt e gerar resposta
        prompt = montar_prompt(texto_site, request.message)
        
        try:
            resposta = gerar_resposta(prompt)
            return ChatResponse(response=resposta, success=True)
        except FileNotFoundError as e:
            raise HTTPException(status_code=500, detail=f"Erro na configuração da API Gemini: {str(e)}")
        except ConnectionError as e:
            raise HTTPException(status_code=503, detail=f"Erro de comunicação com API Gemini: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
            
    except HTTPException:
        # Re-raise HTTPExceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000)

