-- Cria o banco de dados se não existir e o seleciona
CREATE DATABASE IF NOT EXISTS eleicao;
USE eleicao;

-- Limpa as tabelas caso já existam para recriar do zero
DROP TABLE IF EXISTS Votos;
DROP TABLE IF EXISTS Candidatos;
DROP TABLE IF EXISTS Eleitores;

-- Criação da Tabela de Eleitores
CREATE TABLE Eleitores(
    id_eleitor INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    titulo_eleitoral VARCHAR(12) NOT NULL UNIQUE, 
    nome_eleitor VARCHAR(100) NOT NULL,
    CPF_Eleitor VARCHAR(11) NOT NULL UNIQUE,      
    mesario BOOLEAN NOT NULL DEFAULT FALSE,       
    chave_acesso VARCHAR(50) NOT NULL,            
    ja_votou BOOLEAN NOT NULL DEFAULT FALSE       
);

-- Criação da Tabela de Candidatos
CREATE TABLE Candidatos(
    id_candidatos INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    digito_candidatos INT NOT NULL UNIQUE,        
    nome_candidato VARCHAR(100) NOT NULL,
    partido_candidatos VARCHAR(100) NOT NULL
    -- Removi a chave estrangeira de eleitor daqui, pois um candidato 
    -- não precisa estar amarrado a um Eleitor para a tabela existir.
);

-- Criação da Tabela de Votos 
CREATE TABLE Votos(
    id_voto INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    digito_candidato INT NOT NULL,
    data_hora DATETIME NOT NULL,                  
    protocolo VARCHAR(50) NOT NULL UNIQUE,        -- CORREÇÃO: Vírgula adicionada
    id_eleitor INT,                               -- CORREÇÃO: Trocado ; por ,
    id_candidatos INT,                            -- CORREÇÃO: Trocado ; por ,
    FOREIGN KEY (id_eleitor) REFERENCES Eleitores(id_eleitor),    -- CORREÇÃO: Parênteses e vírgula
    FOREIGN KEY (id_candidatos) REFERENCES Candidatos(id_candidatos) -- CORREÇÃO: Parênteses
);

-- Inserindo Candidatos Fictícios
INSERT INTO Candidatos (digito_candidatos, nome_candidato, partido_candidatos) VALUES 
(10, 'Alan Turing', 'PDC (Partido da Computação)'),
(20, 'Ada Lovelace', 'PAL (Partido dos Algoritmos)'),
(30, 'Grace Hopper', 'PBD (Partido do Banco de Dados)'),
(99, 'Voto Nulo/Branco', 'Sem Partido');

-- Inserindo Eleitores Fictícios 
INSERT INTO Eleitores (titulo_eleitoral, nome_eleitor, CPF_Eleitor, mesario, chave_acesso, ja_votou) VALUES 
('004356870906', 'Ana Pereira', '12345678909', TRUE, 'ANPE1234', FALSE),   
('102385010671', 'Carlos Mendes', '98765432100', FALSE, 'CAME5678', FALSE), 
('203496120782', 'Beatriz Souza', '45612378900', FALSE, 'BESO9012', FALSE);