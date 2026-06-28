# 🚀 Guia Rápido de Início - HDBSCAN Hierárquico

## ⚡ Início Rápido (5 minutos)

### 1. Instale as dependências

```bash
pip install pandas numpy torch sentence-transformers umap-learn hdbscan scikit-learn scipy
```

### 2. Prepare seu arquivo de dados

- Nome do arquivo: `base_outros_a_analisar.csv`
- Formato: CSV com separador `;`
- Coluna obrigatória: `prod_xprod` (descrição do produto)
- Encoding: UTF-8 com BOM

### 3. Execute o processamento completo

```bash
python hdbscan_hierarchical_batches.py
```

**Tempo estimado:** 2-4 horas para 1M de linhas

### 4. Analise os resultados

```bash
python analyze_results.py
```

---

## 📋 Checklist de Pré-execução

Antes de rodar, verifique:

- [ ] Arquivo CSV está no mesmo diretório dos scripts
- [ ] Coluna `prod_xprod` existe no CSV
- [ ] Pelo menos 8 GB de RAM disponível
- [ ] 5 GB de espaço em disco livre
- [ ] Python 3.8 ou superior instalado

---

## ⚙️ Configurações Essenciais

Edite o arquivo `hdbscan_hierarchical_batches.py`, seção CONFIG:

```python
CONFIG = {
    'INPUT_FILE': 'base_outros_a_analisar.csv',  # ← SEU ARQUIVO
    'INPUT_SEP': ';',                             # ← SEU SEPARADOR
    'BATCH_SIZE': 100000,                         # ← AJUSTE SE DER ERRO DE MEMÓRIA
}
```

### Se der erro de memória:

1. Reduza `BATCH_SIZE` para 50000
2. Reduza `UMAP_N_COMPONENTS` para 10
3. Feche outros programas

---

## 📊 Arquivos Gerados

Após a execução, você terá:

### 1. `hdbscan_results/resultado_final_clusters.csv`
**O arquivo principal com todos os resultados**

```csv
prod_xprod,cluster_final,batch_id
"MADEIRA COMPENSADA",42,0
"COMPENSADO NAVAL",42,1
"PORTA DE MADEIRA",18,0
"ARGILA BENTONITA",-1,2
```

- **cluster_final = -1**: Outlier (não clusterizado)
- **cluster_final ≥ 0**: ID do cluster

### 2. `hdbscan_results/resumo_clusters_rotulagem.csv`
**Resumo para rotulagem manual**

```csv
cluster_id,tamanho,exemplos
42,15240,"MADEIRA COMPENSADA | COMPENSADO | MADEIRA LAMINADA"
18,12839,"PORTA MADEIRA | PORTA COMPENSADA | FOLHA PORTA"
```

Use este arquivo para rotular manualmente os clusters!

---

## 🎯 Próximos Passos

### 1. Analise os resultados

```bash
python analyze_results.py
```

Isso vai gerar:
- Estatísticas detalhadas
- Gráficos de distribuição
- Wordclouds
- Arquivo Excel para rotulagem

### 2. Rotule os clusters

Abra `clusters_para_rotular_detalhado.xlsx` e:
- Analise os exemplos de cada cluster
- Marque se pertence ao Capítulo 44 do NCM (SIM/NÃO/DÚVIDA)
- Adicione observações

### 3. Use os resultados

Com os clusters rotulados, você pode:
- Criar regras regex automatizadas
- Identificar padrões para inclusão/exclusão
- Treinar modelos supervisionados

---

## 🆘 Problemas Comuns

### Erro: "File not found"

**Solução:** Certifique-se de que o arquivo CSV está no mesmo diretório dos scripts.

```bash
ls -la  # Deve mostrar: base_outros_a_analisar.csv
```

### Erro: "MemoryError" ou "Killed"

**Solução:** Reduza o BATCH_SIZE

```python
'BATCH_SIZE': 50000,  # Ou até 25000 se necessário
```

### Erro: "CUDA out of memory"

**Solução:** Force uso de CPU

```python
device = torch.device('cpu')  # Linha ~96 do código
```

### Processamento muito lento

**Normal!** Para 1M de linhas:
- Com GPU: 2-3 horas
- Sem GPU: 3-5 horas

Você pode:
- Deixar rodando overnight
- Usar `run_stages.py` para pausar entre etapas

---

## 📞 Comandos Úteis

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

---

## 🎓 Conceitos Rápidos

### O que é um cluster?

Grupo de produtos com descrições similares. Exemplo:
- Cluster 42: Todos os tipos de madeira compensada
- Cluster 18: Todos os tipos de portas de madeira

### O que é um outlier?

Item que não se encaixou em nenhum cluster. Pode ser:
- Produto realmente único
- Erro de digitação
- Descrição muito genérica ou muito específica

### O que é um centroide?

Ponto central de um cluster, usado para comparar clusters entre batches.

---

## ✅ Expectativas Realistas

Para uma base de 1M de linhas no NCM Capítulo 44:

| Métrica | Esperado | Bom | Excelente |
|---------|----------|-----|-----------|
| % Clusterizado | 85-90% | 90-95% | >95% |
| % Outliers | 10-15% | 5-10% | <5% |
| N° Clusters | 300-500 | 200-400 | 100-300 |
| Tempo Total | 3-5h | 2-3h | <2h |

---

## 🔄 Fluxo de Trabalho Recomendado

```
1. Executar processamento completo
   ↓
2. Analisar resultados (analyze_results.py)
   ↓
3. Revisar top 20 clusters manualmente
   ↓
4. Rotular clusters no Excel
   ↓
5. Criar regras/regex para automatizar
   ↓
6. Aplicar na base completa
   ↓
7. Validar com amostra manual
```

---

## 💡 Dicas Pro

1. **Execute durante a noite:** O processamento é longo, deixe rodando overnight

2. **Monitore a memória:** Use `htop` (Linux) ou Task Manager (Windows)

3. **Salve os checkpoints:** Não delete a pasta `hdbscan_results/` até ter certeza dos resultados

4. **Valide manualmente:** Sempre revise uma amostra dos clusters para garantir qualidade

5. **Documente padrões:** Anote os padrões que identificar para uso futuro

---

## 📚 Documentação Completa

Para detalhes completos, veja: `DOCUMENTACAO.md`

---

**Boa sorte com seu projeto! 🎉**

*Sistema desenvolvido para classificação de notas fiscais NCM Capítulo 44*
*Receita Federal - Combate à Fraude Fiscal*
