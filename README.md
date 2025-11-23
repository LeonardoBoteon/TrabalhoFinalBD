# Sistema Integrado de Gestão Hoteleira

Este projeto implementa um sistema completo de gerenciamento hoteleiro utilizando Python e PostgreSQL, capaz de criar, popular e administrar um banco de dados relacional que simula o funcionamento real de um hotel. A aplicação gerencia reservas, hóspedes, funcionários, veículos, planos de estadia, pedidos de itens extras e animais de estimação hospedados. Além disso, o sistema inclui consultas analíticas com gráficos e um módulo de Inteligência Artificial capaz de interpretar consultas em linguagem natural e convertê-las automaticamente para SQL.

## Objetivo do Projeto

O objetivo deste trabalho é desenvolver um sistema de apoio à administração operacional e analítica de estabelecimentos hoteleiros. O projeto centraliza o gerenciamento de reservas, serviços, cobranças e recursos físicos (como quartos e vagas), permitindo:

* Controle de reservas, hóspedes e planos
* Registro de serviços adicionais com cobrança automática
* Gestão de veículos e animais de estimação hospedados
* Controle de funcionários por função específica
* Consultas analíticas com visualização gráfica
* Geração automática de consultas SQL a partir de linguagem natural

O sistema atende aos requisitos do trabalho final da disciplina Banco de Dados DEC7588 (UFSC), utilizando modelagem relacional, implementação prática e análises baseadas em dados.

## Modelagem do Banco

O sistema utiliza onze entidades principais, representando um cenário hoteleiro realista:

Hotel, Funcionário, Quarto, Vaga, Reserva, Hóspede, Veículo, Animal de Estimação, Pedido, Item e Plano.

### Modelo Conceitual (DER)

![Modelo Conceitual](./models/modelo_conceitual.png)

### Modelo Lógico

![Modelo lógico](./models/modelo_logico.png)

## Script DDL (Criação das Tabelas)

As tabelas são criadas automaticamente pelo código presente no arquivo `TrabalhoFinal.py`. O script implementa:

* Chaves primárias e estrangeiras
* Integridade referencial
* Restrição CHECK para o tipo de funcionário
* Tipos de dados adequados (inteiro, float, texto, timestamp)

## Tecnologias Utilizadas

| Tecnologia        | Finalidade                                      |
| ----------------- | ----------------------------------------------- |
| Python 3.x        | Implementação do sistema                        |
| PostgreSQL        | Banco de dados relacional                       |
| Psycopg2          | Conexão com PostgreSQL                          |
| Matplotlib        | Visualização de gráficos                        |
| NumPy             | Manipulação auxiliar de dados                   |
| Google Gemini API | Interpretação de consultas em linguagem natural |
| dotenv            | Segurança de variáveis de ambiente              |

## Como Executar o Sistema

### 1) Configuração das variáveis de ambiente

Criar um arquivo `.env` com:

```
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_NAME=nome_do_banco
GEMINI_API_KEY=sua_chave
GEMINI_MODEL=gemini-2.5-flash
```

### 2) Criação de ambiente virtual

```
python -m venv venv
```

### 3) Instalação das dependências

```
pip install -r requirements.txt
```

### 4) Execução do sistema

```
python TrabalhoFinal.py
```

### 5) Funcionalidades disponíveis

A aplicação permite:

* Criar e remover todas as tabelas do banco
* Inserir, atualizar e excluir registros
* Consultar qualquer tabela
* Executar consultas analíticas com gráficos
* Gerar consultas SQL a partir de linguagem natural
* Listar todas as tabelas

## Consultas Analíticas com Gráficos

Foram desenvolvidas três consultas que reúnem múltiplas tabelas, utilizam funções de agregação e representam visualmente os resultados:

| Consulta                      | Função Utilizada | Finalidade                             |
| ----------------------------- | ---------------- | -------------------------------------- |
| Valor gasto por hóspede       | SUM              | Identificar consumo de serviços extras |
| Receita por hotel e por plano | SUM              | Comparar lucratividade entre hotéis    |
| Média de dias hospedados      | AVG              | Analisar comportamento dos hóspedes    |

### Exemplo de Saída (Consulta 1)

| Hóspede        | Pedidos | Total Gasto (R$) |
| -------------- | ------- | ---------------- |
| João da Silva  | 2       | 33,00            |
| Maria Oliveira | 1       | 120,00           |
| Roberto Justus | 1       | 120,00           |
| Luciano Huck   | 0       | 0,00             |
| Fausto Silva   | 1       | 8,00             |

Esse resultado é apresentado também em forma de gráfico de barras, favorecendo análises de consumo.

## Módulo de Inteligência Artificial

O sistema inclui uma funcionalidade que permite consultar o banco de dados utilizando linguagem natural. O módulo:

1. Recebe uma pergunta em português.
2. Traduza para SQL de acordo com o esquema do banco.
3. Executa a consulta automaticamente.
4. Exibe o resultado com explicação textual.

Assim, o sistema amplia a acessibilidade às consultas, eliminando a necessidade de conhecimento prévio em SQL.

## Conclusão

O Sistema Integrado de Gestão Hoteleira demonstra como a modelagem de dados, aliada a uma implementação funcional, pode oferecer uma solução eficiente para a administração de hotéis. A estrutura relacional proporciona integridade e organização, enquanto os recursos analíticos e o módulo de Inteligência Artificial ampliam a capacidade de interpretação e uso das informações registradas. O projeto conclui de forma prática os conteúdos estudados na disciplina, apresentando possibilidades reais de expansão futura, como criação de interface gráfica, relatórios gerenciais mais sofisticados ou integração com plataformas corporativas.