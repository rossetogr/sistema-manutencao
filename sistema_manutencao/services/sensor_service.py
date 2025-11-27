from database.db_setup import get_db_connection
from utils.modelo_regressao import predict_rul, get_nivel_risco
from utils.cli_input import get_float_input
from datetime import datetime

def simular_e_predizer():
    """
    Pede as leituras dos sensores, salva no DB e aplica o modelo de predição de RUL.
    """
    print("\n--- Inserir Nova Leitura do Sensor (Ex: P, T, V) ---")
    
    pressao = get_float_input("Digite a Pressão Atual (bar/psi): ")
    temperatura = get_float_input("Digite a Temperatura Atual (°C): ")
    vibracao = get_float_input("Digite a Vibração Atual (mm/s): ")
    
    rul_predita = predict_rul(pressao, temperatura, vibracao)
    nivel_risco = get_nivel_risco(rul_predita)
    
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        cursor.execute("""
            INSERT INTO leituras_sensor (pressao, temperatura, vibracao, ciclos_ate_falha_real, data_registro)
            VALUES (?, ?, ?, NULL, ?)
        """, (pressao, temperatura, vibracao, data_registro))
        
        leitura_id = cursor.lastrowid
        
        cursor.execute("""
            INSERT INTO predicoes_ml (id_leitura, rul_predita, nivel_risco)
            VALUES (?, ?, ?)
        """, (leitura_id, rul_predita, nivel_risco))
        
        conn.commit()
        
        print("\n==============================================")
        print(f"✅ Nova Leitura Registrada (ID: {leitura_id})")
        print(f"RUL Predita (ML): {rul_predita:.2f} ciclos restantes")
        print(f"Nível de Risco: {nivel_risco}")
        print("==============================================")
        print(f"💡 Sugestão de Ação: Agendar Manutenção {nivel_risco} (RUL abaixo de {rul_predita:.0f})")

    except Exception as e:
        print(f"\n❌ Erro ao registrar leitura e predizer RUL: {e}")
    finally:
        if conn:
            conn.close()