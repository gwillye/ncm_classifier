# DOSSIÊ TÉCNICO 04: AUDITORIA DE QUANTIDADE MÉDIA (QTRIB MÉDIO)
## UNIDADES DE MEDIDA, PADRÕES DE COMERCIALIZAÇÃO E ANOMALIAS ESTATÍSTICAS

Este documento analisa a base de Quantidade Média de Qtrib. Esta é a dimensão mais complexa, pois revela como os produtos são quantificados (unidades, kg, m³, gramas). Quantidades médias extremamente altas geralmente indicam unidades de medida pequenas ou erros de preenchimento, enquanto quantidades médias baixas indicam produtos acabados.

---

### 1. ANOMALIAS DE UNIDADE DE MEDIDA (OUTLIERS)

O topo da lista de Quantidade Média apresenta valores na casa dos milhões, o que exige uma interpretação técnica cuidadosa.

#### 1.1. O Caso MARCHE (1.568.474,44)
*   **Análise**: O termo "MARCHE" (provavelmente parte de "FOB MARCHE" ou similar em contextos de exportação) apresenta uma quantidade média absurda. 
*   **Insight**: Isso indica que o campo `prod_qtrib` está sendo usado para reportar algo que não é a unidade comercial padrão (talvez gramas ou unidades mínimas de um lote gigantesco).
*   **Diretriz de Regex**: Termos com quantidades médias acima de 1 milhão devem ser tratados como "Suspeitos de Erro de Unidade".

#### 1.2. Dimensões como Quantidade (2130X110X30 - 777.848,50)
*   **Análise**: É comum que o sistema confunda códigos de dimensões com quantidades se o CSV não estiver bem formatado.
*   **Insight**: Ver um código de dimensão no topo da quantidade média sugere que o dado está "sujo".
*   **Diretriz de Regex**: Validar se o campo de quantidade não está capturando valores de dimensões.

---

### 2. PADRÕES DE COMERCIALIZAÇÃO DO CAPÍTULO 44

#### 2.1. Produtos de Giro Industrial (Média 10k - 100k)
*   **SEMISSOLIDA (72.521,33)**: Refere-se a portas semissólidas. Uma quantidade média de 72 mil sugere que estas portas são vendidas em grandes lotes para construtoras ou exportação.
*   **MOINHA (53.498,63)**: Resíduo de carvão vendido por peso (kg). O valor alto confirma a venda a granel.
*   **EUCALYPTUS / UROPHYLLA (19k - 50k)**: Refere-se a sementes ou mudas. 
*   **Diretriz de Regex**: Quantidades médias entre 10.000 e 100.000 são típicas de insumos vendidos por peso (kg) ou grandes lotes industriais.

#### 2.2. O Setor de Reflorestamento
*   **MUDAS (42.629,76)**: Quantidade média alta porque mudas são vendidas em bandejas de centenas ou milhares de unidades.
*   **CLONADAS / CLONAIS (27k - 46k)**: Termos técnicos para mudas de eucalipto de alta performance.
*   **Diretriz de Regex**: Estes termos confirmam a base florestal do Capítulo 44, mas podem transitar para o Capítulo 06 (Plantas vivas).

---

### 3. FALSOS POSITIVOS POR UNIDADE DE MEDIDA

*   **FERRAMENTAS (180.373,43)**: Quantidade média altíssima. Provavelmente refere-se a parafusos, pregos ou pequenos componentes metálicos vendidos em milhar.
*   **IMPRESSO (171.478,75)**: Provavelmente etiquetas ou formulários contínuos.
*   **CAPUCCINO (66.794,13)**: Confirma o erro de unidade (provavelmente ml ou gramas).
*   **Diretriz de Regex**: Excluir termos que indiquem miudezas metálicas ou itens de consumo que não sejam madeira.

---

### 4. IDENTIFICAÇÃO DE MATERIAIS CONCORRENTES

*   **EXOTICA (41.841,79)**: Pode referir-se a "Madeira Exótica" ou "Fruta Exótica". O cruzamento com o valor médio (baixo) sugere que pode ser madeira de reflorestamento para energia.
*   **CABOS (41.376,78)**: Pode ser "Cabos de Madeira" (44.17) ou "Cabos Elétricos". A quantidade média alta sugere componentes menores.
*   **Diretriz de Regex**: O termo `CABOS` deve ser condicionado a `MADEIRA` para evitar o Capítulo 85 (Elétricos).

---

### 5. MATRIZ DE DECISÃO PARA REGEX (BASE: QUANTIDADE MÉDIA)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `SEMISSOLIDA` | INCLUIR | Capítulo 44.18. Indica lotes industriais de portas. |
| `MOINHA` | INCLUIR | Capítulo 44.02. Resíduo de carvão a granel. |
| `MUDAS` | ALERTA | Capítulo 06 vs 44. Base florestal. |
| `FERRAMENTAS` | EXCLUIR | Capítulo 82/83. Provavelmente ferragens metálicas. |
| `CAPUCCINO` | EXCLUIR | Erro de unidade / Alimentos. |
| `IMPRESSO` | EXCLUIR | Capítulo 48/49. Papelaria. |

---

### 6. CONCLUSÃO DO DOSSIÊ 04

A análise de Quantidade Média é o "termômetro" da unidade de medida. Ela revela que o Capítulo 44 na sua base é composto por grandes transações industriais (portas em lotes, carvão a granel) e por uma forte base de reflorestamento (mudas). O maior desafio aqui é filtrar os erros de preenchimento (como Capuccino) e as ferragens metálicas que aparecem com quantidades infladas por serem vendidas em milhares.

---
**Fim do Dossiê 04.**
*(Todos os documentos técnicos foram gerados.)*
