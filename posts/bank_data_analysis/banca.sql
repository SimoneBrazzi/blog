CREATE TEMPORARY TABLE features (
  SELECT 
    cliente.id_cliente,
    -- feature età
    TIMESTAMPDIFF(YEAR, cliente.data_nascita, CURRENT_DATE()) AS eta,
    -- numero di transazioni in uscita ed entrata
    COUNT(CASE WHEN tipo_transazione.segno = '-' THEN 1 END) AS n_transazioni_uscita,
    COUNT(CASE WHEN tipo_transazione.segno = '+' THEN 1 END) AS n_transazioni_entrata,
    -- numero di transazioni per tipologia di conto
    -- totale uscita e entrata
    SUM(CASE WHEN tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita,
    SUM(CASE WHEN tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata,
    -- numero di conti 
    COUNT(DISTINCT conto.id_conto) AS n_conti,
    -- numero di conti per tipo di conto
    COUNT(DISTINCT CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' THEN 1 END) AS n_conto_privati,
    COUNT(DISTINCT CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' THEN 1 END) AS n_conto_base,
    COUNT(DISTINCT CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' THEN 1 END) AS n_conto_business,
    COUNT(DISTINCT CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' THEN 1 END) AS n_conto_famiglie,

    -- Numero di transazioni in uscita per tipologia di conto
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' AND tipo_transazione.segno = '-' THEN tipo_transazione.segno END) AS n_uscita_conto_privati,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' AND tipo_transazione.segno = '-' THEN tipo_transazione.segno END) AS n_uscita_conto_base,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' AND tipo_transazione.segno = '-' THEN tipo_transazione.segno END) AS n_uscita_conto_business,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' AND tipo_transazione.segno = '-' THEN tipo_transazione.segno END) AS n_uscita_conto_famiglie,
    -- Numero di transazioni in entrata per tipologia di conto
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' AND tipo_transazione.segno = '+' THEN tipo_transazione.segno END) AS n_entrata_conto_privati,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' AND tipo_transazione.segno = '+' THEN tipo_transazione.segno END) AS n_entrata_conto_base,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' AND tipo_transazione.segno = '+' THEN tipo_transazione.segno END) AS n_entrata_conto_business,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' AND tipo_transazione.segno = '+' THEN tipo_transazione.segno END) AS n_entrata_conto_famiglie,

    -- Importo transato in uscita per tipologia di conto
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_privati,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_base,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_business,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_famiglie,
    -- Importo transato in entrata per tipologia di conto
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' AND tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata_conto_privati,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' AND tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata_conto_base,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' AND tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata_conto_business,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' AND tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata_conto_famiglie
  FROM cliente
  -- serie di join
  LEFT JOIN conto ON cliente.id_cliente = conto.id_cliente
  LEFT JOIN tipo_conto ON conto.id_tipo_conto = tipo_conto.id_tipo_conto
  LEFT JOIN transazioni ON conto.id_conto = transazioni.id_conto
  LEFT JOIN tipo_transazione ON transazioni.id_tipo_trans = tipo_transazione.id_tipo_transazione
  -- raggruppamento per id_cliente
  GROUP BY cliente.id_cliente
  -- assicuro che sia in ordine crescente per id_cliente
  ORDER BY cliente.id_cliente
  );