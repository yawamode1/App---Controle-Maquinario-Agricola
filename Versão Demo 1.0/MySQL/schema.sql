-- 🚜 SCHEMA DO SISTEMA DE CONTROLE AGRÍCOLA (VERSÃO DEMO)
-- Modelo otimizado para MySQL 8.0+

-- 1. Criação do banco (sem DROP statement)
CREATE DATABASE IF NOT EXISTS `controle_pecas_demo` 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `controle_pecas_demo`;

-- 2. Tabela de máquinas (estrutura básica)
CREATE TABLE maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL COMMENT 'Nome comercial do equipamento',
    modelo VARCHAR(50) COMMENT 'Versão/fabricação',
    horas_uso INT DEFAULT 0 COMMENT 'Horímetro acumulado',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_nome (nome)
) ENGINE=InnoDB;

-- 3. Tabela de peças (com constraints documentadas)
CREATE TABLE pecas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL COMMENT 'Descrição da peça',
    quantidade_estoque INT DEFAULT 0 
        CHECK (quantidade_estoque >= 0) COMMENT 'Disponível em estoque',
    quantidade_minima INT DEFAULT 5 
        CHECK (quantidade_minima > 0) COMMENT 'Estoque mínimo alerta',
    vida_util_horas INT COMMENT 'Duração esperada em horas',
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_estoque_valido 
        CHECK (quantidade_estoque >= 0 AND quantidade_minima > 0)
) ENGINE=InnoDB;

-- 4. Tabela de relacionamento (modelo 3NF)
CREATE TABLE pecas_maquinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_peca INT NOT NULL COMMENT 'FK para peças',
    id_maquina INT NOT NULL COMMENT 'FK para máquinas',
    data_associacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_peca) REFERENCES pecas(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_maquina) REFERENCES maquinas(id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uk_peca_maquina (id_peca, id_maquina)
) ENGINE=InnoDB COMMENT 'Tabela de compatibilidade';

-- 5. Dados de exemplo genéricos (sem info real)
INSERT INTO maquinas (nome, modelo) VALUES 
('Trator Demo', 'MOD-1000'),
('Colheitadeira Teste', 'COL-2000');

INSERT INTO pecas (nome, quantidade_estoque, quantidade_minima) VALUES
('Peça Demonstrativa A', 15, 3),
('Componente Genérico B', 8, 2);

INSERT INTO pecas_maquinas (id_peca, id_maquina) VALUES
(1, 1), (2, 2); -- Relacionamentos fictícios
