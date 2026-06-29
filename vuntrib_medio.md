# Dossiê Técnico 02: Auditoria de Valor Médio (VUNTRIB Médio)
## Diferenciação de produtos, bens de capital e identificação de outliers

Este documento analisa a base de Valor Médio de Vuntrib. Enquanto o Valor Total mostra o volume financeiro, o Valor Médio revela a natureza do item: se é um insumo, um produto acabado de luxo ou um bem de capital (máquina). Essa análise é vital para evitar que itens de alto valor de outros capítulos "contaminem" a base do Capítulo 44.

## 1. Análise de bens de capital e máquinas (falsos positivos)

O topo da lista de Valor Médio é dominado por itens que não pertencem ao Capítulo 44, mas que aparecem por causa do seu altíssimo custo unitário.

### 1.1. Maquinário industrial (Capítulo 84)

- PICADOR (R$ 744.008,03): máquinas para produção de cavacos.
- DRILL (R$ 510.378,76): equipamentos de perfuração.
- EIXO (R$ 358.569,22): componentes mecânicos.
- GUINDASTE (R$ 65.436,19): equipamentos de movimentação de carga.
- Diretriz de Regex: estes termos devem entrar em uma lista de exclusão prioritária. O alto valor médio é o principal indicador de que não se trata de madeira, mas de tecnologia para processá-la.

### 1.2. Veículos e equipamentos (Capítulo 87)

- VW (R$ 266.376,88): referência a veículos (Volkswagen).
- JOHN DEERE (R$ 65.264,22): tratores e máquinas florestais.
- CARROCERIA (R$ 113.305,61): embora existam carrocerias de madeira, o valor médio sugere estruturas completas de caminhões.
- Diretriz de Regex: excluir marcas de veículos e termos relacionados a transporte pesado.

## 2. Obras de madeira de alto valor (Capítulo 44)

Aqui estão os itens que realmente pertencem ao Capítulo 44 e têm alto valor agregado.

### 2.1. Madeira em bruto e grandes lotes (posição 4403)

- TORAS (R$ 215.306,98): o valor médio confirma que a tora é vendida em lotes fechados de alto valor. É o item legítimo do Cap. 44 com maior valor médio.
- TRONCO (R$ 20.606,17): variante semântica de toras.
- Diretriz de Regex: validar `TORAS` e `TRONCO` como itens de alta confiança.

### 2.2. Obras de carpintaria e marcenaria (posição 4418)

- MADEIRAMENTO (R$ 39.693,22): refere-se a estruturas de telhado ou decks. O valor médio alto se justifica por ser a venda do projeto estrutural completo.
- ARREMATE (R$ 48.204,17): em valores altos, refere-se a kits de acabamento para grandes vãos ou obras corporativas.
- Diretriz de Regex: estes termos são "marcadores de projeto". Devem ser incluídos, mas monitorados para não capturarem acabamentos metálicos.

## 3. O conflito dos móveis planejados (Capítulo 94)

O Valor Médio expõe a fragilidade da classificação de móveis.

- PLANEJADA (R$ 1.004.634,55): um valor médio de 1 milhão de reais para o termo "planejada" indica que estamos lidando com contratos de mobiliário completo para residências ou escritórios.
- PLANEJADOS (R$ 42.618,95): versão plural com valor mais diluído, mas ainda indicativa de móveis.
- DALMOBILE (R$ 29.348,16): marca de móveis planejados.
- Diretriz de Regex: o termo `PLANEJADA` e as marcas associadas são os maiores inimigos da precisão no Capítulo 44. Devem ser excluídos sumariamente.

## 4. Identificação de termos técnicos específicos

- FLORESTAL (R$ 42.678,82): geralmente associado a "projeto florestal" ou "madeira florestal".
- BOVINA / BOVINOS (R$ 45k - R$ 52k): falsos positivos relacionados a gado que "sujam" a base por compartilharem termos como "tronco" (tronco de contenção).
- Diretriz de Regex: criar uma regra de exclusão para termos do setor pecuário (`BOVINA`, `BOVINOS`, `CONTENCAO`, `PESCOCEIRAS`).

## 5. Matriz de decisão para Regex (base: Valor Médio)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `PLANEJADA` | EXCLUIR | Capítulo 94. Valor médio indica contrato de mobiliário. |
| `PICADOR` | EXCLUIR | Capítulo 84. Valor médio indica máquina industrial. |
| `MADEIRAMENTO` | INCLUIR | Capítulo 44.18. Valor médio indica kit estrutural. |
| `TORAS` | INCLUIR | Capítulo 44.03. Valor médio indica lote de matéria-prima. |
| `BOVINA` | EXCLUIR | Setor Pecuário. Falso positivo por homonímia. |
| `JOHN DEERE` | EXCLUIR | Capítulo 87. Maquinário agrícola/veicular. |

## 6. Conclusão do Dossiê 02

A análise de Valor Médio é a ferramenta definitiva para a "limpeza fina" da base. Ela permite separar o que é madeira (Cap. 44) do que é máquina para madeira (Cap. 84) e do que é móvel de madeira (Cap. 94). A regra de ouro aqui é: valores unitários exorbitantes sem termos de matéria-prima associados são, quase sempre, falsos positivos.

Fim do Dossiê 02.
(Iniciando o processamento do Dossiê 03: Quantidade Total.)
