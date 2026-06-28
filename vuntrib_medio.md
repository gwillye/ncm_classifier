# DOSSIÊ TÉCNICO 02: AUDITORIA DE VALOR MÉDIO (VUNTRIB MÉDIO)
## DIFERENCIAÇÃO DE PRODUTOS, BENS DE CAPITAL E IDENTIFICAÇÃO DE OUTLIERS

Este documento analisa a base de Valor Médio de Vuntrib. Enquanto o Valor Total mostra o volume financeiro, o Valor Médio revela a natureza do item: se é um insumo, um produto acabado de luxo ou um bem de capital (máquina). Esta análise é vital para evitar que itens de alto valor de outros capítulos "contaminem" a base do Capítulo 44.

---

### 1. ANÁLISE DE BENS DE CAPITAL E MÁQUINAS (FALSOS POSITIVOS)

O topo da lista de Valor Médio é dominado por itens que não pertencem ao Capítulo 44, mas que aparecem devido ao seu altíssimo custo unitário.

#### 1.1. Maquinário Industrial (Capítulo 84)
*   **PICADOR (R$ 744.008,03)**: Máquinas para produção de cavacos.
*   **DRILL (R$ 510.378,76)**: Equipamentos de perfuração.
*   **EIXO (R$ 358.569,22)**: Componentes mecânicos.
*   **GUINDASTE (R$ 65.436,19)**: Equipamentos de movimentação de carga.
*   **Diretriz de Regex**: Estes termos devem ser incluídos em uma lista de exclusão prioritária. O alto valor médio é o principal indicador de que não se trata de madeira, mas de tecnologia para processá-la.

#### 1.2. Veículos e Equipamentos (Capítulo 87)
*   **VW (R$ 266.376,88)**: Referência a veículos (Volkswagen).
*   **JOHN DEERE (R$ 65.264,22)**: Tratores e máquinas florestais.
*   **CARROCERIA (R$ 113.305,61)**: Embora existam carrocerias de madeira, o valor médio sugere estruturas completas de caminhões.
*   **Diretriz de Regex**: Excluir marcas de veículos e termos relacionados a transporte pesado.

---

### 2. OBRAS DE MADEIRA DE ALTO VALOR (CAPÍTULO 44)

Aqui identificamos os itens que realmente pertencem ao Capítulo 44 e possuem alto valor agregado.

#### 2.1. Madeira em Bruto e Grandes Lotes (Posição 4403)
*   **TORAS (R$ 215.306,98)**: O valor médio confirma que a tora é vendida em lotes fechados de alto valor. É o item legítimo do Cap. 44 com maior valor médio.
*   **TRONCO (R$ 20.606,17)**: Variante semântica de toras.
*   **Diretriz de Regex**: Validar `TORAS` e `TRONCO` como itens de alta confiança.

#### 2.2. Obras de Carpintaria e Marcenaria (Posição 4418)
*   **MADEIRAMENTO (R$ 39.693,22)**: Refere-se a estruturas de telhado ou decks. O valor médio alto justifica-se por ser a venda do projeto estrutural completo.
*   **ARREMATE (R$ 48.204,17)**: Em valores altos, refere-se a kits de acabamento para grandes vãos ou obras corporativas.
*   **Diretriz de Regex**: Estes termos são "marcadores de projeto". Devem ser incluídos, mas monitorados para não capturarem acabamentos metálicos.

---

### 3. O CONFLITO DOS MÓVEIS PLANEJADOS (CAPÍTULO 94)

O Valor Médio expõe a fragilidade da classificação de móveis.
*   **PLANEJADA (R$ 1.004.634,55)**: Um valor médio de 1 milhão de reais para o termo "Planejada" indica que estamos lidando com contratos de mobiliário completo para residências ou escritórios.
*   **PLANEJADOS (R$ 42.618,95)**: Versão plural com valor mais diluído, mas ainda indicativa de móveis.
*   **DALMOBILE (R$ 29.348,16)**: Marca de móveis planejados.
*   **Diretriz de Regex**: O termo `PLANEJADA` e marcas associadas são os maiores inimigos da precisão no Capítulo 44. Devem ser excluídos sumariamente.

---

### 4. IDENTIFICAÇÃO DE TERMOS TÉCNICOS ESPECÍFICOS

*   **FLORESTAL (R$ 42.678,82)**: Geralmente associado a "Projeto Florestal" ou "Madeira Florestal".
*   **BOVINA / BOVINOS (R$ 45k - R$ 52k)**: Falsos positivos relacionados a gado que "sujam" a base por compartilharem termos como "tronco" (tronco de contenção).
*   **Diretriz de Regex**: Criar uma regra de exclusão para termos do setor pecuário (`BOVINA`, `BOVINOS`, `CONTENCAO`, `PESCOCEIRAS`).

---

### 5. MATRIZ DE DECISÃO PARA REGEX (BASE: VALOR MÉDIO)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `PLANEJADA` | EXCLUIR | Capítulo 94. Valor médio indica contrato de mobiliário. |
| `PICADOR` | EXCLUIR | Capítulo 84. Valor médio indica máquina industrial. |
| `MADEIRAMENTO` | INCLUIR | Capítulo 44.18. Valor médio indica kit estrutural. |
| `TORAS` | INCLUIR | Capítulo 44.03. Valor médio indica lote de matéria-prima. |
| `BOVINA` | EXCLUIR | Setor Pecuário. Falso positivo por homonímia. |
| `JOHN DEERE` | EXCLUIR | Capítulo 87. Maquinário agrícola/veicular. |

---

### 6. CONCLUSÃO DO DOSSIÊ 02

A análise de Valor Médio é a ferramenta definitiva para a "limpeza fina" da base. Ela permite separar o que é madeira (Cap. 44) do que é máquina para madeira (Cap. 84) e do que é móvel de madeira (Cap. 94). A regra de ouro aqui é: valores unitários exorbitantes sem termos de matéria-prima associados são, quase invariavelmente, falsos positivos.

---
**Fim do Dossiê 02.**
*(Iniciando processamento do Dossiê 03: Quantidade Total)*
