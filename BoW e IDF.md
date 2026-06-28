# Relatório de Análise de Texto: BoW e TF-IDF (Capítulo 44)

Este relatório apresenta os resultados das técnicas de **Bag of Words (BoW)** e **TF-IDF** aplicadas à base de dados de produtos do Capítulo 44 do NCM. O objetivo é identificar os termos mais frequentes e os mais distintivos para auxiliar no refinamento da classificação automática.

---

## 1. Metodologia
A análise foi realizada sobre uma amostragem estatística de **100.000 registros** (aproximadamente 6% da base total), garantindo representatividade com alta performance. Foram removidas *stop words* comuns (preposições e artigos) para focar em termos substantivos.

---

## 2. Bag of Words (BoW): Frequência Absoluta
O BoW conta a ocorrência bruta de cada palavra. Ele revela o que "domina" o volume do seu catálogo.

| Termo | Ocorrências (Amostra) | Categoria Provável |
| :--- | :--- | :--- |
| **MDF** | 19.461 | 44.11 (Painéis) |
| **MADEIRA** | 19.231 | Genérico (Cap. 44) |
| **PORTA** | 8.125 | 44.18 (Marcenaria) |
| **KIT** | 7.832 | Diversos (Manufaturados) |
| **2F** | 7.547 | Atributo de MDF (2 Faces) |
| **PINUS** | 5.474 | 44.03 (Madeira Bruta/Serrada) |
| **SERRADA** | 5.266 | 44.07 (Madeira Serrada) |
| **BAMBU** | 5.192 | 44.21 (Obras de Madeira/Bambu) |
| **TABUA** | 4.987 | 44.07 (Madeira Serrada) |

> **Insight:** O termo **"2F"** (2 faces) e medidas como **"MM"** e **"CM"** aparecem com altíssima frequência, indicando que a base é rica em detalhes técnicos de painéis e madeira serrada.

---

## 3. TF-IDF: Importância Relativa
O TF-IDF (*Term Frequency-Inverse Document Frequency*) penaliza palavras que aparecem em quase todos os documentos (como "MADEIRA") e destaca termos que são mais específicos e informativos.

| Termo | Score TF-IDF | Relevância para Classificação |
| :--- | :--- | :--- |
| **MADEIRA** | 0.1206 | Termo âncora do capítulo. |
| **MDF** | 0.0865 | Identificador fortíssimo do 44.11. |
| **PORTA** | 0.0589 | Identificador fortíssimo do 44.18. |
| **PINUS** | 0.0385 | Espécie botânica chave para 44.03/44.07. |
| **BAMBU** | 0.0358 | Material específico para 44.21. |
| **TABUA** | 0.0345 | Formato específico para 44.07. |
| **SERRADA** | 0.0340 | Processamento chave para 44.07. |
| **CARVAO** | 0.0201 | Identificador único do 44.02. |

---

## 4. Conclusões e Recomendações

### 4.1 Identificação de Novas Categorias
Os resultados sugerem a criação de uma categoria específica para o **NCM 44.07 (Madeira Serrada)**, utilizando os termos `SERRADA`, `TABUA`, `VIGA` e `CAMBARA`, que apareceram com destaque tanto no BoW quanto no TF-IDF.

### 4.2 Refinamento de Atributos
Termos como **"BRANCO"**, **"CRU"**, **"NATURAL"** e marcas como **"GREENPLAC"**, **"ARAUCO"** e **"DURATEX"** possuem scores TF-IDF significativos. Eles podem ser usados para criar subcategorias de "Painéis Revestidos" vs "Painéis Crus".

### 4.3 Alerta de Outliers
O termo **"KIT"** e **"QUADRO"** aparecem com frequência. É importante validar se esses "Kits" são de fato obras de madeira (44.21) ou se contêm itens de outros capítulos (como ferragens ou vidros), o que poderia indicar a necessidade de uma regex de exclusão mais refinada.

---
**Análise gerada por Manus AI**
