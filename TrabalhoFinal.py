import psycopg2 

# Variaveis

tables = {'HOTEL': (
    """CREATE TABLE hotel (
    id_hotel integer PRIMARY KEY NOT NULL,
    nome varchar(50),
    endereco text,
    contato text)"""),
    'FUNCIONARIO': (
        """CREATE TABLE funcionario (
        id_funcionario integer PRIMARY KEY NOT NULL,
        id_hotel integer,
        nome varchar(100),
        cpf varchar(14),
        tipo varchar(20),
        CHECK (tipo in ('Cozinheiro', 'Faxineiro', 'Manobrista', 'Recepcionista')),
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel))"""),
    'VAGA': (
        """CREATE TABLE vaga (
        id_vaga integer PRIMARY KEY NOT NULL,
        id_hotel integer,
        no_vaga integer,
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel))"""),
    'QUARTO': (
        """CREATE TABLE quarto (
        id_quarto integer PRIMARY KEY NOT NULL,
        no_quarto integer,
        id_hotel integer,
        id_funcionario integer,
        FOREIGN KEY(id_hotel) REFERENCES hotel(id_hotel),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario))"""),
    'PLANO': (
        """CREATE TABLE plano (
        id_plano integer PRIMARY KEY NOT NULL,
        nome varchar(20),
        descricao text,
        valor float)"""),
    'ITEM': (
        """CREATE TABLE item (
        id_item integer PRIMARY KEY NOT NULL,
        nome varchar(50),
        valor float)"""),
    'RESERVA': (
        """CREATE TABLE reserva (
        id_reserva integer PRIMARY KEY NOT NULL,
        data_entrada timestamp,
        data_saida timestamp,
        conta float,
        id_quarto integer,
        id_funcionario integer,
        id_plano integer,
        FOREIGN KEY(id_quarto) REFERENCES quarto(id_quarto),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario),
        FOREIGN KEY(id_plano) REFERENCES plano(id_plano))"""),
    'HOSPEDE': (
        """CREATE TABLE hospede (
        id_hospede integer PRIMARY KEY NOT NULL,
        nome varchar(100),
        cpf varchar(14),
        endereco text,
        contato text,
        id_reserva integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""),
    'VEICULO': (
        """CREATE TABLE veiculo (
        id_veiculo integer PRIMARY KEY NOT NULL,
        placa varchar(20),
        modelo varchar(50),
        cor varchar(30),
        id_vaga integer,
        id_funcionario integer,
        id_reserva integer,
        FOREIGN KEY(id_vaga) REFERENCES vaga(id_vaga),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario),
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""),
    'ANIMAL_ESTIMACAO': (
        """CREATE TABLE animal_estimacao (
        id_animal integer PRIMARY KEY NOT NULL,
        nome varchar(50),
        especie varchar(50),
        peso float,
        id_reserva integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva))"""),
    'PEDIDO': (
        """CREATE TABLE pedido (
        id_pedido integer PRIMARY KEY NOT NULL,
        valor float,
        id_reserva integer,
        id_item integer,
        id_funcionario integer,
        FOREIGN KEY(id_reserva) REFERENCES reserva(id_reserva),
        FOREIGN KEY(id_item) REFERENCES item(id_item),
        FOREIGN KEY(id_funcionario) REFERENCES funcionario(id_funcionario))"""),
}

drop = {'HOSPEDE': (
    "DROP TABLE hospede"),
    'VEICULO': (
        "DROP TABLE veiculo"),
    'ANIMAL_ESTIMACAO': (
        "DROP TABLE animal_estimacao"),
    'PEDIDO': (
        "DROP TABLE pedido"),
    'ITEM': (
        "DROP TABLE item"),
    'VAGA': (
        "DROP TABLE vaga"),
    'RESERVA': (
        "DROP TABLE reserva"),
    'QUARTO': (
        "DROP TABLE quarto"),
    'FUNCIONARIO': (
        "DROP TABLE funcionario"),
    'HOTEL': (
        "DROP TABLE hotel"),
    'PLANO': (
        "DROP TABLE plano"),
}

# Funçoes

def conectar_banco():
    conn = psycopg2.connect(
        dbname="TrabalhoFinal",
        user="postgres",
        password="12345",
        host="localhost"
    )
    cur = conn.cursor()
    print ("Conexão com o banco bem sucedida!")
    print('PostgreSQL versao:')
    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print(db_version)
    cur.close()
    return conn

def criar_todas_as_tabelas(conn):
    cur = conn.cursor()

    for table_name in tables:
        table_description = tables[table_name]
        try:
            cur.execute(table_description)
        except psycopg2.Error as e:
            print ("Erro ao criar tabelas")
            print (e.pgcode)
            print (e.pgerror)
        else:
            print("Tabela criada com sucesso!")
    conn.commit()
    cur.close()

def remover_todas_as_tabelas(conn):
    cur = conn.cursor()

    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            cur.execute(drop_description)
        except psycopg2.Error as e:
            print ("Erro ao remover tabelas")
            print (e.pgcode)
            print (e.pgerror)
        else:
            print("Tabela removida com sucesso!")
    conn.commit()
    cur.close()

def consulta_individual(conn):
    cur = conn.cursor()

    for table_name in tables:
        print (f"Nome: {table_name}")
    try:
        name = input("Digita o nome da tabela que deseja consultar: ").upper()
        select = "SELECT * FROM " + name
        cur.execute(select)
    except psycopg2.Error as e:
        print ("Erro ao consultar tabela")
        print (e.pgcode)
        print (e.pgerror)
    else:
        print (f"TABELA {name}")
        result = cur.fetchall()
        for x in result:
            print(x)
    cur.close()

def insert(conn):
    cur = conn.cursor()

    for table_name in tables:
        print (f"Nome: {table_name}")
    try:
        name = input("Digite o nome da tabela que deseja consultar: ").upper()
        for table_name in tables:
            table_description = tables[table_name]
            if (table_name == name):
                print (f"A tabela foi criada usando o seguinte código: \n{table_description}")
                new_value = input("Insira os valores em uma tupla. Ex: (101, ABC, 123):\n")
                query = ['INSERT INTO ', name, ' VALUES ', new_value]
                sql = ''.join(query)
                cur.execute(sql)
    except psycopg2.Error as e:
        print ("Erro ao inserir valores")
        print (e.pgcode)
        print (e.pgerror)
    else:
        print (f"Valores Inseridos com sucesso!")

    conn.commit()
    cur.close()

# MAIN

try:
    conn = conectar_banco()
    exit = 0

    while exit == 0:
        opcoes = """\n
        Gerenciador do Banco de Dados
        1 - Criar todas as tabelas
        2 - Inserir todos os valores
        3 - Insert
        4 - Update
        5 - Delete
        6 - Consulta 01
        7 - Consulta 02
        8 - Consulta 03
        9 - Consulta Tabela Individual
        10 - Consulta Text2SQL
        11 - Remover todas as tabelas
        12 - TESTE Listar todas as tabelas
        0 - Sair do Programa \n"""
        print(opcoes)

        escolha = int(input("Opção: "))
        if (escolha < 0 or escolha > 12):
            print("Digite uma das opções listadas")
            escolha = int(input("Opção: "))

        if (escolha == 0):
            exit = 1
            conn.close()
            print ("Conexão com o banco de Dados encerrada")

        if (escolha == 1):
            criar_todas_as_tabelas(conn)
        
        if (escolha == 3):
            insert(conn)

        if (escolha == 9):
            consulta_individual(conn)
        
        if (escolha == 11):
            remover_todas_as_tabelas(conn)
    conn.close()

except psycopg2.Error as e:
    print ("Erro encontrado no banco de dados")
    print (e.pgcode)
    print (e.pgerror)