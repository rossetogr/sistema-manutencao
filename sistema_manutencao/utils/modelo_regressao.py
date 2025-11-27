import random
from database.db_setup import get_db_connection
from datetime import datetime

# --- Parâmetros para a classificação de Risco ---
LIMITE_ALTO_RISCO = 50  
LIMITE_MEDIO_RISCO = 150 

def predict_rul(pressao: float, temperatura: float, vibracao: float) -> float:
    """
    Simula um modelo de Regressão treinado para prever a Vida Útil Restante (RUL).
    
    A heurística simula que:
    - RUL é inversamente proporcional a P, T, V (quanto maior o desgaste, menor a RUL).
    - O peso da Vibração é maior, pois é um indicador crítico de falha mecânica.
    """
    
    
    desvio_pressao = max(0, pressao - 75.0) * 1.5
    desvio_temperatura = max(0, temperatura - 48.0) * 2.0
    
    desvio_vibracao = max(0, vibracao - 2.5) * 20.0 
    
    fator_desgaste_total = desvio_pressao + desvio_temperatura + desvio_vibracao
    
    rul_base = 300 
    rul_predita_raw = rul_base - fator_desgaste_total * 3 
    
    rul_predita = max(0, rul_predita_raw + random.uniform(-5, 5))
    
    return round(rul_predita, 2)

def get_nivel_risco(rul_predita: float) -> str:
    """Classifica a RUL predita em um nível de risco acionável."""
    if rul_predita < LIMITE_ALTO_RISCO:
        return "ALTO" # Necessidade de Manutenção Imediata
    elif rul_predita <= LIMITE_MEDIO_RISCO:
        return "MÉDIO" # Agendar Manutenção Proativa
    else:
        return "BAIXO" # Monitoramento Rotineiro

def popular_dados_iniciais(conn):
    """
    Popula o DB com leituras de sensor iniciais (Algumas com Ground Truth para relatório).
    Esta função deve ser chamada APÓS a inicialização das tabelas (init_db).
    """
    if conn is None:
        print("❌ Conexão com o banco de dados inválida. Não foi possível popular dados iniciais.")
        return
        
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM leituras_sensor")
        if cursor.fetchone()[0] == 0:
            print("População do DB com dados iniciais de sensores...")
            
            # Dados de exemplo: P, T, V, Ciclos_Reais_Ate_Falha (Ground Truth)
            leituras_iniciais = [
                (70.0, 45.0, 1.2, 250),   # Máquina nova, RUL Alta
                (75.5, 48.2, 2.5, 120),   # Desgaste médio, RUL Média
                (85.1, 52.9, 4.1, 40),    # Alto desgaste, RUL Baixa
                (68.9, 44.0, 1.5, 200),   # RUL Média-Alta
                (88.0, 55.5, 5.0, 10),    # Crítico, RUL muito Baixa
                (72.0, 46.0, 2.0, None),  # Dado sem Ground Truth (em uso real)
            ]
            
            for p, t, v, ciclos_reais in leituras_iniciais:
                data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("""
                    INSERT INTO leituras_sensor (pressao, temperatura, vibracao, ciclos_ate_falha_real, data_registro)
                    VALUES (?, ?, ?, ?, ?)
                """, (p, t, v, ciclos_reais, data_registro))
            
            conn.commit()
            print("✅ Leituras de sensores iniciais (dados de treinamento/teste) inseridas.")
            
    except Exception as e:
        # Se o erro persistir, ele será reportado aqui.
        print(f"❌ Erro ao popular DB com leituras: {e}")