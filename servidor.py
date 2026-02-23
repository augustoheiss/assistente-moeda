# pyre-ignore-all-errors
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Carrega as Variáveis de Ambiente
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")

if not CHAVE_API:
    print("🚨 ERRO FATAL: Chave da API não encontrada no .env!")
    exit()

# 2. Inicializa o Servidor Web e libera a comunicação (CORS)
app = Flask(__name__)
CORS(app) 

# 3. Conecta com a Matriz
client = genai.Client(api_key=CHAVE_API)

def carregar_contexto():
    """Lê os arquivos do projeto para injetar na mente da IA"""
    contexto = ""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            contexto += "FILOSOFIA DO PROJETO (README):\n" + f.read() + "\n\n"
    except FileNotFoundError:
        pass

    try:
        with open("dados_processados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
            contexto += "DADOS FINANCEIROS ATUAIS (JSON):\n" + json.dumps(dados, indent=2, ensure_ascii=False)
    except FileNotFoundError:
        pass
        
    return contexto

# Carrega o contexto uma vez só quando o servidor liga, para economizar processamento
CONTEXTO_PROJETO = carregar_contexto()

INSTRUCAO_SISTEMA = f"""
Você é o 'Assistente Moeda', uma IA integrada a um dashboard financeiro automotivo.
Seu objetivo é ajudar o usuário a entender seus pagamentos, calcular juros compostos e manter a organização financeira.
Responda SEMPRE com base nos DADOS e na FILOSOFIA fornecidos abaixo.
Seja analítico, direto, encorajador e use um tom profissional mas acessível.

CONTEXTO OBRIGATÓRIO:
{CONTEXTO_PROJETO}
"""

# Variável global para manter a memória da conversa viva enquanto o servidor roda
sessao_chat = None

# Rota de "Campainha" para acordar o Render sem gastar tokens da IA
@app.route('/ping', methods=['GET', 'POST', 'OPTIONS'])
def ping():
    return jsonify({"status": "acordado"}), 200

@app.route('/chat', methods=['POST'])
def conversar():
    global sessao_chat
    
    # Pega os dados que o HTML enviou
    dados_recebidos = request.get_json()
    pergunta = dados_recebidos.get("mensagem")
    contexto_tela = dados_recebidos.get("contexto_tela", "O usuário está vendo o painel geral.")

    if not pergunta:
        return jsonify({"erro": "Nenhuma mensagem foi enviada."}), 400

    # Se a sessão ainda não existir, cria uma nova
    if sessao_chat is None:
        config = types.GenerateContentConfig(
            system_instruction=INSTRUCAO_SISTEMA,
            temperature=0.3,
        )
        sessao_chat = client.chats.create(model="gemini-2.5-flash", config=config)

    # A MÁGICA: Injetamos o filtro invisivelmente na pergunta do usuário!
    pergunta_enriquecida = f"[INFORMAÇÃO DO SISTEMA: {contexto_tela}]\n\nPergunta do usuário: {pergunta}"

    # Envia para o Gemini e devolve para o HTML
    try:
        # Imprime no terminal só para você (Arquiteto) ver a mágica acontecendo
        print(f"Enviando para a IA: {pergunta_enriquecida}") 
        
        resposta = sessao_chat.send_message(pergunta_enriquecida)
        return jsonify({"resposta": resposta.text})
    except Exception as e:
        return jsonify({"erro": f"Erro na matriz: {str(e)}"}), 500

if __name__ == '__main__':
    print("="*50)
    print("🕵️ Servidor do Assistente Moeda ATIVADO!")
    print("📡 Escutando na porta 5000...")
    print("="*50)
    app.run(debug=True, port=5000)