-- Ho capito solo ora la richiesta. Ho riletto pià volte fino a farmi entrare in testa che dovevo creare una tabella di features per un modello. Non so perché ero convinto fosse un esercizio diverso.
-- Grazie per la pazienza e spero sia la consegna definitiva :-) 
-- Di sicuro ho imparato ad interagire correttamente da CLI con un mariadb: installarlo e farlo funzionare correttamente è stata un'impresa, soprattutto perché su mac non setta correttamente la password e lavorare in locale è un'impresa.


-- crea table temporanea
CREATE TEMPORARY TABLE IF NOT EXISTS features (
  SELECT 
    cliente.id_cliente,
    -- feature età
    TIMESTAMPDIFF(YEAR, cliente.data_nascita, CURRENT_DATE()) AS eta,
    -- numero di transazioni in uscita ed entrata
    COUNT(CASE WHEN tipo_transazione.segno = '-' THEN 1 ELSE 0 END) AS n_transazioni_uscita,
    COUNT(CASE WHEN tipo_transazione.segno = '+' THEN 1 ELSE 0 END) AS n_transazioni_entrata,
    -- totale uscita e entrata
    SUM(CASE WHEN tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita,
    SUM(CASE WHEN tipo_transazione.segno = '+' THEN transazioni.importo ELSE 0 END) AS tot_entrata,
    -- numero di conti 
    COUNT(DISTINCT conto.id_conto) AS n_conti,
    -- numero di conti per tipo di conto
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' THEN 1 ELSE 0 END) AS n_conto_privati,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' THEN 1 ELSE 0 END) AS n_conto_base,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' THEN 1 ELSE 0 END) AS n_conto_business,
    COUNT(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' THEN 1 ELSE 0 END) AS n_conto_famiglie,
    -- numero di conti per tipo di conto con operazioni in uscita
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Privati' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_privati,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Base' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_base,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Business' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_business,
    SUM(CASE WHEN tipo_conto.desc_tipo_conto = 'Conto Famiglie' AND tipo_transazione.segno = '-' THEN transazioni.importo ELSE 0 END) AS tot_uscita_conto_famiglie,
    -- numero di conti per tipo di conto con operazioni in entrata
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
  ORDER BY cliente.id_cliente);