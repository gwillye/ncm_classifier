"""
Análise e Visualização dos Resultados do HDBSCAN Hierárquico
Gera estatísticas, gráficos e relatórios para análise dos clusters
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

class ClusterAnalyzer:
    """
    Classe para análise detalhada dos resultados de clustering
    """
    
    def __init__(self, clusters_file='hdbscan_results/resultado_final_clusters.csv',
                 summary_file='hdbscan_results/resumo_clusters_rotulagem.csv'):
        """
        Inicializa o analisador
        
        Args:
            clusters_file: Arquivo com resultados completos
            summary_file: Arquivo com resumo dos clusters
        """
        print("Carregando resultados...")
        self.df = pd.read_csv(clusters_file)
        self.summary = pd.read_csv(summary_file)
        
        print(f"✓ {len(self.df):,} registros carregados")
        print(f"✓ {len(self.summary)} clusters identificados")
    
    def general_statistics(self):
        """
        Estatísticas gerais do clustering
        """
        print("\n" + "="*70)
        print("ESTATÍSTICAS GERAIS")
        print("="*70)
        
        total = len(self.df)
        outliers = len(self.df[self.df['cluster_final'] == -1])
        clustered = total - outliers
        n_clusters = self.df[self.df['cluster_final'] != -1]['cluster_final'].nunique()
        
        print(f"\nTotal de registros: {total:,}")
        print(f"Registros clusterizados: {clustered:,} ({100*clustered/total:.2f}%)")
        print(f"Outliers: {outliers:,} ({100*outliers/total:.2f}%)")
        print(f"Número de clusters: {n_clusters}")
        print(f"Tamanho médio dos clusters: {clustered/n_clusters:.1f}")
        
        # Distribuição de tamanhos
        cluster_sizes = self.df[self.df['cluster_final'] != -1]['cluster_final'].value_counts()
        
        print(f"\nDistribuição de tamanhos:")
        print(f"  Menor cluster: {cluster_sizes.min():,} itens")
        print(f"  Maior cluster: {cluster_sizes.max():,} itens")
        print(f"  Mediana: {cluster_sizes.median():.0f} itens")
        print(f"  Desvio padrão: {cluster_sizes.std():.1f}")
        
        # Percentis
        print(f"\nPercentis de tamanho:")
        for p in [25, 50, 75, 90, 95, 99]:
            val = cluster_sizes.quantile(p/100)
            print(f"  {p}%: {val:.0f} itens")
        
        return {
            'total': total,
            'clustered': clustered,
            'outliers': outliers,
            'n_clusters': n_clusters,
            'cluster_sizes': cluster_sizes
        }
    
    def top_clusters_analysis(self, top_n=20):
        """
        Análise dos maiores clusters
        """
        print("\n" + "="*70)
        print(f"TOP {top_n} MAIORES CLUSTERS")
        print("="*70)
        
        cluster_sizes = self.df[self.df['cluster_final'] != -1]['cluster_final'].value_counts().head(top_n)
        
        total_clustered = len(self.df[self.df['cluster_final'] != -1])
        
        print(f"\n{'Cluster':<10} {'Tamanho':>10} {'% do Total':>12} {'Exemplos'}")
        print("-" * 70)
        
        for cluster_id, size in cluster_sizes.items():
            pct = 100 * size / total_clustered
            
            # Buscar exemplos
            samples = self.df[self.df['cluster_final'] == cluster_id]['prod_xprod'].head(3).tolist()
            sample_str = samples[0][:40] if samples else "N/A"
            
            print(f"{cluster_id:<10} {size:>10,} {pct:>11.2f}% {sample_str}")
        
        # Concentração
        top_10_total = cluster_sizes.head(10).sum()
        concentration = 100 * top_10_total / total_clustered
        
        print(f"\n{'='*70}")
        print(f"Top 10 clusters representam {concentration:.2f}% dos registros clusterizados")
        
        return cluster_sizes
    
    def cluster_detail(self, cluster_id, n_samples=20):
        """
        Análise detalhada de um cluster específico
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISE DETALHADA - CLUSTER {cluster_id}")
        print("="*70)
        
        cluster_data = self.df[self.df['cluster_final'] == cluster_id]
        
        if len(cluster_data) == 0:
            print(f"✗ Cluster {cluster_id} não encontrado!")
            return None
        
        print(f"\nTamanho: {len(cluster_data):,} itens")
        
        # Amostras
        print(f"\nAmostras ({min(n_samples, len(cluster_data))} primeiros):")
        print("-" * 70)
        for i, prod in enumerate(cluster_data['prod_xprod'].head(n_samples), 1):
            print(f"{i:2d}. {prod}")
        
        # Análise de palavras
        all_text = ' '.join(cluster_data['prod_xprod'].astype(str).tolist())
        words = re.findall(r'\b\w+\b', all_text.upper())
        word_freq = Counter(words)
        
        # Remover stopwords comuns
        stopwords = {'DE', 'E', 'A', 'O', 'EM', 'COM', 'PARA', 'DA', 'DO', 'NA', 'NO'}
        word_freq = {w: c for w, c in word_freq.items() if w not in stopwords and len(w) > 2}
        
        print(f"\nPalavras mais frequentes:")
        print("-" * 70)
        for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:15]:
            pct = 100 * count / len(cluster_data)
            print(f"  {word:<20} {count:>6} vezes ({pct:>5.1f}% dos itens)")
        
        return cluster_data
    
    def outliers_analysis(self, n_samples=50):
        """
        Análise dos outliers
        """
        print("\n" + "="*70)
        print("ANÁLISE DE OUTLIERS")
        print("="*70)
        
        outliers = self.df[self.df['cluster_final'] == -1]
        
        print(f"\nTotal de outliers: {len(outliers):,}")
        print(f"Percentual do total: {100*len(outliers)/len(self.df):.2f}%")
        
        if len(outliers) == 0:
            print("✓ Nenhum outlier encontrado!")
            return None
        
        print(f"\nAmostras de outliers ({min(n_samples, len(outliers))} primeiros):")
        print("-" * 70)
        for i, prod in enumerate(outliers['prod_xprod'].head(n_samples), 1):
            print(f"{i:2d}. {prod}")
        
        # Análise de comprimento
        outliers['text_len'] = outliers['prod_xprod'].astype(str).str.len()
        
        print(f"\nCaracterísticas dos outliers:")
        print(f"  Comprimento médio: {outliers['text_len'].mean():.1f} caracteres")
        print(f"  Comprimento mediano: {outliers['text_len'].median():.0f} caracteres")
        
        return outliers
    
    def generate_wordcloud(self, cluster_id=None, save_path='wordcloud.png'):
        """
        Gera wordcloud para um cluster ou para todos os dados
        """
        if cluster_id is None:
            print("\nGerando wordcloud de todos os dados...")
            text_data = self.df['prod_xprod'].astype(str).tolist()
        else:
            print(f"\nGerando wordcloud do cluster {cluster_id}...")
            text_data = self.df[self.df['cluster_final'] == cluster_id]['prod_xprod'].astype(str).tolist()
        
        text = ' '.join(text_data)
        
        # Limpar texto
        text = re.sub(r'[^\w\s]', ' ', text.upper())
        text = re.sub(r'\d+', '', text)
        
        # Stopwords em português
        stopwords = set([
            'DE', 'E', 'A', 'O', 'EM', 'COM', 'PARA', 'DA', 'DO', 'NA', 'NO',
            'DAS', 'DOS', 'AO', 'UM', 'UMA', 'OS', 'AS', 'POR', 'SEM', 'PELO'
        ])
        
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            stopwords=stopwords,
            max_words=100,
            colormap='viridis'
        ).generate(text)
        
        plt.figure(figsize=(16, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Wordcloud - {"Todos os dados" if cluster_id is None else f"Cluster {cluster_id}"}', 
                  fontsize=16, pad=20)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Wordcloud salvo em: {save_path}")
        plt.close()
    
    def plot_cluster_distribution(self, top_n=30, save_path='cluster_distribution.png'):
        """
        Plota distribuição dos tamanhos dos clusters
        """
        print("\nGerando gráfico de distribuição...")
        
        cluster_sizes = self.df[self.df['cluster_final'] != -1]['cluster_final'].value_counts().head(top_n)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Gráfico de barras
        cluster_sizes.plot(kind='bar', ax=ax1, color='steelblue')
        ax1.set_xlabel('Cluster ID', fontsize=12)
        ax1.set_ylabel('Número de Itens', fontsize=12)
        ax1.set_title(f'Top {top_n} Maiores Clusters', fontsize=14, pad=15)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(axis='y', alpha=0.3)
        
        # Histograma de tamanhos
        all_sizes = self.df[self.df['cluster_final'] != -1]['cluster_final'].value_counts()
        ax2.hist(all_sizes, bins=50, color='coral', edgecolor='black', alpha=0.7)
        ax2.set_xlabel('Tamanho do Cluster', fontsize=12)
        ax2.set_ylabel('Frequência', fontsize=12)
        ax2.set_title('Distribuição de Tamanhos dos Clusters', fontsize=14, pad=15)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Gráfico salvo em: {save_path}")
        plt.close()
    
    def export_clusters_for_labeling(self, output_file='clusters_para_rotular_detalhado.xlsx'):
        """
        Exporta arquivo Excel formatado para rotulagem manual
        """
        print("\nGerando arquivo para rotulagem...")
        
        # Preparar dados
        export_data = []
        
        for cluster_id in self.summary['cluster_id']:
            cluster_data = self.df[self.df['cluster_final'] == cluster_id]
            
            # Amostrar até 10 exemplos
            samples = cluster_data['prod_xprod'].head(10).tolist()
            
            export_data.append({
                'cluster_id': cluster_id,
                'tamanho': len(cluster_data),
                'exemplo_1': samples[0] if len(samples) > 0 else '',
                'exemplo_2': samples[1] if len(samples) > 1 else '',
                'exemplo_3': samples[2] if len(samples) > 2 else '',
                'exemplo_4': samples[3] if len(samples) > 3 else '',
                'exemplo_5': samples[4] if len(samples) > 4 else '',
                'rotulo_cap44': '',  # Para preenchimento manual
                'observacoes': ''    # Para preenchimento manual
            })
        
        df_export = pd.DataFrame(export_data)
        df_export = df_export.sort_values('tamanho', ascending=False)
        
        # Salvar como Excel
        df_export.to_excel(output_file, index=False, sheet_name='Clusters')
        
        print(f"✓ Arquivo salvo: {output_file}")
        print(f"  {len(df_export)} clusters para rotular")
        print(f"\nInstruções:")
        print(f"  1. Abra o arquivo no Excel")
        print(f"  2. Analise os exemplos de cada cluster")
        print(f"  3. Preencha 'rotulo_cap44' com: SIM, NÃO ou DÚVIDA")
        print(f"  4. Adicione observações se necessário")
    
    def compare_batches(self):
        """
        Compara distribuição de clusters entre batches
        """
        print("\n" + "="*70)
        print("COMPARAÇÃO ENTRE BATCHES")
        print("="*70)
        
        batch_stats = []
        
        for batch_id in sorted(self.df['batch_id'].unique()):
            batch_data = self.df[self.df['batch_id'] == batch_id]
            
            total = len(batch_data)
            outliers = len(batch_data[batch_data['cluster_final'] == -1])
            clustered = total - outliers
            n_clusters = batch_data[batch_data['cluster_final'] != -1]['cluster_final'].nunique()
            
            batch_stats.append({
                'batch': batch_id,
                'total': total,
                'clusterizados': clustered,
                'outliers': outliers,
                'n_clusters': n_clusters,
                'pct_clusterizado': 100 * clustered / total if total > 0 else 0
            })
        
        df_batches = pd.DataFrame(batch_stats)
        
        print(f"\n{'Batch':<8} {'Total':>10} {'Clusterizados':>15} {'Outliers':>10} {'N Clusters':>12} {'% Clust.':>10}")
        print("-" * 70)
        
        for _, row in df_batches.iterrows():
            print(f"{row['batch']:<8} {row['total']:>10,} {row['clusterizados']:>15,} "
                  f"{row['outliers']:>10,} {row['n_clusters']:>12} {row['pct_clusterizado']:>9.1f}%")
        
        print(f"\n{'='*70}")
        print(f"Média de clusterização: {df_batches['pct_clusterizado'].mean():.2f}%")
        print(f"Desvio padrão: {df_batches['pct_clusterizado'].std():.2f}%")
        
        return df_batches

def main():
    """
    Executa análise completa
    """
    print("="*70)
    print("ANÁLISE DE RESULTADOS - HDBSCAN HIERÁRQUICO")
    print("="*70)
    
    try:
        analyzer = ClusterAnalyzer()
    except FileNotFoundError as e:
        print(f"\n✗ ERRO: Arquivo não encontrado!")
        print(f"  {str(e)}")
        print(f"\nCertifique-se de que o processamento foi concluído.")
        return
    
    # 1. Estatísticas gerais
    stats = analyzer.general_statistics()
    
    # 2. Top clusters
    top_clusters = analyzer.top_clusters_analysis(top_n=20)
    
    # 3. Análise de outliers
    outliers = analyzer.outliers_analysis(n_samples=30)
    
    # 4. Comparação entre batches
    batch_comparison = analyzer.compare_batches()
    
    # 5. Detalhes de clusters específicos (top 3)
    print("\n" + "="*70)
    print("ANÁLISE DETALHADA DOS TOP 3 CLUSTERS")
    print("="*70)
    for cluster_id in top_clusters.head(3).index:
        analyzer.cluster_detail(cluster_id, n_samples=10)
    
    # 6. Gerar visualizações
    print("\n" + "="*70)
    print("GERANDO VISUALIZAÇÕES")
    print("="*70)
    
    try:
        analyzer.plot_cluster_distribution(top_n=30, save_path='cluster_distribution.png')
    except Exception as e:
        print(f"⚠ Não foi possível gerar gráfico: {e}")
    
    try:
        analyzer.generate_wordcloud(save_path='wordcloud_all.png')
        # Wordcloud do maior cluster
        top_cluster = top_clusters.index[0]
        analyzer.generate_wordcloud(cluster_id=top_cluster, 
                                   save_path=f'wordcloud_cluster_{top_cluster}.png')
    except Exception as e:
        print(f"⚠ Não foi possível gerar wordcloud: {e}")
    
    # 7. Exportar para rotulagem
    try:
        analyzer.export_clusters_for_labeling('clusters_para_rotular_detalhado.xlsx')
    except Exception as e:
        print(f"⚠ Não foi possível exportar Excel: {e}")
        print(f"  Certifique-se de ter instalado: pip install openpyxl")
    
    print("\n" + "="*70)
    print("ANÁLISE CONCLUÍDA!")
    print("="*70)
    print("\nArquivos gerados:")
    print("  - cluster_distribution.png")
    print("  - wordcloud_all.png")
    print("  - wordcloud_cluster_X.png")
    print("  - clusters_para_rotular_detalhado.xlsx")

if __name__ == "__main__":
    main()
