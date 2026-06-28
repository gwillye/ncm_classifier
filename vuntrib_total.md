# DOSSIÊ TÉCNICO 01: AUDITORIA DE VALOR TOTAL (VUNTRIB TOTAL)
## ANÁLISE EXAUSTIVA DE IMPACTO FINANCEIRO E CLASSIFICAÇÃO NCM - CAPÍTULO 44

Este documento apresenta uma análise técnica profunda sobre a base de dados de Valor Total de Vuntrib, identificando a concentração de capital e definindo parâmetros de classificação para o Capítulo 44 da NCM. A análise é conduzida de forma direta, técnica e objetiva, visando a construção de um motor de classificação via Regex de alta precisão.

---

### 1. MACRO-ANÁLISE DA CONCENTRAÇÃO DE CAPITAL

A base de Valor Total revela que o Capítulo 44 não é homogêneo. O capital está concentrado em três grandes frentes: **Matéria-Prima Bruta**, **Painéis Industrializados** e **Esquadrias de Construção**. A presença de termos como `MADEIRA` (R$ 588M) e `TORAS` (R$ 334M) no topo da lista confirma que a base é dominada por transações de grande porte, provavelmente B2B (Business to Business), envolvendo serrarias e indústrias de beneficiamento.

#### 1.1. O Termo Âncora: MADEIRA (R$ 588.611.628,48)
O termo `MADEIRA` é a maior fonte de ruído e, simultaneamente, o maior validador. Com 335.705 ocorrências, ele possui um valor médio de R$ 1.753,35. 
*   **Análise Técnica**: Este valor médio sugere que o termo não descreve apenas a matéria-prima, mas sim produtos acabados ou lotes de madeira serrada. 
*   **Risco de Classificação**: Por ser genérico, ele pode ocultar itens que deveriam estar em subposições específicas (4407, 4408, 4412). 
*   **Diretriz de Regex**: Não deve ser usado isoladamente para classificação final, mas sim como um "trigger" de entrada para análise de termos secundários.

#### 1.2. O Pilar da Extração: TORAS (R$ 334.156.448,39)
Diferente do termo genérico, `TORAS` é um descritor técnico específico da posição **4403** (Madeira em bruto).
*   **Análise de Valor**: O valor médio de R$ 215.306,98 é um dos mais altos da base. Isso indica que cada transação envolve volumes massivos (cargas completas).
*   **Validação NCM**: 100% de aderência ao Capítulo 44. 
*   **Diretriz de Regex**: Termo de inclusão imediata. Deve ser priorizado sobre termos como "tronco" ou "madeira bruta" devido à sua frequência e valor.

---

### 2. ANÁLISE DETALHADA POR CATEGORIA INDUSTRIAL

#### 2.1. Painéis e Chapas (Posições 4410, 4411 e 4412)
Esta categoria é representada pelos termos `COMPENSADO`, `MDF`, `PLASTIFICADO` e `HDF`.
*   **COMPENSADO (R$ 137M)**: Valor médio de R$ 18.049,34. Indica venda por paletes ou fardos. A posição NCM é **4412**.
*   **MDF (R$ 137M)**: Valor médio de R$ 411,05. Note a discrepância: o MDF tem o mesmo valor total que o compensado, mas com 333.475 ocorrências (contra 7.613 do compensado). Isso prova que o MDF é vendido em unidades menores ou chapas avulsas, sendo o item de maior capilaridade da base.
*   **PLASTIFICADO (R$ 134M)**: Este termo é um qualificador crítico. Refere-se ao compensado com filme fenólico para construção civil. 
*   **Diretriz de Regex**: O termo `PLASTIFICADO` deve ser condicionado à presença de `MADEIRA` ou `COMPENSADO` para evitar confusão com plásticos do Cap. 39.

#### 2.2. Madeira Serrada e Beneficiada (Posição 4407 e 4418)
*   **SERRADA (R$ 119M)**: Valor médio de R$ 1.328,41. É o descritor padrão para a posição **4407**.
*   **BENEFICIADA (R$ 44M)**: Indica madeira que passou por plaina ou lixamento. 
*   **TABUA (R$ 38M)**: Com 88.108 ocorrências, é o termo popular para madeira serrada.
*   **Diretriz de Regex**: Criar um grupo de "Serrados" que inclua `SERRADA`, `TABUA`, `VIGA`, `CAIBRO` e `RIPAS`.

---

### 3. IDENTIFICAÇÃO DE ANOMALIAS E FALSOS POSITIVOS

A análise de Valor Total permite identificar "intrusos" que, pelo alto faturamento, distorcem a base do Capítulo 44.

#### 3.1. O Conflito com o Capítulo 94 (Móveis)
*   **COZINHA (R$ 21M)**: Este termo é um falso positivo clássico. Cozinhas planejadas são móveis (9403). 
*   **PLANEJADA (R$ 18M)**: Reforça a exclusão. 
*   **Diretriz de Regex**: Criar uma lista de exclusão (Blacklist) contendo `COZINHA`, `PLANEJADA`, `ARMARIO`, `DORMITORIO`.

#### 3.2. O Conflito com o Capítulo 84 (Máquinas)
*   **PICADOR (R$ 17M)**: Embora processe madeira, é uma máquina. 
*   **Diretriz de Regex**: Excluir termos que indiquem ferramentas ou máquinas industriais.

---

### 4. ANÁLISE DE DIMENSÕES E PADRÕES TÉCNICOS

A base de Valor Total revela que a madeira é definida por suas medidas.
*   **18MM (R$ 110M)**: É a espessura dominante. Quase sempre associada a MDF ou Compensado.
*   **1100X2200 (R$ 100M)**: Medida padrão de chapas industriais.
*   **Diretriz de Regex**: Capturar padrões numéricos seguidos de `MM` ou `X` como validadores de itens do Capítulo 44.

---

### 5. MATRIZ DE DECISÃO PARA REGEX (BASE: VALOR TOTAL)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `TORAS` | INCLUIR | Posição 4403. Alto valor unitário e total. |
| `MDF` | INCLUIR | Posição 4411. Maior frequência da base. |
| `COMPENSADO` | INCLUIR | Posição 4412. Alto valor total. |
| `SERRADA` | INCLUIR | Posição 4407. Termo técnico de alto giro. |
| `COZINHA` | EXCLUIR | Capítulo 94. Móveis acabados. |
| `PICADOR` | EXCLUIR | Capítulo 84. Máquinas industriais. |
| `18MM` | VALIDAR | Marcador de espessura para painéis de madeira. |

---

### 6. CONCLUSÃO DO DOSSIÊ 01

A base de Valor Total demonstra que o sucesso da classificação do Capítulo 44 depende da captura dos termos de alto giro industrial (`MDF`, `TORAS`, `SERRADA`) e da exclusão rigorosa de móveis planejados e máquinas. O capital está concentrado na matéria-prima e nos painéis, que devem ser o foco principal do motor de busca.

---
**Fim do Dossiê 01.**
*(Iniciando processamento do Dossiê 02: Valor Médio)*
