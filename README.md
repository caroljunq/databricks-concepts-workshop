# databricks-concepts-workshop
databricks-concepts-workshop

# Descrição dos dados
```python
import pandas as pd

files = [
    'automl.csv', 
    'frota_locomotivas.csv', 
    'geografia_linha.csv', 
    'monitoramento_trilhos.csv', 
    'paradas.csv', 
    'telemetria.csv'
]

data_info = {}

for file in files:
    try:
        df = pd.read_csv(file)
        # Store column names and types
        cols = []
        for col, dtype in df.dtypes.items():
            cols.append((col, str(dtype)))
        
        data_info[file] = {
            "columns": cols,
            "head": df.head(2).to_dict(orient='records'),
            "rows": len(df)
        }
    except Exception as e:
        data_info[file] = f"Error: {e}"

print(data_info)


```

```text
{'automl.csv': {'columns': [('Data', 'object'), ('Eficiencia_L_TBK', 'float64'), ('Peso_Bruto_Total_Ton', 'int64'), ('Velocidade_Media_KmH', 'float64'), ('Qtd_Paradas_Semaforo', 'int64'), ('Eventos_Retomada_Aceleracao', 'int64'), ('Tempo_Total_Atraso_Min', 'int64'), ('Consumo_Medio_L_100km', 'float64')], 'head': [{'Data': '2024-01-01', 'Eficiencia_L_TBK': 2.297, 'Peso_Bruto_Total_Ton': 127450, 'Velocidade_Media_KmH': 40.4, 'Qtd_Paradas_Semaforo': 14, 'Eventos_Retomada_Aceleracao': 22, 'Tempo_Total_Atraso_Min': 183, 'Consumo_Medio_L_100km': 43.53504571179799}, {'Data': '2024-01-02', 'Eficiencia_L_TBK': 2.059, 'Peso_Bruto_Total_Ton': 117926, 'Velocidade_Media_KmH': 39.1, 'Qtd_Paradas_Semaforo': 10, 'Eventos_Retomada_Aceleracao': 12, 'Tempo_Total_Atraso_Min': 125, 'Consumo_Medio_L_100km': 48.56726566294317}], 'rows': 100}, 'frota_locomotivas.csv': {'columns': [('id_locomotiva', 'object'), ('modelo', 'object'), ('ano_fabricacao', 'int64'), ('ultima_manutencao', 'object')], 'head': [{'id_locomotiva': 'LOC_LOG_9000', 'modelo': 'Heavy Haul AC44', 'ano_fabricacao': 2020, 'ultima_manutencao': '2024-02-14'}, {'id_locomotiva': 'LOC_LOG_9001', 'modelo': 'Heavy Haul AC44', 'ano_fabricacao': 2022, 'ultima_manutencao': '2024-03-18'}], 'rows': 20}, 'geografia_linha.csv': {'columns': [('id_secao', 'object'), ('cidade_referencia', 'object'), ('estado', 'object'), ('tipo_geometria', 'object'), ('raio_curva_metros', 'float64')], 'head': [{'id_secao': 'SEC_01', 'cidade_referencia': 'Juiz de Fora', 'estado': 'MG', 'tipo_geometria': 'Curva Acentuada', 'raio_curva_metros': 300.0}, {'id_secao': 'SEC_02', 'cidade_referencia': 'Brumadinho', 'estado': 'MG', 'tipo_geometria': 'Curva Leve', 'raio_curva_metros': 800.0}], 'rows': 6}, 'monitoramento_trilhos.csv': {'columns': [('id_inspecao', 'object'), ('id_secao', 'object'), ('data_inspecao', 'object'), ('atrito_topo_trilho', 'float64'), ('atrito_lateral_flange', 'float64'), ('tipo_geometria_snapshot', 'object'), ('custo_manutencao_corretiva_brl', 'float64')], 'head': [{'id_inspecao': 'INS_2000', 'id_secao': 'SEC_01', 'data_inspecao': '2024-01-16', 'atrito_topo_trilho': 0.4, 'atrito_lateral_flange': 0.43, 'tipo_geometria_snapshot': 'Curva Acentuada', 'custo_manutencao_corretiva_brl': 20374.24}, {'id_inspecao': 'INS_2001', 'id_secao': 'SEC_03', 'data_inspecao': '2024-05-16', 'atrito_topo_trilho': 0.32, 'atrito_lateral_flange': 0.2, 'tipo_geometria_snapshot': 'Reta', 'custo_manutencao_corretiva_brl': 717.14}], 'rows': 500}, 'paradas.csv': {'columns': [('id_evento', 'object'), ('id_locomotiva', 'object'), ('id_secao', 'object'), ('data_evento', 'object'), ('motivo_parada', 'object'), ('duracao_minutos', 'int64'), ('custo_estimado_perda_brl', 'float64')], 'head': [{'id_evento': 'EVT_1000', 'id_locomotiva': 'LOC_LOG_9004', 'id_secao': 'SEC_04', 'data_evento': '2024-05-03', 'motivo_parada': 'Cruzamento/Sinal Vermelho', 'duracao_minutos': 179, 'custo_estimado_perda_brl': 5014.43}, {'id_evento': 'EVT_1001', 'id_locomotiva': 'LOC_LOG_9017', 'id_secao': 'SEC_04', 'data_evento': '2024-05-22', 'motivo_parada': 'Cruzamento/Sinal Vermelho', 'duracao_minutos': 156, 'custo_estimado_perda_brl': 4540.47}], 'rows': 1000}, 'telemetria.csv': {'columns': [('id_locomotiva', 'object'), ('timestamp_leitura', 'object'), ('velocidade_atual_kmh', 'float64'), ('posicao_acelerador_notch', 'int64'), ('peso_total_toneladas', 'int64'), ('inclinacao_terreno_graus', 'float64'), ('target_consumo_litros_hr', 'float64')], 'head': [{'id_locomotiva': 'LOC_LOG_9002', 'timestamp_leitura': '2024-01-01 00:09:00', 'velocidade_atual_kmh': 15.5, 'posicao_acelerador_notch': 2, 'peso_total_toneladas': 22000, 'inclinacao_terreno_graus': -1.46, 'target_consumo_litros_hr': 209.86}, {'id_locomotiva': 'LOC_LOG_9000', 'timestamp_leitura': '2024-01-01 00:24:00', 'velocidade_atual_kmh': 15.1, 'posicao_acelerador_notch': 8, 'peso_total_toneladas': 12000, 'inclinacao_terreno_graus': 1.1, 'target_consumo_litros_hr': 432.75}], 'rows': 5000}}


```

Aqui está o schema detalhado e o resumo de cada tabela disponível nos seus dados.

---

### 1. `telemetria.csv`

**Resumo:** Tabela de dados de sensores de alta frequência. Registra o comportamento instantâneo das locomotivas ao longo do tempo, fundamental para analisar consumo e pilotagem.

* **Chaves de Ligação:** `id_locomotiva`

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `id_locomotiva` | Texto | Identificador único da locomotiva. |
| `timestamp_leitura` | Data/Hora | Data e hora exata da leitura do sensor. |
| `velocidade_atual_kmh` | Decimal | Velocidade instantânea em km/h. |
| `posicao_acelerador_notch` | Inteiro | Posição do acelerador (0 a 8), indicando a potência aplicada. |
| `peso_total_toneladas` | Inteiro | Peso total da composição (trem + carga) naquele momento. |
| `inclinacao_terreno_graus` | Decimal | Inclinação da via no ponto de leitura (positivo = subida). |
| `target_consumo_litros_hr` | Decimal | Taxa de consumo de combustível instantâneo em litros/hora. |

---

### 2. `paradas.csv`

**Resumo:** Registro de eventos operacionais onde o trem ficou parado. É a fonte principal para calcular custos de ineficiência e gargalos (sinal vermelho).

* **Chaves de Ligação:** `id_locomotiva`, `id_secao`

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `id_evento` | Texto | ID único do evento de parada. |
| `id_locomotiva` | Texto | Locomotiva envolvida. |
| `id_secao` | Texto | Seção da linha onde ocorreu a parada. |
| `data_evento` | Data | Data em que a parada ocorreu. |
| `motivo_parada` | Texto | Razão da parada (ex: Cruzamento/Sinal Vermelho, Manutenção). |
| `duracao_minutos` | Inteiro | Tempo total que o trem ficou parado. |
| `custo_estimado_perda_brl` | Decimal | Estimativa financeira do prejuízo causado pela parada. |

---

### 3. `monitoramento_trilhos.csv`

**Resumo:** Histórico de inspeções da via permanente (trilhos). Crucial para analisar o desgaste e a eficácia da lubrificação nas curvas.

* **Chaves de Ligação:** `id_secao`

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `id_inspecao` | Texto | ID único da inspeção. |
| `id_secao` | Texto | Seção da via inspecionada. |
| `data_inspecao` | Data | Data da medição. |
| `atrito_topo_trilho` | Decimal | Coeficiente de atrito no topo do trilho (ideal ser alto para tração). |
| `atrito_lateral_flange` | Decimal | Coeficiente de atrito na lateral (ideal ser baixo para evitar desgaste). |
| `tipo_geometria_snapshot` | Texto | Tipo de geometria no local (ex: Curva Acentuada). |
| `custo_manutencao_corretiva_brl` | Decimal | Custo gasto para reparar o trecho após desgaste. |

---

### 4. `automl.csv`

**Resumo:** Dados agregados diariamente contendo métricas de performance (KPIs). Parece ser um dataset já preparado (feature engineering) para treinar modelos preditivos.

* **Chaves de Ligação:** `Data` (pode ser cruzado temporalmente com outras tabelas)

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `Data` | Data | Dia de referência dos KPIs. |
| `Eficiencia_L_TBK` | Decimal | Litros por Tonelada Bruta Quilômetro (métrica padrão de eficiência). |
| `Peso_Bruto_Total_Ton` | Inteiro | Peso total transportado no dia. |
| `Velocidade_Media_KmH` | Decimal | Velocidade média da frota no dia. |
| `Qtd_Paradas_Semaforo` | Inteiro | Contagem total de paradas por sinal vermelho no dia. |
| `Eventos_Retomada_Aceleracao` | Inteiro | Quantidade de vezes que trens tiveram que retomar velocidade. |
| `Tempo_Total_Atraso_Min` | Inteiro | Minutos totais perdidos em atrasos. |
| `Consumo_Medio_L_100km` | Decimal | Média de consumo por distância percorrida. |

---

### 5. `geografia_linha.csv`

**Resumo:** Tabela de dimensão com as características físicas da ferrovia. Mapeia os códigos de seção (`SEC_XX`) para características reais.

* **Chaves de Ligação:** `id_secao`

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `id_secao` | Texto | Código da seção (ex: SEC_01). |
| `cidade_referencia` | Texto | Cidade próxima. |
| `estado` | Texto | Estado (UF). |
| `tipo_geometria` | Texto | Classificação do traçado (Reta, Curva, Serra). |
| `raio_curva_metros` | Decimal | Raio da curva (quanto menor, mais fechada a curva). Vazio se for reta. |

---

### 6. `frota_locomotivas.csv`

**Resumo:** Cadastro de ativos (dimensão). Detalha as características técnicas de cada locomotiva.

* **Chaves de Ligação:** `id_locomotiva`

| Coluna | Tipo de Dado | Descrição |
| --- | --- | --- |
| `id_locomotiva` | Texto | Código da locomotiva. |
| `modelo` | Texto | Modelo técnico (ex: AC44, SD70). |
| `ano_fabricacao` | Inteiro | Ano de produção. |
| `ultima_manutencao` | Data | Data da última revisão preventiva. |
