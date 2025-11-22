import psycopg2
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Variaveis

tables = {
    'HOTEL': (
        """CREATE TABLE IF NOT EXISTS hotel (
        id_hotel integer PRIMARY KEY NOT NULL,
        nome varchar(50),
        endereco text,
        contato text)"""
    ),
    'PLANO': (
        """CREATE TABLE IF NOT EXISTS plano (
        id_plano integer PRIMARY KEY NOT NULL,
        nome varchar(20),
        descricao text,
        valor float)"""
    ),
    'FUNCIONARIO': (
        """CREATE TABLE IF NOT EXISTS funcionario (
        id_funcionario integer PRIMARY KEY NOT NULL,
        id_hotel integer,
        nome varchar(100),
        cpf varchar(14),
        tipo varchar(20),
        CHECK (tipo in ('Cozinheiro', 'Faxineiro', 'Manobrista', 'Recepcionista')),
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel))"""
    ),
    'VAGA': (
        """CREATE TABLE IF NOT EXISTS vaga (
        id_vaga integer PRIMARY KEY NOT NULL,
        id_hotel integer,
        no_vaga integer,
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel))"""
    ),
    'QUARTO': (
        """CREATE TABLE IF NOT EXISTS quarto (
        id_quarto integer PRIMARY KEY NOT NULL,
        no_quarto integer,
        id_hotel integer,
        id_funcionario integer,
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario))"""
    ),
    'ITEM': (
        """CREATE TABLE IF NOT EXISTS item (
        id_item integer PRIMARY KEY NOT NULL,
        nome varchar(50),
        valor float)"""
    ),
    'RESERVA': (
        """CREATE TABLE IF NOT EXISTS reserva (
        id_reserva integer PRIMARY KEY NOT NULL,
        data_entrada timestamp,
        data_saida timestamp,
        conta float,
        id_quarto integer,
        id_funcionario integer,
        id_plano integer,
        FOREIGN KEY(id_quarto) REFERENCES quarto(id_quarto),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario),
        FOREIGN KEY(id_plano) REFERENCES plano(id_plano))"""
    ),
    'HOSPEDE': (
        """CREATE TABLE IF NOT EXISTS hospede (
        id_hospede integer PRIMARY KEY NOT NULL,
        nome varchar(100),
        cpf varchar(14),
        endereco text,
        contato text,
        id_reserva integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""
    ),
    'VEICULO': (
        """CREATE TABLE IF NOT EXISTS veiculo (
        id_veiculo integer PRIMARY KEY NOT NULL,
        placa varchar(20),
        modelo varchar(50),
        cor varchar(30),
        id_vaga integer,
        id_funcionario integer,
        id_reserva integer,
        FOREIGN KEY(id_vaga) REFERENCES vaga(id_vaga),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario),
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""
    ),
    'ANIMAL_ESTIMACAO': (
        """CREATE TABLE IF NOT EXISTS animal_estimacao (
        id_animal integer PRIMARY KEY NOT NULL,
        nome varchar(50),
        especie varchar(50),
        peso float,
        id_reserva integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""
    ),
    'PEDIDO': (
        """CREATE TABLE IF NOT EXISTS pedido (
        id_pedido integer PRIMARY KEY NOT NULL,
        valor float,
        id_reserva integer,
        id_item integer,
        id_funcionario integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva),
        FOREIGN KEY(id_item) REFERENCES item(id_item),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario))"""
    ),
}

inserts = {'HOTEL': (
    """INSERT INTO hotel (id_hotel, nome, endereco, contato) values
    (1, 'Hotel Grand Plaza', 'Av. Atlântica, 1000 - Rio de Janeiro', '21-5555-0001'),
    (2, 'Pousada Serra Verde', 'Rua das Flores, 50 - Gramado', '54-5555-0002'),
    (3, 'Resort Beira Mar', 'Rodovia do Sol, Km 10 - Bahia', '71-5555-0003')"""),
    'PLANO': (
        """INSERT INTO plano (id_plano, nome, descricao, valor) values
        (1, 'Standard', 'Apenas café da manhã', 250.00),
        (2, 'Premium', 'Café e Jantar inclusos', 400.00),
        (3, 'Deluxe', 'Todas as refeições e bebidas', 800.00)"""),
    'ITEM': (
        """INSERT INTO item (id_item, nome, valor) values
        (1, 'Refrigerante Lata', 8.00),
        (2, 'Sanduíche Natural', 25.00),
        (3, 'Jantar Especial', 120.00)"""),
    'FUNCIONARIO': (
        """INSERT INTO funcionario (id_funcionario, id_hotel, nome, cpf, tipo) values
        (1, 1, 'Carlos Silva', '111.111.111-01', 'Faxineiro'),
        (2, 1, 'Ana Pereira', '111.111.111-02', 'Recepcionista'),
        (3, 1, 'Roberto Santos', '111.111.111-03', 'Manobrista'),
        (4, 1, 'Eduardo da Silva', '111.111.111-04', 'Cozinheiro'),
        (5, 2, 'Mariana Costa', '222.222.222-01', 'Faxineiro'),
        (6, 2, 'Paulo Lima', '222.222.222-02', 'Recepcionista'),
        (7, 2, 'Fernanda Alves', '222.222.222-03', 'Manobrista'),
        (8, 2, 'Augusto Vieira', '222.222.222-04', 'Cozinheiro'),
        (9, 3, 'Ricardo Oliveira', '333.333.333-01', 'Faxineiro'),
        (10, 3, 'Juliana Mendes', '333.333.333-02', 'Recepcionista'),
        (11, 3, 'Lucas Martins', '333.333.333-03', 'Manobrista'),
        (12, 3, 'Mauricio Ferreira', '333.333.333-04', 'Cozinheiro')"""),
    'QUARTO': (
        """INSERT INTO quarto (id_quarto, no_quarto, id_hotel, id_funcionario) values
        (1, 101, 1, 1),
        (2, 102, 1, 1),
        (3, 201, 1, 1),
        (4, 10, 2, 5),
        (5, 11, 2, 5),
        (6, 12, 2, 5),
        (7, 501, 3, 9), 
        (8, 502, 3, 9), 
        (9, 503, 3, 9)"""),
    'VAGA': (
        """INSERT INTO vaga (id_vaga, id_hotel, no_vaga) values
        (1, 1, 10),
        (2, 1, 11),
        (3, 1, 12),
        (4, 2, 1),
        (5, 2, 2),
        (6, 3, 100),
        (7, 3, 101),
        (8, 3, 102)"""),
    'RESERVA': (
        """INSERT INTO reserva (id_reserva, data_entrada, data_saida, conta, id_quarto, id_funcionario, id_plano) values
        (1, '2023-10-01 14:00', '2023-10-05 12:00', 1200.00, 1, 2, 1),
        (2, '2023-10-02 14:00', '2023-10-03 12:00', 400.00, 2, 2, 2),
        (3, '2023-11-10 10:00', '2023-11-15 10:00', 2500.00, 4, 6, 3),
        (4, '2023-11-12 14:00', '2023-11-14 12:00', 800.00, 5, 6, 2),
        (5, '2023-12-20 12:00', '2023-12-27 12:00', 5600.00, 7, 10, 3),
        (6, '2023-12-21 12:00', '2023-12-22 12:00', 800.00, 8, 10, 3),
        (7, '2024-01-05 14:00', '2024-01-10 12:00', 1500.00, 3, 2, 1),
        (8, '2024-01-06 14:00', '2024-01-08 12:00', 600.00, 6, 6, 3)"""),
    'HOSPEDE': (
        """INSERT INTO hospede (id_hospede, nome, cpf, endereco, contato, id_reserva) values
        (1, 'João da Silva', '999.888.777-01', 'São Paulo, SP', 'joao@email.com', 1),
        (2, 'Maria Oliveira', '888.777.666-02', 'Belo Horizonte, MG', 'maria@email.com', 2),
        (3, 'Pedro Santos', '777.666.555-03', 'Curitiba, PR', 'pedro@email.com', 3),
        (4, 'Cláudia Raia', '666.555.444-04', 'Rio de Janeiro, RJ', 'claudia@email.com', 4),
        (5, 'Roberto Justus', '555.444.333-05', 'São Paulo, SP', 'justus@email.com', 5),
        (6, 'Luciano Huck', '444.333.222-06', 'Angra, RJ', 'luciano@email.com', 6),
        (7, 'Xuxa Meneghel', '333.222.111-07', 'Santa Rosa, RS', 'xuxa@email.com', 7),
        (8, 'Fausto Silva', '222.111.000-08', 'São Paulo, SP', 'faustao@email.com', 8)"""),
    'ANIMAL_ESTIMACAO': (
        """INSERT INTO animal_estimacao (id_animal, nome, especie, peso, id_reserva) values
        (1, 'Rex', 'Cachorro', 12.5, 3),
        (2, 'Mimi', 'Gato', 4.0, 3),
        (3, 'Thor', 'Cachorro', 25.0, 8)"""),
    'VEICULO': (
        """INSERT INTO veiculo (id_veiculo, placa, modelo, cor, id_vaga, id_funcionario, id_reserva) values
        (1, 'ABC-1234', 'Honda Civic', 'Prata', 1, 3, 1),
        (2, 'DEF-5678', 'Fiat Toro', 'Vermelho', 4, 7, 3),
        (3, 'GHI-9012', 'BMW X5', 'Preto', 6, 11, 5),
        (4, 'JKL-3456', 'Porsche Cayenne', 'Branco', 7, 11, 6),
        (5, 'MNO-7890', 'Jeep Compass', 'Cinza', 2, 3, 7)"""),
    'PEDIDO': (
        """INSERT INTO pedido (id_pedido, valor, id_reserva, id_item, id_funcionario) values
        (1, 8.00, 1, 1, 4),
        (2, 25.00, 1, 2, 4),
        (3, 120.00, 2, 3, 4),
        (4, 120.00, 5, 3, 12),
        (5, 8.00, 8, 1, 8)"""
    )}

drop = {
    'HOSPEDE': "DROP TABLE IF EXISTS hospede CASCADE",
    'VEICULO': "DROP TABLE IF EXISTS veiculo CASCADE",
    'ANIMAL_ESTIMACAO': "DROP TABLE IF EXISTS animal_estimacao CASCADE",
    'PEDIDO': "DROP TABLE IF EXISTS pedido CASCADE",
    'ITEM': "DROP TABLE IF EXISTS item CASCADE",
    'VAGA': "DROP TABLE IF EXISTS vaga CASCADE",
    'RESERVA': "DROP TABLE IF EXISTS reserva CASCADE",
    'QUARTO': "DROP TABLE IF EXISTS quarto CASCADE",
    'FUNCIONARIO': "DROP TABLE IF EXISTS funcionario CASCADE",
    'HOTEL': "DROP TABLE IF EXISTS hotel CASCADE",
    'PLANO': "DROP TABLE IF EXISTS plano CASCADE",
}

# Funcoes

def conectar_banco():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    cur = conn.cursor()
    print("Conexão com o banco bem sucedida!")
    print("PostgreSQL versão:")
    cur.execute("SELECT version()")
    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return conn


def criar_todas_as_tabelas(conn):
    cur = conn.cursor()
    for table_name, table_description in tables.items():
        try:
            cur.execute(table_description)
            conn.commit()
            print(f"Tabela {table_name} criada com sucesso!")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Erro ao criar a tabela {table_name}")
            print(e.pgcode)
            print(e.pgerror)
    cur.close()

def inserir_valores(conn):
    cur = conn.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            cur.execute(insert_description)
        except psycopg2.Error as e:
            print ("Erro ao inserir valores")
            print (e.pgcode)
            print (e.pgerror)
        else:
            print ("Valores inseridos com sucesso!")
    conn.commit()
    cur.close()

def remover_todas_as_tabelas(conn):
    cur = conn.cursor()
    for drop_name, drop_description in drop.items():
        try:
            cur.execute(drop_description)
            conn.commit()
            print(f"Tabela {drop_name} removida, se existia.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Erro ao remover tabela {drop_name}")
            print(e.pgcode)
            print(e.pgerror)
    cur.close()


def consulta_individual(conn):
    cur = conn.cursor()
    for table_name in tables:
        print(f"Nome: {table_name}")
    try:
        name = input("Digite o nome da tabela que deseja consultar: ").upper().strip()
        print (f"A tabela foi gerada usando o seguinte codigo: \n{tables[name]}")
        select = "SELECT * FROM " + name
        cur.execute(select)
    except psycopg2.Error as e:
        print("Erro ao consultar tabela")
        print(e.pgcode)
        print(e.pgerror)
    else:
        print(f"TABELA {name}")
        result = cur.fetchall()
        for x in result:
            print(x)
    cur.close()


def insert(conn):
    cur = conn.cursor()
    for table_name in tables:
        print(f"Nome: {table_name}")
    try:
        name = input("Digite o nome da tabela onde deseja inserir: ").upper().strip()
        for table_name, table_description in tables.items():
            if table_name == name:
                print(f"A tabela foi criada usando o seguinte código: \n{table_description}")
                new_value = input("Insira os valores em uma tupla. Ex: (101, 'ABC', 123):\n")
                query = ["INSERT INTO ", name, " VALUES ", new_value]
                sql = "".join(query)
                cur.execute(sql)
                conn.commit()
                print("Valores inseridos com sucesso!")
                break
        else:
            print("Tabela não encontrada.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao inserir valores")
        print(e.pgcode)
        print(e.pgerror)
    finally:
        cur.close()


def update(conn):
    cur = conn.cursor()
    for table_name in tables:
        print(f"Nome: {table_name}")
    try:
        name = input("Digite o nome da tabela que deseja atualizar: ").upper().strip()
        for table_name, table_description in tables.items():
            if table_name == name:
                print(f"A tabela foi criada usando o seguinte código: \n{table_description}")
                atributo = input("Digite o atributo a ser alterado: ").strip()
                valor = input("Digite o valor a ser atribuído (como você escreveria no SQL): ").strip()
                codigo_f = input("Digite o nome da coluna da chave primária: ").strip()
                codigo = input("Digite o valor numérico da chave primária: ").strip()
                query = [
                    "UPDATE ", name,
                    " SET ", atributo, " = ", valor,
                    " WHERE ", codigo_f, " = ", codigo
                ]
                sql = "".join(query)
                cur.execute(sql)
                conn.commit()
                print("Valor atualizado com sucesso!")
                break
        else:
            print("Tabela não encontrada.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao atualizar valor")
        print(e.pgcode)
        print(e.pgerror)
    finally:
        cur.close()


def delete(conn):
    cur = conn.cursor()
    for table_name in tables:
        print(f"Nome: {table_name}")
    try:
        name = input("Digite o nome da tabela que deseja alterar: ").upper().strip()
        for table_name, table_description in tables.items():
            if table_name == name:
                print(f"A tabela foi criada usando o seguinte código: \n{table_description}")
                codigo_f = input("Digite o nome da coluna da chave primária: ").strip()
                codigo = input("Digite o valor numérico da chave primária: ").strip()
                query = [
                    "DELETE FROM ", name,
                    " WHERE ", codigo_f, " = ", codigo
                ]
                sql = "".join(query)
                cur.execute(sql)
                conn.commit()
                print("DELETE realizado com sucesso!")
                break
        else:
            print("Tabela não encontrada.")
    except psycopg2.Error as e:
        conn.rollback()
        print("Erro ao realizar o DELETE")
        print(e.pgcode)
        print(e.pgerror)
    finally:
        cur.close()


def consulta01(conn):
    cur = conn.cursor()

    select_query = """
SELECT 
    h.nome AS nome_hospede,
    COUNT(p.id_pedido) AS total_pedidos_realizados,
    SUM(i.valor) AS valor_total_gasto
FROM 
    hospede h
JOIN 
    reserva r ON h.id_reserva = r.id_reserva
JOIN 
    pedido p ON r.id_reserva = p.id_reserva
JOIN 
    item i ON p.id_item = i.id_item
GROUP BY 
    h.nome
ORDER BY 
    valor_total_gasto DESC"""

    print ("Primeira Consulta: calcula o valor total gasto com pedidos extras (serviço de quarto/itens) por cada hóspede. "
            "Ela relaciona o hóspede à sua reserva e aos pedidos e itens solicitados durante a estadia")
    cur.execute(select_query)
    result = cur.fetchall()
    for x in result:
        print(x)
    
    cur.close()

def consulta02(conn):
    cur = conn.cursor()

    select_query = """
SELECT 
    hot.nome AS nome_hotel,
    pl.nome AS nome_plano,
    COUNT(r.id_reserva) AS quantidade_reservas,
    SUM(r.conta) AS receita_total
FROM 
    hotel hot
JOIN 
    quarto q ON hot.id_hotel = q.id_hotel
JOIN 
    reserva r ON q.id_quarto = r.id_quarto
JOIN 
    plano pl ON r.id_plano = pl.id_plano
GROUP BY 
    hot.nome, pl.nome;"""

    print ("Segunda Consulta: Analisa a receita gerada pelas reservas,"
        " agrupada pelo nome do hotel e pelo tipo de plano escolhido")
    cur.execute(select_query)
    result = cur.fetchall()
    for x in result:
        print (x)
    
    cur.close()

def consulta03(conn):
    cur = conn.cursor()
    
    select_query = """
SELECT 
    h.nome AS nome_hotel,
    COUNT(r.id_reserva) AS total_reservas,
    AVG(EXTRACT(DAY FROM (r.data_saida - r.data_entrada))) AS media_dias_estadia
FROM 
    hotel h
JOIN 
    quarto q ON h.id_hotel = q.id_hotel
JOIN 
    reserva r ON q.id_quarto = r.id_quarto
GROUP BY 
    h.nome
ORDER BY 
    media_dias_estadia DESC;"""

    print ("Terceira Consulta: Calcula quantos dias, em média, os hóspedes ficam em cada hotel")
    cur.execute(select_query)
    result = cur.fetchall()
    for x in result:
        print (x)
        
    cur.close()

def text2sql(conn, GEMINI_API_KEY, tables):
    cur = conn.cursor()
    consulta = input("Utilizando linguagem natural, descreva a consulta desejada: ")
    genai_client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f'''Considering the database {tables}, 
            write an SQL query to answer the query: "{consulta}". 
            The generated queries must attribute an alias for 
            each column when is not used the column name. 
            In the answer, present only the SQL query without any formatting or line breaks as a string, 
            without the ";" character at the end and without the "\" character''' 
    response = genai_client.models.generate_content(
        model="gemini-2.5-flash", contents=[prompt], config=types.GenerateContentConfig(
            temperature = 0.0
        )
    )
    cur.execute(response.text)
    result = cur.fetchall()
    for x in result:
        print (x)
    
    cur.close()


def listar_tabelas_definidas():
    print("Tabelas definidas no dicionário:")
    for table_name in tables:
        print(f"- {table_name}")


MENU = """
Gerenciador do Banco de Dados
1  Criar todas as tabelas
2  Inserir todos os valores
3  Insert
4  Update
5  Delete
6  Consulta 01
7  Consulta 02
8  Consulta 03
9  Consulta Tabela Individual
10 Consulta Text2SQL (não implementado)
11 Remover todas as tabelas
12 Listar tabelas definidas
0  Sair do Programa
> """


def main():
    try:
        conn = conectar_banco()
    except psycopg2.Error as e:
        print("Erro encontrado no banco de dados")
        print(e.pgcode)
        print(e.pgerror)
        return
    except Exception as e:
        print(f"Erro inesperado ao conectar: {e}")
        return

    opcoes_validas = {str(i) for i in range(13)}  # '0' a '12'

    try:
        while True:
            escolha = input(MENU).strip()
            if escolha not in opcoes_validas:
                print("Digite uma das opções listadas")
                continue

            if escolha == '0':
                print("Conexão com o banco de dados encerrada")
                break

            if escolha == '1':
                criar_todas_as_tabelas(conn)
            elif escolha == '2':
                inserir_valores(conn)
            elif escolha == '3':
                insert(conn)
            elif escolha == '4':
                update(conn)
            elif escolha == '5':
                delete(conn)
            elif escolha == '6':
                consulta01(conn)
            elif escolha == '7':
                consulta02(conn)
            elif escolha == '8':
                consulta03(conn)
            elif escolha == '9':
                consulta_individual(conn)
            elif escolha == '10':
                text2sql(conn, GEMINI_API_KEY, tables)
            elif escolha == '11':
                remover_todas_as_tabelas(conn)
            elif escolha == '12':
                listar_tabelas_definidas()

        conn.close()
    except ValueError:
        print("Valor inválido")
    except Exception as e:
        print(f"Erro inesperado em tempo de execução: {e}")
        conn.close()


if __name__ == "__main__":
    main()