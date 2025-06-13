import os
import json
from tabulate import tabulate

# define the class
class Warehouse():
    """
    Classe che rappresenta un software gestionale. SUpporta la registrazione permanente delle vendite e il calcolo dei profitti.

    Attributi:
        **_filename** (str): nome del file principale del magazzino. Senza estensione.
        **_filename_sell** (str): nome del file per le vendite. Definito in automatico dal filename.
        **_path** (str): working directory corrente.
        **_filepath** (str): percorso completo del file principale JSON del magazzino.
        **_filepath_sell** (str): percorso completo del file JSON delle vendite.
        **_headers** (list): intestazioni della tabella per la visualizzazione del magazzino.

    Metodi:
        **__init__(filename)**: inizializza l'oggetto magazzino con il nome del file fornito.
        **save_data(data, sell=False)**: salva i dati in formato JSON, con possibilità di scegliere tra magazzino o vendite.
        **load_data(sell=False)**: carica i dati da un file JSON. Se il file non esiste, offre di crearne uno vuoto.
        **__repr__()**: restituisce una rappresentazione testuale tecnica dell'oggetto.
        **__str__()**: restituisce una rappresentazione testuale leggibile dell'oggetto.
        **get_table(data)**: restituisce una lista formattata dei dati per la stampa tabellare.
        **add_product(data)**: aggiunge un nuovo prodotto o aggiorna la quantità di uno esistente nel magazzino.
        **list_products(warehouse)**: stampa i prodotti del magazzino in formato tabella.
        **help_me()**: mostra i comandi disponibili all’utente.
        **close()**: chiude l'applicazione terminando il processo.
        **not_available_cmd(cmd)**: gestisce i comandi non riconosciuti mostrando un messaggio di errore.
        **profits(warehouse_sell)**: calcola e stampa i profitti totali dalle vendite registrate.
        **sell(warehouse, warehouse_sell)**: registra una o più vendite, aggiornando i rispettivi magazzini e mostrando il riepilogo delle transazioni.

    Comandi disponibili per l'utente:
        - **aggiungi**: aggiungi un nuovo oggetto al magazzino.
        - **elenca**: mostra i prodotti in magazzino in formato tabellare.
        - **vendita**: registra una o più vendite effettuate.
        - **profitti**: calcola e mostra i profitti.
        - **aiuto**: mostra le funzioni disponibili.
        - **chiudi**: chiude il software.
    """

    def __init__(self, filename):
        """
        Inizializza l'oggetto Warehouse con il nome assegnato.

        Parametri:
            filename (str): nome base del file JSON (senza estensione) per il magazzino.
        """
        self._filename = filename
        self._filename_sell = f"{self._filename}_sell"
        self._path = os.getcwd()
        self._filepath = os.path.join(self._path, f"{self._filename}.json")
        self._filepath_sell = os.path.join(self._path, f"{self._filename_sell}.json")
        self._headers = ["PRODOTTO", "QUANTITÀ", "PREZZO", "COSTO"]

    def save_data(self, data, sell=False):
        """
        Salva i dati del magazzino o delle vendite in formato JSON.

        Parametri:
            data (dict): dizionario con i dati da salvare.
            sell (bool): se True, salva nel file delle vendite; altrimenti nel file del magazzino.
        """
        filename = self._filename_sell if sell else self._filename
        filepath = self._filepath_sell if sell else self._filepath

        while True:
            try:
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                    break
            except FileNotFoundError:
                q = input(f"Vuoi inizializzare un database vuoto? (sì/no): ")
                if q.lower() in ["sì", "si"]:
                    tmp = input("Scegli un nome per il db: ")
                    with open(filepath, "w") as f:
                        json.dump({}, f, indent=4)
                        print(f"Database inizializzato come '{tmp}.json'.")
                    break
                else:
                    print("File non trovato e l'utente non ha voluto inizializzarlo.")
                    return None

    def load_data(self, sell=False):
        """
        Carica i dati del magazzino o delle vendite da un file JSON.

        Parametri:
            sell (bool): se True, carica i dati dal file delle vendite; altrimenti dal magazzino.

        Ritorna:
            dict: dati del magazzino o delle vendite. Se il file non esiste, chiede se inizializzarlo.
        """
        filename = self._filename_sell if sell else self._filename
        filepath = self._filepath_sell if sell else self._filepath

        while True:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    return data
            except FileNotFoundError:
                q = input(f"Vuoi inizializzare un {filename.title()} database? (sì/no): ")
                if q.lower() in ["sì", "si"]:
                    data = {}
                    print(f"{filename.title()} inizializzato.")
                    self.save_data(data, sell)
                    return data
                elif q.lower() == "no":
                    print("File non trovato e l'utente non ha voluto inizializzarlo.")
                    break
                else:
                    print("Risposta non valida. Riprova.")

    def __repr__(self):
        """
        Rappresentazione tecnica dell'oggetto Warehouse.

        Ritorna:
            str: informazioni sui file e percorsi del magazzino.
        """
        info = f"FILENAME: {self._filename}.json.\n"
        info += f"FILENAME SELL: {self._filename_sell}.json.\n"
        info += f"FILEPATH: {self._filepath}."
        return info

    def __str__(self):
        """
        Rappresentazione leggibile dell'oggetto Warehouse.

        Ritorna:
            str: alias di __repr__.
        """
        return self.__repr__()

    def get_table(self, data):
        """
        Prepara i dati in formato tabellare per la visualizzazione in CLI.

        Parametri:
            data (dict): dati del magazzino.

        Ritorna:
            list: lista di liste con informazioni per ogni prodotto.
        """
        return [[product, info["quantity"], info["price_sell"], info["price_buy"]] for product, info in data.items()]

    def add_product(self, data):
        """
        Aggiunge un nuovo prodotto al magazzino o aggiunge la quantità se già esistente.

        Parametri:
            data (dict): dizionario dei prodotti del magazzino.
        """
        while True:
            try:
                name = input("Nome del prodotto: ")
                name = name.title()
                if not name.isalpha():
                    raise ValueError("Il nome deve contenere solo lettere.")
                break
            except ValueError as e:
                print(e)

        if name not in data.keys():
            try:
                quantity = int(input("Quantità: "))
                price_buy = float(input("Prezzo d'acquisto: "))
                price_sell = float(input("Prezzo di vendita: "))
            except ValueError:
                print("Errore: Inserisci valori numerici validi per quantità e prezzi.")
                return

            values = {"quantity": int(quantity), "price_buy": float(price_buy), "price_sell": float(price_sell)}
            data[name] = values

        else:
            while True:
                try:
                    quantity = int(input("Quantità da aggiungere: "))
                    data[name]["quantity"] += quantity
                    break
                except ValueError:
                    print("Errore: Inserisci una quantità numerica valida.")

    def list_products(self, warehouse):
        """
        Mostra il contenuto del magazzino in formato tabellare.

        Parametri:
            warehouse (dict): dizionario contenente i prodotti del magazzino.
        """
        table = self.get_table(warehouse)
        print(tabulate(table, headers=self._headers, tablefmt="github"))

    def help_me(self):
        """
        Stampa l'elenco dei comandi disponibili per l'utente.
        """
        print("""
        I comandi disponibili sono i seguenti:\n
        - aggiungi: aggiungi un prodotto al magazzino.
        - elenca: elenca i prodotto in magazzino.
        - vendita: registra una vendita effettuata.
        - profitti: mostra i profitti totali.
        - aiuto: mostra i possibili comandi.
        - chiudi: esci dal programma.
        """)

    def close(self):
        """
        Termina il programma con un messaggio di chiusura.
        """
        print("Bye bye!")
        os._exit(0)

    def not_available_cmd(self, cmd):
        """
        Gestisce un comando non riconosciuto e mostra un messaggio d'errore.

        Parametri:
            cmd (str): comando non valido inserito dall'utente.
        """
        print(
            f"""
            {cmd.title()} è un comando non valido!
            I comandi disponibili sono i seguenti:\n
            - aggiungi: aggiungi un prodotto al magazzino.
            - elenca: elenca i prodotto in magazzino.
            -  vendita: registra una vendita effettuata.
            - profitti: mostra i profitti totali.
            - aiuto: mostra i possibili comandi.
            - chiudi: esci dal programma.
            """
        )

    def profits(self, warehouse_sell):
        """
        Calcola e mostra i profitti totali generati dalle vendite.

        Parametri:
            warehouse_sell (dict): dizionario contenente i prodotti venduti.
        """
        print(f"\nPROFITTI: € {sum([v['quantity'] * (v['price_sell'] - v['price_buy']) for v in warehouse_sell.values()]) :.2f}\n")

    def sell(self, warehouse, warehouse_sell):
        """
        Registra una o più vendite aggiornando il magazzino principale, riducendo la quantitò, e il magazzino delle vendite, aumentado.

        Parametri:
            warehouse (dict): magazzino principale da cui vengono sottratti i prodotti.
            warehouse_sell (dict): magazzino delle vendite in cui vengono aggiunti i prodotti venduti.
        """
        while True:
            while True:
                try:
                    name_sell = input("Nome del prodotto: ")
                    name_sell = name_sell.title()
                    if not name_sell.isalpha():
                        raise ValueError("Il nome deve contenere solo lettere.")
                    if name_sell in warehouse.keys():
                        break
                except ValueError as e:
                    print(e)

            while True:
                try:
                    quantity_sell = int(input("Quantità vendute: "))
                    if quantity_sell > warehouse[name_sell]["quantity"]:
                        raise ValueError(f"La quantità per il prodotto {name_sell} non è in magazzino.\nIn magazino ci sono {warehouse[name_sell]['quantity']} unità di {name_sell}.")
                    break
                except ValueError as e:
                    print(e)
                    print("Errore: Inserisci una quantità numerica valida o una quantità disponibile.")

            if name_sell in warehouse_sell.keys():
                warehouse_sell[name_sell]["quantity"] += quantity_sell
            else:
                warehouse_sell[name_sell] = {
                    "quantity": quantity_sell,
                    "price_buy": warehouse[name_sell]["price_buy"],
                    "price_sell": warehouse[name_sell]["price_sell"]
                }

            warehouse[name_sell]["quantity"] -= quantity_sell

            while True:
                try:
                    choice = input("Aggiungere un altro prodotto? (sì/no): ")
                    if choice.lower() == "no" and len(warehouse_sell.keys()) == 1:
                        print("VENDITA REGISTRATA")
                        print(f"{quantity_sell} X {name_sell}")
                        print(f"TOTALE: {warehouse_sell[name_sell]['quantity'] * warehouse_sell[name_sell]['price_sell'] - warehouse_sell[name_sell]['quantity'] * warehouse_sell[name_sell]['price_buy']:.2f}")
                        return
                    elif choice.lower() == "no" and len(warehouse_sell.keys()) > 1:
                        for k, v in warehouse_sell.items():
                            print("VENDITA REGISTRATA")
                            print(f"- {v['quantity']} X {k}: €{v['quantity'] * v['price_sell'] - v['quantity'] * v['price_buy']:.2f}")
                        print(f"TOTALE: {sum([v['quantity'] * v['price_sell'] - v['quantity'] * v['price_buy'] for v in warehouse_sell.values()]):.2f}")
                        return
                    elif choice.lower() in ["sì", "si"]:
                        break
                    else:
                        raise ValueError(f"Valore {choice} non valido. Scegli tra sì o no.")
                except ValueError as e:
                    print(e)


# get warehouse name from the user with try-except
while True:
    try:
      user_filename = input(f"Inserisci il nome del magazzino: ")
      user_filename = user_filename.lower()
      if not user_filename.isalpha():
        raise ValueError("Il nome deve contenere solo lettere.")
      break
    except ValueError as e:
      print(e)
wh = Warehouse(user_filename)

# read the warehouse. If not in the folder, the script will prompt the user to create it.
warehouse = wh.load_data(sell=False)
warehouse_sell = wh.load_data(sell=True)

# welcome message to know which cmds are in the sw
print(
  """
  I comandi disponibili sono i seguenti:

    - aggiungi: aggiungi un prodotto al magazzino.
    - elenca: elenca i prodotto in magazzino.
    - vendita: registra una vendita effettuata.
    - profitti: mostra i profitti totali.
    - aiuto: mostra i possibili comandi.
    - chiudi: esci dal programma.
  """)

# script
while True:
  
  cmd = input("Inserisci un comando: ")
  
  if cmd == "aggiungi":
    wh.add_product(warehouse)
    wh.save_data(warehouse, sell=False)
  elif cmd == "elenca":
    wh.list_products(warehouse)
  elif cmd == "vendita":
    wh.sell(warehouse, warehouse_sell)
    wh.save_data(warehouse, sell=False)
    wh.save_data(warehouse_sell, sell=True)
  elif cmd == "profitti":
    new_warehouse_sell = wh.load_data(sell=True)
    wh.profits(new_warehouse_sell)
  elif cmd == "aiuto":
    wh.help_me()
  elif cmd == "chiudi":
    wh.close()
  elif cmd not in ["aggiungi", "elenca", "vendita", "profitti", "aiuto", "chiudi"]:
    wh.not_available_cmd(cmd)
  