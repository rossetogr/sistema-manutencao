# sistema-manutencao
Projeto desenvolvido em Python que simula um modelo de Machine Learning de Regressão para prever a Vida Útil Restante (RUL) de equipamentos industriais.
O foco está em transformar leituras de sensores (Pressão, Temperatura, Vibração) em alertas de manutenção proativa.

## Tecnologias
- Python
- SQLite
- SQL
- ML Simulado (Regressão)

## Funcionalidades
- Predição de RUL: Cálculo da Vida Útil Restante com base em inputs de sensores.
-  Classificação de Risco: Conversão da RUL em Níveis de Risco (ALTO, MÉDIO, BAIXO).
-  Validação (Ground Truth): Função para registrar a RUL Real (Ground Truth) após a falha do equipamento.
-  Relatório de Desempenho: Cálculo do Erro Absoluto Médio (MAE), crucial para medir a precisão e a confiabilidade do modelo.

## Como Executar
python main.py

### Fluxo de Uso Recomendado:
1. Predição: Menu [1] Simular Nova Leitura... (Gera uma previsão e um ID de Leitura).
2. Monitorar/Validar: Menu [2] Monitorar Previsões....
3. Atualizar Ground Truth: Dentro do Menu [2], use a Opção [3] Atualizar RUL Real... para registrar o valor da falha (necessário para o MAE).
4. Relatar MAE: Dentro do Menu [2], use a Opção [2] Gerar Relatório de Desempenho (MAE)....
