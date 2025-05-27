-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 27-Maio-2025 às 02:47
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
(1946, 100, 180, 5, 0),
(1947, 101, 320, 4, 0),
(1948, 102, 250, 6, 0),
(1949, 103, 600, 3, 0),
(1950, 104, 1000, 4, 0),
(1951, 105, 850, 5, 0),
(1952, 106, 300, 6, 0),
(1953, 107, 420, 3, 0),
(1954, 108, 700, 4, 0),
(1955, 109, 1500, 2, 0),
(1956, 110, 175, 7, 0),
(1957, 100, 280, 6, 0),
(1958, 101, 900, 5, 0),
(1959, 102, 330, 3, 0),
(1960, 103, 1250, 2, 0),
(1961, 104, 200, 5, 0),
(1962, 105, 350, 4, 0),
(1963, 106, 450, 6, 0),
(1964, 107, 950, 3, 0),
(1965, 108, 780, 5, 0),
(1966, 100, 200, 5, 0),
(1967, 101, 350, 4, 0),
(1968, 111, 500, 7, 0),
(1969, 112, 120, 8, 0),
(1970, 103, 750, 3, 0),
(1971, 104, 1100, 4, 0),
(1972, 105, 900, 5, 0),
(1973, 113, 220, 6, 0),
(1974, 114, 650, 2, 0),
(1975, 100, 220, 6, 0),
(1976, 101, 400, 3, 0),
(1977, 109, 65000, 2, 1),
(1978, 110, 72000, 1, 1),
(1979, 100, 49000, 3, 1),
(1980, 101, 30500, 2, 1),
(1981, 102, 44000, 4, 1),
(1982, 103, 88000, 1, 1),
(1983, 104, 52000, 2, 1),
(1984, 105, 93000, 3, 1),
(1985, 106, 76000, 2, 1),
(1986, 107, 47000, 5, 1),
(1987, 108, 15000, 28, 1),
(1988, 109, 18000, 30, 1),
(1989, 110, 12500, 27, 1),
(1990, 100, 16800, 25, 1),
(1991, 101, 19200, 26, 1),
(1992, 102, 20500, 29, 1),
(1993, 103, 17500, 28, 1),
(1994, 104, 61000, 1, 1),
(1995, 105, 79000, 2, 1),
(1996, 106, 54000, 3, 1),
(1997, 111, 5000, 15, 1),
(1998, 112, 10000, 20, 1),
(1999, 100, 15000, 2, 1),
(2000, 101, 2500, 1, 1),
(2001, 107, 30000, 2, 1),
(2002, 113, 85000, 1, 1),
(2003, 114, 1800, 20, 1),
(2004, 102, 50000, 5, 1),
(2005, 106, 728, 7, NULL),
(2006, 101, 206, 8, NULL),
(2007, 105, 1977, 26, NULL),
(2008, 106, 2024, 2, NULL),
(2009, 109, 5993, 4, NULL),
(2010, 101, 1882, 14, NULL),
(2011, 108, 4783, 18, NULL),
(2012, 109, 3510, 23, NULL),
(2013, 110, 5727, 3, NULL),
(2014, 108, 976, 4, NULL),
(2015, 109, 377, 2, NULL),
(2016, 100, 8511, 5, NULL),
(2017, 100, 9197, 1, NULL),
(2018, 107, 4338, 9, NULL),
(2019, 106, 5947, 15, NULL),
(2020, 108, 810, 2, NULL),
(2021, 102, 898, 3, NULL),
(2022, 109, 1149, 13, NULL),
(2023, 107, 8715, 11, NULL),
(2024, 107, 6754, 7, NULL),
(2025, 101, 8554, 5, NULL),
(2026, 100, 266, 7, NULL),
(2027, 105, 766, 5, NULL),
(2028, 101, 516, 3, NULL),
(2029, 104, 360, 8, NULL),
(2030, 107, 177, 9, NULL),
(2031, 105, 568, 1, NULL),
(2032, 101, 307, 5, NULL),
(2033, 105, 543, 7, NULL),
(2034, 101, 716, 4, NULL),
(2035, 105, 7910, 17, NULL),
(2036, 109, 6981, 2, NULL),
(2037, 105, 8259, 4, NULL),
(2038, 102, 4858, 3, NULL),
(2039, 102, 8619, 11, NULL),
(2040, 101, 3264, 19, NULL),
(2041, 109, 6634, 9, NULL),
(2042, 106, 6316, 24, NULL),
(2043, 101, 2117, 6, NULL);

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
  MODIFY `Transacao_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2044;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
