-- Create the main table "banca"
CREATE TEMPORARY TABLE IF NOT EXISTS banca (
  SELECT 
    cliente.id_cliente, cliente.nome, cliente.cognome, cliente.data_nascita,
    tipo_conto.id_tipo_conto, tipo_conto.desc_tipo_conto,
    transazioni.data, transazioni.importo,
    conto.id_conto,
    tipo_transazione.id_tipo_transazione, tipo_transazione.desc_tipo_trans, tipo_transazione.segno
  FROM cliente
  LEFT JOIN conto ON cliente.id_cliente = conto.id_cliente
  LEFT JOIN tipo_conto ON conto.id_tipo_conto = tipo_conto.id_tipo_conto
  LEFT JOIN transazioni ON conto.id_conto = transazioni.id_conto
  LEFT JOIN tipo_transazione ON transazioni.id_tipo_trans = tipo_transazione.id_tipo_transazione);

-- Create TEMP TABLE "eta"
CREATE TEMPORARY TABLE IF NOT EXISTS eta (
  SELECT id_cliente, data_nascita, TIMESTAMPDIFF(YEAR, data_nascita, CURRENT_DATE()) AS age
  FROM banca
  ORDER BY id_cliente);

-- Create TEMP TABLE "n_trans_out"
CREATE TEMPORARY TABLE IF NOT EXISTS n_trans_out (
  SELECT id_conto, segno, COUNT(*) AS n_uscita
  FROM banca
  WHERE segno = '-'
  GROUP BY id_conto, segno
  ORDER BY id_conto);

-- Create TEMP TABLE "n_trans_in"
CREATE TEMPORARY TABLE IF NOT EXISTS n_trans_in (
  SELECT id_conto, segno, COUNT(*) AS n_entrata
  FROM banca
  WHERE segno = '+'
  GROUP BY id_conto, segno
  ORDER BY id_conto);

-- Create TEMP TABLE "tot_trans_out"
CREATE TEMPORARY TABLE IF NOT EXISTS tot_trans_out (
  SELECT segno, SUM(importo) AS totale_uscita
  FROM banca
  WHERE segno = '-'
  GROUP BY segno);

-- Create TEMP TABLE "tot_trans_in"
CREATE TEMPORARY TABLE IF NOT EXISTS tot_trans_in (
  SELECT segno, SUM(importo) AS totale_entrata
  FROM banca
  WHERE segno = '+'
  GROUP BY segno);

-- Create TEMP TABLE "n_conti_cliente"
CREATE TEMPORARY TABLE IF NOT EXISTS n_conti_cliente (
  SELECT id_cliente, COUNT(id_conto) AS n
  FROM banca
  GROUP BY id_cliente);

-- Create TEMP TABLE "n_conti_tipo"
CREATE TEMPORARY TABLE IF NOT EXISTS n_conti_tipo (
  SELECT desc_tipo_conto, COUNT(*) AS n_desc_tipo_conto
  FROM banca
  GROUP BY desc_tipo_conto);

-- Create TEMP TABLE "n_trans_out_tipo_conto"
CREATE TEMPORARY TABLE IF NOT EXISTS n_trans_out_tipo_conto (
  SELECT desc_tipo_conto, COUNT(*) AS n_out
  FROM banca
  WHERE segno = '-'
  GROUP BY desc_tipo_conto);

-- Create TEMP TABLE "n_trans_in_tipo_conto"
CREATE TEMPORARY TABLE IF NOT EXISTS n_trans_in_tipo_conto (
  SELECT desc_tipo_conto, COUNT(*) AS n_in
  FROM banca
  WHERE segno = '+'
  GROUP BY desc_tipo_conto);

-- Create TEMP TABLE "importo_trans_out_tipo_conto"
CREATE TEMPORARY TABLE IF NOT EXISTS importo_trans_out_tipo_conto (
  SELECT desc_tipo_conto, SUM(importo) AS tot_out
  FROM banca
  WHERE segno = '-'
  GROUP BY desc_tipo_conto
  ORDER BY desc_tipo_conto);

-- Create TEMP TABLE "importo_trans_in_tipo_conto"
CREATE TEMPORARY TABLE IF NOT EXISTS importo_trans_in_tipo_conto (
  SELECT desc_tipo_conto, SUM(importo) AS tot_in
  FROM banca
  WHERE segno = '+'
  GROUP BY desc_tipo_conto
  ORDER BY desc_tipo_conto);
