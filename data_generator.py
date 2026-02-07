import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuração para reprodutibilidade
np.random.seed(42)
random.seed(42)

# ==========================================
# 1. Tabela Dimensional: Frota de Locomotivas (20 Unidades)
# ==========================================
num_locomotivas = 20
ids_locomotivas = [f'LOC_LOG_{9000+i}' for i in range(num_locomotivas)]
opcoes_modelos = ['Heavy Haul AC44', 'Standard SD70', 'Dash-9 Gen2', 'Legacy C30']

# Gerando metadados aleatórios para as 20 locomotivas
data_frota = {
    'id_locomotiva': ids_locomotivas,
    'modelo': [random.choice(opcoes_modelos) for _ in range(num_locomotivas)],
    'ano_fabricacao': [random.randint(1995, 2023) for _ in range(num_locomotivas)],
    'ultima_manutencao': [(datetime(2024, 1, 1) + timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d') for _ in range(num_locomotivas)]
}
df_frota = pd.DataFrame(data_frota)

# ==========================================
# 2. Tabela Dimensional: Geografia da Linha
# ==========================================
cidades_brasil = [
    ('SEC_01', 'Juiz de Fora', 'MG', 'Curva Acentuada', 300),
    ('SEC_02', 'Brumadinho', 'MG', 'Curva Leve', 800),
    ('SEC_03', 'Santos', 'SP', 'Reta', None),
    ('SEC_04', 'Barra do Piraí', 'RJ', 'Declive / Serra', 400),
    ('SEC_05', 'Cubatão', 'SP', 'Reta', None),
    ('SEC_06', 'Itaguaí', 'RJ', 'Curva Acentuada', 250)
]
df_geografia = pd.DataFrame(cidades_brasil, columns=['id_secao', 'cidade_referencia', 'estado', 'tipo_geometria', 'raio_curva_metros'])

# ==========================================
# 3. Tabela Fato: Telemetria e Consumo (5000 Pontos)
# ==========================================
num_registros_telemetria = 5000
data_inicial = datetime(2024, 1, 1)
telemetria_data = []

for i in range(num_registros_telemetria):
    loco = random.choice(ids_locomotivas)
    
    # Distribui os dados ao longo de 6 meses aleatoriamente
    dt = data_inicial + timedelta(minutes=random.randint(0, 260000)) 
    
    velocidade = round(np.random.uniform(0, 80), 1)
    notch = random.randint(0, 8)
    peso_total = random.choice([8000, 12000, 15000, 18000, 22000]) # Adicionado peso extra-pesado
    inclinacao = round(np.random.uniform(-2.5, 2.5), 2)
    
    # Lógica física para TARGET (Consumo)
    consumo_base = (notch * 35) + (peso_total * 0.006) + (max(0, inclinacao) * 60) 
    consumo_final = consumo_base + np.random.normal(0, 12)
    
    if velocidade == 0:
        consumo_final = 18.0 

    telemetria_data.append([
        loco, 
        dt.strftime('%Y-%m-%d %H:%M:%S'), 
        velocidade, 
        notch, 
        peso_total, 
        inclinacao, 
        round(max(0, consumo_final), 2)
    ])

df_telemetria = pd.DataFrame(telemetria_data, columns=[
    'id_locomotiva', 'timestamp_leitura', 'velocidade_atual_kmh', 
    'posicao_acelerador_notch', 'peso_total_toneladas', 
    'inclinacao_terreno_graus', 'target_consumo_litros_hr'
])

# Ordenar por data para ficar bonito
df_telemetria = df_telemetria.sort_values(by='timestamp_leitura')

# ==========================================
# 4. Tabela Fato: Eventos de Parada (1000 Eventos)
# ==========================================
num_eventos = 1000
eventos_data = []
ids_secoes = df_geografia['id_secao'].tolist()

for i in range(num_eventos): 
    dt_evento = data_inicial + timedelta(minutes=random.randint(0, 260000))
    loco = random.choice(ids_locomotivas)
    secao = random.choice(ids_secoes)
    
    motivos = ['Cruzamento/Sinal Vermelho', 'Manutenção Via', 'Aguardando Pátio', 'Falha Mecânica']
    motivo = np.random.choice(motivos, p=[0.5, 0.2, 0.2, 0.1])
    
    duracao = random.randint(10, 240) # Até 4 horas parado
    custo_total = (duracao * 25) + random.uniform(300, 1200)
    
    eventos_data.append([
        f'EVT_{1000+i}',
        loco,
        secao,
        dt_evento.strftime('%Y-%m-%d'),
        motivo,
        duracao,
        round(custo_total, 2)
    ])

df_paradas = pd.DataFrame(eventos_data, columns=[
    'id_evento', 'id_locomotiva', 'id_secao', 'data_evento', 
    'motivo_parada', 'duracao_minutos', 'custo_estimado_perda_brl'
])

# ==========================================
# 5. Tabela Fato: Monitoramento de Trilhos (500 Inspeções)
# ==========================================
num_inspecoes = 500
inspecao_data = []

for i in range(num_inspecoes):
    dt_inspecao = data_inicial + timedelta(days=random.randint(0, 180))
    secao = random.choice(ids_secoes)
    
    geo_tipo = df_geografia.loc[df_geografia['id_secao'] == secao, 'tipo_geometria'].values[0]
    
    # Lógica de atrito e desgaste
    if 'Curva' in geo_tipo:
        atrito_lateral = round(np.random.uniform(0.30, 0.60), 2)
        # 30% de chance de um custo muito alto em curvas (falha crítica)
        if random.random() > 0.7:
             custo_manut = random.uniform(15000, 45000)
        else:
             custo_manut = random.uniform(2000, 10000)
    else:
        atrito_lateral = round(np.random.uniform(0.10, 0.25), 2)
        custo_manut = random.uniform(0, 2000)
        
    atrito_topo = round(np.random.uniform(0.30, 0.45), 2)
    
    inspecao_data.append([
        f'INS_{2000+i}',
        secao,
        dt_inspecao.strftime('%Y-%m-%d'),
        atrito_topo,
        atrito_lateral,
        geo_tipo,
        round(custo_manut, 2)
    ])

df_trilhos = pd.DataFrame(inspecao_data, columns=[
    'id_inspecao', 'id_secao', 'data_inspecao', 
    'atrito_topo_trilho', 'atrito_lateral_flange', 'tipo_geometria_snapshot', 
    'custo_manutencao_corretiva_brl'
])

# ==========================================
# Exportação
# ==========================================
df_telemetria.to_csv('automl.csv', index=False)
df_paradas.to_csv('paradas.csv', index=False)
df_trilhos.to_csv('monitoramento_trilhos.csv', index=False)
df_geografia.to_csv('geografia_linha.csv', index=False)
df_frota.to_csv('frota_locomotivas.csv', index=False)

print("Geração concluída com sucesso!")
print(f"Telemetria: {len(df_telemetria)} linhas")
print(f"Paradas: {len(df_paradas)} linhas")
print(f"Monitoramento Trilhos: {len(df_trilhos)} linhas")
print(f"Frota: {len(df_frota)} locomotivas")