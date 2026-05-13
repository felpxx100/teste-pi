import os
# Importa a função de limpar
from gerenciamento import pausar_e_limpar

def exibir_logs():

    #Lê e exibe o ficheiro de texto contendo os logs de ocorrência da urna.

    print("\n--- EXIBIÇÃO DE LOGS DE OCORRÊNCIAS ---")
    
    # Verifica se o ficheiro já foi criado
    if os.path.exists("logs_urna.txt"):
        arquivo = open("logs_urna.txt", "r", encoding="utf-8")
        conteudo = arquivo.read()
        print(conteudo)
        arquivo.close()
    else:
        print("\n[Aviso] Nenhum log encontrado. A urna ainda não registou eventos.")
        
    pausar_e_limpar()

def exibir_protocolos(cursor):

   # Busca e exibe todos os protocolos de votação gerados no sistema em ordem alfabética.

    print("\n--- EXIBIÇÃO DOS PROTOCOLOS DE VOTAÇÃO ---")
    
    # O comando ORDER BY protocolo ASC garante a ordem alfabética exigida no PDF
    cursor.execute("SELECT protocolo FROM Votos ORDER BY protocolo ASC")
    protocolos = cursor.fetchall()
    
    if len(protocolos) == 0:
        print("\n[Aviso] Nenhum protocolo registado até ao momento.")
    else:
        for p in protocolos:
            print(f"Protocolo Validado: {p[0]}")
            
    pausar_e_limpar()