import os
import bancodedados
import gerenciamento
import candidatos # Importa o seu novo ficheiro de candidatos
import votacao
import auditoria
from gerenciamento import pausar_e_limpar # Importado para não repetir código

# Conecta no banco de dados usando o módulo banco.py
conexao = bancodedados.conectar()
cursor = conexao.cursor()
os.system('cls' if os.name == 'nt' else 'clear')
print("[Sistema: Conexão com banco de dados estabelecida com sucesso.]")

## título do programa
el="Eleição"
print(f"{el:^90}\n")
pausar_e_limpar()

# Variável de controle do menu principal
menup = 0

## menu principal
while menup != 3:
    print("\n--- MENU PRINCIPAL ---")
    print("Escolha a opção")
    menup = int(input("1- Módulo de gerenciamento\n2- Módulo de votação\n3- Sair\n"))
    os.system('cls' if os.name == 'nt' else 'clear')

    match menup:
        ## menu de modulo de gerenciamento
        case 1:
            modulo_gere = 0
            while modulo_gere != 11:
                print("\n--- MÓDULO DE GERENCIAMENTO ---")
                print("Escolha uma opção")
                modulo_gere = int(input("1- Cadastra novo eleitor\n2- Editar dados do eleitor\n3- Remover eleitor\n4- Buscar eleitor\n5- Listar todos os eleitores\n6- Cadastrar novo candidato\n7- Editar dados do candidato\n8- Remover candidato\n9- Buscar candidato\n10- Listar todos os candidatos\n11- Voltar\n"))
                os.system('cls' if os.name == 'nt' else 'clear')
                
                match modulo_gere:
                    case 1:
                        gerenciamento.cadastrar_eleitor(cursor, conexao)
                    case 2:
                        print("Função em desenvolvimento.")
                        pausar_e_limpar()
                    case 3:
                        print("Função em desenvolvimento.")
                        pausar_e_limpar()
                    case 4:
                        gerenciamento.buscar_eleitor(cursor)
                    case 5:
                        gerenciamento.listar_eleitores(cursor)
                    case 6:
                        candidatos.cadastrar_candidato(cursor, conexao)
                    case 7:
                        candidatos.editar_candidato(cursor, conexao)
                    case 8:
                        candidatos.remover_candidato(cursor, conexao)
                    case 9:
                        candidatos.buscar_candidato(cursor)
                    case 10:
                        candidatos.listar_candidatos(cursor)
                    case 11:
                        print("Voltando ao Menu Principal...")
                        pausar_e_limpar()
                    case _:
                        print("Opção inválida")
                        pausar_e_limpar()

        case 2:
            modulo_vot = 0
            while modulo_vot != 4:
                print("\n--- MÓDULO DE VOTAÇÃO ---")
                print("Escolha uma opção")
                modulo_vot = int(input("1- Abrir Sistema de Votação\n2- Auditoria do Sistema de Votação\n3- Resultado da Votação\n4- Voltar\n"))
                os.system('cls' if os.name == 'nt' else 'clear')
                
                match modulo_vot:
                    case 1:
                        if votacao.abrir_votacao(conexao, cursor):
                            menu_urna = 0
                            while menu_urna != 2:
                                print("\nEscolha a opção da Urna")
                                menu_urna = int(input("1- Votar\n2- Encerrar Sistema de Votação\n"))
                                os.system('cls' if os.name == 'nt' else 'clear')
                                
                                match menu_urna:
                                    case 1:
                                        votacao.realizar_voto(conexao, cursor)
                                    case 2:
                                        if votacao.encerrar_votacao(cursor):
                                            menu_urna = 2 # Força a saída do laço da urna
                                    case _:
                                        print("Opção inválida")
                                        pausar_e_limpar()
                    
                    case 2:
                        menu_auditoria = 0
                        while menu_auditoria != 3:
                            print("\n--- AUDITORIA DO SISTEMA ---")
                            menu_auditoria = int(input("1- Exibição de Logs de Ocorrências\n2- Exibição dos Protocolos de Votação\n3- Voltar\n"))
                            os.system('cls' if os.name == 'nt' else 'clear')
                            match menu_auditoria:
                                case 1: 
                                    auditoria.exibir_logs()
                                case 2: 
                                    auditoria.exibir_protocolos(cursor)
                                case 3: 
                                    print("Voltando...")
                                case _: 
                                    print("Opção inválida")
                                    pausar_e_limpar()
                                    
                    case 3:
                        menu_resultados = 0
                        while menu_resultados != 5:
                            print("\n--- RESULTADO DA VOTAÇÃO ---")
                            menu_resultados = int(input("1- Boletim de Urna\n2- Estatística de Comparecimento\n3- Votos por Partido\n4- Validação de Integridade\n5- Voltar\n"))
                            os.system('cls' if os.name == 'nt' else 'clear')
                            match menu_resultados:
                                case 1: 
                                    print("Função em desenvolvimento.")
                                    pausar_e_limpar()
                                case 2: 
                                    print("Função em desenvolvimento.")
                                    pausar_e_limpar()
                                case 3: 
                                    print("Função em desenvolvimento.")
                                    pausar_e_limpar()
                                case 4: 
                                    print("Função em desenvolvimento.")
                                    pausar_e_limpar()
                                case 5: 
                                    print("Voltando...")
                                case _: 
                                    print("Opção inválida")
                                    pausar_e_limpar()
                                    
                    case 4:
                        print("Voltando ao Menu Principal...")
                        pausar_e_limpar()
                    case _:
                        print("Opção inválida")
                        pausar_e_limpar()

        case 3:
            print("Saindo do sistema...")
        case _:
            print("Opção inválida")
            pausar_e_limpar()

cursor.close()
conexao.close()