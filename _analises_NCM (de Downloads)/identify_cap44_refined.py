"""
Identificação Automática de Clusters do Capítulo 44
VERSÃO REFINADA - Usa estrutura de regex validada
"""

import pandas as pd
import re
from collections import Counter

# ============================================================================
# ESTRUTURA DE REGEX VALIDADA (baseada no sistema atual)
# ============================================================================

# Termos de exclusão para as regras complexas
termos_excl_janela = 'ALUMINIO|FERRO|METAL|INOX|PVC|VIDRO|BLINDEX|FUME|ACRILICO|PLASTICO|APLIQUE|RECORTE|LASER|MINIATURA|BONECA|POLLY|BRINQUEDO|ARTESANATO|ENFEITE|DECORACAO|FERRAGEM|FECHADURA|DOBRADICA|TRILHO|PUXADOR|CREMONA|ESPUMA|PU|VEDACAO|IMA|GELADEIRA|CORTINA|PERSIANA|TELA|MOSQUITEIRO|ADESIVO|LIMPEZA|PET|GATO|CACHORRO|ALIMENTADOR|ALBUM|FOTO|FICHARIO|HARD CASE|BAMBU|GIRASSOL|VASO|FLOR|PASSARO|CENARIO|ALTAR|CAPELA|ESPELHO|BASTIDOR|CACHEPO|PORTA RETRATO|JOIA|PRESENTE|ORGANIZADOR|TAMPO|FOGAO|MESA|CADEIRA'
termos_excl_carvao = 'ATIVADO|ATIVO|MINERAL|ANTRACIT|COQUE|HULHA|LINHITA|TURFA|FILTRO|MASCARA|SHAMPOO|SABONETE|CAPSULA|COMPRIMIDO|DENTIFRICO|PASTA DE DENTE'
termos_excl_palete = 'LOCACAO|REFORMA|ALUGUEL|CONSERTO|FRETE|MANUTENCAO|REPARO'
termos_excl_mdf = 'ARMARIO|ESTANTE|GAVETEIRO|MESA|CADEIRA|BALCAO|CRIADO|GUARDA ROUPA'
termos_ambiguos_exclusao = 'PLANEJADA|PLANEJADOS|COZINHA|DALMOBILE|EIXO|GUINDASTE|ELEVADOR|AUTOMATIC|ELETROMECANICO|ELETROHIDRAULICO|VW|DEERE|JOHN|CABINES|BOVINA|BOVINOS|CONTENCAO|PESCOCEIRAS|COIMMA|CAPUCCINO|FAVOS|IMPRESSO'
termos_ambiguos_inclusao = 'CABO|CABOS|FOLHA|FERRAMENTAS'

# Categorias REGEX (ordem importa!)
categorias_regex = [
    ('ROTULADOS ANTES', r'(LENHA|TORA DE MADEIRA|MADEIRA CERRADA|CABO DE MADEIRA|ARTIGO DOMESTICO DE MADEIRA|CARVAO VEGETAL|PORTA-BATENTE DE MADEIRA|PALITO DE DENTE|PALLET-EMBALAGEM DE MADEIRA|CHAPAS DE MDF|CHAPAS DE COMPENSADO|CHAPAS DE TAPUME|RESIDUO DE MADEIRA)', True),
    ('OUTLIER__MAQUINAS', r'(PICADOR|TRATOR|COLHEITADEIRA|MÁQUINA|MAQUINA|VEÍCULO|VEICULO|PICADOR FLORESTAL)', False),
    ('44.18.JANELA_MADEIRA', rf'^(?=.*JANELA)(?!.*({termos_excl_janela})).*', True),
    ('44.02.CARVAO_VEGETAL', rf'^(?=.*(CARVÃO|CARVAO|MOINHA))(?!.*({termos_excl_carvao})).*', True),
    ('44.21.PALETE_PALLET', rf'^(?=.*(PALETE|PALLET))(?!.*({termos_excl_palete})).*', True),
    ('44.11.MDF_PAINEL', rf'^(?=.*(MDF|MDP|OSB|CHAPATEX|HDF))(?!.*({termos_excl_mdf})).*', True),
    ('AMBIGUOS_EXCLUSAO', rf'.*({termos_ambiguos_exclusao}).*', False),
    ('NOMES_AMBÍGUOS', rf'^(?=.*({termos_ambiguos_inclusao}))(?=.*(MADEIRA|MDF|MDP|PINUS|MM|X)).*', True),
    ('44.03.MADEIRA_BRUTA', r'(MADEIRA.*(BRUTA|TORA|CELULOSE)|EUCALIPTO.*(TORA|CELULOSE)|PINUS.*BRUTA)', True),
    ('44.18.FOLHA_PORTA', r'(FOLHA DE PORTA|PORTA|BATENTE|CAIXILHO|FORRO|SOALHO|PISO|ASSOALHO)', True),
    ('44.01.CAVACO_RESIDUO', r'(CAVACO DE EUCALIPTO|LENHA|CAVACO|RESIDUO|GRANULADO|BIOMASSA|SERRAGEM|PO DE MADEIRA)', True),
    ('44.21.OUTRAS_OBRAS', r'(PALITO|CEPO|ESTRADO|CAIXOTE)', True),
]

def classify_text(text):
    """
    Classifica um texto usando as regras regex
    Retorna: (categoria, is_cap44)
    """
    text_upper = str(text).upper()
    
    for categoria, pattern, is_cap44 in categorias_regex:
        if re.search(pattern, text_upper):
            return categoria, is_cap44
    
    return 'OUTROS', None  # Não classificado

def analyze_cluster_samples(exemplos_text, num_samples=50):
    """
    Analisa múltiplos exemplos de um cluster para classificação robusta
    Retorna: (classificacao_final, categoria_mais_comum, confianca, detalhes)
    """
    # Dividir exemplos (separados por |)
    samples = [s.strip() for s in exemplos_text.split('|') if s.strip()]
    
    if not samples:
        return 'INDEFINIDO', 'OUTROS', 0.0, {}
    
    # Classificar cada amostra
    classifications = []
    for sample in samples[:num_samples]:
        categoria, is_cap44 = classify_text(sample)
        classifications.append((categoria, is_cap44))
    
    # Contar classificações
    cat_counter = Counter([c[0] for c in classifications])
    cap44_counter = Counter([c[1] for c in classifications])
    
    # Categoria mais comum
    categoria_mais_comum = cat_counter.most_common(1)[0][0]
    freq_categoria = cat_counter[categoria_mais_comum]
    
    # Classificação Cap 44
    total = len(classifications)
    cap44_true = cap44_counter.get(True, 0)
    cap44_false = cap44_counter.get(False, 0)
    cap44_none = cap44_counter.get(None, 0)
    
    # Confiança (% da categoria mais comum)
    confianca = freq_categoria / total
    
    # Decisão final
    if categoria_mais_comum in ['OUTLIER__MAQUINAS', 'AMBIGUOS_EXCLUSAO']:
        classificacao_final = 'NÃO É CAP 44'
    elif cap44_true > cap44_false and cap44_true > cap44_none:
        # Maioria é Cap 44
        if confianca >= 0.7:
            classificacao_final = 'CAP 44 - ALTA CONFIANÇA'
        elif confianca >= 0.5:
            classificacao_final = 'CAP 44 - MÉDIA CONFIANÇA'
        else:
            classificacao_final = 'CAP 44 - BAIXA CONFIANÇA'
    elif cap44_false > cap44_true:
        classificacao_final = 'NÃO É CAP 44'
    else:
        classificacao_final = 'REVISAR MANUALMENTE'
    
    detalhes = {
        'total_samples': total,
        'cap44_samples': cap44_true,
        'nao_cap44_samples': cap44_false,
        'indefinidos': cap44_none,
        'categorias': dict(cat_counter),
        'confianca': confianca
    }
    
    return classificacao_final, categoria_mais_comum, confianca, detalhes

# ============================================================================
# PROCESSAMENTO PRINCIPAL
# ============================================================================

print("Carregando resultados...")
df_summary = pd.read_csv('hdbscan_results_pca/resumo_clusters_rotulagem.csv')
df_full = pd.read_csv('hdbscan_results_pca/resultado_final_clusters.csv')

print(f"Analisando {len(df_summary)} clusters...")

cluster_analysis = []

for idx, row in df_summary.iterrows():
    if idx % 500 == 0:
        print(f"  Processando cluster {idx}/{len(df_summary)}...")
    
    cluster_id = row['cluster_id']
    tamanho = row['tamanho']
    exemplos = row['exemplos']
    
    # Analisar cluster
    classificacao, categoria, confianca, detalhes = analyze_cluster_samples(exemplos)
    
    cluster_analysis.append({
        'cluster_id': cluster_id,
        'tamanho': tamanho,
        'classificacao': classificacao,
        'categoria_principal': categoria,
        'confianca': f"{confianca:.2%}",
        'amostras_cap44': detalhes['cap44_samples'],
        'amostras_nao_cap44': detalhes['nao_cap44_samples'],
        'amostras_indefinidas': detalhes['indefinidos'],
        'exemplos': exemplos[:150]
    })

df_analysis = pd.DataFrame(cluster_analysis)

# Ordenar por classificação e tamanho
ordem_classificacao = {
    'CAP 44 - ALTA CONFIANÇA': 1,
    'CAP 44 - MÉDIA CONFIANÇA': 2,
    'CAP 44 - BAIXA CONFIANÇA': 3,
    'REVISAR MANUALMENTE': 4,
    'NÃO É CAP 44': 5,
    'INDEFINIDO': 6
}

df_analysis['ordem'] = df_analysis['classificacao'].map(ordem_classificacao)
df_analysis = df_analysis.sort_values(['ordem', 'tamanho'], ascending=[True, False])
df_analysis = df_analysis.drop('ordem', axis=1)

# ============================================================================
# ESTATÍSTICAS E RELATÓRIOS
# ============================================================================

print(f"\n{'='*100}")
print("CLASSIFICAÇÃO AUTOMÁTICA DOS CLUSTERS (Usando Regex Validadas)")
print(f"{'='*100}")

# Estatísticas gerais
stats = df_analysis['classificacao'].value_counts()
stats_size = df_analysis.groupby('classificacao')['tamanho'].sum()
total_registros = df_full.shape[0]

print("\n📊 DISTRIBUIÇÃO POR CLASSIFICAÇÃO:")
print(f"{'─'*100}")
print(f"{'Classificação':<30} {'Clusters':>10} {'Itens':>15} {'% Total':>10}")
print(f"{'─'*100}")

for classificacao in ordem_classificacao.keys():
    if classificacao in stats.index:
        n_clusters = stats[classificacao]
        n_itens = stats_size[classificacao]
        pct = 100 * n_itens / total_registros
        print(f"{classificacao:<30} {n_clusters:>10,} {n_itens:>15,} {pct:>9.2f}%")

print(f"{'─'*100}")
print(f"{'TOTAL':<30} {len(df_analysis):>10,} {stats_size.sum():>15,} {100:>9.1f}%")

# Estatísticas por categoria NCM
print(f"\n\n📋 DISTRIBUIÇÃO POR CATEGORIA NCM:")
print(f"{'─'*100}")
print(f"{'Categoria':<30} {'Clusters':>10} {'Itens':>15} {'% Total':>10}")
print(f"{'─'*100}")

cat_stats = df_analysis['categoria_principal'].value_counts()
cat_stats_size = df_analysis.groupby('categoria_principal')['tamanho'].sum()

for categoria in cat_stats.index[:20]:  # Top 20 categorias
    n_clusters = cat_stats[categoria]
    n_itens = cat_stats_size[categoria]
    pct = 100 * n_itens / total_registros
    print(f"{categoria:<30} {n_clusters:>10,} {n_itens:>15,} {pct:>9.2f}%")

# Salvar análise completa
output_file = 'hdbscan_results_pca/analise_cap44_regex.csv'
df_analysis.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n✅ Análise completa salva em: {output_file}")

# ============================================================================
# RELATÓRIO DETALHADO - CAP 44 ALTA CONFIANÇA
# ============================================================================

print(f"\n\n{'='*100}")
print("🎯 TOP 30 CLUSTERS - CAP 44 ALTA CONFIANÇA")
print(f"{'='*100}")

cap44_alta = df_analysis[df_analysis['classificacao'] == 'CAP 44 - ALTA CONFIANÇA'].head(30)

if len(cap44_alta) > 0:
    print(f"\n{'Cluster':<10} {'Tamanho':>10} {'Categoria':<25} {'Conf':>6} {'Exemplos'}")
    print("─" * 100)
    
    for _, row in cap44_alta.iterrows():
        print(f"{row['cluster_id']:<10} {row['tamanho']:>10,} {row['categoria_principal']:<25} "
              f"{row['confianca']:>6} {row['exemplos'][:40]}")
    
    total_alta = cap44_alta['tamanho'].sum()
    print(f"\n✓ Total: {len(cap44_alta)} clusters, {total_alta:,} itens ({100*total_alta/total_registros:.2f}%)")
else:
    print("\n⚠ Nenhum cluster com alta confiança")

# ============================================================================
# RELATÓRIO - CLUSTERS PARA REVISÃO MANUAL
# ============================================================================

print(f"\n\n{'='*100}")
print("⚠️  TOP 30 CLUSTERS - REVISAR MANUALMENTE")
print(f"{'='*100}")

revisar = df_analysis[df_analysis['classificacao'] == 'REVISAR MANUALMENTE'].head(30)

if len(revisar) > 0:
    print(f"\n{'Cluster':<10} {'Tamanho':>10} {'Categoria':<25} {'Exemplos'}")
    print("─" * 100)
    
    for _, row in revisar.iterrows():
        print(f"{row['cluster_id']:<10} {row['tamanho']:>10,} {row['categoria_principal']:<25} "
              f"{row['exemplos'][:50]}")
    
    total_revisar = revisar['tamanho'].sum()
    print(f"\n⚠ Total: {len(revisar)} clusters, {total_revisar:,} itens")
else:
    print("\n✓ Nenhum cluster precisa de revisão manual!")

# ============================================================================
# RELATÓRIO - NÃO É CAP 44
# ============================================================================

print(f"\n\n{'='*100}")
print("❌ TOP 20 CLUSTERS - NÃO É CAP 44")
print(f"{'='*100}")

nao_cap44 = df_analysis[df_analysis['classificacao'] == 'NÃO É CAP 44'].head(20)

if len(nao_cap44) > 0:
    print(f"\n{'Cluster':<10} {'Tamanho':>10} {'Categoria':<25} {'Exemplos'}")
    print("─" * 100)
    
    for _, row in nao_cap44.iterrows():
        print(f"{row['cluster_id']:<10} {row['tamanho']:>10,} {row['categoria_principal']:<25} "
              f"{row['exemplos'][:50]}")
    
    total_nao = nao_cap44['tamanho'].sum()
    print(f"\n✓ Total identificado como NÃO Cap 44: {len(nao_cap44)} clusters, {total_nao:,} itens")

# ============================================================================
# EXPORTAR LISTAS PARA APLICAÇÃO
# ============================================================================

print(f"\n\n{'='*100}")
print("📁 GERANDO LISTAS PARA APLICAÇÃO")
print(f"{'='*100}")

# Lista de clusters Cap 44 (alta + média confiança)
cap44_clusters = df_analysis[
    df_analysis['classificacao'].isin(['CAP 44 - ALTA CONFIANÇA', 'CAP 44 - MÉDIA CONFIANÇA'])
]['cluster_id'].tolist()

# Lista de clusters NÃO Cap 44
nao_cap44_clusters = df_analysis[
    df_analysis['classificacao'] == 'NÃO É CAP 44'
]['cluster_id'].tolist()

# Salvar listas
with open('hdbscan_results_pca/clusters_cap44.txt', 'w') as f:
    f.write("# Clusters identificados como Cap 44\n")
    f.write("# Use esta lista para rotulação automática\n\n")
    f.write(f"cap44_clusters = {cap44_clusters}\n")

with open('hdbscan_results_pca/clusters_nao_cap44.txt', 'w') as f:
    f.write("# Clusters identificados como NÃO Cap 44\n")
    f.write("# Use esta lista para exclusão\n\n")
    f.write(f"nao_cap44_clusters = {nao_cap44_clusters}\n")

print(f"\n✅ Lista Cap 44 salva: clusters_cap44.txt ({len(cap44_clusters)} clusters)")
print(f"✅ Lista NÃO Cap 44 salva: clusters_nao_cap44.txt ({len(nao_cap44_clusters)} clusters)")

# ============================================================================
# RESUMO EXECUTIVO
# ============================================================================

print(f"\n\n{'='*100}")
print("📊 RESUMO EXECUTIVO")
print(f"{'='*100}")

total_clusters = len(df_analysis)
cap44_total = len(df_analysis[df_analysis['classificacao'].str.contains('CAP 44')])
cap44_itens = stats_size.get('CAP 44 - ALTA CONFIANÇA', 0) + stats_size.get('CAP 44 - MÉDIA CONFIANÇA', 0) + stats_size.get('CAP 44 - BAIXA CONFIANÇA', 0)
nao_cap44_total = len(df_analysis[df_analysis['classificacao'] == 'NÃO É CAP 44'])
nao_cap44_itens = stats_size.get('NÃO É CAP 44', 0)
revisar_total = len(df_analysis[df_analysis['classificacao'] == 'REVISAR MANUALMENTE'])
revisar_itens = stats_size.get('REVISAR MANUALMENTE', 0)

print(f"""
📈 CLUSTERS ANALISADOS: {total_clusters:,}

✅ IDENTIFICADOS COMO CAP 44:
   • {cap44_total:,} clusters ({100*cap44_total/total_clusters:.1f}%)
   • {cap44_itens:,} itens ({100*cap44_itens/total_registros:.2f}% da base)

❌ IDENTIFICADOS COMO NÃO CAP 44:
   • {nao_cap44_total:,} clusters ({100*nao_cap44_total/total_clusters:.1f}%)
   • {nao_cap44_itens:,} itens ({100*nao_cap44_itens/total_registros:.2f}% da base)

⚠️  PRECISAM REVISÃO MANUAL:
   • {revisar_total:,} clusters ({100*revisar_total/total_clusters:.1f}%)
   • {revisar_itens:,} itens ({100*revisar_itens/total_registros:.2f}% da base)
""")

print(f"{'='*100}")
print("🎯 PRÓXIMOS PASSOS:")
print(f"{'='*100}")
print("""
1. ✅ Revise o arquivo: analise_cap44_regex.csv
   - Valide clusters "CAP 44 - ALTA CONFIANÇA"
   - Analise clusters "REVISAR MANUALMENTE"

2. 📊 Use quick_analysis.py para ver detalhes de clusters específicos
   - Digite IDs para ver 30 exemplos de cada cluster

3. 🔧 Aplique as listas geradas:
   - Use clusters_cap44.txt para rotulação automática
   - Use clusters_nao_cap44.txt para exclusão

4. 📝 Refine regras se necessário:
   - Baseado nos clusters que precisam revisão
   - Atualize as regex no código
""")

print(f"\n{'='*100}")
print("✨ ANÁLISE CONCLUÍDA COM SUCESSO!")
print(f"{'='*100}\n")
