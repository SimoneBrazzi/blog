
path = os.path.expanduser(os.getcwd())
# headers for CLI table
headers = ["PRODOTTO", "QUANTITÀ", "PREZZO", "COSTO"]


def save_json(data, file):
    
    while True:
      try:
        with open(path + file + ".json", "w") as f:
          json.dump(data, f, indent=4)
        break
      except FileNotFoundError:
        q = input(f"Vuoi inizializzare un database vuoto? (sì/no): ")
        if q.lower() in ["sì", "si"]:
          tmp = input("Scegli un nome per il db: ")
          with open(path + tmp + ".json", "w") as f:
            json.dump({}, f, indent=4)
            print(f"Database inizializzato come '{tmp}.json'.")
          break
        else:
          print("File non trovato e l'utente non ha voluto inizializzarlo.")
          return None


def read_json(path, file):
  
    while True:
        try:
            with open(path + file + ".json", 'r') as f:
                data = json.load(f)
                return data

        except FileNotFoundError:
            q = input(f"Vuoi inizializzare un {file.title()} database? (sì/no): ")

            if q.lower() in ["sì", "si"]:
                data = {}
                print(f"{file.title()} inizializzato.")
                save_json(data, file)
                return data
                
            elif q.lower() == "no":
                print("File non trovato e l'utente non ha voluto inizializzarlo.")
                break

            else:
              print("Risposta non valida. Riprova.")


def get_table(data):
  return [[product, info["quantity"], info["price_sell"], info["price_buy"]] for product, info in data.items()]


def add_product(d):
  
  while True:
    try:
      name = input("Nome del prodotto: ")
      name = name.title()
      if not name.isalpha():
        raise ValueError("Il nome deve contenere solo lettere.")
      break
    except ValueError as e:
      print(e)
  
  if name not in d.keys():
    # quantity
    try:
      quantity = int(input("Quantità: "))
      price_buy = float(input("Prezzo d'acquisto: "))
      price_sell = float(input("Prezzo di vendita: "))
    except ValueError:
      print("Errore: Inserisci valori numerici validi per quantità e prezzi.")
      return
    
    values = {"quantity": int(quantity), "price_buy": float(price_buy), "price_sell": float(price_sell)}
    d[name] = values
  
  else:
    while True:
      try:
        # existing product: update quantity
        quantity = int(input("Quantità da aggiungere: "))
        d[name]["quantity"] += quantity
        break
      except ValueError:
        print("Errore: Inserisci una quantità numerica valida.")


def list_products(warehouse):
  table = get_table(warehouse)
  print(tabulate(table, headers=headers, tablefmt="github"))


def help_me():
    print("""
    I comandi disponibili sono i seguenti:\n
    - aggiungi: aggiungi un prodotto al magazzino.
    - elenca: elenca i prodotto in magazzino.
    - vendita: registra una vendita effettuata.
    - profitti: mostra i profitti totali.
    - aiuto: mostra i possibili comandi.
    - chiudi: esci dal programma.
    """
    )  


def close():
    print("Bye bye!")
    os._exit(0)


def not_available_cmd(cmd):
      print(
        f"""
        {cmd.title()} è un comando non valido!
        I comandi disponibili sono i seguenti:\n
        - aggiungi: aggiungi un prodotto al magazzino.
        - elenca: elenca i prodotto in magazzino.
        - vendita: registra una vendita effettuata.
        - profitti: mostra i profitti totali.
        - aiuto: mostra i possibili comandi.
        - chiudi: esci dal programma.
        """
      )


def profits(warehouse_sell):

  print(f"\nPROFITTI: € {sum([v['quantity'] * (v['price_sell'] - v['price_buy']) for v in warehouse_sell.values()]) :.2f}\n")


def sell(warehouse, warehouse_sell):
  
  while True:
    
    # input nome prodotto
    while True:
      try:
        name_sell = input("Nome del prodotto: ")
        name_sell = name_sell.title()
        
        if not name_sell.isalpha():
          raise ValueError("Il nome deve contenere solo lettere.")
        if name_sell in warehouse.keys():
          break  # name is valid, exit this loop
      
      except ValueError as e:
        print(e)
    
    # input quantità
    while True:
      try:
        # existing product: update quantity
        quantity_sell = int(input("Quantità vendute: "))
        if quantity_sell > warehouse[name_sell]["quantity"]:
          raise ValueError(f"La quantità per il prodotto {name_sell} non è in magazzino.\nIn magazino ci sono {warehouse[name_sell]['quantity']} unità di {name_sell}.")
        break  # quantity is valid, exit this loop
      
      except ValueError as e:
        print(e)
        print("Errore: Inserisci una quantità numerica valida o una quantità disponibile.")
    
    # update warehouse_sell adding selled products
    if name_sell in warehouse_sell.keys():
        warehouse_sell[name_sell]["quantity"] += quantity_sell
    else:
        warehouse_sell[name_sell] = {
            "quantity": quantity_sell,
            "price_buy": warehouse[name_sell]["price_buy"],
            "price_sell": warehouse[name_sell]["price_sell"]
            }
    # update warehouse to remove selled products
    warehouse[name_sell]["quantity"] -= quantity_sell
    
    # add another selled product?
    while True:
      try:
        choice = input("Aggiungere un altro prodotto? (sì/no): ")
        
        if choice.lower() == "no" and len(warehouse_sell.keys()) == 1:
          print("VENDITA REGISTRATA")
          print(f"{quantity_sell} X {name_sell}")
          print(f"TOTALE: {warehouse_sell[name_sell]['quantity'] * warehouse_sell[name_sell]['price_sell'] - warehouse_sell[name_sell]['quantity'] * warehouse_sell[name_sell]['price_buy']:.2f}")
          
          return
        
        elif choice.lower() == "no" and len(warehouse_sell.keys()) > 1:
          for k,v in warehouse_sell.items():
            print("VENDITA REGISTRATA")
            print(f"- {v['quantity']} X {k}: €{warehouse_sell[k]['quantity']*warehouse_sell[k]['price_sell'] - warehouse_sell[k]['quantity']*warehouse_sell[k]['price_buy']:.2f}")
          
          print(f"TOTALE: {sum([warehouse_sell[k]['quantity']*warehouse_sell[k]['price_sell'] - warehouse_sell[k]['quantity']*warehouse_sell[k]['price_buy'] for k,v in warehouse_sell.items()]):.2f}")
          
          return

        elif choice.lower() in ["sì", "si"]:
          break # repeat the cycle

        else:
          raise ValueError("Valore {choice} non valido. Scegli tra sì o no.")
      
      except ValueError as e:
        print(e)

