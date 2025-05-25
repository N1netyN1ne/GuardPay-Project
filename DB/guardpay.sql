-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 25-Maio-2025 às 17:29
-- Versão do servidor: 10.4.27-MariaDB
-- versão do PHP: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `guardpay`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `transacoes`
--

CREATE TABLE `transacoes` (
  `Transacao_ID` int(11) NOT NULL,
  `Cliente_ID` int(11) NOT NULL,
  `Valor_Transacao` float NOT NULL,
  `Frequencia` int(11) NOT NULL,
  `fraude_real` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Extraindo dados da tabela `transacoes`
--

INSERT INTO `transacoes` (`Transacao_ID`, `Cliente_ID`, `Valor_Transacao`, `Frequencia`, `fraude_real`) VALUES
(447, 100, 180, 5, 0),
(448, 101, 320, 4, 0),
(449, 102, 250, 6, 0),
(450, 103, 600, 3, 0),
(451, 104, 1000, 4, 0),
(452, 105, 850, 5, 0),
(453, 106, 300, 6, 0),
(454, 107, 420, 3, 0),
(455, 108, 700, 4, 0),
(456, 109, 1500, 2, 0),
(457, 110, 175, 7, 0),
(458, 100, 280, 6, 0),
(459, 101, 900, 5, 0),
(460, 102, 330, 3, 0),
(461, 103, 1250, 2, 0),
(462, 104, 200, 5, 0),
(463, 105, 350, 4, 0),
(464, 106, 450, 6, 0),
(465, 107, 950, 3, 0),
(466, 108, 780, 5, 0),
(467, 109, 65000, 2, 1),
(468, 110, 72000, 1, 1),
(469, 100, 49000, 3, 1),
(470, 101, 30500, 2, 1),
(471, 102, 44000, 4, 1),
(472, 103, 88000, 1, 1),
(473, 104, 52000, 2, 1),
(474, 105, 93000, 3, 1),
(475, 106, 76000, 2, 1),
(476, 107, 47000, 5, 1),
(477, 108, 15000, 28, 1),
(478, 109, 18000, 30, 1),
(479, 110, 12500, 27, 1),
(480, 100, 16800, 25, 1),
(481, 101, 19200, 26, 1),
(482, 102, 20500, 29, 1),
(483, 103, 17500, 28, 1),
(484, 104, 61000, 1, 1),
(485, 105, 79000, 2, 1),
(486, 106, 54000, 3, 1);

--
-- Índices para tabelas despejadas
--

--
-- Índices para tabela `transacoes`
--
ALTER TABLE `transacoes`
  ADD PRIMARY KEY (`Transacao_ID`);

--
-- AUTO_INCREMENT de tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `transacoes`
--
ALTER TABLE `transacoes`
  MODIFY `Transacao_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
