import psycopg2 as pg


def connect():
    try:
        conn = pg.connect(
            dbname="postgres",
            user="postgres",
            password="clinicamedica",
            host="clinica-medica.cc0h3awq4n8e.us-east-1.rds.amazonaws.com",
            port="5432"
        )
        return conn
    except pg.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def inserir_paciente(nome, cep, num_residencia, telefone,sexo,cpf):
    conn = connect()
    if conn is None:
        return  # Encerra a função se não conseguir conectar
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mydb.pacientes(nome, cep, num_residencia, telefone,sexo,cpf) VALUES (%s, %s, %s, %s,%s,%s)",
            (nome, cep, num_residencia, telefone,sexo,cpf)
        )
        conn.commit()
        print("Paciente inserido com sucesso.")
    except pg.DatabaseError as e:
        print(f"Erro ao inserir paciente: {e}")
        conn.rollback()  # Desfaz a transação em caso de erro
    finally:
        if conn:
            cursor.close()  # Fecha o cursor antes de fechar a conexão
            conn.close()


def consultar_pacientes():
    conn = connect()
    if conn is None:
        return  # Encerra a função se não conseguir conectar
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mydb.pacientes")
        result = cursor.fetchall()
        return result
    except pg.DatabaseError as e:
        print(f"Erro ao consultar pacientes: {e}")
        return []
    finally:
        if conn:
            cursor.close()  # Fecha o cursor antes de fechar a conexão
            conn.close()


def main():
    inserir_paciente("João", "12345678", "123", "12345678", "M", "12345678901")
    pacientes = consultar_pacientes()

    if pacientes:
        print("Pacientes cadastrados:")
        for paciente in pacientes:
            print(paciente)
    else:
        print("Nenhum paciente cadastrado.")


if __name__ == "__main__":
    main()
