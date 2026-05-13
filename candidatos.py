from gerenciamento import pausar_e_limpar 

def cadastrar_candidato(cursor, conexao):

    #Cadastra um novo candidato na base de dados.

    print("\n--- CADASTRO DE NOVO CANDIDATO ---")
    nome = input("Nome do candidato: ")
    digito = input("Número de votação (dígito numérico): ")
    partido = input("Partido: ")

    # Verifica se o número já existe (RF001.10)
    cursor.execute(f"SELECT * FROM Candidatos WHERE digito_candidatos = '{digito}'")
    if len(cursor.fetchall()) > 0:
        print("\n[Erro] Já existe um candidato registado com este número.")
    else:
        cursor.execute("INSERT INTO Candidatos (digito_candidatos, nome_candidato, partido_candidatos) VALUES (%s, %s, %s)", (digito, nome, partido))
        conexao.commit()
        print(f"\n[Sucesso] Candidato {nome} cadastrado com o número {digito}!")

    pausar_e_limpar()

def editar_candidato(cursor, conexao):
 
    #Edita o nome e partido de um candidato existente.
    
    print("\n--- EDITAR DADOS DO CANDIDATO ---")
    digito = input("Digite o número do candidato que deseja editar: ")

    cursor.execute(f"SELECT nome_candidato, partido_candidatos FROM Candidatos WHERE digito_candidatos = '{digito}'")
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("\n[Erro] Candidato não encontrado.")
    else:
        candidato = resultado[0]
        print(f"Dados atuais -> Nome: {candidato[0]} | Partido: {candidato[1]}")
        novo_nome = input("Novo nome (ou aperte ENTER para manter o mesmo): ")
        novo_partido = input("Novo partido (ou aperte ENTER para manter o mesmo): ")

        if novo_nome == "":
            novo_nome = candidato[0]
        if novo_partido == "":
            novo_partido = candidato[1]

        cursor.execute("UPDATE Candidatos SET nome_candidato = %s, partido_candidatos = %s WHERE digito_candidatos = %s", (novo_nome, novo_partido, digito))
        conexao.commit()
        print("\n[Sucesso] Dados do candidato atualizados!")

    pausar_e_limpar()

def remover_candidato(cursor, conexao):
 
    #Remove um candidato da base de dados pelo seu número.

    print("\n--- REMOVER CANDIDATO ---")
    digito = input("Digite o número do candidato que deseja remover: ")

    cursor.execute(f"SELECT nome_candidato FROM Candidatos WHERE digito_candidatos = '{digito}'")
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("\n[Erro] Candidato não encontrado.")
    else:
        nome = resultado[0][0]
        confirma = input(f"Tem certeza que deseja remover o candidato {nome}? (S/N): ").upper()
        if confirma == 'S':
            cursor.execute(f"DELETE FROM Candidatos WHERE digito_candidatos = '{digito}'")
            conexao.commit()
            print("\n[Sucesso] Candidato removido.")
        else:
            print("\nRemoção cancelada.")

    pausar_e_limpar()

def buscar_candidato(cursor):

   # Busca e exibe as informações de um candidato específico.


    print("\n--- BUSCAR CANDIDATO ---")
    digito = input("Digite o número do candidato: ")

    cursor.execute(f"SELECT nome_candidato, partido_candidatos FROM Candidatos WHERE digito_candidatos = '{digito}'")
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        print("\n[Aviso] Nenhum candidato encontrado com este número.")
    else:
        candidato = resultado[0]
        print("\nRESULTADO DA BUSCA:")
        print(f"Nome: {candidato[0]} | Partido: {candidato[1]} | Número: {digito}")

    pausar_e_limpar()

def listar_candidatos(cursor):

    #Lista todos os candidatos cadastrados na base de dados.


    print("\n--- LISTA DE CANDIDATOS CADASTRADOS ---")
    cursor.execute("SELECT digito_candidatos, nome_candidato, partido_candidatos FROM Candidatos ORDER BY digito_candidatos ASC")
    candidatos = cursor.fetchall()

    if len(candidatos) == 0:
        print("\n[Aviso] Nenhum candidato cadastrado na base de dados.")
    else:
        for cand in candidatos:
            print(f"Número: {cand[0]} | Nome: {cand[1]} | Partido: {cand[2]}")

    pausar_e_limpar()