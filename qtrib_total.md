# DOSSIÊ TÉCNICO 03: AUDITORIA DE QUANTIDADE TOTAL (QTRIB TOTAL)
## ANÁLISE DE COMMODITIES, VOLUMES DE MASSA E RESÍDUOS INDUSTRIAIS

Este documento analisa a base de Quantidade Total de Qtrib. Esta dimensão identifica os itens que possuem o maior giro físico na base de dados. No Capítulo 44, as maiores quantidades estão associadas a produtos de baixo valor unitário, mas de importância vital para a biomassa, energia e insumos industriais básicos.

---

### 1. O DOMÍNIO DA BIOMASSA E ENERGIA (POSIÇÕES 4401 E 4402)

O topo da lista de Quantidade Total é quase inteiramente composto por itens destinados à queima ou processamento primário.

#### 1.1. Lenha e Resíduos (Posição 4401)
*   **LENHA (130.159.304,21)**: É o líder absoluto em volume físico. 
*   **CAVACO (66.648.143,43)**: Madeira picada para caldeiras ou produção de celulose.
*   **RESIDUO / RESIDUOS (105M / 56M)**: Sobras de serraria.
*   **BIOMASSA (83.926.296,42)**: Termo genérico para material orgânico combustível.
*   **Diretriz de Regex**: Estes termos são validadores de 100% para o Capítulo 44. Devem ser incluídos como "Commodities de Giro".

#### 1.2. Carvão Vegetal (Posição 4402)
*   **CARVAO (110.624.346,39)**: Volume massivo.
*   **VEGETAL (14.787.983,26)**: Geralmente qualificador de "Carvão Vegetal".
*   **MOINHA (90.359.191,26)**: Resíduo fino de carvão.
*   **Diretriz de Regex**: O termo `CARVAO` deve ser sempre validado com `VEGETAL` para evitar confusão com carvão mineral (Cap. 27).

---

### 2. MATÉRIA-PRIMA E SEMI-PROCESSADOS (POSIÇÕES 4403 E 4407)

*   **EUCALIPTO (109.249.094,53)**: A espécie de madeira mais comum no Brasil. Sua presença massiva indica a base do reflorestamento.
*   **SERRADA (103.855.703,13)**: Confirma o volume de madeira processada longitudinalmente.
*   **BRUTA (111.492.522,59)**: Qualificador de madeira sem acabamento.
*   **Diretriz de Regex**: `EUCALIPTO` é um termo de inclusão obrigatória. `SERRADA` e `BRUTA` são qualificadores de alta frequência.

---

### 3. PAINÉIS E DERIVADOS (POSIÇÕES 4410 E 4411)

*   **MDF (19.337.645,72)**: Embora tenha menos volume total que a lenha, possui o maior número de ocorrências (333.475). Isso indica que o MDF é o produto de madeira mais distribuído na economia.
*   **HDF (37.750.352,37)**: Painel de alta densidade, muitas vezes usado em pisos ou fundos de móveis.
*   **3MM (38.457.033,48)**: A espessura padrão para painéis finos.
*   **Diretriz de Regex**: Padrões de espessura como `3MM`, `6MM`, `15MM`, `18MM` são excelentes validadores de volume para painéis.

---

### 4. IDENTIFICAÇÃO DE ANOMALIAS DE VOLUME (FALSOS POSITIVOS)

Volumes na casa dos milhões para itens não-madeireiros indicam erros de base ou unidades de medida distorcidas.

*   **CAPUCCINO (64.322.750,52)**: Claramente um erro de base. Provavelmente medido em gramas ou mililitros.
*   **PLASTICO (39.321.094,06)**: Indica componentes plásticos que acompanham a madeira ou embalagens.
*   **PET (27.073.288,00)**: Provavelmente fitas de arquear ou embalagens.
*   **Diretriz de Regex**: Excluir `CAPUCCINO`, `PLASTICO` e `PET` para evitar distorção nos volumes do Capítulo 44.

---

### 5. MATRIZ DE DECISÃO PARA REGEX (BASE: QUANTIDADE TOTAL)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `LENHA` | INCLUIR | Posição 4401. Maior volume físico da base. |
| `CARVAO` | INCLUIR | Posição 4402. Deve ser validado como "Vegetal". |
| `CAVACO` | INCLUIR | Posição 4401. Insumo industrial de alto giro. |
| `EUCALIPTO` | INCLUIR | Base florestal. Espécie dominante. |
| `CAPUCCINO` | EXCLUIR | Erro de base / Alimentos. |
| `PLASTICO` | EXCLUIR | Capítulo 39. Material concorrente/embalagem. |

---

### 6. CONCLUSÃO DO DOSSIÊ 03

A análise de Quantidade Total revela a "base da pirâmide" do Capítulo 44. O volume está concentrado em energia (lenha/carvão) e insumos básicos (cavaco/serrada). Para um Regex eficiente, capturar estes termos garante a cobertura da maior parte da movimentação física da base, enquanto a exclusão de anomalias como "Capuccino" protege a integridade estatística dos dados.

---
**Fim do Dossiê 03.**
*(Iniciando processamento do Dossiê 04: Quantidade Média)*
