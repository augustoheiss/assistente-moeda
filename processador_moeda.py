import csv
import json
from collections import defaultdict
from datetime import datetime

def processar_dados(arquivo_entrada="pagamentos_ficticios.csv", arquivo_saida="dados_processados.json"):
    print("🕵️ Sherlock: Analisando pagamentos e calculando a matemática avançada...")

    # Estruturas para guardar os valores temporariamente
    dados_por_ano = defaultdict(lambda: {"bruto": 0, "dias": set(), "semanas": set(), "meses": set()})
    dados_por_mes = defaultdict(lambda: {"bruto": 0, "dias": set(), "semanas": set(), "pagamentos_diarios": {}})
    dados_por_semana = defaultdict(float) # Rastreador do Bruto Semanal!

    # Variáveis Globais (Todos os tempos)
    total_global = 0
    dias_totais = set()
    semanas_totais = set()
    meses_totais = set()
    anos_totais = set()

    # Lendo a nossa planilha burra
    with open(arquivo_entrada, mode="r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            data_str = linha["Data"]
            valor = float(linha["Valor"])
            
            if valor == 0:
                continue # Ignora dias zerados para não arruinar a média de trabalho
                
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            ano = data_str[:4]
            mes = data_str[5:7]
            ano_mes = f"{ano}-{mes}"
            
            # Calendário ISO para precisão das semanas
            ano_iso, semana_iso, _ = data_obj.isocalendar()
            chave_semana = f"{ano_iso}-W{semana_iso:02d}"

            # 1. Acumulando no Global
            total_global += valor
            dias_totais.add(data_str)
            semanas_totais.add(chave_semana)
            meses_totais.add(ano_mes)
            anos_totais.add(ano)

            # 2. Acumulando por Ano
            dados_por_ano[ano]["bruto"] += valor
            dados_por_ano[ano]["dias"].add(data_str)
            dados_por_ano[ano]["semanas"].add(chave_semana)
            dados_por_ano[ano]["meses"].add(ano_mes)

            # 3. Acumulando por Mês e Semana
            dados_por_mes[ano_mes]["bruto"] += valor
            dados_por_mes[ano_mes]["dias"].add(data_str)
            dados_por_mes[ano_mes]["semanas"].add(chave_semana)
            dados_por_mes[ano_mes]["pagamentos_diarios"][data_str] = valor
            
            dados_por_semana[chave_semana] += valor

    # Construindo a Árvore JSON Final
    resultado = {
        "geral": {
            "bruto_total": round(total_global, 2),
            "media_diaria_global": round(total_global / len(dias_totais), 2) if dias_totais else 0,
            "media_semanal_global": round(total_global / len(semanas_totais), 2) if semanas_totais else 0,
            "media_mensal_global": round(total_global / len(meses_totais), 2) if meses_totais else 0,
            "media_anual_global": round(total_global / len(anos_totais), 2) if anos_totais else 0
        },
        "anos": {},
        "meses": {},
        "semanas": {k: round(v, 2) for k, v in dados_por_semana.items()}
    }

    # Fechando cálculos por Ano
    for ano, dados in dados_por_ano.items():
        resultado["anos"][ano] = {
            "bruto_anual": round(dados["bruto"], 2),
            "media_diaria_anual": round(dados["bruto"] / len(dados["dias"]), 2) if dados["dias"] else 0,
            "media_semanal_anual": round(dados["bruto"] / len(dados["semanas"]), 2) if dados["semanas"] else 0,
            "media_mensal_anual": round(dados["bruto"] / len(dados["meses"]), 2) if dados["meses"] else 0
        }

    # Fechando cálculos por Mês
    for ano_mes, dados in sorted(dados_por_mes.items()):
        lista_semanas = sorted(list(dados["semanas"]))
        # Pega a última semana do mês para exibir como destaque
        ultima_semana = lista_semanas[-1] if lista_semanas else None
        
        resultado["meses"][ano_mes] = {
            "bruto_mensal": round(dados["bruto"], 2),
            "media_diaria_mes": round(dados["bruto"] / len(dados["dias"]), 2) if dados["dias"] else 0,
            "media_semanal_mes": round(dados["bruto"] / len(dados["semanas"]), 2) if dados["semanas"] else 0,
            "bruto_ultima_semana": round(dados_por_semana[ultima_semana], 2) if ultima_semana else 0,
            "pagamentos_diarios": dados["pagamentos_diarios"]
        }

    with open(arquivo_saida, mode="w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=4, ensure_ascii=False)

    print(f"✅ Arquivo '{arquivo_saida}' gerado! O cérebro está pronto.")

if __name__ == "__main__":
    processar_dados()