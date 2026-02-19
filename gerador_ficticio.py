import csv
import random
from datetime import datetime, timedelta

def gerar_dados_ficticios(nome_arquivo="pagamentos_ficticios.csv"):
    # Data de hoje como ponto de partida (Fevereiro de 2026)
    hoje = datetime(2026, 2, 19)
    
    # Voltando 3 anos no tempo (passado)
    data_inicio = hoje - timedelta(days=3 * 365)
    
    # Indo 3 anos para o futuro
    data_fim = hoje + timedelta(days=3 * 365)

    print(f"🕵️ Sherlock: Iniciando a investigação de dados...")
    print(f"🗓️ Período: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}")

    dados = []
    
    # Cabeçalho da nossa planilha burra
    dados.append(["Data", "Valor", "Descricao"])

    data_atual = data_inicio
    dias_trabalhados = 0
    total_arrecadado = 0

    while data_atual <= data_fim:
        # Pega o dia da semana: 0=Seg, 1=Ter, ..., 5=Sáb, 6=Dom
        dia_da_semana = data_atual.weekday()
        
        # Só trabalha de segunda a sexta (dias 0 a 4)
        if dia_da_semana < 5:
            # Sorteia um valor entre 100 e 300 reais (com centavos aleatórios para ficar realista)
            valor_inteiro = random.randint(100, 299)
            centavos = random.choice([0, 50, 90, 25, 75]) # Centavos redondos parecem mais reais
            valor_final = valor_inteiro + (centavos / 100)
            
            # Formata a data e o valor
            data_str = data_atual.strftime("%Y-%m-%d") # Padrão universal (Ano-Mês-Dia)
            valor_str = f"{valor_final:.2f}"
            
            dados.append([data_str, valor_str, "Pagamento Fictício"])
            dias_trabalhados += 1
            total_arrecadado += valor_final

        # Avança para o próximo dia
        data_atual += timedelta(days=1)

    # Escreve tudo no arquivo CSV
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerows(dados)

    print(f"✅ Arquivo '{nome_arquivo}' gerado com sucesso!")
    print(f"📊 Resumo: {dias_trabalhados} dias trabalhados.")
    print(f"💰 Total Movimentado nessa linha do tempo: R$ {total_arrecadado:,.2f}")

# Executa a função
if __name__ == "__main__":
    gerar_dados_ficticios()