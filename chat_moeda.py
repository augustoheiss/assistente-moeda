import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Carrega o Escudo de Segurança (O arquivo .env)
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")

if not CHAVE_API:
    print("🚨 ERRO: Chave da API não encontrada! Verifique seu arquivo .env")
    exit()

# 2. Inicia o Cliente Moderno do Google
client = genai.Client(api_key=CHAVE_API)

def carregar_contexto():
    """Lê os arquivos do projeto para injetar na mente da IA"""
    contexto = ""
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            contexto += "FILOSOFIA DO PROJETO (README):\n" + f.read() + "\n\n"
    except FileNotFoundError:
        contexto += "O arquivo README.md não foi encontrado.\n"

    try:
        with open("dados_processados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            contexto += "DADOS FINANCEIROS ATUAIS (JSON):\n" + json.dumps(dados, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        contexto += "Os dados processados não foram encontrados. Certifique-se de gerar o JSON."
        
    return contexto

def iniciar_chat():
    print("🕵️ Sherlock: Iniciando o Sistema RAG (Nova Geração)...")
    contexto_projeto = carregar_contexto()
    
    # Criamos o "Prompt do Sistema" (A personalidade da IA)
    instrucao_sistema = f"""
    Você é o 'Assistente Moeda', uma IA integrada a um dashboard financeiro automotivo.
    Seu objetivo é ajudar o usuário a entender seus pagamentos, calcular juros compostos e manter a organização financeira.
    Responda SEMPRE com base nos DADOS e na FILOSOFIA fornecidos abaixo.
    Seja analítico, direto, encorajador e use um tom profissional mas acessível.
    
    CONTEXTO OBRIGATÓRIO:
    {contexto_projeto}
    """
    
    # Configura a personalidade e a "frieza" da IA (temperature baixa = mais preciso com números)
    config = types.GenerateContentConfig(
        system_instruction=instrucao_sistema,
        temperature=0.3,
    )
    
    try:
        # Iniciamos o chat com o modelo Flash (Gratuito e super rápido)
        chat = client.chats.create(model="gemini-2.5-flash", config=config)
        
        print("\n" + "="*50)
        print("🚗 ASSISTENTE MOEDA ONLINE (Motor Flash)")
        print("O motor RAG está ligado. Digite 'sair' para encerrar.")
        print("="*50 + "\n")
        
        while True:
            pergunta = input("\nVocê: ")
            
            if pergunta.lower() in ['sair', 'exit', 'quit']:
                print("Desligando os motores... Até logo!")
                break
                
            print("Pensando...")
            resposta = chat.send_message(pergunta)
            print(f"\n🤖 Assistente Moeda: {resposta.text}")
            
    except Exception as e:
        print(f"\n🚨 Houve um erro no núcleo da matriz: {e}")

if __name__ == "__main__":
    iniciar_chat()