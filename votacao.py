import datetime
import random

import datetime
import random
# Importando a função que você já criou no outro arquivo!
from gerenciamento import pausar_e_limpar 

def registrar_log(mensagem):
 
    #Regista um evento no ficheiro de log da urna com a data e hora exatas.

    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Abre o ficheiro em modo de adição ("a" - append)
    arquivo = open("logs_urna.txt", "a", encoding="utf-8")
    arquivo.write(f"[{agora}] {mensagem}\n")
    arquivo.close()

def validar_credenciais(cursor, titulo, cpf_4_digitos, chave, perfil_exigido):

    #Verifica na base de dados se as credenciais inseridas estão corretas.

    cursor.execute(f"SELECT CPF_Eleitor, mesario FROM Eleitores WHERE titulo_eleitoral = '{titulo}' AND chave_acesso = '{chave}'")
    resultado = cursor.fetchall()
    
    if len(resultado) > 0:
        cpf_banco = resultado[0][0]
        e_mesario = resultado[0][1]
        
        # Verifica se os 4 primeiros dígitos correspondem
        if cpf_banco[0:4] == cpf_4_digitos:
            if perfil_exigido == "mesario" and e_mesario == 1:
                return True
            elif perfil_exigido == "eleitor":
                return True
                
    return False

def abrir_votacao(conexao, cursor):
    
    ##Efetua a autenticação do mesário, executa a Zerézima e abre a urna.
    
    print("\n--- ABERTURA DO SISTEMA DE VOTAÇÃO ---")
    titulo = input("Digite o título de eleitor do mesário: ")
    cpf_4 = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite a chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "mesario") == False:
        print("\n[Erro] Falha na validação do mesário. Acesso negado.")
        registrar_log("ALERTA: Tentativa de acesso negado")
        pausar_e_limpar()
        return False

    # Processo de Zerézima (Limpar votos antigos)
    cursor.execute("DELETE FROM Votos")
    conexao.commit()
    
    print("\n--- ZERÉZIMA CONCLUÍDA ---")
    cursor.execute("SELECT digito_candidatos, nome_candidato FROM Candidatos")
    candidatos = cursor.fetchall()
    
    if len(candidatos) > 0:
        for cand in candidatos:
            print(f"Candidato: {cand[1]} | Número: {cand[0]} | Votos: 0")
    else:
        print("Nenhum candidato registado na base de dados.")

    registrar_log("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")
    print("\n[Sistema] Votação aberta com sucesso!")
    pausar_e_limpar()
    return True

def realizar_voto(conexao, cursor):
  
    ##Identifica o eleitor, valida duplo voto e regista a escolha na base de dados.
    print("\n--- IDENTIFICAÇÃO DO ELEITOR ---")
    titulo = input("Digite seu título de eleitor: ")
    cpf_4 = input("Digite os 4 primeiros dígitos do seu CPF: ")
    chave = input("Digite sua chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "eleitor") == False:
        print("\n[Erro] Dados inválidos ou incorretos.")
        registrar_log("ALERTA: Tentativa de acesso negado")
        pausar_e_limpar()
        return

    # Verificar se o eleitor já votou para impedir voto duplo
    cursor.execute(f"SELECT id_eleitor, ja_votou FROM Eleitores WHERE titulo_eleitoral = '{titulo}'")
    eleitor_info = cursor.fetchall()[0]
    id_eleitor = eleitor_info[0]
    ja_votou = eleitor_info[1]

    if ja_votou == 1:
        print("\n[Erro] A participação deste eleitor já foi realizada.")
        registrar_log("ALERTA: Tentativa de voto duplo")
        pausar_e_limpar()
        return

    num_cand = input("\nDigite o número do candidato: ")
    cursor.execute(f"SELECT nome_candidato, partido_candidatos, id_candidatos FROM Candidatos WHERE digito_candidatos = '{num_cand}'")
    resultado_candidato = cursor.fetchall()

    if len(resultado_candidato) > 0:
        candidato = resultado_candidato[0]
        print(f"\nVocê está votando em: {candidato[0]} ({candidato[1]})")
        id_candidato = candidato[2]
    else:
        print("\nCandidato não encontrado. Você está votando NULO/BRANCO.")
        # Assumindo que o candidato 99 é o Nulo, criado no seu SQL
        cursor.execute("SELECT id_candidatos FROM Candidatos WHERE digito_candidatos = 99")
        id_candidato = cursor.fetchall()[0][0]

    confirma = input("Confirma o voto? (Sim/Não): ").upper()
    
    if confirma == "SIM":
        # Gerar o protocolo: Letra V + 2 letras + 26 + num_candidato + 5 dígitos
        letras = chr(random.randint(65, 90)) + chr(random.randint(65, 90))
        numeros = str(random.randint(10000, 99999))
        
        # Formatar o número do candidato para garantir que tem 2 dígitos mínimos
        num_formatado = num_cand
        if len(num_formatado) == 1:
            num_formatado = "0" + num_formatado
            
        protocolo = f"V{letras}26{num_formatado}{numeros}"
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserir o voto e atualizar o status do eleitor
        cursor.execute("INSERT INTO Votos (digito_candidato, data_hora, protocolo, id_eleitor, id_candidatos) VALUES (%s, %s, %s, %s, %s)", (num_cand, data_hora, protocolo, id_eleitor, id_candidato))
        cursor.execute(f"UPDATE Eleitores SET ja_votou = TRUE WHERE id_eleitor = {id_eleitor}")
        conexao.commit()

        registrar_log("SUCESSO: Voto realizado com sucesso")
        print(f"\n[Voto Confirmado] Guarde seu protocolo: {protocolo}")
    else:
        print("\nVoto cancelado pelo eleitor.")

    pausar_e_limpar()

def encerrar_votacao(cursor):

    ##Exige a autenticação do mesário e encerra a urna de forma definitiva.

    print("\n--- ENCERRAMENTO DA VOTAÇÃO ---")
    titulo = input("Digite o título de eleitor do mesário: ")
    cpf_4 = input("Digite os 4 primeiros dígitos do CPF: ")
    chave = input("Digite a chave de acesso: ")

    if validar_credenciais(cursor, titulo, cpf_4, chave, "mesario") == False:
        print("\n[Erro] Falha na validação do mesário. Acesso negado.")
        registrar_log("ALERTA: Tentativa de acesso negado")
        pausar_e_limpar()
        return False

    confirma = input("\nDeseja realmente encerrar a votação? (Sim/Não): ").upper()
    if confirma == "SIM":
        chave_confirma = input("Digite sua chave de acesso novamente para confirmar: ")
        if chave_confirma == chave:
            registrar_log("ENCERRAMENTO: Votação finalizada com sucesso.")
            print("\n[Sistema] Votação encerrada definitivamente.")
            pausar_e_limpar()
            return True
        else:
            print("\n[Erro] Chave incorreta. Encerramento cancelado.")
    else:
        print("\nEncerramento cancelado.")

    pausar_e_limpar()
    return False