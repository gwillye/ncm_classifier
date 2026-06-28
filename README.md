# Classificador NCM — Capítulo 44 (produtos de madeira)

Pipeline de **classificação/clusterização de textos** para apoiar a classificação fiscal
de produtos no **NCM (Nomenclatura Comum do Mercosul), capítulo 44 (madeira e suas obras)**.

## Método
- **Pré-processamento + N-gramas (BoW/TF-IDF)** das descrições de produto (ver `BoW e IDF.md`).
- **HDBSCAN** para clusterização não-supervisionada (`2.HDBSCAN.py`, `hdbscan_full.py`, `HDBSCAN_test/`).
- Notebooks de análise por categoria (`0.*`, `1.Execução_N_gram.ipynb`, `_analises_NCM/`).

## ⚠️ Dados não incluídos
As bases (`*.csv`/`*.txt`) são **dados do cliente (NDA)** e ficam fora do repositório
(ver `.gitignore`). O código demonstra a **metodologia**; rode com seus próprios dados de descrições NCM.

> Portfólio de **NLP/ML** (texto → features → clusterização). Outputs dos notebooks foram limpos; CPFs/CNPJs/e-mails anonimizados.
