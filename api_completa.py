from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Adicionar caminho para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from services.web_scraper import coletar_texto_site
    from services.gemini_service import configurar_gemini, gerar_resposta
    from utils.prompt_builder import montar_prompt
    GEMINI_AVAILABLE = True
    print("✅ Módulos do Gemini carregados com sucesso!")
except ImportError as e:
    print(f"⚠️ Erro ao carregar módulos: {e}")
    GEMINI_AVAILABLE = False

app = FastAPI(title="Mentor IA - Completa", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    success: bool

# Configurar Gemini se disponível
if GEMINI_AVAILABLE:
    try:
        configurar_gemini()
        print("✅ Gemini configurado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao configurar Gemini: {e}")
        GEMINI_AVAILABLE = False

@app.get("/")
async def root():
    status = "completa" if GEMINI_AVAILABLE else "teste"
    return {
        "message": f"🚀 Mentor IA API ({status}) está funcionando!", 
        "status": "online",
        "gemini_available": GEMINI_AVAILABLE
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "service": "Mentor IA API",
        "gemini_available": GEMINI_AVAILABLE,
        "message": "API funcionando perfeitamente!"
    }

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")
        
        user_message = request.message.strip()
        
        # Se Gemini está disponível, usar IA real
        if GEMINI_AVAILABLE:
            try:
                # Coletar texto do site
                texto_site = coletar_texto_site()
                
                # Montar prompt e gerar resposta
                prompt = montar_prompt(texto_site, user_message)
                resposta = gerar_resposta(prompt)
                
                return ChatResponse(response=resposta, success=True)
                
            except Exception as e:
                print(f"❌ Erro no Gemini: {e}")
                # Fallback para resposta inteligente
                return ChatResponse(response=get_smart_response(user_message), success=True)
        
        else:
            # Resposta inteligente sem IA
            response = get_smart_response(user_message)
            return ChatResponse(response=response, success=True)
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro no endpoint /chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

def get_smart_response(message):
    """Resposta inteligente baseada na mensagem"""
    msg = message.lower()
    
    if any(word in msg for word in [ "inscrição",  "cadastrar"]):
        return "📝 Para se inscrever no Programa Jovem Programador, você pode:\n\n1. Acessar o site oficial do programa\n2. Preencher o formulário de inscrição\n3. Aguardar o processo seletivo\n4. Participar das aulas e atividades\n\n💡 É um programa excelente para aprender programação!"
    
    elif any(word in msg for word in ["olá", "oi", "hello", "bom dia", "boa tarde"]):
        return "👋 Olá! Sou o Mentor IA, seu assistente especializado em programação. Posso ajudar com:\n\n• Conceitos de programação\n• Linguagens como Python, JavaScript\n• Algoritmos e estruturas de dados\n• Dúvidas sobre o Programa Jovem Programador\n\nComo posso ajudar você hoje?"
    
    elif "python" in msg:
        return "🐍 Python é uma linguagem fantástica para iniciantes!\n\n📚 Conceitos importantes:\n• Sintaxe simples e legível\n• Bibliotecas poderosas (Django, Flask, Pandas)\n• Ótima para automação e análise de dados\n• Comunidade ativa e recursos abundantes\n\n💡 Quer saber algo específico sobre Python?"
    
    elif "javascript" in msg:
        return "⚡ JavaScript é essencial para desenvolvimento web!\n\n🌐 Principais usos:\n• Interatividade em páginas web\n• Desenvolvimento frontend (React, Vue)\n• Backend com Node.js\n• Aplicações mobile (React Native)\n\n💡 Qual aspecto do JavaScript te interessa?"
    
    elif any(word in msg for word in ["programação", "programar", "código", "desenvolver"]):
        return "💻 Programação é uma área incrível e em constante crescimento!\n\n🎯 Dicas para iniciantes:\n• Comece com uma linguagem (Python ou JavaScript)\n• Pratique regularmente\n• Faça projetos práticos\n• Participe de comunidades\n• Não tenha medo de errar!\n\n💡 Por onde você gostaria de começar?"
    
    elif any(word in msg for word in ["jovem programador", "programa", "senac"]):
        return "🎓 O Programa Jovem Programador é uma excelente oportunidade!\n\n📖 Sobre o programa:\n• Formação completa em programação\n• Metodologia prática e atual\n• Suporte de mentores experientes\n• Networking com outros estudantes\n• Preparação para o mercado de trabalho\n\n💡 Tem alguma dúvida específica sobre o programa?"
    
    else:
        return f"🤔 Interessante pergunta sobre '{message}'!\n\n💡 Como seu Mentor IA, posso ajudar com:\n• Conceitos de programação\n• Linguagens específicas\n• Dúvidas sobre o Programa Jovem Programador\n• Carreira em tecnologia\n• Projetos práticos\n\n🔍 Pode reformular sua pergunta ou perguntar algo mais específico?"

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 MENTOR IA API - VERSÃO COMPLETA")
    print("=" * 60)
    print(f"🤖 Gemini AI: {'✅ Disponível' if GEMINI_AVAILABLE else '❌ Indisponível'}")
    print("📡 Servidor: http://localhost:8000")
    print("📚 Documentação: http://localhost:8000/docs")
    print("🔍 Teste: http://localhost:8000/health")
    print("=" * 60)
    print("🔄 Para parar: Ctrl+C")
    print("=" * 60)
    
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {str(e)}")
