import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

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


def listar_tabelas_definidas():
   print("Tabelas definidas no dicionário:")
   for table_name in tables:
      print(f"- {table_name}")


MENU = """
Gerenciador do Banco de Dados
1  Criar todas as tabelas
2  Inserir todos os valores (não implementado)
3  Insert
4  Update
5  Delete
6  Consulta 01 (não implementado)
7  Consulta 02 (não implementado)
8  Consulta 03 (não implementado)
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
               print("Opção 2 ainda não implementada.")
         elif escolha == '3':
               insert(conn)
         elif escolha == '4':
               update(conn)
         elif escolha == '5':
               delete(conn)
         elif escolha == '6':
               print("Opção 6 ainda não implementada.")
         elif escolha == '7':
               print("Opção 7 ainda não implementada.")
         elif escolha == '8':
               print("Opção 8 ainda não implementada.")
         elif escolha == '9':
               consulta_individual(conn)
         elif escolha == '10':
               print("Opção 10 Text2SQL ainda não implementada.")
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