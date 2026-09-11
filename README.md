# E-commerce Data Pipeline

## Objetivo

Construir um pipeline para coletar, tratar e disponibilizar dados de produtos a fim de viabilizar análise da relação entre desconto e avaliação.

## Pergunta de negócio

Produtos com maior desconto aplicado possuem avaliações (ratings) menores?

## Fonte de dados

DummyJSON API — https://dummyjson.com/products
[1 frase: o que a API oferece — catálogo de produtos com preço, desconto, categoria, rating, estoque]

## Limitações conhecidas

A API oferece um catálogo estático de produtos, sem histórico de vendas ao longo do tempo.
Por isso, essa primeira versão do pipeline analisa o catálogo como um todo (sem quebra
por categoria ou variação temporal). A quebra por categoria fica planejada como evolução (v2).

## Status

🚧 Em construção — Sprint 0: estrutura inicial do projeto
