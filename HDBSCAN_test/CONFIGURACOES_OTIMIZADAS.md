# Configurações Otimizadas - HDBSCAN Hierárquico

## 🎯 Escolha Seu Cenário

Este arquivo contém configurações pré-otimizadas para diferentes situações.
**Copie e cole** a configuração adequada no arquivo `hdbscan_hierarchical_batches.py`.

---

## 📊 Cenário 1: Máxima Qualidade (Máquina Potente)

**Quando usar:**
- Você tem 16+ GB de RAM
- Possui GPU dedicada
- Tempo não é crítico (pode levar 3-5 horas)
- Quer os melhores resultados possíveis

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batches grandes para melhor contexto
    'BATCH_SIZE': 150000,
    'RANDOM_STATE': 42,
    
    # Modelo de melhor qualidade
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 128,  # GPU necessária
    
    # UMAP com mais componentes
    'UMAP_N_NEIGHBORS': 75,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 20,  # Mais informação preservada
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN mais granular
    'HDBSCAN_MIN_CLUSTER_SIZE': 8,
    'HDBSCAN_MIN_SAMPLES': 4,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge conservador (mais clusters)
    'CENTROID_SIMILARITY_THRESHOLD': 0.80,
    'CENTROID_MERGE_METHOD': 'complete',  # Mais conservador
    
    # Reclassificação conservadora
    'OUTLIER_MAX_DISTANCE': 0.25,
}
```

**Resultados esperados:**
- Outliers: 3-5%
- Clusters: 400-600
- Tempo: 3-5 horas
- Qualidade: Excelente

---

## ⚡ Cenário 2: Máxima Velocidade (Resultados Rápidos)

**Quando usar:**
- Você quer resultados em 1-2 horas
- Precisa de uma primeira análise rápida
- Qualidade pode ser um pouco menor
- RAM limitada (8 GB)

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batches grandes se possível
    'BATCH_SIZE': 200000,  # Menos batches = mais rápido
    'RANDOM_STATE': 42,
    
    # Modelo rápido
    'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2',  # Mais rápido
    'EMBEDDING_BATCH_SIZE': 128,
    
    # UMAP rápido
    'UMAP_N_NEIGHBORS': 30,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 8,  # Menos componentes = mais rápido
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN rápido
    'HDBSCAN_MIN_CLUSTER_SIZE': 15,  # Clusters maiores
    'HDBSCAN_MIN_SAMPLES': 8,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge agressivo (menos clusters)
    'CENTROID_SIMILARITY_THRESHOLD': 0.90,
    'CENTROID_MERGE_METHOD': 'average',
    
    # Reclassificação rápida
    'OUTLIER_MAX_DISTANCE': 0.35,
}
```

**Resultados esperados:**
- Outliers: 5-8%
- Clusters: 200-300
- Tempo: 1-2 horas
- Qualidade: Boa

---

## 🖥️ Cenário 3: Máquina Fraca (8GB RAM, Sem GPU)

**Quando usar:**
- Você tem apenas 8 GB de RAM
- Não tem GPU dedicada
- Está OK em esperar mais tempo
- Quer evitar travamentos

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batches PEQUENOS para não travar
    'BATCH_SIZE': 50000,
    'RANDOM_STATE': 42,
    
    # Modelo padrão, batch pequeno para CPU
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 32,  # CPU friendly
    
    # UMAP conservador em memória
    'UMAP_N_NEIGHBORS': 30,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 10,
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN padrão
    'HDBSCAN_MIN_CLUSTER_SIZE': 10,
    'HDBSCAN_MIN_SAMPLES': 5,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge padrão
    'CENTROID_SIMILARITY_THRESHOLD': 0.85,
    'CENTROID_MERGE_METHOD': 'average',
    
    # Reclassificação padrão
    'OUTLIER_MAX_DISTANCE': 0.30,
}
```

**Resultados esperados:**
- Outliers: 5-10%
- Clusters: 300-400
- Tempo: 5-8 horas
- Qualidade: Boa

---

## 🎯 Cenário 4: Menos Outliers (Máxima Cobertura)

**Quando usar:**
- Você quer clusterizar o máximo possível
- Outliers devem ser < 5%
- OK em ter clusters maiores e mais heterogêneos
- Prioriza quantidade sobre pureza

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batch padrão
    'BATCH_SIZE': 100000,
    'RANDOM_STATE': 42,
    
    # Modelo padrão
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 64,
    
    # UMAP que favorece agrupamento
    'UMAP_N_NEIGHBORS': 100,  # Muito alto = mais agrupamento
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 15,
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN liberal
    'HDBSCAN_MIN_CLUSTER_SIZE': 5,   # Clusters menores
    'HDBSCAN_MIN_SAMPLES': 3,        # Mais flexível
    'HDBSCAN_CLUSTER_SELECTION': 'leaf',  # Mais clusters
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge agressivo
    'CENTROID_SIMILARITY_THRESHOLD': 0.95,  # Muito alto
    'CENTROID_MERGE_METHOD': 'single',  # Mais agressivo
    
    # Reclassificação MUY liberal
    'OUTLIER_MAX_DISTANCE': 0.45,  # Alto = aceita mais distantes
}
```

**Resultados esperados:**
- Outliers: 2-5%
- Clusters: 150-250
- Tempo: 2-4 horas
- Qualidade: Clusters menos puros, mas alta cobertura

---

## 📐 Cenário 5: Mais Clusters (Máxima Granularidade)

**Quando usar:**
- Você quer muitos clusters específicos
- Prefere clusters pequenos e homogêneos
- OK em ter mais outliers (10-15%)
- Vai fazer rotulagem manual detalhada

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batch padrão
    'BATCH_SIZE': 100000,
    'RANDOM_STATE': 42,
    
    # Modelo padrão
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 64,
    
    # UMAP que preserva estrutura local
    'UMAP_N_NEIGHBORS': 15,  # Baixo = clusters mais locais
    'UMAP_MIN_DIST': 0.1,    # Mais separação
    'UMAP_N_COMPONENTS': 20,  # Mais dimensões = mais estrutura
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN rigoroso
    'HDBSCAN_MIN_CLUSTER_SIZE': 15,  # Clusters maiores
    'HDBSCAN_MIN_SAMPLES': 10,       # Mais rigoroso
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge MUITO conservador
    'CENTROID_SIMILARITY_THRESHOLD': 0.70,  # Baixo = mais clusters
    'CENTROID_MERGE_METHOD': 'complete',     # Mais conservador
    
    # Reclassificação conservadora
    'OUTLIER_MAX_DISTANCE': 0.20,  # Baixo = menos reclassificação
}
```

**Resultados esperados:**
- Outliers: 10-15%
- Clusters: 600-1000
- Tempo: 3-5 horas
- Qualidade: Clusters muito puros e específicos

---

## ⚖️ Cenário 6: Balanceado (Recomendado para Iniciantes)

**Quando usar:**
- Primeira vez usando o sistema
- Não sabe qual escolher
- Quer resultados equilibrados
- Configuração "padrão de fábrica"

```python
CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Batch padrão
    'BATCH_SIZE': 100000,
    'RANDOM_STATE': 42,
    
    # Modelo padrão
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 64,
    
    # UMAP balanceado
    'UMAP_N_NEIGHBORS': 50,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 15,
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN balanceado
    'HDBSCAN_MIN_CLUSTER_SIZE': 10,
    'HDBSCAN_MIN_SAMPLES': 5,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge balanceado
    'CENTROID_SIMILARITY_THRESHOLD': 0.85,
    'CENTROID_MERGE_METHOD': 'average',
    
    # Reclassificação balanceada
    'OUTLIER_MAX_DISTANCE': 0.30,
}
```

**Resultados esperados:**
- Outliers: 5-10%
- Clusters: 300-400
- Tempo: 2-4 horas
- Qualidade: Boa para maioria dos casos

---

## 🔧 Ajuste Fino Personalizado

### Quer MENOS outliers?
```python
'OUTLIER_MAX_DISTANCE': 0.35,      # ↑ Aumente
'HDBSCAN_MIN_CLUSTER_SIZE': 5,     # ↓ Diminua
'HDBSCAN_MIN_SAMPLES': 3,          # ↓ Diminua
```

### Quer MENOS clusters?
```python
'CENTROID_SIMILARITY_THRESHOLD': 0.90,  # ↑ Aumente
'HDBSCAN_MIN_CLUSTER_SIZE': 20,         # ↑ Aumente
'UMAP_N_NEIGHBORS': 75,                 # ↑ Aumente
```

### Quer MAIS velocidade?
```python
'BATCH_SIZE': 200000,                   # ↑ Aumente (se tiver RAM)
'UMAP_N_COMPONENTS': 10,                # ↓ Diminua
'UMAP_N_NEIGHBORS': 30,                 # ↓ Diminua
'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2',  # Modelo menor
```

### Está sem memória?
```python
'BATCH_SIZE': 50000,                    # ↓ Diminua
'UMAP_N_COMPONENTS': 10,                # ↓ Diminua
'EMBEDDING_BATCH_SIZE': 32,             # ↓ Diminua
```

---

## 📊 Tabela Comparativa

| Cenário | RAM Mín. | Tempo | Outliers | Clusters | Melhor Para |
|---------|----------|-------|----------|----------|-------------|
| Máxima Qualidade | 16 GB | 3-5h | 3-5% | 400-600 | Produção final |
| Máxima Velocidade | 8 GB | 1-2h | 5-8% | 200-300 | Análise rápida |
| Máquina Fraca | 8 GB | 5-8h | 5-10% | 300-400 | Hardware limitado |
| Menos Outliers | 12 GB | 2-4h | 2-5% | 150-250 | Máxima cobertura |
| Mais Clusters | 16 GB | 3-5h | 10-15% | 600-1000 | Análise detalhada |
| Balanceado | 12 GB | 2-4h | 5-10% | 300-400 | Primeira vez |

---

## 💡 Dicas de Escolha

### Escolha "Máxima Qualidade" se:
- ✅ Este é seu resultado final para produção
- ✅ Você tem hardware potente
- ✅ Tempo não é limitante

### Escolha "Máxima Velocidade" se:
- ✅ Você quer uma análise exploratória rápida
- ✅ Vai iterar múltiplas vezes
- ✅ Precisa de resultados hoje

### Escolha "Máquina Fraca" se:
- ✅ Você tem 8GB de RAM ou menos
- ✅ Seu computador trava facilmente
- ✅ Pode deixar rodando overnight

### Escolha "Menos Outliers" se:
- ✅ Seu objetivo é clusterizar o máximo possível
- ✅ Outliers são problemáticos para seu caso
- ✅ Pode revisar clusters manualmente

### Escolha "Mais Clusters" se:
- ✅ Você precisa de granularidade máxima
- ✅ Vai fazer rotulagem manual detalhada
- ✅ Prefere precisão sobre cobertura

### Escolha "Balanceado" se:
- ✅ Primeira vez usando o sistema
- ✅ Não tem certeza do que quer
- ✅ Quer um bom ponto de partida

---

## 🔄 Workflow Recomendado

1. **Primeira execução:** Use **Balanceado**
2. **Analise os resultados:** `python analyze_results.py`
3. **Ajuste conforme necessário:**
   - Muitos outliers? → **Menos Outliers**
   - Clusters muito grandes? → **Mais Clusters**
   - Demorou muito? → **Máxima Velocidade**
4. **Refinamento final:** Use **Máxima Qualidade**

---

## 📝 Como Usar Este Arquivo

1. **Escolha seu cenário** baseado nas descrições acima
2. **Copie** o bloco CONFIG completo do cenário escolhido
3. **Cole** no arquivo `hdbscan_hierarchical_batches.py`
   - Substitua o CONFIG existente (linhas ~20-50)
4. **Execute:** `python hdbscan_hierarchical_batches.py`
5. **Analise os resultados**
6. **Ajuste se necessário**

---

## 🎯 Exemplo Prático

**Situação:** Você tem um notebook com 8GB RAM, precisa de resultados em 2 horas, e quer clusterizar o máximo possível.

**Escolha:** Híbrido entre "Máquina Fraca" + "Máxima Velocidade" + "Menos Outliers"

```python
CONFIG = {
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    'BATCH_SIZE': 75000,  # Médio para não travar
    'RANDOM_STATE': 42,
    
    'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2',  # Rápido
    'EMBEDDING_BATCH_SIZE': 32,  # CPU friendly
    
    'UMAP_N_NEIGHBORS': 50,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 10,  # Rápido
    'UMAP_METRIC': 'cosine',
    
    'HDBSCAN_MIN_CLUSTER_SIZE': 8,   # Flexível
    'HDBSCAN_MIN_SAMPLES': 4,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    'CENTROID_SIMILARITY_THRESHOLD': 0.88,  # Meio termo
    'CENTROID_MERGE_METHOD': 'average',
    
    'OUTLIER_MAX_DISTANCE': 0.35,  # Liberal
}
```

---

**Boa escolha de configuração! 🚀**
