import mysql.connector

def conectar():

    #Estabelece a conexão com o banco de dados.

    # Conecta no banco de dados "eleicao" criado na Etapa 1
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  # Altere para a senha do seu banco, se for diferente
        database="eleicao"
    )
    
    return conexao