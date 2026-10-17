# E-commerce Data Pipeline

## Objetivo

Construir um pipeline para coletar, tratar e disponibilizar dados de produtos a fim de viabilizar análise da relação entre desconto e avaliação.

## Pergunta de negócio

Produtos com maior desconto aplicado possuem avaliações (ratings) menores?

## Fonte de dados

DummyJSON API — https://dummyjson.com/products
Dados relevantes - preço, desconto, rating, categoria

## Como rodar

Requisito: Python 3.12 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.pipeline
```

O pipeline salva os dados brutos em `data/raw/` e o banco SQLite em `data/processed/ecommerce.db`.

Para conferir os dados no banco, rode (requer o cliente `sqlite3`, opcional):

```bash
sqlite3 data/processed/ecommerce.db "SELECT COUNT(*) FROM products;"
```

## Limitações conhecidas

A API oferece um catálogo estático de produtos, sem histórico de vendas ao longo do tempo.
Por isso, essa primeira versão do pipeline analisa o catálogo como um todo (sem quebra
por categoria ou variação temporal). A quebra por categoria fica planejada como evolução (v2).

Se o usuário rodar muitas vezes o projeto, vai gerar vários arquivos de dados brutos e pode pesar um pouco o projeto local.

## Status

Concluído — Sprint 0: estrutura inicial do projeto

Concluído — Sprint 1: extração dos dados

Concluído — Sprint 2: transformação/load dos dados

Em andamento — Sprint 3: refatoração e testes
