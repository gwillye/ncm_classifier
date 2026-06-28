"""
Identificação Automática de Clusters do Capítulo 44
Usa palavras-chave para sugerir quais clusters pertencem ao Cap 44
"""

import pandas as pd
import re
from collections import Counter

# Palavras-chave do Capítulo 44 (Madeira e suas obras)
KEYWORDS_CAP44 = [
    'MADEIRA', 'COMPENSADO', 'COMPENSADA', 'LAMINADO', 'LAMINADA',
    'MDF', 'AGLOMERADO', 'AGLOMERADA', 'OSB',
    'PAINEL', 'CHAPA',
    'PORTA', 'PORTAO', 'JANELA', 'BATENTE',
    'TABUA', 'SARRAFO', 'RIPA', 'CAIBRO', 'VIGA',
    'PISO', 'ASSOALHO', 'DECK',
    'MOVEL', 'ARMARIO', 'ESTANTE', 'RACK', 'MESA', 'CADEIRA',
    'MOLDURA', 'RODAPE', 'ESQUADRIA',
    'LENHA', 'CARVAO', 'CAVACO',
    'COMPENSAD', 'MADEIRITE',
    'EUCALIPTO', 'PINUS', 'PEROBA', 'MOGNO', 'CEDRO', 'TECA',
    'NAVAL', 'RESINADO', 'PLASTIFICAD',
]

# Palavras que EXCLUEM do Cap 44
EXCLUDE_KEYWORDS = [
    'PLASTICO', 'PLASTICA', 'PVC', 'VINIL',
    'METAL', 'METALICO', 'FERRO', 'ACO', 'ALUMINIO',
    'VIDRO',
    'CONCRETO', 'CIMENTO', 'ARGAMASSA',
    'CERAMICA', 'PORCELANATO',
    'TECIDO', 'TEXTIL',
]

def calculate_cap44_score(text):
    """
    Calcula score de pertencimento ao Cap 44
    Retorna: (score, keywords_found, exclude_found)
    """
    text_upper = str(text).upper()
    
    # Contar keywords do Cap 44
    keywords_found = []
    for keyword in KEYWORDS_CAP44:
        if keyword in text_upper:
            keywords_found.append(keyword)
    
    # Contar keywords de exclusão
    exclude_found = []
    for keyword in EXCLUDE_KEYWORDS:
        if keyword in text_upper:
            exclude_found.append(keyword)
    
    # Score = keywords encontradas - exclusões
    score = len(keywords_found) - (len(exclude_found) * 2)  # Exclusões pesam mais
    
    return score, keywords_found, exclude_found

print("Carregando resultados...")
df_summary = pd.read_csv('hdbscan_results_pca/resumo_clusters_rotulagem.csv')
df_full = pd.read_csv('hdbscan_results_pca/resultado_final_clusters.csv')

print("Analisando clusters...")

cluster_analysis = []

for _, row in df_summary.iterrows():
    cluster_id = row['cluster_id']
    tamanho = row['tamanho']
    exemplos = row['exemplos']
    
    # Analisar exemplos
    score, keywords, excludes = calculate_cap44_score(exemplos)
    
    # Classificação automática
    if score >= 2 and len(excludes) == 0:
        classificacao = 'PROVÁVEL CAP 44'
    elif score >= 1 and len(excludes) == 0:
        classificacao = 'POSSÍVEL CAP 44'
    elif len(excludes) > 0:
        classificacao = 'PROVÁVEL OUTRO'
    else:
        classificacao = 'REVISAR MANUALMENTE'
    
    cluster_analysis.append({
        'cluster_id': cluster_id,
        'tamanho': tamanho,
        'score': score,
        'classificacao': classificacao,
        'keywords_encontradas': ', '.join(keywords[:5]),  # Primeiras 5
        'excludes_encontradas': ', '.join(excludes),
        'exemplos': exemplos[:100]
    })

df_analysis = pd.DataFrame(cluster_analysis)
df_analysis = df_analysis.sort_values(['classificacao', 'tamanho'], ascending=[True, False])

# Estatísticas
print(f"\n{'='*80}")
print("CLASSIFICAÇÃO AUTOMÁTICA DOS CLUSTERS")
print(f"{'='*80}")

stats = df_analysis['classificacao'].value_counts()
stats_size = df_analysis.groupby('classificacao')['tamanho'].sum()

print("\nDistribuição por classificação:")
for classificacao in ['PROVÁVEL CAP 44', 'POSSÍVEL CAP 44', 'REVISAR MANUALMENTE', 'PROVÁVEL OUTRO']:
    if classificacao in stats.index:
        n_clusters = stats[classificacao]
        n_itens = stats_size[classificacao]
        pct = 100 * n_itens / df_full.shape[0]
        print(f"  {classificacao:<25}: {n_clusters:>5} clusters, {n_itens:>10,} itens ({pct:>5.2f}%)")

# Salvar análise
output_file = 'hdbscan_results_pca/analise_cap44_automatica.csv'
df_analysis.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✓ Análise salva em: {output_file}")

# Mostrar top clusters do Cap 44
print(f"\n{'='*80}")
print("TOP 30 CLUSTERS - PROVÁVEL CAP 44")
print(f"{'='*80}")

cap44_clusters = df_analysis[df_analysis['classificacao'] == 'PROVÁVEL CAP 44'].head(30)

if len(cap44_clusters) > 0:
    print(f"\n{'Cluster':<10} {'Tamanho':>10} {'Score':>7} {'Keywords':<30} {'Exemplos'}")
    print("-" * 100)
    
    for _, row in cap44_clusters.iterrows():
        print(f"{row['cluster_id']:<10} {row['tamanho']:>10,} {row['score']:>7} "
              f"{row['keywords_encontradas'][:30]:<30} {row['exemplos'][:40]}")
else:
    print("\n⚠ Nenhum cluster classificado como 'PROVÁVEL CAP 44'")

# Mostrar clusters para revisão manual
print(f"\n{'='*80}")
print("TOP 20 CLUSTERS - REVISAR MANUALMENTE")
print(f"{'='*80}")

revisar = df_analysis[df_analysis['classificacao'] == 'REVISAR MANUALMENTE'].head(20)

if len(revisar) > 0:
    print(f"\n{'Cluster':<10} {'Tamanho':>10} {'Exemplos'}")
    print("-" * 80)
    
    for _, row in revisar.iterrows():
        print(f"{row['cluster_id']:<10} {row['tamanho']:>10,} {row['exemplos'][:60]}")

# Resumo final
print(f"\n{'='*80}")
print("RESUMO PARA ROTULAGEM")
print(f"{'='*80}")

total_clusters = len(df_analysis)
cap44_auto = len(df_analysis[df_analysis['classificacao'].str.contains('CAP 44')])
revisar_manual = len(df_analysis[df_analysis['classificacao'] == 'REVISAR MANUALMENTE'])

print(f"\nTotal de clusters: {total_clusters:,}")
print(f"Identificados automaticamente como Cap 44: {cap44_auto:,} ({100*cap44_auto/total_clusters:.1f}%)")
print(f"Precisam de revisão manual: {revisar_manual:,} ({100*revisar_manual/total_clusters:.1f}%)")

print(f"\n✓ Próximos passos:")
print(f"  1. Revise o arquivo: {output_file}")
print(f"  2. Valide os clusters 'PROVÁVEL CAP 44' manualmente")
print(f"  3. Analise os clusters 'REVISAR MANUALMENTE'")
print(f"  4. Use quick_analysis.py para ver detalhes de clusters específicos")
