"""
HDBSCAN Hierárquico em Batches - Clustering de 1M+ linhas
Autor: Sistema de Classificação NCM Cap. 44
Estratégia: Batch processing + merge de centroides + reclassificação de outliers
"""

import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan
import re
import pickle
import os
from datetime import datetime
from scipy.spatial.distance import cdist
from sklearn.cluster import AgglomerativeClustering
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================

CONFIG = {
    # Arquivos
    'INPUT_FILE': 'base_outros_a_analisar.csv',
    'INPUT_SEP': ';',
    'INPUT_ENCODING': 'utf-8-sig',
    'OUTPUT_DIR': 'hdbscan_results',
    
    # Processamento em Batches
    'BATCH_SIZE': 100000,  # 100k linhas por batch (ajuste conforme sua memória)
    'RANDOM_STATE': 42,
    
    # Modelo de Embeddings
    'MODEL_NAME': 'paraphrase-multilingual-mpnet-base-v2',
    'EMBEDDING_BATCH_SIZE': 64,
    
    # UMAP
    'UMAP_N_NEIGHBORS': 50,
    'UMAP_MIN_DIST': 0.0,
    'UMAP_N_COMPONENTS': 15,
    'UMAP_METRIC': 'cosine',
    
    # HDBSCAN
    'HDBSCAN_MIN_CLUSTER_SIZE': 10,
    'HDBSCAN_MIN_SAMPLES': 5,
    'HDBSCAN_CLUSTER_SELECTION': 'eom',
    'HDBSCAN_METRIC': 'euclidean',
    
    # Merge de Centroides
    'CENTROID_SIMILARITY_THRESHOLD': 0.85,  # Cosine similarity para merge
    'CENTROID_MERGE_METHOD': 'average',  # 'single', 'complete', 'average'
    
    # Reclassificação de Outliers
    'OUTLIER_MAX_DISTANCE': 0.3,  # Distância máxima para atribuir outlier a cluster
}

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def setup_output_dir():
    """Cria diretório para resultados"""
    os.makedirs(CONFIG['OUTPUT_DIR'], exist_ok=True)
    print(f"✓ Diretório de saída: {CONFIG['OUTPUT_DIR']}/")

def clean_text(text):
    """Normalização de texto (mesma do seu código original)"""
    text = str(text).upper()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    return text.strip()

def save_checkpoint(data, filename):
    """Salva checkpoint intermediário"""
    filepath = os.path.join(CONFIG['OUTPUT_DIR'], filename)
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
    print(f"✓ Checkpoint salvo: {filename}")

def load_checkpoint(filename):
    """Carrega checkpoint intermediário"""
    filepath = os.path.join(CONFIG['OUTPUT_DIR'], filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    return None

# ============================================================================
# ETAPA 1: PROCESSAMENTO EM BATCHES
# ============================================================================

def process_single_batch(batch_df, batch_id, model, device):
    """
    Processa um único batch com HDBSCAN
    Retorna: dict com clusters, centroides e metadados
    """
    print(f"\n{'='*60}")
    print(f"BATCH {batch_id} - {len(batch_df)} linhas")
    print(f"{'='*60}")
    
    # Limpeza de texto
    print("→ Limpando texto...")
    batch_df['clean_text'] = batch_df['prod_xprod'].apply(clean_text)
    
    # Geração de embeddings
    print("→ Gerando embeddings...")
    embeddings = model.encode(
        batch_df['clean_text'].tolist(),
        batch_size=CONFIG['EMBEDDING_BATCH_SIZE'],
        show_progress_bar=True,
        device=device
    )
    
    # UMAP
    print("→ Redução dimensional (UMAP)...")
    reducer = umap.UMAP(
        n_neighbors=CONFIG['UMAP_N_NEIGHBORS'],
        min_dist=CONFIG['UMAP_MIN_DIST'],
        n_components=CONFIG['UMAP_N_COMPONENTS'],
        metric=CONFIG['UMAP_METRIC']
    )
    X_reduced = reducer.fit_transform(embeddings)
    
    # HDBSCAN
    print("→ Clusterização (HDBSCAN)...")
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=CONFIG['HDBSCAN_MIN_CLUSTER_SIZE'],
        min_samples=CONFIG['HDBSCAN_MIN_SAMPLES'],
        cluster_selection_method=CONFIG['HDBSCAN_CLUSTER_SELECTION'],
        metric=CONFIG['HDBSCAN_METRIC']
    )
    clusters = clusterer.fit_predict(X_reduced)
    
    # Estatísticas
    unique_clusters = np.unique(clusters)
    n_clusters = len(unique_clusters) - (1 if -1 in unique_clusters else 0)
    n_outliers = np.sum(clusters == -1)
    
    print(f"✓ Clusters encontrados: {n_clusters}")
    print(f"✓ Outliers: {n_outliers} ({100*n_outliers/len(batch_df):.1f}%)")
    
    # Calcular centroides (no espaço original de embeddings)
    centroids = {}
    cluster_sizes = {}
    cluster_samples = {}
    
    for cluster_id in unique_clusters:
        if cluster_id == -1:  # Pula outliers
            continue
            
        mask = clusters == cluster_id
        cluster_embeddings = embeddings[mask]
        
        # Centroide = média dos embeddings do cluster
        centroid = np.mean(cluster_embeddings, axis=0)
        centroids[f"batch{batch_id}_cluster{cluster_id}"] = centroid
        cluster_sizes[f"batch{batch_id}_cluster{cluster_id}"] = np.sum(mask)
        
        # Amostras do cluster (para análise posterior)
        cluster_samples[f"batch{batch_id}_cluster{cluster_id}"] = batch_df[mask]['prod_xprod'].head(5).tolist()
    
    # Preparar resultado
    result = {
        'batch_id': batch_id,
        'df': batch_df.copy(),
        'clusters': clusters,
        'embeddings': embeddings,
        'centroids': centroids,
        'cluster_sizes': cluster_sizes,
        'cluster_samples': cluster_samples,
        'n_clusters': n_clusters,
        'n_outliers': n_outliers
    }
    
    return result

def run_batch_processing():
    """
    Executa HDBSCAN em todos os batches e salva resultados
    """
    print("\n" + "="*60)
    print("ETAPA 1: PROCESSAMENTO EM BATCHES")
    print("="*60)
    
    # Carregar dados
    print(f"\n→ Carregando {CONFIG['INPUT_FILE']}...")
    df = pd.read_csv(
        CONFIG['INPUT_FILE'],
        sep=CONFIG['INPUT_SEP'],
        encoding=CONFIG['INPUT_ENCODING']
    )
    print(f"✓ Total de linhas: {len(df):,}")
    
    # Configurar device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"✓ Dispositivo: {device}")
    
    # Carregar modelo
    print(f"→ Carregando modelo {CONFIG['MODEL_NAME']}...")
    model = SentenceTransformer(CONFIG['MODEL_NAME'], device=device)
    print("✓ Modelo carregado")
    
    # Dividir em batches
    n_batches = int(np.ceil(len(df) / CONFIG['BATCH_SIZE']))
    print(f"\n✓ Total de batches: {n_batches}")
    
    batch_results = []
    
    for i in range(n_batches):
        start_idx = i * CONFIG['BATCH_SIZE']
        end_idx = min((i + 1) * CONFIG['BATCH_SIZE'], len(df))
        batch_df = df.iloc[start_idx:end_idx].copy().reset_index(drop=True)
        
        # Processar batch
        result = process_single_batch(batch_df, i, model, device)
        batch_results.append(result)
        
        # Salvar checkpoint após cada batch
        save_checkpoint(result, f'batch_{i}_result.pkl')
    
    # Salvar todos os resultados
    save_checkpoint(batch_results, 'all_batches_results.pkl')
    print(f"\n✓ Processamento de batches concluído!")
    print(f"✓ {len(batch_results)} batches processados")
    
    return batch_results

# ============================================================================
# ETAPA 2: MERGE DE CENTROIDES
# ============================================================================

def merge_centroids(batch_results):
    """
    Agrupa centroides similares de diferentes batches
    """
    print("\n" + "="*60)
    print("ETAPA 2: MERGE DE CENTROIDES")
    print("="*60)
    
    # Coletar todos os centroides
    all_centroids = {}
    all_sizes = {}
    all_samples = {}
    
    for result in batch_results:
        all_centroids.update(result['centroids'])
        all_sizes.update(result['cluster_sizes'])
        all_samples.update(result['cluster_samples'])
    
    print(f"\n✓ Total de centroides antes do merge: {len(all_centroids)}")
    
    # Converter para matriz
    centroid_ids = list(all_centroids.keys())
    centroid_matrix = np.array([all_centroids[cid] for cid in centroid_ids])
    
    # Normalizar para cosine similarity
    centroid_matrix_norm = centroid_matrix / np.linalg.norm(centroid_matrix, axis=1, keepdims=True)
    
    # Calcular matriz de similaridade
    print("→ Calculando similaridade entre centroides...")
    similarity_matrix = np.dot(centroid_matrix_norm, centroid_matrix_norm.T)
    
    # Converter para distância
    distance_matrix = 1 - similarity_matrix
    
    # Clustering hierárquico dos centroides
    print("→ Agrupando centroides similares...")
    threshold_distance = 1 - CONFIG['CENTROID_SIMILARITY_THRESHOLD']
    
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold_distance,
        linkage=CONFIG['CENTROID_MERGE_METHOD'],
        metric='precomputed'
    )
    
    merged_labels = clustering.fit_predict(distance_matrix)
    
    # Criar mapeamento de cluster original -> cluster merged
    centroid_mapping = {}
    for i, cid in enumerate(centroid_ids):
        centroid_mapping[cid] = merged_labels[i]
    
    n_merged_clusters = len(np.unique(merged_labels))
    print(f"✓ Centroides após merge: {n_merged_clusters}")
    print(f"✓ Redução: {len(all_centroids) - n_merged_clusters} clusters mesclados")
    
    # Criar novos centroides (média dos centroides mesclados)
    merged_centroids = {}
    merged_sizes = {}
    merged_samples = {}
    
    for new_cluster_id in np.unique(merged_labels):
        # Identificar centroides originais que pertencem a este cluster merged
        original_ids = [cid for cid, label in centroid_mapping.items() if label == new_cluster_id]
        
        # Calcular novo centroide (média ponderada pelo tamanho)
        total_size = sum(all_sizes[cid] for cid in original_ids)
        weighted_centroid = np.sum([
            all_centroids[cid] * all_sizes[cid] for cid in original_ids
        ], axis=0) / total_size
        
        merged_centroids[new_cluster_id] = weighted_centroid
        merged_sizes[new_cluster_id] = total_size
        
        # Coletar amostras
        samples = []
        for cid in original_ids[:3]:  # Até 3 clusters originais
            samples.extend(all_samples[cid][:2])  # 2 amostras de cada
        merged_samples[new_cluster_id] = samples[:10]  # Max 10 amostras
    
    result = {
        'centroid_mapping': centroid_mapping,
        'merged_centroids': merged_centroids,
        'merged_sizes': merged_sizes,
        'merged_samples': merged_samples,
        'n_original': len(all_centroids),
        'n_merged': n_merged_clusters
    }
    
    save_checkpoint(result, 'merged_centroids.pkl')
    return result

# ============================================================================
# ETAPA 3: RECLASSIFICAÇÃO DE OUTLIERS
# ============================================================================

def reclassify_outliers(batch_results, merged_centroids_result):
    """
    Reclassifica outliers comparando com todos os centroides merged
    """
    print("\n" + "="*60)
    print("ETAPA 3: RECLASSIFICAÇÃO DE OUTLIERS")
    print("="*60)
    
    merged_centroids = merged_centroids_result['merged_centroids']
    centroid_mapping = merged_centroids_result['centroid_mapping']
    
    # Converter centroides para matriz
    merged_ids = sorted(merged_centroids.keys())
    merged_matrix = np.array([merged_centroids[mid] for mid in merged_ids])
    
    total_outliers_original = 0
    total_outliers_reclassified = 0
    
    reclassified_results = []
    
    for batch_result in batch_results:
        batch_id = batch_result['batch_id']
        clusters = batch_result['clusters'].copy()
        embeddings = batch_result['embeddings']
        
        # Identificar outliers
        outlier_mask = clusters == -1
        n_outliers = np.sum(outlier_mask)
        total_outliers_original += n_outliers
        
        if n_outliers == 0:
            print(f"\nBatch {batch_id}: Sem outliers")
            reclassified_results.append({
                'batch_id': batch_id,
                'clusters_final': clusters,
                'n_reclassified': 0
            })
            continue
        
        print(f"\nBatch {batch_id}: {n_outliers} outliers a reclassificar...")
        
        # Embeddings dos outliers
        outlier_embeddings = embeddings[outlier_mask]
        
        # Calcular distâncias para todos os centroides merged
        distances = cdist(outlier_embeddings, merged_matrix, metric='cosine')
        
        # Para cada outlier, encontrar centroide mais próximo
        min_distances = np.min(distances, axis=1)
        closest_centroids = np.argmin(distances, axis=1)
        
        # Reclassificar se distância < threshold
        reclassify_mask = min_distances < CONFIG['OUTLIER_MAX_DISTANCE']
        n_reclassified = np.sum(reclassify_mask)
        
        # Atualizar clusters
        outlier_indices = np.where(outlier_mask)[0]
        for i, should_reclassify in enumerate(reclassify_mask):
            if should_reclassify:
                merged_cluster_id = merged_ids[closest_centroids[i]]
                clusters[outlier_indices[i]] = merged_cluster_id
        
        total_outliers_reclassified += n_reclassified
        
        print(f"  ✓ Reclassificados: {n_reclassified}/{n_outliers} ({100*n_reclassified/n_outliers:.1f}%)")
        
        reclassified_results.append({
            'batch_id': batch_id,
            'clusters_final': clusters,
            'n_reclassified': n_reclassified
        })
    
    print(f"\n{'='*60}")
    print(f"RESUMO DA RECLASSIFICAÇÃO")
    print(f"{'='*60}")
    print(f"Outliers originais: {total_outliers_original}")
    print(f"Outliers reclassificados: {total_outliers_reclassified}")
    print(f"Outliers finais: {total_outliers_original - total_outliers_reclassified}")
    print(f"Taxa de reclassificação: {100*total_outliers_reclassified/total_outliers_original:.1f}%")
    
    result = {
        'reclassified_results': reclassified_results,
        'total_outliers_original': total_outliers_original,
        'total_outliers_reclassified': total_outliers_reclassified
    }
    
    save_checkpoint(result, 'reclassification_results.pkl')
    return result

# ============================================================================
# ETAPA 4: GERAÇÃO DE RESULTADOS FINAIS
# ============================================================================

def generate_final_results(batch_results, reclassification_result, merged_centroids_result):
    """
    Gera arquivos finais com resultados consolidados
    """
    print("\n" + "="*60)
    print("ETAPA 4: GERAÇÃO DE RESULTADOS FINAIS")
    print("="*60)
    
    # Consolidar todos os dados
    all_data = []
    
    for batch_result in batch_results:
        batch_id = batch_result['batch_id']
        df = batch_result['df']
        
        # Buscar clusters finais reclassificados
        reclassified = next(r for r in reclassification_result['reclassified_results'] 
                           if r['batch_id'] == batch_id)
        
        df['cluster_final'] = reclassified['clusters_final']
        df['batch_id'] = batch_id
        
        all_data.append(df[['prod_xprod', 'cluster_final', 'batch_id']])
    
    # Concatenar tudo
    df_final = pd.concat(all_data, ignore_index=True)
    
    # Estatísticas finais
    print(f"\n→ Gerando estatísticas...")
    n_total = len(df_final)
    n_outliers_final = np.sum(df_final['cluster_final'] == -1)
    n_clustered = n_total - n_outliers_final
    unique_clusters = df_final[df_final['cluster_final'] != -1]['cluster_final'].nunique()
    
    print(f"\n{'='*60}")
    print(f"ESTATÍSTICAS FINAIS")
    print(f"{'='*60}")
    print(f"Total de registros: {n_total:,}")
    print(f"Registros clusterizados: {n_clustered:,} ({100*n_clustered/n_total:.1f}%)")
    print(f"Outliers finais: {n_outliers_final:,} ({100*n_outliers_final/n_total:.1f}%)")
    print(f"Número de clusters finais: {unique_clusters}")
    print(f"Tamanho médio dos clusters: {n_clustered/unique_clusters:.1f}")
    
    # Salvar resultado principal
    output_file = os.path.join(CONFIG['OUTPUT_DIR'], 'resultado_final_clusters.csv')
    df_final.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ Arquivo principal salvo: resultado_final_clusters.csv")
    
    # Gerar resumo dos clusters para rotulagem
    print(f"\n→ Gerando resumo para rotulagem...")
    cluster_summary = []
    
    merged_samples = merged_centroids_result['merged_samples']
    merged_sizes = merged_centroids_result['merged_sizes']
    
    for cluster_id in sorted(merged_samples.keys()):
        if cluster_id == -1:
            continue
            
        size = merged_sizes.get(cluster_id, 0)
        samples = merged_samples.get(cluster_id, [])
        
        cluster_summary.append({
            'cluster_id': cluster_id,
            'tamanho': size,
            'exemplos': ' | '.join(samples[:5])
        })
    
    df_summary = pd.DataFrame(cluster_summary)
    df_summary = df_summary.sort_values('tamanho', ascending=False)
    
    summary_file = os.path.join(CONFIG['OUTPUT_DIR'], 'resumo_clusters_rotulagem.csv')
    df_summary.to_csv(summary_file, index=False, encoding='utf-8-sig')
    print(f"✓ Resumo para rotulagem salvo: resumo_clusters_rotulagem.csv")
    
    # Distribuição dos top 20 clusters
    print(f"\n{'='*60}")
    print("TOP 20 MAIORES CLUSTERS")
    print(f"{'='*60}")
    top_clusters = df_final[df_final['cluster_final'] != -1]['cluster_final'].value_counts().head(20)
    for cluster_id, count in top_clusters.items():
        print(f"Cluster {cluster_id:3d}: {count:6,} itens ({100*count/n_total:5.2f}%)")
    
    print(f"\n{'='*60}")
    print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"{'='*60}")
    print(f"\nArquivos gerados em: {CONFIG['OUTPUT_DIR']}/")
    print(f"  - resultado_final_clusters.csv (todos os registros)")
    print(f"  - resumo_clusters_rotulagem.csv (clusters para rotular)")
    
    return df_final, df_summary

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """
    Executa todo o pipeline
    """
    start_time = datetime.now()
    print("\n" + "="*60)
    print("HDBSCAN HIERÁRQUICO EM BATCHES")
    print("Sistema de Classificação NCM Capítulo 44")
    print("="*60)
    print(f"Início: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    setup_output_dir()
    
    # ETAPA 1: Processar batches
    print("\n→ Iniciando Etapa 1...")
    batch_results = load_checkpoint('all_batches_results.pkl')
    if batch_results is None:
        batch_results = run_batch_processing()
    else:
        print("✓ Etapa 1 já concluída (checkpoint encontrado)")
    
    # ETAPA 2: Merge de centroides
    print("\n→ Iniciando Etapa 2...")
    merged_centroids_result = load_checkpoint('merged_centroids.pkl')
    if merged_centroids_result is None:
        merged_centroids_result = merge_centroids(batch_results)
    else:
        print("✓ Etapa 2 já concluída (checkpoint encontrado)")
    
    # ETAPA 3: Reclassificar outliers
    print("\n→ Iniciando Etapa 3...")
    reclassification_result = load_checkpoint('reclassification_results.pkl')
    if reclassification_result is None:
        reclassification_result = reclassify_outliers(batch_results, merged_centroids_result)
    else:
        print("✓ Etapa 3 já concluída (checkpoint encontrado)")
    
    # ETAPA 4: Gerar resultados finais
    print("\n→ Iniciando Etapa 4...")
    df_final, df_summary = generate_final_results(
        batch_results,
        reclassification_result,
        merged_centroids_result
    )
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print(f"Término: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duração total: {duration}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
