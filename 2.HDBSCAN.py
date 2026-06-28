import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import plotly.express as px
import re

# --- CONFIGURAÇÃO ---
FILE_PATH = 'tb_treina_cap44.csv'
SAMPLE_SIZE = 100000 # None para base completa
MODEL_NAME = 'paraphrase-multilingual-mpnet-base-v2' # Modelo SBERT multilíngue
N_VISUAL_COMPONENTS = 10 # Componentes para a visualização 3D

print(f"Carregando {FILE_PATH}...")
df_full = pd.read_csv(FILE_PATH, sep='\t', decimal='.', encoding='utf-8') # tabulação

# Amostragem (None para rodar na base completa)
if SAMPLE_SIZE is not None and len(df_full) > SAMPLE_SIZE:
    df = df_full.sample(n=SAMPLE_SIZE, random_state=42).copy()
else:
    df = df_full.copy()

print(f"Tamanho da base para clusterização: {len(df)}.")

df['prod_xprod_clean'] = df['prod_xprod'].astype(str).str.upper().fillna('')
df['prod_xprod_clean'] = df['prod_xprod_clean'].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))
df['prod_xprod_clean'] = df['prod_xprod_clean'].apply(lambda x: re.sub(r'\d+', ' ', x))

print("Normalização end.")

# Configuração do Dispositivo (GPU/CPU)
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(f"Usando dispositivo: {device}")

# Carregamento do Modelo
print(f"Carregando SBERT: {MODEL_NAME}...")
model = SentenceTransformer(MODEL_NAME, device=device)

# Geração dos Embeddings
print("Geração de embeddings...")
embeddings = model.encode(df['prod_xprod_clean'].tolist(), show_progress_bar=True)
print(f"Embeddings gerados com formato: {embeddings.shape}")

# UMAP é superior ao PCA/SVD para embeddings
print("Redução de Dimensionalidade com UMAP...")
N_CLUSTER_COMPONENTS = 15
reducer = umap.UMAP(
    n_neighbors=50, #aumentar pra auxiliar o UMAP a executar ou reduzir pra deixar mais reduzido
    min_dist=0.0, 
    n_components=N_CLUSTER_COMPONENTS,
    #random_state=42, #comentado porque tava forçando muito a CPU
    metric='cosine'
)

X_reduced = reducer.fit_transform(embeddings)
print("Redução de Dimensionalidade end.")

print("Clusterização HDBSCAN...")
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=10, 
    min_samples=5, 
    cluster_selection_method='eom', 
    metric='euclidean'
)

df['cluster'] = clusterer.fit_predict(X_reduced)

n_clusters = len(df['cluster'].unique()) - (1 if -1 in df['cluster'].unique() else 0)
n_outliers = len(df[df['cluster'] == -1])

print(f"Clusterização concluída.")
print(f"Número de Clusters Encontrados: {n_clusters}")
print(f"Número de Outliers (Cluster -1): {n_outliers}")
print("Distribuição de Clusters:\n", df['cluster'].value_counts().head(10))

# 5.2. Exportação dos Resultados
df_export = df[['prod_xprod', 'cluster']].copy()
df_export.to_csv('produtos_clusters_PRO.csv', index=False)

print("Exportação concluída. Arquivo 'produtos_clusters_PRO.csv' gerado com sucesso.")

# 5.3. Amostra dos Clusters
top_clusters = df['cluster'].value_counts().index[1:6] # Ignora o cluster -1 (outliers)

for c in top_clusters:
    print(f"\n--- Amostra do Cluster {c} ---")
    print(df[df['cluster'] == c]['prod_xprod'].head(10).tolist())