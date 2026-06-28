import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
import re
import gc

FILE_PATH = 'base_outros_a_analisar.csv'
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2'
N_CLUSTERS = 50000

def clean_text(text):
    text = str(text).upper()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    return text.strip()

# 1. Carregamento
print(f"Arquivo: {FILE_PATH}")
df = pd.read_csv(FILE_PATH, sep=';', decimal='.', encoding='utf-8-sig')
df['clean_text'] = df['prod_xprod'].apply(clean_text)

# 2. Gerar Embeddings (em lotes para não travar a GPU/RAM)
print("Parte 2")
model = SentenceTransformer(MODEL_NAME)
embeddings = model.encode(df['clean_text'].tolist(), batch_size=64, show_progress_bar=True)

# 3. Clusterização com MiniBatchKMeans
print(f"Clusterizando em {N_CLUSTERS} grupos.")
kmeans = MiniBatchKMeans(n_clusters=N_CLUSTERS, batch_size=1024, random_state=42)
df['cluster'] = kmeans.fit_predict(embeddings)

# 4. Identificar Centroides
print("Parte 4")
centroids = kmeans.cluster_centers_

cluster_samples = []
for i in range(N_CLUSTERS):
    sample = df[df['cluster'] == i]['prod_xprod'].head(3).tolist()
    cluster_samples.append({'cluster': i, 'exemplos': " | ".join(sample)})

# 5. Salvar Resultados
df[['prod_xprod', 'cluster']].to_csv('resultado_clusters_final.csv', index=False)
pd.DataFrame(cluster_samples).to_csv('resumo_para_rotulagem.csv', index=False)

print("Concluído")
#resultado_clusters_final.csv': Todos os 1M de itens
#resumo_para_rotulagem.csv': Lista dos 500 grupos para rotulagem
