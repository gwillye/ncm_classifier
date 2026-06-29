# Configurações Otimizadas - HDBSCAN Hierárquico

## Escolha o seu cenário

Este arquivo reúne configurações pré-otimizadas para diferentes situações. A ideia é simples: copie e cole o bloco do cenário que melhor se encaixa no seu caso dentro do arquivo `hdbscan_hierarchical_batches.py`.

## Cenário 1: Máxima qualidade (máquina potente)

Quando usar este cenário: você tem 16 GB de RAM ou mais, possui GPU dedicada, o tempo não é crítico (pode levar de 3 a 5 horas) e você quer os melhores resultados possíveis.

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

Resultados esperados: outliers entre 3% e 5%, de 400 a 600 clusters, tempo de 3 a 5 horas, qualidade excelente.

## Cenário 2: Máxima velocidade (resultados rápidos)

Quando usar este cenário: você quer resultados em 1 ou 2 horas, precisa de uma primeira análise rápida, a qualidade pode ser um pouco menor e a RAM é limitada (8 GB).

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

Resultados esperados: outliers entre 5% e 8%, de 200 a 300 clusters, tempo de 1 a 2 horas, qualidade boa.

## Cenário 3: Máquina fraca (8GB RAM, sem GPU)

Quando usar este cenário: você tem apenas 8 GB de RAM, não tem GPU dedicada, está OK em esperar mais tempo e quer evitar travamentos.

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

Resultados esperados: outliers entre 5% e 10%, de 300 a 400 clusters, tempo de 5 a 8 horas, qualidade boa.

## Cenário 4: Menos outliers (máxima cobertura)

Quando usar este cenário: você quer clusterizar o máximo possível, os outliers devem ficar abaixo de 5%, está OK em ter clusters maiores e mais heterogêneos e prioriza quantidade sobre pureza.

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

    # Reclassificação muito liberal
    'OUTLIER_MAX_DISTANCE': 0.45,  # Alto = aceita mais distantes
}
```

Resultados esperados: outliers entre 2% e 5%, de 150 a 250 clusters, tempo de 2 a 4 horas, com clusters menos puros mas alta cobertura.

## Cenário 5: Mais clusters (máxima granularidade)

Quando usar este cenário: você quer muitos clusters específicos, prefere clusters pequenos e homogêneos, está OK em ter mais outliers (entre 10% e 15%) e vai fazer rotulagem manual detalhada.

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

Resultados esperados: outliers entre 10% e 15%, de 600 a 1000 clusters, tempo de 3 a 5 horas, com clusters muito puros e específicos.

## Cenário 6: Balanceado (recomendado para iniciantes)

Quando usar este cenário: é a sua primeira vez usando o sistema, você não sabe qual escolher, quer resultados equilibrados e prefere a configuração "padrão de fábrica".

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

Resultados esperados: outliers entre 5% e 10%, de 300 a 400 clusters, tempo de 2 a 4 horas, com qualidade boa para a maioria dos casos.

## Ajuste fino personalizado

### Quer MENOS outliers?

```python
'OUTLIER_MAX_DISTANCE': 0.35,      # Aumente
'HDBSCAN_MIN_CLUSTER_SIZE': 5,     # Diminua
'HDBSCAN_MIN_SAMPLES': 3,          # Diminua
```

### Quer MENOS clusters?

```python
'CENTROID_SIMILARITY_THRESHOLD': 0.90,  # Aumente
'HDBSCAN_MIN_CLUSTER_SIZE': 20,         # Aumente
'UMAP_N_NEIGHBORS': 75,                 # Aumente
```

### Quer MAIS velocidade?

```python
'BATCH_SIZE': 200000,                   # Aumente (se tiver RAM)
'UMAP_N_COMPONENTS': 10,                # Diminua
'UMAP_N_NEIGHBORS': 30,                 # Diminua
'MODEL_NAME': 'paraphrase-multilingual-MiniLM-L12-v2',  # Modelo menor
```

### Está sem memória?

```python
'BATCH_SIZE': 50000,                    # Diminua
'UMAP_N_COMPONENTS': 10,                # Diminua
'EMBEDDING_BATCH_SIZE': 32,             # Diminua
```

## Tabela comparativa

| Cenário | RAM Mín. | Tempo | Outliers | Clusters | Melhor Para |
|---------|----------|-------|----------|----------|-------------|
| Máxima Qualidade | 16 GB | 3-5h | 3-5% | 400-600 | Produção final |
| Máxima Velocidade | 8 GB | 1-2h | 5-8% | 200-300 | Análise rápida |
| Máquina Fraca | 8 GB | 5-8h | 5-10% | 300-400 | Hardware limitado |
| Menos Outliers | 12 GB | 2-4h | 2-5% | 150-250 | Máxima cobertura |
| Mais Clusters | 16 GB | 3-5h | 10-15% | 600-1000 | Análise detalhada |
| Balanceado | 12 GB | 2-4h | 5-10% | 300-400 | Primeira vez |

## Dicas de escolha

Escolha "Máxima Qualidade" se este for o seu resultado final para produção, se você tem hardware potente e se o tempo não é limitante.

Escolha "Máxima Velocidade" se você quer uma análise exploratória rápida, se vai iterar várias vezes e se precisa de resultados hoje.

Escolha "Máquina Fraca" se você tem 8GB de RAM ou menos, se o computador trava com facilidade e se você pode deixar rodando durante a noite.

Escolha "Menos Outliers" se o objetivo é clusterizar o máximo possível, se os outliers são problemáticos para o seu caso e se você pode revisar os clusters manualmente.

Escolha "Mais Clusters" se você precisa de granularidade máxima, se vai fazer rotulagem manual detalhada e se prefere precisão sobre cobertura.

Escolha "Balanceado" se é a sua primeira vez usando o sistema, se você não tem certeza do que quer e se busca um bom ponto de partida.

## Workflow recomendado

1. Primeira execução: use o cenário Balanceado.
2. Analise os resultados com `python analyze_results.py`.
3. Ajuste conforme necessário: muitos outliers levam ao cenário Menos Outliers, clusters muito grandes levam ao cenário Mais Clusters e um processamento demorado leva ao cenário Máxima Velocidade.
4. Refinamento final: use o cenário Máxima Qualidade.

## Como usar este arquivo

1. Escolha o seu cenário com base nas descrições acima.
2. Copie o bloco CONFIG completo do cenário escolhido.
3. Cole no arquivo `hdbscan_hierarchical_batches.py`, substituindo o CONFIG existente (linhas ~20-50).
4. Execute com `python hdbscan_hierarchical_batches.py`.
5. Analise os resultados.
6. Ajuste se necessário.

## Exemplo prático

Situação: você tem um notebook com 8GB de RAM, precisa de resultados em 2 horas e quer clusterizar o máximo possível.

Escolha: um híbrido entre "Máquina Fraca", "Máxima Velocidade" e "Menos Outliers".

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

Boa escolha de configuração.
