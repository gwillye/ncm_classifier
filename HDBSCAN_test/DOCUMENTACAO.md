# HDBSCAN Hierárquico em Batches - Documentação

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura do Sistema](#arquitetura-do-sistema)
3. [Requisitos](#requisitos)
4. [Instalação](#instalação)
5. [Configuração](#configuração)
6. [Modo de Uso](#modo-de-uso)
7. [Estrutura de Arquivos](#estrutura-de-arquivos)
8. [Parâmetros e Ajustes](#parâmetros-e-ajustes)
9. [Troubleshooting](#troubleshooting)
10. [Perguntas Frequentes](#perguntas-frequentes)

---

## 🎯 Visão Geral

Este sistema implementa uma solução hierárquica de clustering para bases de dados de grande escala (1M+ registros) usando HDBSCAN, superando limitações computacionais através de processamento em batches.

### Problema Resolvido

**Antes**: 
- Processamento de amostras (100k linhas) resultava em ~20% de outliers inflados
- Clusters duplicados entre diferentes amostras
- Impossibilidade de processar base completa (1M+ linhas) por limitações de memória

**Depois**:
- Processamento completo da base em batches gerenciáveis
- Merge inteligente de clusters similares entre batches
- Reclassificação de outliers usando todos os centroides
- Redução significativa de outliers (tipicamente de 20% para 5-10%)

### Fluxo do Processo

```
ENTRADA: base_outros_a_analisar.csv (1M+ linhas)
    ↓
ETAPA 1: Dividir em batches → HDBSCAN em cada batch
    ↓
ETAPA 2: Extrair centroides → Merge de clusters similares
    ↓
ETAPA 3: Reclassificar outliers usando todos os centroides
    ↓
ETAPA 4: Consolidar resultados finais
    ↓
SAÍDA: Clusters finais + Resumo para rotulagem
```

---

## 🏗️ Arquitetura do Sistema

### Componentes Principais

1. **hdbscan_hierarchical_batches.py**: Script principal com toda a lógica
2. **run_stages.py**: Interface para execução por etapas
3. **hdbscan_results/**: Diretório com checkpoints e resultados

### Etapa 1: Processamento em Batches

**O que faz:**
- Divide a base em batches de N linhas (padrão: 100k)
- Para cada batch:
  - Limpa e normaliza texto
  - Gera embeddings usando Sentence Transformers
  - Reduz dimensionalidade com UMAP
  - Aplica HDBSCAN
  - Calcula centroides de cada cluster
  - Salva checkpoint

**Output:**
- `batch_X_result.pkl`: Checkpoint de cada batch
- `all_batches_results.pkl`: Consolidação de todos os batches

**Tempo estimado:** 10-15 minutos por batch de 100k linhas

### Etapa 2: Merge de Centroides

**O que faz:**
- Coleta todos os centroides de todos os batches
- Calcula matriz de similaridade (cosine)
- Aplica clustering hierárquico aos centroides
- Mescla clusters similares entre batches
- Cria mapeamento: cluster_original → cluster_merged

**Exemplo:**
```
Batch 0, Cluster 5: "MADEIRA COMPENSADA"     ↘
Batch 2, Cluster 12: "COMPENSADO NAVAL"      → Cluster Final 42
Batch 5, Cluster 8: "MADEIRA LAMINADA"       ↗

Redução típica: 800 clusters → 300 clusters finais
```

**Output:**
- `merged_centroids.pkl`: Centroides consolidados

**Tempo estimado:** 2-5 minutos

### Etapa 3: Reclassificação de Outliers

**O que faz:**
- Para cada batch, identifica outliers (cluster -1)
- Calcula distância de cada outlier para todos os centroides merged
- Reclassifica outlier se distância < threshold
- Mantém como outlier se muito distante de todos os clusters

**Exemplo:**
```
Batch 3, Outlier 1547: "COMPENSADO ESPECIAL"
  → Distância para Cluster 42 = 0.22 (< 0.30)
  → RECLASSIFICADO para Cluster 42

Batch 3, Outlier 2891: "ARGILA BENTONITA" 
  → Distância mínima = 0.78 (> 0.30)
  → MANTIDO como outlier
```

**Output:**
- `reclassification_results.pkl`: Resultados da reclassificação

**Tempo estimado:** 5-10 minutos

### Etapa 4: Geração de Resultados Finais

**O que faz:**
- Consolida todos os batches com clusters finais
- Gera estatísticas completas
- Cria arquivo principal com todos os registros
- Cria resumo para rotulagem manual

**Output:**
- `resultado_final_clusters.csv`: Todos os registros com cluster final
- `resumo_clusters_rotulagem.csv`: Top clusters para análise

**Tempo estimado:** 1-2 minutos

---

## 📦 Requisitos

### Hardware Mínimo

- **RAM**: 8 GB (16 GB recomendado)
- **Disco**: 5 GB livres
- **GPU**: Opcional (acelera embeddings, mas não obrigatória)

### Dependências Python

```
pandas>=1.5.0
numpy>=1.23.0
torch>=2.0.0
sentence-transformers>=2.2.0
umap-learn>=0.5.3
hdbscan>=0.8.29
scikit-learn>=1.2.0
scipy>=1.9.0
plotly>=5.0.0  # Opcional, para visualizações
```

---

## 🚀 Instalação

### Passo 1: Criar Ambiente Virtual

```bash
python -m venv venv_hdbscan
source venv_hdbscan/bin/activate  # Linux/Mac
# ou
venv_hdbscan\Scripts\activate  # Windows
```

### Passo 2: Instalar Dependências

```bash
pip install pandas numpy torch sentence-transformers umap-learn hdbscan scikit-learn scipy
```

### Passo 3: Verificar Instalação

```python
import torch
print(f"PyTorch: {torch.__version__}")
print(f"CUDA disponível: {torch.cuda.is_available()}")

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
print("✓ Modelo carregado com sucesso!")
```

---

## ⚙️ Configuração

Edite o dicionário `CONFIG` no arquivo `hdbscan_hierarchical_batches.py`:

### Configurações Essenciais

```python
CONFIG = {
    # Seu arquivo de entrada
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    
    # Tamanho do batch (ajuste conforme sua memória)
    'BATCH_SIZE': 100000,  # ↓ Reduza se der erro de memória
}
```

### Configurações de Performance

```python
# Para máquinas com menos memória
'BATCH_SIZE': 50000,           # Batches menores
'UMAP_N_NEIGHBORS': 30,        # Menos vizinhos
'UMAP_N_COMPONENTS': 10,       # Menos componentes

# Para máquinas mais potentes
'BATCH_SIZE': 150000,          # Batches maiores
'UMAP_N_NEIGHBORS': 75,        # Mais vizinhos
'UMAP_N_COMPONENTS': 20,       # Mais componentes
```

### Configurações de Qualidade

```python
# Merge mais agressivo (menos clusters finais)
'CENTROID_SIMILARITY_THRESHOLD': 0.90,

# Merge mais conservador (mais clusters finais)
'CENTROID_SIMILARITY_THRESHOLD': 0.80,

# Reclassificação mais liberal (menos outliers)
'OUTLIER_MAX_DISTANCE': 0.35,

# Reclassificação mais conservadora (mais outliers)
'OUTLIER_MAX_DISTANCE': 0.25,
```

---

## 📖 Modo de Uso

### Método 1: Execução Completa (Recomendado)

Execute todo o pipeline de uma vez:

```bash
python hdbscan_hierarchical_batches.py
```

**Vantagens:**
- Automático, sem intervenção
- Checkpoints salvos automaticamente
- Pode retomar de onde parou se interrompido

**Tempo estimado total:** 2-4 horas para 1M de linhas

### Método 2: Execução por Etapas (Debugging)

Use o menu interativo:

```bash
python run_stages.py
```

**Opções do menu:**
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

**Quando usar:**
- Debugging de etapas específicas
- Ajuste fino de parâmetros
- Verificação de resultados intermediários

### Método 3: Importar como Módulo

```python
from hdbscan_hierarchical_batches import *

# Executar apenas uma etapa
batch_results = run_batch_processing()

# Ou todo o pipeline
main()
```

---

## 📁 Estrutura de Arquivos

### Arquivos de Entrada

```
projeto/
├── base_outros_a_analisar.csv     # Sua base de dados
├── hdbscan_hierarchical_batches.py
└── run_stages.py
```

### Arquivos Gerados

```
projeto/
├── hdbscan_results/
│   ├── batch_0_result.pkl         # Checkpoint batch 0
│   ├── batch_1_result.pkl         # Checkpoint batch 1
│   ├── ...
│   ├── all_batches_results.pkl    # Todos os batches
│   ├── merged_centroids.pkl       # Centroides mesclados
│   ├── reclassification_results.pkl
│   ├── resultado_final_clusters.csv      # ⭐ RESULTADO PRINCIPAL
│   └── resumo_clusters_rotulagem.csv     # ⭐ PARA ROTULAGEM
```

### Descrição dos Outputs

#### resultado_final_clusters.csv

```csv
prod_xprod,cluster_final,batch_id
"MADEIRA COMPENSADA NAVAL",42,0
"COMPENSADO 18MM",42,0
"ARGILA BENTONITA",-1,0
...
```

**Colunas:**
- `prod_xprod`: Descrição original do produto
- `cluster_final`: ID do cluster (ou -1 se outlier)
- `batch_id`: Batch de origem (informativo)

#### resumo_clusters_rotulagem.csv

```csv
cluster_id,tamanho,exemplos
42,15240,"MADEIRA COMPENSADA | COMPENSADO NAVAL | MADEIRA LAMINADA"
18,12839,"PORTA MADEIRA | PORTA COMPENSADA | FOLHA PORTA"
...
```

**Uso:**
Arquivo para rotulagem manual dos clusters identificados. Cada linha representa um cluster com exemplos representativos.

---

## 🔧 Parâmetros e Ajustes

### Guia de Ajuste por Objetivo

#### Quero MENOS clusters (agrupamento mais agressivo)

```python
# Merge de centroides
'CENTROID_SIMILARITY_THRESHOLD': 0.95,  # ↑ Aumentar

# HDBSCAN
'HDBSCAN_MIN_CLUSTER_SIZE': 20,  # ↑ Aumentar

# UMAP
'UMAP_N_NEIGHBORS': 75,  # ↑ Aumentar
```

#### Quero MAIS clusters (agrupamento mais granular)

```python
# Merge de centroides
'CENTROID_SIMILARITY_THRESHOLD': 0.75,  # ↓ Diminuir

# HDBSCAN
'HDBSCAN_MIN_CLUSTER_SIZE': 5,  # ↓ Diminuir

# UMAP
'UMAP_N_NEIGHBORS': 30,  # ↓ Diminuir
```

#### Quero MENOS outliers (mais itens clusterizados)

```python
# Reclassificação
'OUTLIER_MAX_DISTANCE': 0.40,  # ↑ Aumentar

# HDBSCAN
'HDBSCAN_MIN_SAMPLES': 3,  # ↓ Diminuir
'HDBSCAN_MIN_CLUSTER_SIZE': 5,  # ↓ Diminuir
```

#### Quero MAIS velocidade (menos qualidade)

```python
# Batches maiores
'BATCH_SIZE': 200000,  # ↑ Aumentar (cuidado com RAM!)

# UMAP mais rápido
'UMAP_N_COMPONENTS': 8,  # ↓ Diminuir
'UMAP_N_NEIGHBORS': 30,  # ↓ Diminuir

# Embeddings em batches maiores
'EMBEDDING_BATCH_SIZE': 128,  # ↑ Aumentar (se tiver GPU)
```

### Tabela de Parâmetros

| Parâmetro | Valor Padrão | Range Típico | Impacto |
|-----------|--------------|--------------|---------|
| BATCH_SIZE | 100000 | 50k - 200k | Memória vs Velocidade |
| UMAP_N_NEIGHBORS | 50 | 15 - 100 | Estrutura local vs global |
| UMAP_N_COMPONENTS | 15 | 5 - 30 | Qualidade vs Velocidade |
| HDBSCAN_MIN_CLUSTER_SIZE | 10 | 5 - 50 | Granularidade dos clusters |
| HDBSCAN_MIN_SAMPLES | 5 | 3 - 20 | Rigidez da clusterização |
| CENTROID_SIMILARITY_THRESHOLD | 0.85 | 0.75 - 0.95 | Merge agressivo/conservador |
| OUTLIER_MAX_DISTANCE | 0.30 | 0.20 - 0.40 | Reclassificação liberal/conservadora |

---

## 🐛 Troubleshooting

### Erro: MemoryError / Killed

**Sintomas:**
```
Killed
Process finished with exit code 137
```

**Soluções:**
1. Reduza `BATCH_SIZE` para 50000 ou menos
2. Reduza `UMAP_N_COMPONENTS` para 10
3. Reduza `UMAP_N_NEIGHBORS` para 30
4. Feche outros programas que consomem memória

### Erro: CUDA out of memory

**Sintomas:**
```
RuntimeError: CUDA out of memory
```

**Soluções:**
1. Reduza `EMBEDDING_BATCH_SIZE` para 32 ou 16
2. Force uso de CPU:
   ```python
   device = torch.device('cpu')
   ```

### Muitos outliers no resultado final (>15%)

**Causas:**
- Parâmetros muito rígidos
- Threshold de reclassificação muito baixo

**Soluções:**
1. Aumente `OUTLIER_MAX_DISTANCE` para 0.35 ou 0.40
2. Diminua `HDBSCAN_MIN_CLUSTER_SIZE` para 5
3. Diminua `HDBSCAN_MIN_SAMPLES` para 3

### Clusters muito grandes (>50k itens)

**Causas:**
- Merge muito agressivo
- Base com poucos padrões distintos

**Soluções:**
1. Diminua `CENTROID_SIMILARITY_THRESHOLD` para 0.75
2. Aumente `HDBSCAN_MIN_CLUSTER_SIZE` para 20
3. Verifique se a limpeza de texto não está muito agressiva

### Processamento muito lento

**Causas:**
- CPU/GPU fraco
- Batches muito grandes
- UMAP com muitos componentes

**Soluções:**
1. Aumente `BATCH_SIZE` (se tiver RAM disponível)
2. Diminua `UMAP_N_COMPONENTS` para 10
3. Use GPU se disponível
4. Execute em horários ociosos do computador

### Checkpoint corrompido

**Sintomas:**
```
EOFError: Ran out of input
pickle.UnpicklingError
```

**Solução:**
1. Delete o checkpoint corrompido:
   ```bash
   rm hdbscan_results/nome_do_arquivo.pkl
   ```
2. Reexecute a etapa correspondente

---

## ❓ Perguntas Frequentes

### 1. Posso interromper o processamento?

**Sim!** O sistema salva checkpoints após cada etapa. Se interromper:
- Na Etapa 1: Perde apenas o batch atual (outros batches salvos)
- Nas Etapas 2-4: Pode retomar de onde parou

### 2. Como interpretar o cluster -1?

Cluster -1 representa **outliers** - itens que não se encaixaram bem em nenhum cluster. Razões:
- Item realmente único na base
- Erro de digitação/descrição malformada
- Produto raro ou específico demais

### 3. Quantos clusters devo esperar?

Para bases de NCM Capítulo 44 (madeira):
- **Esperado**: 200-500 clusters
- **Poucos (<100)**: Parâmetros muito agressivos
- **Muitos (>1000)**: Parâmetros muito granulares

### 4. Como uso o resultado para rotulagem?

1. Abra `resumo_clusters_rotulagem.csv`
2. Para cada cluster, analise os exemplos
3. Rotule: "Capítulo 44" ou "Outro"
4. Use regex/regras para automatizar itens similares

### 5. Posso processar bases maiores (5M, 10M)?

**Sim**, mas ajustes necessários:
- Aumente número de batches (reduza `BATCH_SIZE`)
- Execute em máquina com mais RAM
- Considere processar em servidor/nuvem
- Tempo estimado: ~1 hora por 1M de linhas

### 6. E se meu CSV usar outro separador?

Ajuste no CONFIG:
```python
'INPUT_SEP': ',',  # Para vírgula
'INPUT_SEP': '\t', # Para tab
'INPUT_SEP': '|',  # Para pipe
```

### 7. Preciso de GPU?

**Não é obrigatório**, mas acelera significativamente:
- **Com GPU**: ~10 min/batch
- **Sem GPU**: ~15-20 min/batch

### 8. Como validar a qualidade dos clusters?

1. Verifique % de outliers (ideal: 5-15%)
2. Analise amostras dos top 10 clusters
3. Verifique se clusters fazem sentido semântico
4. Compare com rotulagem manual de amostra

### 9. Posso usar com outros modelos de embeddings?

**Sim!** Modelos alternativos:
```python
# Modelo menor (mais rápido)
'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2'

# Modelo maior (mais preciso)
'MODEL_NAME': 'sentence-transformers/paraphrase-xlm-r-multilingual-v1'
```

### 10. Como exportar apenas clusters do Cap. 44?

Após rotular os clusters:
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

---

## 📊 Exemplo de Output Esperado

### Console durante execução

```
============================================================
HDBSCAN HIERÁRQUICO EM BATCHES
Sistema de Classificação NCM Capítulo 44
============================================================
Início: 2026-01-27 14:30:00

✓ Diretório de saída: hdbscan_results/

============================================================
ETAPA 1: PROCESSAMENTO EM BATCHES
============================================================

→ Carregando base_outros_a_analisar.csv...
✓ Total de linhas: 1,050,000
✓ Dispositivo: cuda
→ Carregando modelo paraphrase-multilingual-mpnet-base-v2...
✓ Modelo carregado

✓ Total de batches: 11

============================================================
BATCH 0 - 100000 linhas
============================================================
→ Limpando texto...
→ Gerando embeddings...
100%|████████████████████████████████| 100000/100000 [02:15<00:00]
→ Redução dimensional (UMAP)...
→ Clusterização (HDBSCAN)...
✓ Clusters encontrados: 78
✓ Outliers: 18234 (18.2%)
✓ Checkpoint salvo: batch_0_result.pkl

[... batches 1-10 ...]

✓ Processamento de batches concluído!
✓ 11 batches processados

============================================================
ETAPA 2: MERGE DE CENTROIDES
============================================================

✓ Total de centroides antes do merge: 847
→ Calculando similaridade entre centroides...
→ Agrupando centroides similares...
✓ Centroides após merge: 312
✓ Redução: 535 clusters mesclados

============================================================
ETAPA 3: RECLASSIFICAÇÃO DE OUTLIERS
============================================================

Batch 0: 18234 outliers a reclassificar...
  ✓ Reclassificados: 12891/18234 (70.7%)

[... outros batches ...]

============================================================
RESUMO DA RECLASSIFICAÇÃO
============================================================
Outliers originais: 187450
Outliers reclassificados: 142338
Outliers finais: 45112
Taxa de reclassificação: 75.9%

============================================================
ETAPA 4: GERAÇÃO DE RESULTADOS FINAIS
============================================================

→ Gerando estatísticas...

============================================================
ESTATÍSTICAS FINAIS
============================================================
Total de registros: 1,050,000
Registros clusterizados: 1,004,888 (95.7%)
Outliers finais: 45,112 (4.3%)
Número de clusters finais: 312
Tamanho médio dos clusters: 3,220.0

✓ Arquivo principal salvo: resultado_final_clusters.csv
✓ Resumo para rotulagem salvo: resumo_clusters_rotulagem.csv

============================================================
TOP 20 MAIORES CLUSTERS
============================================================
Cluster  42: 15,240 itens ( 1.45%)
Cluster  18: 12,839 itens ( 1.22%)
Cluster 103:  9,476 itens ( 0.90%)
...

============================================================
PROCESSAMENTO CONCLUÍDO COM SUCESSO!
============================================================

Arquivos gerados em: hdbscan_results/
  - resultado_final_clusters.csv (todos os registros)
  - resumo_clusters_rotulagem.csv (clusters para rotular)

Término: 2026-01-27 17:45:00
Duração total: 3:15:00
```

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção Troubleshooting
2. Revise as FAQs
3. Execute com `run_stages.py` para debug por etapa
4. Verifique logs de erro completos

---

## 🎓 Conceitos Técnicos

### O que é HDBSCAN?

Hierarchical Density-Based Spatial Clustering of Applications with Noise
- Identifica clusters de densidade variável
- Automaticamente determina número de clusters
- Robusta a outliers

### O que é UMAP?

Uniform Manifold Approximation and Projection
- Redução de dimensionalidade não-linear
- Preserva estrutura local e global dos dados
- Superior a PCA para embeddings

### O que são Embeddings?

Representações vetoriais densas de texto que capturam semântica
- Textos similares = vetores próximos
- Gerados por modelos de linguagem treinados

### O que é Cosine Similarity?

Medida de similaridade entre vetores baseada no ângulo
- 1.0 = Idênticos
- 0.0 = Ortogonais (não relacionados)
- -1.0 = Opostos

---

**Versão:** 1.0  
**Data:** Janeiro 2026  
**Projeto:** Sistema de Classificação NCM Capítulo 44
