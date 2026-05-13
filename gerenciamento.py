import random
import os

def pausar_e_limpar():
    """Pausa o sistema até o usuário apertar ENTER e depois limpa o terminal."""
    input("\n[ Pressione ENTER para continuar... ]")
    # Limpa a tela (funciona no Windows e no Mac/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_cpf(cpf):
    """Verifica se o CPF informado é válido."""
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
        
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
        
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
        
    if str(digito1) == cpf[9] and str(digito2) == cpf[10]:
        return True
    return False

def validar_titulo(titulo):
    """Verifica se o Título de Eleitor informado é válido"""
    if len(titulo) != 12:
        return False
        
    soma1 = 0
    multiplicadores1 = [2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(8):
        soma1 += int(titulo[i]) * multiplicadores1[i]
    
    resto1 = soma1 % 11
    uf = titulo[8:10]
    
    if resto1 == 10:
        dv1 = 0
    elif resto1 == 0 and (uf == '01' or uf == '02'):
        dv1 = 1
    else:
        dv1 = resto1
        
    soma2 = int(titulo[8]) * 7 + int(titulo[9]) * 8 + dv1 * 9
    resto2 = soma2 % 11
    
    if resto2 == 10:
        dv2 = 0
    elif resto2 == 0 and (uf == '01' or uf == '02'):
        dv2 = 1
    else:
        dv2 = resto2
        
    if str(dv1) == titulo[10] and str(dv2) == titulo[11]:
        return True
    return False

def gerar_chave_acesso(nome):
    """Gera uma chave de acesso automática para o eleitor."""
    partes = nome.split()
    if len(partes) > 1:
        letras = (partes[0][:2] + partes[1][0]).upper()
    else:
        letras = partes[0][:3].upper()
        
    numeros = ""
    for i in range(4):
        numeros += str(random.randint(0, 9))
        
    return letras + numeros

def cadastrar_eleitor(cursor, conexao):
    """Realiza a coleta de dados, validação e o cadastro de um novo eleitor no banco."""
    print("\n--- CADASTRO DE NOVO ELEITOR ---")
    nome = input("Nome completo: ")
    titulo = input("Título de eleitor (12 dígitos numéricos): ")
    
    if not validar_titulo(titulo):
        print("\n[Erro] Título de eleitor inválido segundo o cálculo verificador.")
        pausar_e_limpar()
        return

    cpf = input("CPF (11 dígitos numéricos): ")
    if not validar_cpf(cpf):
        print("\n[Erro] CPF inválido segundo o cálculo verificador.")
        pausar_e_limpar()
        return

    cursor.execute(f"SELECT * FROM Eleitores WHERE CPF_Eleitor = '{cpf}' OR titulo_eleitoral = '{titulo}'")
    if len(cursor.fetchall()) > 0:
        print("\n[Erro] CPF ou Título já constam na nossa base de dados.")
        pausar_e_limpar()
        return

    resp_mesario = input("O eleitor será mesário? (S/N): ").upper()
    if resp_mesario == 'S':
        mesario = True
    else:
        mesario = False

    chave = gerar_chave_acesso(nome)

    sql = "INSERT INTO Eleitores (titulo_eleitoral, nome_eleitor, CPF_Eleitor, mesario, chave_acesso, ja_votou) VALUES (%s, %s, %s, %s, %s, %s)"
    valores = (titulo, nome, cpf, mesario, chave, False)

    cursor.execute(sql, valores)
    conexao.commit()
    print(f"\n[Sucesso] Eleitor cadastrado! Anote a Chave de Acesso: {chave}")
    pausar_e_limpar()

def buscar_eleitor(cursor):
    """Realiza a busca de um eleitor específico informando o CPF ou Título."""
    print("\n--- BUSCA DE ELEITOR ---")
    print("1 - Buscar por CPF")
    print("2 - Buscar por Título")
    opcao = input("Escolha a opção de busca: ")
    
    if opcao == "1":
        cpf = input("Digite o CPF (apenas números): ")
        cursor.execute(f"SELECT nome_eleitor, titulo_eleitoral, mesario FROM Eleitores WHERE CPF_Eleitor = '{cpf}'")
    elif opcao == "2":
        titulo = input("Digite o Título (apenas números): ")
        cursor.execute(f"SELECT nome_eleitor, CPF_Eleitor, mesario FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    else:
        print("\n[Erro] Opção inválida.")
        pausar_e_limpar()
        return

    resultado = cursor.fetchall()
    if len(resultado) == 0:
        print("\n[Aviso] Nenhum eleitor encontrado com os dados informados.")
    else:
        print("\nRESULTADO DA BUSCA:")
        for eleitor in resultado:
            if eleitor[2]:
                perfil = "Mesário"
            else:
                perfil = "Eleitor Comum"
            print(f"Nome: {eleitor[0]} | Documento cadastrado: {eleitor[1]} | Perfil: {perfil}")
            
    pausar_e_limpar()

def listar_eleitores(cursor):
    """Lista todos os eleitores cadastrados no banco de dados."""
    print("\n--- LISTA DE ELEITORES CADASTRADOS ---")
    cursor.execute("SELECT id_eleitor, nome_eleitor, CPF_Eleitor, titulo_eleitoral, mesario FROM Eleitores")
    eleitores = cursor.fetchall()
    
    if len(eleitores) == 0:
        print("\n[Aviso] Nenhum eleitor cadastrado na base de dados.")
    else:
        for eleitor in eleitores:
            if eleitor[4]:
                perfil = "Mesário"
            else:
                perfil = "Eleitor Comum"
            print(f"ID: {eleitor[0]} | Nome: {eleitor[1]} | CPF: {eleitor[2]} | Título: {eleitor[3]} | Perfil: {perfil}")
            
    pausar_e_limpar()
