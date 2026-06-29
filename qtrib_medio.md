# Dossiê Técnico 04: Auditoria de Quantidade Média (QTRIB Médio)
## Unidades de medida, padrões de comercialização e anomalias estatísticas

Este documento analisa a base de Quantidade Média de Qtrib. Esta é a dimensão mais complexa, porque revela como os produtos são quantificados (unidades, kg, m³, gramas). Quantidades médias muito altas costumam indicar unidades de medida pequenas ou erros de preenchimento, enquanto quantidades médias baixas indicam produtos acabados.

## 1. Anomalias de unidade de medida (outliers)

O topo da lista de Quantidade Média apresenta valores na casa dos milhões, o que exige uma interpretação técnica cuidadosa.

### 1.1. O caso MARCHE (1.568.474,44)

- Análise: o termo "MARCHE" (provavelmente parte de "FOB MARCHE" ou algo similar em contextos de exportação) apresenta uma quantidade média absurda.
- Insight: isso indica que o campo `prod_qtrib` está sendo usado para reportar algo que não é a unidade comercial padrão (talvez gramas ou unidades mínimas de um lote gigantesco).
- Diretriz de Regex: termos com quantidades médias acima de 1 milhão devem ser tratados como "suspeitos de erro de unidade".

### 1.2. Dimensões como quantidade (2130X110X30 - 777.848,50)

- Análise: é comum o sistema confundir códigos de dimensões com quantidades quando o CSV não está bem formatado.
- Insight: ver um código de dimensão no topo da quantidade média sugere que o dado está "sujo".
- Diretriz de Regex: validar se o campo de quantidade não está capturando valores de dimensões.

## 2. Padrões de comercialização do Capítulo 44

### 2.1. Produtos de giro industrial (média 10k - 100k)

- SEMISSOLIDA (72.521,33): refere-se a portas semissólidas. Uma quantidade média de 72 mil sugere que essas portas são vendidas em grandes lotes para construtoras ou exportação.
- MOINHA (53.498,63): resíduo de carvão vendido por peso (kg). O valor alto confirma a venda a granel.
- EUCALYPTUS / UROPHYLLA (19k - 50k): refere-se a sementes ou mudas.
- Diretriz de Regex: quantidades médias entre 10.000 e 100.000 são típicas de insumos vendidos por peso (kg) ou em grandes lotes industriais.

### 2.2. O setor de reflorestamento

- MUDAS (42.629,76): quantidade média alta porque mudas são vendidas em bandejas de centenas ou milhares de unidades.
- CLONADAS / CLONAIS (27k - 46k): termos técnicos para mudas de eucalipto de alta performance.
- Diretriz de Regex: estes termos confirmam a base florestal do Capítulo 44, mas podem transitar para o Capítulo 06 (plantas vivas).

## 3. Falsos positivos por unidade de medida

- FERRAMENTAS (180.373,43): quantidade média altíssima. Provavelmente refere-se a parafusos, pregos ou pequenos componentes metálicos vendidos em milhar.
- IMPRESSO (171.478,75): provavelmente etiquetas ou formulários contínuos.
- CAPUCCINO (66.794,13): confirma o erro de unidade (provavelmente ml ou gramas).
- Diretriz de Regex: excluir termos que indiquem miudezas metálicas ou itens de consumo que não sejam madeira.

## 4. Identificação de materiais concorrentes

- EXOTICA (41.841,79): pode se referir a "madeira exótica" ou "fruta exótica". O cruzamento com o valor médio (baixo) sugere que pode ser madeira de reflorestamento para energia.
- CABOS (41.376,78): pode ser "cabos de madeira" (44.17) ou "cabos elétricos". A quantidade média alta sugere componentes menores.
- Diretriz de Regex: o termo `CABOS` deve ser condicionado a `MADEIRA` para evitar o Capítulo 85 (elétricos).

## 5. Matriz de decisão para Regex (base: Quantidade Média)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `SEMISSOLIDA` | INCLUIR | Capítulo 44.18. Indica lotes industriais de portas. |
| `MOINHA` | INCLUIR | Capítulo 44.02. Resíduo de carvão a granel. |
| `MUDAS` | ALERTA | Capítulo 06 vs 44. Base florestal. |
| `FERRAMENTAS` | EXCLUIR | Capítulo 82/83. Provavelmente ferragens metálicas. |
| `CAPUCCINO` | EXCLUIR | Erro de unidade / Alimentos. |
| `IMPRESSO` | EXCLUIR | Capítulo 48/49. Papelaria. |

## 6. Conclusão do Dossiê 04

A análise de Quantidade Média é o "termômetro" da unidade de medida. Ela mostra que o Capítulo 44 nesta base é composto por grandes transações industriais (portas em lotes, carvão a granel) e por uma forte base de reflorestamento (mudas). O maior desafio aqui é filtrar os erros de preenchimento (como Capuccino) e as ferragens metálicas que aparecem com quantidades infladas por serem vendidas em milhares.

Fim do Dossiê 04.
(Todos os documentos técnicos foram gerados.)
