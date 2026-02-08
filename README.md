# databricks-concepts-workshop
databricks-concepts-workshop

# Descrição dos dados

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
