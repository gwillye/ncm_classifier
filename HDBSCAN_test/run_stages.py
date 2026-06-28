"""
HDBSCAN Hierárquico - Execução por Etapas
Permite executar/reexecutar etapas individuais do processamento
"""

import sys
from hdbscan_hierarchical_batches import (
    setup_output_dir,
    run_batch_processing,
    merge_centroids,
    reclassify_outliers,
    generate_final_results,
    load_checkpoint,
    CONFIG
)

def print_menu():
    print("\n" + "="*60)
    print("HDBSCAN HIERÁRQUICO - MENU DE EXECUÇÃO")
    print("="*60)
    print("\nEscolha uma opção:")
    print("\n1 - Executar Etapa 1: Processar Batches")
    print("2 - Executar Etapa 2: Merge de Centroides")
    print("3 - Executar Etapa 3: Reclassificar Outliers")
    print("4 - Executar Etapa 4: Gerar Resultados Finais")
    print("5 - Executar Pipeline Completo")
    print("6 - Ver Status dos Checkpoints")
    print("7 - Limpar Checkpoints")
    print("0 - Sair")
    print("\n" + "="*60)

def check_status():
    """Verifica quais etapas já foram executadas"""
    print("\n" + "="*60)
    print("STATUS DOS CHECKPOINTS")
    print("="*60)
    
    checkpoints = [
        ('Etapa 1: Batches', 'all_batches_results.pkl'),
        ('Etapa 2: Centroides', 'merged_centroids.pkl'),
        ('Etapa 3: Reclassificação', 'reclassification_results.pkl')
    ]
    
    for name, file in checkpoints:
        data = load_checkpoint(file)
        status = "✓ CONCLUÍDA" if data is not None else "✗ Não executada"
        print(f"{name}: {status}")
    
    print("="*60)

def clear_checkpoints():
    """Remove todos os checkpoints"""
    import os
    import glob
    
    pattern = f"{CONFIG['OUTPUT_DIR']}/*.pkl"
    files = glob.glob(pattern)
    
    if not files:
        print("\nNenhum checkpoint encontrado.")
        return
    
    print(f"\nEncontrados {len(files)} arquivo(s) de checkpoint.")
    confirm = input("Deseja realmente remover todos? (s/n): ")
    
    if confirm.lower() == 's':
        for file in files:
            os.remove(file)
            print(f"✓ Removido: {os.path.basename(file)}")
        print("\n✓ Todos os checkpoints foram removidos.")
    else:
        print("\nOperação cancelada.")

def run_stage_1():
    """Executa apenas a Etapa 1"""
    print("\n→ Executando Etapa 1: Processar Batches...")
    setup_output_dir()
    batch_results = run_batch_processing()
    print("\n✓ Etapa 1 concluída!")
    return batch_results

def run_stage_2():
    """Executa apenas a Etapa 2"""
    print("\n→ Executando Etapa 2: Merge de Centroides...")
    
    # Carregar resultado da Etapa 1
    batch_results = load_checkpoint('all_batches_results.pkl')
    if batch_results is None:
        print("\n✗ ERRO: Etapa 1 não foi executada!")
        print("Execute primeiro a Etapa 1.")
        return None
    
    merged_centroids_result = merge_centroids(batch_results)
    print("\n✓ Etapa 2 concluída!")
    return merged_centroids_result

def run_stage_3():
    """Executa apenas a Etapa 3"""
    print("\n→ Executando Etapa 3: Reclassificar Outliers...")
    
    # Carregar resultados das etapas anteriores
    batch_results = load_checkpoint('all_batches_results.pkl')
    merged_centroids_result = load_checkpoint('merged_centroids.pkl')
    
    if batch_results is None or merged_centroids_result is None:
        print("\n✗ ERRO: Etapas anteriores não foram executadas!")
        if batch_results is None:
            print("- Etapa 1 (Batches) não executada")
        if merged_centroids_result is None:
            print("- Etapa 2 (Centroides) não executada")
        return None
    
    reclassification_result = reclassify_outliers(batch_results, merged_centroids_result)
    print("\n✓ Etapa 3 concluída!")
    return reclassification_result

def run_stage_4():
    """Executa apenas a Etapa 4"""
    print("\n→ Executando Etapa 4: Gerar Resultados Finais...")
    
    # Carregar resultados de todas as etapas anteriores
    batch_results = load_checkpoint('all_batches_results.pkl')
    merged_centroids_result = load_checkpoint('merged_centroids.pkl')
    reclassification_result = load_checkpoint('reclassification_results.pkl')
    
    if any(x is None for x in [batch_results, merged_centroids_result, reclassification_result]):
        print("\n✗ ERRO: Etapas anteriores não foram executadas!")
        if batch_results is None:
            print("- Etapa 1 (Batches) não executada")
        if merged_centroids_result is None:
            print("- Etapa 2 (Centroides) não executada")
        if reclassification_result is None:
            print("- Etapa 3 (Reclassificação) não executada")
        return None
    
    df_final, df_summary = generate_final_results(
        batch_results,
        reclassification_result,
        merged_centroids_result
    )
    print("\n✓ Etapa 4 concluída!")
    return df_final, df_summary

def run_full_pipeline():
    """Executa o pipeline completo"""
    from hdbscan_hierarchical_batches import main
    main()

def main_menu():
    """Menu principal interativo"""
    setup_output_dir()
    
    while True:
        print_menu()
        choice = input("\nDigite sua opção: ").strip()
        
        if choice == '0':
            print("\nEncerrando...")
            break
        
        elif choice == '1':
            run_stage_1()
        
        elif choice == '2':
            run_stage_2()
        
        elif choice == '3':
            run_stage_3()
        
        elif choice == '4':
            run_stage_4()
        
        elif choice == '5':
            run_full_pipeline()
        
        elif choice == '6':
            check_status()
        
        elif choice == '7':
            clear_checkpoints()
        
        else:
            print("\n✗ Opção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")

if __name__ == "__main__":
    main_menu()
