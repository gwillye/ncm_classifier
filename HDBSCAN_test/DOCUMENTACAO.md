# HDBSCAN HierÃ¡rquico em Batches - DocumentaÃ§Ã£o

## Ãndice

1. [VisÃ£o Geral](#visÃ£o-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Requisitos](#requisitos)
4. [InstalaÃ§Ã£o](#instalaÃ§Ã£o)
5. [ConfiguraÃ§Ã£o](#configuraÃ§Ã£o)
6. [Modo de Uso](#modo-de-uso)
7. [Estrutura de Arquivos](#estrutura-de-arquivos)
8. [ParÃ¢metros e Ajustes](#parÃ¢metros-e-ajustes)
9. [Troubleshooting](#troubleshooting)
10. [Perguntas Frequentes](#perguntas-frequentes)

## VisÃ£o Geral

Este sistema implementa uma soluÃ§Ã£o hierÃ¡rquica de clustering para bases de dados de grande escala (1M+ registros) usando HDBSCAN. A ideia central Ã© contornar as limitaÃ§Ãµes computacionais processando os dados em batches, em vez de tentar carregar tudo de uma vez na memÃ³ria.

### Problema que estÃ¡vamos resolvendo

Antes, o fluxo tinha trÃªs dores claras:

- Processar amostras de 100k linhas resultava em cerca de 20% de outliers inflados.
- Apareciam clusters duplicados entre diferentes amostras.
- Era impossÃ­vel processar a base completa (1M+ linhas) por limitaÃ§Ãµes de memÃ³ria.

Depois da abordagem em batches, o cenÃ¡rio muda:

- A base completa Ã© processada em batches gerenciÃ¡veis.
- HÃ¡ um merge inteligente de clusters similares entre batches.
- Os outliers sÃ£o reclassificados usando todos os centroides.
- A taxa de outliers cai de forma significativa (tipicamente de 20% para algo entre 5% e 10%).

### Fluxo do processo

```
ENTRADA: base_outros_a_analisar.csv (1M+ linhas)
    |
ETAPA 1: Dividir em batches -> HDBSCAN em cada batch
    |
ETAPA 2: Extrair centroides -> Merge de clusters similares
    |
ETAPA 3: Reclassificar outliers usando todos os centroides
    |
ETAPA 4: Consolidar resultados finais
    |
SAÃDA: Clusters finais + Resumo para rotulagem
```

## Arquitetura do Sistema

### Componentes principais

1. `hdbscan_hierarchical_batches.py`: script principal com toda a lÃ³gica.
2. `run_stages.py`: interface para execuÃ§Ã£o por etapas.
3. `hdbscan_results/`: diretÃ³rio com checkpoints e resultados.

### Etapa 1: Processamento em batches

O que faz:

- Divide a base em batches de N linhas (padrÃ£o: 100k).
- Para cada batch, ele limpa e normaliza o texto, gera embeddings usando Sentence Transformers, reduz a dimensionalidade com UMAP, aplica HDBSCAN, calcula os centroides de cada cluster e salva um checkpoint.

Output:

- `batch_X_result.pkl`: checkpoint de cada batch.
- `all_batches_results.pkl`: consolidaÃ§Ã£o de todos os batches.

Tempo estimado: 10 a 15 minutos por batch de 100k linhas.

### Etapa 2: Merge de centroides

O que faz:

- Coleta todos os centroides de todos os batches.
- Calcula a matriz de similaridade (cosine).
- Aplica clustering hierÃ¡rquico aos centroides.
- Mescla clusters similares entre batches.
- Cria o mapeamento cluster_original -> cluster_merged.

Exemplo:

```
Batch 0, Cluster 5: "MADEIRA COMPENSADA"     \
Batch 2, Cluster 12: "COMPENSADO NAVAL"      -> Cluster Final 42
Batch 5, Cluster 8: "MADEIRA LAMINADA"       /

ReduÃ§Ã£o tÃ­pica: 800 clusters -> 300 clusters finais
```

Output:

- `merged_centroids.pkl`: centroides consolidados.

Tempo estimado: 2 a 5 minutos.

### Etapa 3: ReclassificaÃ§Ã£o de outliers

O que faz:

- Para cada batch, identifica os outliers (cluster -1).
- Calcula a distÃ¢ncia de cada outlier para todos os centroides merged.
- Reclassifica o outlier se a distÃ¢ncia for menor que o threshold.
- MantÃ©m como outlier se ele estiver muito distante de todos os clusters.

Exemplo:

```
Batch 3, Outlier 1547: "COMPENSADO ESPECIAL"
  -> DistÃ¢ncia para Cluster 42 = 0.22 (< 0.30)
  -> RECLASSIFICADO para Cluster 42

Batch 3, Outlier 2891: "ARGILA BENTONITA"
  -> DistÃ¢ncia mÃ­nima = 0.78 (> 0.30)
  -> MANTIDO como outlier
```

Output:

- `reclassification_results.pkl`: resultados da reclassificaÃ§Ã£o.

Tempo estimado: 5 a 10 minutos.

### Etapa 4: GeraÃ§Ã£o de resultados finais

O que faz:

- Consolida todos os batches com os clusters finais.
- Gera as estatÃ­sticas completas.
- Cria o arquivo principal com todos os registros.
- Cria um resumo para rotulagem manual.

Output:

- `resultado_final_clusters.csv`: todos os registros com o cluster final.
- `resumo_clusters_rotulagem.csv`: top clusters para anÃ¡lise.

Tempo estimado: 1 a 2 minutos.

## Requisitos

### Hardware mÃ­nimo

- RAM: 8 GB (16 GB recomendado).
- Disco: 5 GB livres.
- GPU: opcional (acelera os embeddings, mas nÃ£o Ã© obrigatÃ³ria).

### DependÃªncias Python

```
pandas>=1.5.0
numpy>=1.23.0
torch>=2.0.0
sentence-transformers>=2.2.0
umap-learn>=0.5.3
hdbscan>=0.8.29
scikit-learn>=1.2.0
scipy>=1.9.0
plotly>=5.0.0  # Opcional, para visualizaÃ§Ãµes
```

## InstalaÃ§Ã£o

### Passo 1: Criar ambiente virtual

```bash
python -m venv venv_hdbscan
source venv_hdbscan/bin/activate  # Linux/Mac
# ou
venv_hdbscan\Scripts\activate  # Windows
```

### Passo 2: Instalar dependÃªncias

```bash
pip install pandas numpy torch sentence-transformers umap-learn hdbscan scikit-learn scipy
```

### Passo 3: Verificar instalaÃ§Ã£o

```python
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA disponÃ­vel: {torch.cuda.is_available()}")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("Modelo carregado com sucesso!")
```

## ConfiguraÃ§Ã£o

Edite o dicionÃ¡rio `CONFIG` no arquivo `hdbscan_hierarchical_batches.py`.

### ConfiguraÃ§Ãµes essenciais

```python
CONFIG = {
    # Seu arquivo de entrada
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',

    # Tamanho do batch (ajuste conforme sua memÃ³ria)
    'BATCH_SIZE': 100000,  # Reduza se der erro de memÃ³ria
}
```

### ConfiguraÃ§Ãµes de performance

```python
# Para mÃ¡quinas com menos memÃ³ria
'BATCH_SIZE': 50000,           # Batches menores
'UMAP_N_NEIGHBORS': 30,        # Menos vizinhos
'UMAP_N_COMPONENTS': 10,       # Menos componentes

# Para mÃ¡quinas mais potentes
'BATCH_SIZE': 150000,          # Batches maiores
'UMAP_N_NEIGHBORS': 75,        # Mais vizinhos
'UMAP_N_COMPONENTS': 20,       # Mais componentes
```

### ConfiguraÃ§Ãµes de qualidade

```python
# Merge mais agressivo (menos clusters finais)
'CENTROID_SIMILARITY_THRESHOLD': 0.90,

# Merge mais conservador (mais clusters finais)
'CENTROID_SIMILARITY_THRESHOLD': 0.80,

# ReclassificaÃ§Ã£o mais liberal (menos outliers)
'OUTLIER_MAX_DISTANCE': 0.35,

# ReclassificaÃ§Ã£o mais conservadora (mais outliers)
'OUTLIER_MAX_DISTANCE': 0.25,
```

## Modo de Uso

### MÃ©todo 1: ExecuÃ§Ã£o completa (recomendado)

Execute todo o pipeline de uma vez:

```bash
python hdbscan_hierarchical_batches.py
```

Vantagens: Ã© automÃ¡tico e nÃ£o exige intervenÃ§Ã£o, os checkpoints sÃ£o salvos automaticamente e o processo pode retomar de onde parou se for interrompido.

Tempo estimado total: 2 a 4 horas para 1M de linhas.

### MÃ©todo 2: ExecuÃ§Ã£o por etapas (debugging)

Use o menu interativo:

```bash
python run_stages.py
```

OpÃ§Ãµes do menu:

```
1 - Executar Etapa 1: Processar Batches
2 - Executar Etapa 2: Merge de Centroides
3 - Executar Etapa 3: Reclassificar Outliers
4 - Executar Etapa 4: Gerar Resultados Finais
5 - Executar Pipeline Completo
6 - Ver Status dos Checkpoints
7 - Limpar Checkpoints
0 - Sair
```

Quando usar: debugging de etapas especÃ­ficas, ajuste fino de parÃ¢metros ou verificaÃ§Ã£o de resultados intermediÃ¡rios.

### MÃ©todo 3: Importar como mÃ³dulo

```python
from hdbscan_hierarchical_batches import *

# Executar apenas uma etapa
batch_results = run_batch_processing()

# Ou todo o pipeline
main()
```

## Estrutura de Arquivos

### Arquivos de entrada

```
projeto/
â”œâ”€â”€ base_outros_a_analisar.csv     # Sua base de dados
â”œâ”€â”€ hdbscan_hierarchical_batches.py
â””â”€â”€ run_stages.py
```

### Arquivos gerados

```
projeto/
â”œâ”€â”€ hdbscan_results/
â”‚   â”œâ”€â”€ batch_0_result.pkl         # Checkpoint batch 0
â”‚   â”œâ”€â”€ batch_1_result.pkl         # Checkpoint batch 1
â”‚   â”œâ”€â”€ ...
â”‚   â”œâ”€â”€ all_batches_results.pkl    # Todos os batches
â”‚   â”œâ”€â”€ merged_centroids.pkl       # Centroides mesclados
â”‚   â”œâ”€â”€ reclassification_results.pkl
â”‚   â”œâ”€â”€ resultado_final_clusters.csv      # RESULTADO PRINCIPAL
â”‚   â””â”€â”€ resumo_clusters_rotulagem.csv     # PARA ROTULAGEM
```

### DescriÃ§Ã£o dos outputs

#### resultado_final_clusters.csv

```csv
prod_xprod,cluster_final,batch_id
"MADEIRA COMPENSADA NAVAL",42,0
"COMPENSADO 18MM",42,0
"ARGILA BENTONITA",-1,0
...
```

Colunas:

- `prod_xprod`: descriÃ§Ã£o original do produto.
- `cluster_final`: ID do cluster (ou -1 se for outlier).
- `batch_id`: batch de origem (informativo).

#### resumo_clusters_rotulagem.csv

```csv
cluster_id,tamanho,exemplos
42,15240,"MADEIRA COMPENSADA | COMPENSADO NAVAL | MADEIRA LAMINADA"
18,12839,"PORTA MADEIRA | PORTA COMPENSADA | FOLHA PORTA"
...
```

Uso: este Ã© o arquivo para rotulagem manual dos clusters identificados. Cada linha representa um cluster com exemplos representativos.

## ParÃ¢metros e Ajustes

### Guia de ajuste por objetivo

#### Quero MENOS clusters (agrupamento mais agressivo)

```python
# Merge de centroides
'CENTROID_SIMILARITY_THRESHOLD': 0.95,  # Aumentar

# HDBSCAN
'HDBSCAN_MIN_CLUSTER_SIZE': 20,  # Aumentar

# UMAP
'UMAP_N_NEIGHBORS': 75,  # Aumentar
```

#### Quero MAIS clusters (agrupamento mais granular)

```python
# Merge de centroides
'CENTROID_SIMILARITY_THRESHOLD': 0.75,  # Diminuir

# HDBSCAN
'HDBSCAN_MIN_CLUSTER_SIZE': 5,  # Diminuir

# UMAP
'UMAP_N_NEIGHBORS': 30,  # Diminuir
```

#### Quero MENOS outliers (mais itens clusterizados)

```python
# ReclassificaÃ§Ã£o
'OUTLIER_MAX_DISTANCE': 0.40,  # Aumentar

# HDBSCAN
'HDBSCAN_MIN_SAMPLES': 3,  # Diminuir
'HDBSCAN_MIN_CLUSTER_SIZE': 5,  # Diminuir
```

#### Quero MAIS velocidade (menos qualidade)

```python
# Batches maiores
'BATCH_SIZE': 200000,  # Aumentar (cuidado com a RAM!)

# UMAP mais rÃ¡pido
'UMAP_N_COMPONENTS': 8,  # Diminuir
'UMAP_N_NEIGHBORS': 30,  # Diminuir

# Embeddings em batches maiores
'EMBEDDING_BATCH_SIZE': 128,  # Aumentar (se tiver GPU)
```

### Tabela de parÃ¢metros

| ParÃ¢metro | Valor PadrÃ£o | Range TÃ­pico | Impacto |
|-----------|--------------|--------------|---------|
| BATCH_SIZE | 100000 | 50k - 200k | MemÃ³ria vs Velocidade |
| UMAP_N_NEIGHBORS | 50 | 15 - 100 | Estrutura local vs global |
| UMAP_N_COMPONENTS | 15 | 5 - 30 | Qualidade vs Velocidade |
| HDBSCAN_MIN_CLUSTER_SIZE | 10 | 5 - 50 | Granularidade dos clusters |
| HDBSCAN_MIN_SAMPLES | 5 | 3 - 20 | Rigidez da clusterizaÃ§Ã£o |
| CENTROID_SIMILARITY_THRESHOLD | 0.85 | 0.75 - 0.95 | Merge agressivo/conservador |
| OUTLIER_MAX_DISTANCE | 0.30 | 0.20 - 0.40 | ReclassificaÃ§Ã£o liberal/conservadora |

## Troubleshooting

### Erro: MemoryError / Killed

Sintomas:

```
Killed
Process finished with exit code 137
```

SoluÃ§Ãµes:

1. Reduza `BATCH_SIZE` para 50000 ou menos.
2. Reduza `UMAP_N_COMPONENTS` para 10.
3. Reduza `UMAP_N_NEIGHBORS` para 30.
4. Feche outros programas que consomem memÃ³ria.

### Erro: CUDA out of memory

Sintomas:

```
RuntimeError: CUDA out of memory
```

SoluÃ§Ãµes:

1. Reduza `EMBEDDING_BATCH_SIZE` para 32 ou 16.
2. Force o uso de CPU:
   ```python
   device = torch.device('cpu')
   ```

### Muitos outliers no resultado final (>15%)

Causas: parÃ¢metros muito rÃ­gidos ou threshold de reclassificaÃ§Ã£o muito baixo.

SoluÃ§Ãµes:

1. Aumente `OUTLIER_MAX_DISTANCE` para 0.35 ou 0.40.
2. Diminua `HDBSCAN_MIN_CLUSTER_SIZE` para 5.
3. Diminua `HDBSCAN_MIN_SAMPLES` para 3.

### Clusters muito grandes (>50k itens)

Causas: merge muito agressivo ou base com poucos padrÃµes distintos.

SoluÃ§Ãµes:

1. Diminua `CENTROID_SIMILARITY_THRESHOLD` para 0.75.
2. Aumente `HDBSCAN_MIN_CLUSTER_SIZE` para 20.
3. Verifique se a limpeza de texto nÃ£o estÃ¡ muito agressiva.

### Processamento muito lento

Causas: CPU/GPU fraco, batches muito grandes ou UMAP com muitos componentes.

SoluÃ§Ãµes:

1. Aumente `BATCH_SIZE` (se tiver RAM disponÃ­vel).
2. Diminua `UMAP_N_COMPONENTS` para 10.
3. Use GPU se disponÃ­vel.
4. Execute em horÃ¡rios ociosos do computador.

### Checkpoint corrompido

Sintomas:

```
EOFError: Ran out of input
pickle.UnpicklingError
```

SoluÃ§Ã£o:

1. Delete o checkpoint corrompido:
   ```bash
   rm hdbscan_results/nome_do_arquivo.pkl
   ```
2. Reexecute a etapa correspondente.

## Perguntas Frequentes

### 1. Posso interromper o processamento?

Sim. O sistema salva checkpoints apÃ³s cada etapa. Se vocÃª interromper na Etapa 1, perde apenas o batch atual (os outros jÃ¡ estÃ£o salvos). Nas Etapas 2 a 4, dÃ¡ para retomar de onde parou.

### 2. Como interpretar o cluster -1?

O cluster -1 representa os outliers, ou seja, itens que nÃ£o se encaixaram bem em nenhum cluster. As razÃµes costumam ser: item realmente Ãºnico na base, erro de digitaÃ§Ã£o ou descriÃ§Ã£o malformada, ou produto raro e especÃ­fico demais.

### 3. Quantos clusters devo esperar?

Para bases de NCM CapÃ­tulo 44 (madeira), o esperado Ã© algo entre 200 e 500 clusters. Poucos clusters (menos de 100) indicam parÃ¢metros muito agressivos. Muitos clusters (mais de 1000) indicam parÃ¢metros muito granulares.

### 4. Como uso o resultado para rotulagem?

1. Abra `resumo_clusters_rotulagem.csv`.
2. Para cada cluster, analise os exemplos.
3. Rotule como "CapÃ­tulo 44" ou "Outro".
4. Use regex e regras para automatizar itens similares.

### 5. Posso processar bases maiores (5M, 10M)?

Sim, mas alguns ajustes sÃ£o necessÃ¡rios: aumente o nÃºmero de batches (reduzindo o `BATCH_SIZE`), execute em uma mÃ¡quina com mais RAM e considere rodar em servidor ou nuvem. O tempo estimado fica em torno de 1 hora por 1M de linhas.

### 6. E se meu CSV usar outro separador?

Ajuste no CONFIG:

```python
'INPUT_SEP': ',',  # Para vÃ­rgula
'INPUT_SEP': '\t', # Para tab
'INPUT_SEP': '|',  # Para pipe
```

### 7. Preciso de GPU?

NÃ£o Ã© obrigatÃ³rio, mas acelera bastante. Com GPU o tempo fica em torno de 10 min por batch. Sem GPU, entre 15 e 20 min por batch.

### 8. Como validar a qualidade dos clusters?

1. Verifique a porcentagem de outliers (o ideal fica entre 5% e 15%).
2. Analise amostras dos top 10 clusters.
3. Verifique se os clusters fazem sentido semÃ¢ntico.
4. Compare com a rotulagem manual de uma amostra.

### 9. Posso usar com outros modelos de embeddings?

Sim. Alguns modelos alternativos:

```python
# Modelo menor (mais rÃ¡pido)
'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2'

# Modelo maior (mais preciso)
'MODEL_NAME': 'sentence-transformers/paraphrase-xlm-r-multilingual-v1'
```

### 10. Como exportar apenas clusters do Cap. 44?

Depois de rotular os clusters:

```python
import pandas as pd

# Carregar resultado
df = pd.read_csv('hdbscan_results/resultado_final_clusters.csv')

# Clusters identificados como Cap. 44
clusters_cap44 = [5, 12, 18, 23, 42, ...]  # Seus clusters

# Filtrar
df_cap44 = df[df['cluster_final'].isin(clusters_cap44)]
df_cap44.to_csv('produtos_cap44_identificados.csv', index=False)
```

## Exemplo de Output Esperado

### Console durante a execuÃ§Ã£o

```
============================================================
HDBSCAN HIERÃRQUICO EM BATCHES
Sistema de ClassificaÃ§Ã£o NCM CapÃ­tulo 44
============================================================
InÃ­cio: 2026-01-27 14:30:00

DiretÃ³rio de saÃ­da: hdbscan_results/

============================================================
ETAPA 1: PROCESSAMENTO EM BATCHES
============================================================

-> Carregando base_outros_a_analisar.csv...
Total de linhas: 1,050,000
Dispositivo: cuda
-> Carregando modelo paraphrase-multilingual-mpnet-base-v2...
Modelo carregado

Total de batches: 11

============================================================
BATCH 0 - 100000 linhas
============================================================
-> Limpando texto...
-> Gerando embeddings...
100%|â-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆâ-ˆ| 100000/100000 [02:15<00:00]
-> ReduÃ§Ã£o dimensional (UMAP)...
-> ClusterizaÃ§Ã£o (HDBSCAN)...
Clusters encontrados: 78
Outliers: 18234 (18.2%)
Checkpoint salvo: batch_0_result.pkl

[... batches 1-10 ...]

Processamento de batches concluÃ­do!
11 batches processados

============================================================
ETAPA 2: MERGE DE CENTROIDES
============================================================

Total de centroides antes do merge: 847
-> Calculando similaridade entre centroides...
-> Agrupando centroides similares...
Centroides apÃ³s merge: 312
ReduÃ§Ã£o: 535 clusters mesclados

============================================================
ETAPA 3: RECLASSIFICAÃ‡ÃƒO DE OUTLIERS
============================================================

Batch 0: 18234 outliers a reclassificar...
  Reclassificados: 12891/18234 (70.7%)

[... outros batches ...]

============================================================
RESUMO DA RECLASSIFICAÃ‡ÃƒO
============================================================
Outliers originais: 187450
Outliers reclassificados: 142338
Outliers finais: 45112
Taxa de reclassificaÃ§Ã£o: 75.9%

============================================================
ETAPA 4: GERAÃ‡ÃƒO DE RESULTADOS FINAIS
============================================================

-> Gerando estatÃ­sticas...

============================================================
ESTATÃSTICAS FINAIS
============================================================
Total de registros: 1,050,000
Registros clusterizados: 1,004,888 (95.7%)
Outliers finais: 45,112 (4.3%)
NÃºmero de clusters finais: 312
Tamanho mÃ©dio dos clusters: 3,220.0

Arquivo principal salvo: resultado_final_clusters.csv
Resumo para rotulagem salvo: resumo_clusters_rotulagem.csv

============================================================
TOP 20 MAIORES CLUSTERS
============================================================
Cluster  42: 15,240 itens ( 1.45%)
Cluster  18: 12,839 itens ( 1.22%)
Cluster 103:  9,476 itens ( 0.90%)
...

============================================================
PROCESSAMENTO CONCLUÃDO COM SUCESSO!
============================================================

Arquivos gerados em: hdbscan_results/
  - resultado_final_clusters.csv (todos os registros)
  - resumo_clusters_rotulagem.csv (clusters para rotular)

TÃ©rmino: 2026-01-27 17:45:00
DuraÃ§Ã£o total: 3:15:00
```

## Suporte

Para dÃºvidas ou problemas:

1. Verifique a seÃ§Ã£o de Troubleshooting.
2. Revise as FAQs.
3. Execute com `run_stages.py` para fazer debug por etapa.
4. Verifique os logs de erro completos.

## Conceitos TÃ©cnicos

### O que Ã© HDBSCAN?

Hierarchical Density-Based Spatial Clustering of Applications with Noise. Ele identifica clusters de densidade variÃ¡vel, determina automaticamente o nÃºmero de clusters e Ã© robusto a outliers.

### O que Ã© UMAP?

Uniform Manifold Approximation and Projection. Ã‰ uma tÃ©cnica de reduÃ§Ã£o de dimensionalidade nÃ£o linear que preserva a estrutura local e global dos dados, sendo superior ao PCA para embeddings.

### O que sÃ£o embeddings?

SÃ£o representaÃ§Ãµes vetoriais densas de texto que capturam semÃ¢ntica. Textos similares ficam com vetores prÃ³ximos, e eles sÃ£o gerados por modelos de linguagem treinados.

### O que Ã© Cosine Similarity?

Ã‰ uma medida de similaridade entre vetores baseada no Ã¢ngulo entre eles. O valor 1.0 indica vetores idÃªnticos, 0.0 indica vetores ortogonais (nÃ£o relacionados) e -1.0 indica vetores opostos.

VersÃ£o: 1.0
Data: Janeiro 2026
Projeto: Sistema de ClassificaÃ§Ã£o NCM CapÃ­tulo 44
