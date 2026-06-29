# Classificador NCM, Capítulo 44 (produtos de madeira)

Este é um pipeline de classificação e clusterização de textos para apoiar a classificação fiscal de produtos no NCM (Nomenclatura Comum do Mercosul), focado no capítulo 44, que cobre madeira e suas obras.

A ideia central é pegar descrições de produtos escritas em texto livre e organizá-las em grupos coerentes, de forma a apoiar quem precisa enquadrar esses produtos no código fiscal correto. O trabalho foi feito no contexto de um projeto para uma secretaria de fazenda estadual, voltado à detecção de inconsistências fiscais, e funciona como companheiro de um módulo separado que usa um LLM como julgador.

## Como funciona

O fluxo vai de texto para features e depois para clusterização:

- Pré-processamento das descrições de produto seguido de extração de N-gramas com Bag of Words e TF-IDF. Os detalhes dessa etapa estão documentados em `BoW e IDF.md`.
- Clusterização não supervisionada com HDBSCAN, implementada em `2.HDBSCAN.py`, `hdbscan_full.py` e na pasta `HDBSCAN_test/`.
- Notebooks de análise por categoria, organizados nos arquivos `0.*`, em `1.Execução_N_gram.ipynb` e na pasta `_analises_NCM/`.

A escolha do HDBSCAN se justifica porque não exige definir o número de clusters de antemão e lida bem com ruído, o que é útil quando as descrições de produto vêm bagunçadas e em volume variável.

## Dados não incluídos

As bases de dados (arquivos `.csv` e `.txt`) são dados do cliente, cobertos por NDA, e por isso ficam fora do repositório (ver `.gitignore`). O código aqui demonstra a metodologia, não os dados em si. Para rodar, use suas próprias descrições de produtos com codificação NCM.

## Como rodar

Os notebooks e scripts assumem que você vai fornecer seus próprios dados de descrições NCM no lugar das bases originais. O caminho recomendado é começar pela extração de N-gramas (`1.Execução_N_gram.ipynb`), seguir para a clusterização com HDBSCAN (`2.HDBSCAN.py` ou `hdbscan_full.py`) e então usar os notebooks de análise por categoria para inspecionar os grupos resultantes.

## Observações

Este projeto serve como portfólio de NLP e ML, percorrendo o caminho de texto para features para clusterização. Os outputs dos notebooks foram limpos antes da publicação, e dados sensíveis como CPFs, CNPJs e e-mails foram anonimizados.
