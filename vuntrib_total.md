# Dossiê Técnico 01: Auditoria de Valor Total (VUNTRIB Total)
## Análise de impacto financeiro e classificação NCM - Capítulo 44

Este documento traz uma análise técnica detalhada sobre a base de dados de Valor Total de Vuntrib. A ideia é identificar onde o capital está concentrado e definir os parâmetros de classificação para o Capítulo 44 da NCM. A condução é direta, técnica e objetiva, com o objetivo de construir um motor de classificação via Regex de alta precisão.

## 1. Macro-análise da concentração de capital

A base de Valor Total mostra que o Capítulo 44 não é homogêneo. O capital se concentra em três grandes frentes: matéria-prima bruta, painéis industrializados e esquadrias de construção. A presença de termos como `MADEIRA` (R$ 588M) e `TORAS` (R$ 334M) no topo da lista confirma que a base é dominada por transações de grande porte, provavelmente B2B (business to business), envolvendo serrarias e indústrias de beneficiamento.

### 1.1. O termo âncora: MADEIRA (R$ 588.611.628,48)

O termo `MADEIRA` é a maior fonte de ruído e, ao mesmo tempo, o maior validador. Com 335.705 ocorrências, ele tem um valor médio de R$ 1.753,35.

- Análise técnica: esse valor médio sugere que o termo não descreve apenas a matéria-prima, mas também produtos acabados ou lotes de madeira serrada.
- Risco de classificação: por ser genérico, ele pode ocultar itens que deveriam estar em subposições específicas (4407, 4408, 4412).
- Diretriz de Regex: não deve ser usado isoladamente para a classificação final, mas sim como um trigger de entrada para a análise de termos secundários.

### 1.2. O pilar da extração: TORAS (R$ 334.156.448,39)

Diferente do termo genérico, `TORAS` é um descritor técnico específico da posição 4403 (madeira em bruto).

- Análise de valor: o valor médio de R$ 215.306,98 é um dos mais altos da base. Isso indica que cada transação envolve volumes massivos (cargas completas).
- Validação NCM: 100% de aderência ao Capítulo 44.
- Diretriz de Regex: termo de inclusão imediata. Deve ser priorizado sobre termos como "tronco" ou "madeira bruta" pela sua frequência e valor.

## 2. Análise detalhada por categoria industrial

### 2.1. Painéis e chapas (posições 4410, 4411 e 4412)

Esta categoria é representada pelos termos `COMPENSADO`, `MDF`, `PLASTIFICADO` e `HDF`.

- COMPENSADO (R$ 137M): valor médio de R$ 18.049,34. Indica venda por paletes ou fardos. A posição NCM é 4412.
- MDF (R$ 137M): valor médio de R$ 411,05. Repare na discrepância: o MDF tem o mesmo valor total que o compensado, mas com 333.475 ocorrências (contra 7.613 do compensado). Isso prova que o MDF é vendido em unidades menores ou chapas avulsas, sendo o item de maior capilaridade da base.
- PLASTIFICADO (R$ 134M): este termo é um qualificador crítico. Refere-se ao compensado com filme fenólico para construção civil.
- Diretriz de Regex: o termo `PLASTIFICADO` deve ser condicionado à presença de `MADEIRA` ou `COMPENSADO` para evitar confusão com plásticos do Cap. 39.

### 2.2. Madeira serrada e beneficiada (posições 4407 e 4418)

- SERRADA (R$ 119M): valor médio de R$ 1.328,41. É o descritor padrão para a posição 4407.
- BENEFICIADA (R$ 44M): indica madeira que passou por plaina ou lixamento.
- TABUA (R$ 38M): com 88.108 ocorrências, é o termo popular para madeira serrada.
- Diretriz de Regex: criar um grupo de "serrados" que inclua `SERRADA`, `TABUA`, `VIGA`, `CAIBRO` e `RIPAS`.

## 3. Identificação de anomalias e falsos positivos

A análise de Valor Total permite identificar "intrusos" que, pelo alto faturamento, distorcem a base do Capítulo 44.

### 3.1. O conflito com o Capítulo 94 (móveis)

- COZINHA (R$ 21M): este termo é um falso positivo clássico. Cozinhas planejadas são móveis (9403).
- PLANEJADA (R$ 18M): reforça a exclusão.
- Diretriz de Regex: criar uma lista de exclusão (blacklist) contendo `COZINHA`, `PLANEJADA`, `ARMARIO` e `DORMITORIO`.

### 3.2. O conflito com o Capítulo 84 (máquinas)

- PICADOR (R$ 17M): embora processe madeira, é uma máquina.
- Diretriz de Regex: excluir termos que indiquem ferramentas ou máquinas industriais.

## 4. Análise de dimensões e padrões técnicos

A base de Valor Total mostra que a madeira é definida pelas suas medidas.

- 18MM (R$ 110M): é a espessura dominante. Quase sempre associada a MDF ou compensado.
- 1100X2200 (R$ 100M): medida padrão de chapas industriais.
- Diretriz de Regex: capturar padrões numéricos seguidos de `MM` ou `X` como validadores de itens do Capítulo 44.

## 5. Matriz de decisão para Regex (base: Valor Total)

| Termo | Ação | Justificativa Técnica |
| :--- | :--- | :--- |
| `TORAS` | INCLUIR | Posição 4403. Alto valor unitário e total. |
| `MDF` | INCLUIR | Posição 4411. Maior frequência da base. |
| `COMPENSADO` | INCLUIR | Posição 4412. Alto valor total. |
| `SERRADA` | INCLUIR | Posição 4407. Termo técnico de alto giro. |
| `COZINHA` | EXCLUIR | Capítulo 94. Móveis acabados. |
| `PICADOR` | EXCLUIR | Capítulo 84. Máquinas industriais. |
| `18MM` | VALIDAR | Marcador de espessura para painéis de madeira. |

## 6. Conclusão do Dossiê 01

A base de Valor Total mostra que o sucesso da classificação do Capítulo 44 depende de capturar os termos de alto giro industrial (`MDF`, `TORAS`, `SERRADA`) e de excluir com rigor móveis planejados e máquinas. O capital está concentrado na matéria-prima e nos painéis, que devem ser o foco principal do motor de busca.

Fim do Dossiê 01.
(Iniciando o processamento do Dossiê 02: Valor Médio.)
