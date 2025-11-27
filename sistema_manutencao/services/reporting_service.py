from database.db_setup import get_db_connection
from utils.cli_input import get_int_input, get_float_input

def listar_predicoes():
    """Lista as últimas previsões de RUL e Nível de Risco para monitoramento."""
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                l.id, l.pressao, l.temperatura, l.vibracao, 
                p.rul_predita, p.nivel_risco, l.ciclos_ate_falha_real
            FROM leituras_sensor l
            JOIN predicoes_ml p ON l.id = p.id_leitura
            ORDER BY l.id DESC 
            LIMIT 10
        """)
        predicoes = cursor.fetchall()

        if not predicoes:
            print("\nNenhuma previsão de RUL registrada.")
            return

        print("\n--- Histórico Recente de Predições de RUL ---")
        print("{:<5} | {:<7} | {:<7} | {:<7} | {:<10} | {:<10} | {:<10}".format(
            "ID", "Pressão", "Temp", "Vib.", "RUL Predita", "Risco", "RUL Real"))
        print("-" * 65)
        
        for p in predicoes:
            rul_real = f"{p['ciclos_ate_falha_real']:.0f}" if p['ciclos_ate_falha_real'] is not None else "N/A"
            print("{:<5} | {:<7.2f} | {:<7.2f} | {:<7.2f} | {:<10.2f} | {:<10} | {:<10}".format(
                p['id'], p['pressao'], p['temperatura'], p['vibracao'], p['rul_predita'], p['nivel_risco'], rul_real))
        print("-" * 65)

    except Exception as e:
        print(f"\n❌ Erro ao listar previsões: {e}")
    finally:
        if conn:
            conn.close()

def gerar_relatorio_desempenho():
    """
    Calcula o Erro Absoluto Médio (MAE) do modelo de Regressão.
    MAE = média(|RUL Real - RUL Predita|)
    """
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT 
                l.ciclos_ate_falha_real, p.rul_predita
            FROM leituras_sensor l
            JOIN predicoes_ml p ON l.id = p.id_leitura
            WHERE l.ciclos_ate_falha_real IS NOT NULL
        """)
        dados_avaliacao = cursor.fetchall()

        if not dados_avaliacao:
            print("\nNenhum dado com 'Ciclos Reais Até Falha' (Ground Truth) para calcular o MAE.")
            print("Por favor, garanta que alguns registros na tabela 'leituras_sensor' tenham esse valor.")
            return

        total_erros = 0
        total_registros = len(dados_avaliacao)

        for d in dados_avaliacao:
            erro_absoluto = abs(d['ciclos_ate_falha_real'] - d['rul_predita'])
            total_erros += erro_absoluto

        mae = total_erros / total_registros if total_registros > 0 else 0
        
        print("\n--- Relatório de Desempenho do Modelo de Regressão ---")
        print(f"Amostras de Avaliação (Ground Truth): {total_registros}")
        print("-" * 50)
        print(f"MÉTRICA CHAVE (MAE): {mae:.2f} ciclos")
        print("-" * 50)
        print("\n**Interpretação:**")
        print(f"O modelo erra em média por {mae:.2f} ciclos ao prever a falha.")
        print("Um MAE menor indica um modelo mais preciso.")

    except Exception as e:
        print(f"\n❌ Erro ao gerar relatório de desempenho: {e}")
    finally:
        if conn:
            conn.close()

def atualizar_ground_truth():
    """
    Permite ao usuário inserir a RUL Real (Ground Truth) para um ID de leitura 
    existente, simulando o conhecimento de quando a falha ocorreu.
    """
    print("\n--- Atualizar RUL Real (Ground Truth) ---")
    
    id_leitura = get_int_input("Digite o ID da Leitura (Sensor) que teve a falha/manutenção: ")
    

    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM leituras_sensor WHERE id = ?", (id_leitura,))
        if cursor.fetchone() is None:
            print(f"❌ ID de Leitura {id_leitura} não encontrado.")
            return


        rul_real = get_float_input("Digite os Ciclos REAIS que a máquina durou APÓS aquela leitura: ")
        
        cursor.execute("""
            UPDATE leituras_sensor
            SET ciclos_ate_falha_real = ?
            WHERE id = ?
        """, (rul_real, id_leitura))
        
        conn.commit()
        
        print("\n==============================================")
        print(f"✅ Ground Truth atualizado com sucesso para o ID: {id_leitura}")
        print(f"RUL Real (Ciclos Até Falha) definida como: {rul_real:.0f}")
        print("==============================================")
        print("💡 Sugestão: Agora gere o Relatório de Desempenho (Opção 2) para ver o impacto no MAE.")

    except Exception as e:
        print(f"\n❌ Erro ao atualizar o Ground Truth: {e}")
    finally:
        if conn:
            conn.close()