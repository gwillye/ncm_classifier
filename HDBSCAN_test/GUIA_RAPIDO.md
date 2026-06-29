# Guia Rápido de Início - HDBSCAN Hierárquico

## Início rápido (5 minutos)

### 1. Instale as dependências

```bash
pip install pandas numpy torch sentence-transformers umap-learn hdbscan scikit-learn scipy
```

### 2. Prepare o seu arquivo de dados

- Nome do arquivo: `base_outros_a_analisar.csv`.
- Formato: CSV com separador `;`.
- Coluna obrigatória: `prod_xprod` (descrição do produto).
- Encoding: UTF-8 com BOM.

### 3. Execute o processamento completo

```bash
python hdbscan_hierarchical_batches.py
```

Tempo estimado: 2 a 4 horas para 1M de linhas.

### 4. Analise os resultados

```bash
python analyze_results.py
```

## Checklist de pré-execução

Antes de rodar, verifique:

- [ ] O arquivo CSV está no mesmo diretório dos scripts.
- [ ] A coluna `prod_xprod` existe no CSV.
- [ ] Há pelo menos 8 GB de RAM disponível.
- [ ] Há 5 GB de espaço em disco livre.
- [ ] Python 3.8 ou superior está instalado.

## Configurações essenciais

Edite o arquivo `hdbscan_hierarchical_batches.py`, na seção CONFIG:

```python
CONFIG = {
    'INPUT_FILE': 'base_outros_a_analisar.csv',  # SEU ARQUIVO
    'INPUT_SEP': ';',                             # SEU SEPARADOR
    'BATCH_SIZE': 100000,                         # AJUSTE SE DER ERRO DE MEMÓRIA
}
```

### Se der erro de memória

1. Reduza `BATCH_SIZE` para 50000.
2. Reduza `UMAP_N_COMPONENTS` para 10.
3. Feche outros programas.

## Arquivos gerados

Após a execução, você terá dois arquivos principais.

### 1. `hdbscan_results/resultado_final_clusters.csv`

É o arquivo principal, com todos os resultados.

```csv
prod_xprod,cluster_final,batch_id
"MADEIRA COMPENSADA",42,0
"COMPENSADO NAVAL",42,1
"PORTA DE MADEIRA",18,0
"ARGILA BENTONITA",-1,2
```

Quando `cluster_final = -1`, o item é um outlier (não clusterizado). Quando `cluster_final >= 0`, o número é o ID do cluster.

### 2. `hdbscan_results/resumo_clusters_rotulagem.csv`

É o resumo para rotulagem manual.

```csv
cluster_id,tamanho,exemplos
42,15240,"MADEIRA COMPENSADA | COMPENSADO | MADEIRA LAMINADA"
18,12839,"PORTA MADEIRA | PORTA COMPENSADA | FOLHA PORTA"
```

Use este arquivo para rotular manualmente os clusters.

## Próximos passos

### 1. Analise os resultados

```bash
python analyze_results.py
```

Isso vai gerar estatísticas detalhadas, gráficos de distribuição, wordclouds e um arquivo Excel para rotulagem.

### 2. Rotule os clusters

Abra `clusters_para_rotular_detalhado.xlsx` e, para cada cluster, analise os exemplos, marque se ele pertence ao Capítulo 44 do NCM (SIM/NÃO/DÚVIDA) e adicione observações.

### 3. Use os resultados

Com os clusters rotulados, você pode criar regras regex automatizadas, identificar padrões para inclusão ou exclusão e treinar modelos supervisionados.

## Problemas comuns

### Erro: "File not found"

Solução: certifique-se de que o arquivo CSV está no mesmo diretório dos scripts.

```bash
ls -la  # Deve mostrar: base_outros_a_analisar.csv
```

### Erro: "MemoryError" ou "Killed"

Solução: reduza o BATCH_SIZE.

```python
'BATCH_SIZE': 50000,  # Ou até 25000 se necessário
```

### Erro: "CUDA out of memory"

Solução: force o uso de CPU.

```python
device = torch.device('cpu')  # Linha ~96 do código
```

### Processamento muito lento

Isso é normal. Para 1M de linhas, com GPU leva de 2 a 3 horas e sem GPU de 3 a 5 horas. Você pode deixar rodando durante a noite ou usar `run_stages.py` para pausar entre as etapas.

## Comandos úteis

### Ver status do processamento

```bash
python run_stages.py
# Escolha opção 6: Ver Status dos Checkpoints
```

### Reexecutar apenas uma etapa

```bash
python run_stages.py
# Escolha a etapa que deseja reexecutar (1-4)
```

### Limpar tudo e recomeçar

```bash
python run_stages.py
# Escolha opção 7: Limpar Checkpoints
```

## Conceitos rápidos

### O que é um cluster?

É um grupo de produtos com descrições similares. Por exemplo, o Cluster 42 pode reunir todos os tipos de madeira compensada e o Cluster 18 todos os tipos de portas de madeira.

### O que é um outlier?

É um item que não se encaixou em nenhum cluster. Pode ser um produto realmente único, um erro de digitação ou uma descrição muito genérica (ou muito específica).

### O que é um centroide?

É o ponto central de um cluster, usado para comparar clusters entre batches.

## Expectativas realistas

Para uma base de 1M de linhas no NCM Capítulo 44:

| Métrica | Esperado | Bom | Excelente |
|---------|----------|-----|-----------|
| % Clusterizado | 85-90% | 90-95% | >95% |
| % Outliers | 10-15% | 5-10% | <5% |
| N° Clusters | 300-500 | 200-400 | 100-300 |
| Tempo Total | 3-5h | 2-3h | <2h |

## Fluxo de trabalho recomendado

```
1. Executar processamento completo
   |
2. Analisar resultados (analyze_results.py)
   |
3. Revisar top 20 clusters manualmente
   |
4. Rotular clusters no Excel
   |
5. Criar regras/regex para automatizar
   |
6. Aplicar na base completa
   |
7. Validar com amostra manual
```

## Dicas pro

1. Execute durante a noite. O processamento é longo, então vale deixar rodando overnight.
2. Monitore a memória. Use `htop` (Linux) ou o Gerenciador de Tarefas (Windows).
3. Salve os checkpoints. Não delete a pasta `hdbscan_results/` até ter certeza dos resultados.
4. Valide manualmente. Sempre revise uma amostra dos clusters para garantir a qualidade.
5. Documente os padrões. Anote os padrões que identificar para uso futuro.

## Documentação completa

Para detalhes completos, veja `DOCUMENTACAO.md`.

Boa sorte com o seu projeto.

Sistema desenvolvido para classificação de notas fiscais por NCM (Capítulo 44), no contexto de um projeto de auditoria fiscal para um órgão público de fiscalização tributária.
