import argparse
import pandas as pd
from pathlib import Path

# Module de gestion de la base consolidée
database = pd.DataFrame()

def load_csv(file_path: str) -> pd.DataFrame:
    try:
        print(f"Tentative de chargement du fichier : {file_path}")
        data = pd.read_csv(file_path)
        print(f"Contenu chargé :\n{data}")
        return data
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return pd.DataFrame()

def consolidate_files(file_paths: list[Path]):
    global database
    frames = []
    for file_path in file_paths:
        data = load_csv(str(file_path))
        if not data.empty:
            print(f"Données chargées depuis {file_path} :\n{data.head()}")
            frames.append(data)
        else:
            print(f"Fichier vide ou non valide : {file_path}")
    if frames:
        database = pd.concat([database] + frames, ignore_index=True)
        print("Base consolidée mise à jour avec succès.")
        save_database()
    else:
        print("Aucun fichier valide à consolider.")

def save_database():
    global database
    if not database.empty:
        database.to_csv("consolidated_database.csv", index=False)
        print("Base consolidée sauvegardée.")
    else:
        print("La base consolidée est vide, aucune sauvegarde effectuée.")

def load_database():
    global database
    try:
        database = pd.read_csv("consolidated_database.csv")
        print("Base consolidée chargée avec succès.")
    except FileNotFoundError:
        print("Aucune base consolidée trouvée, démarrage avec une base vide.")
        database = pd.DataFrame()

def search_inventory(criteria: str, value):
    global database
    if criteria not in database.columns:
        print(f"Critère '{criteria}' non valide. Colonnes disponibles : {', '.join(database.columns)}")
        return

    if value.lower() == "nan":
        results = database[pd.isnull(database[criteria])]
    else:
        column_type = database[criteria].dtype
        try:
            if column_type == 'int64':
                value = int(value)
            elif column_type == 'float64':
                value = float(value)
        except ValueError:
            print(f"Impossible de convertir la valeur '{value}' au type attendu ({column_type}).")
            return

        results = database[database[criteria] == value]

    if results.empty:
        print("Aucun résultat trouvé.")
    else:
        print(f"Résultats trouvés pour {criteria} = {value} :\n{results}")

def generate_report(output_path: str):
    global database
    if database.empty:
        print("La base consolidée est vide. Aucun rapport à générer.")
        return
    summary = database.groupby('Category').agg(
        TotalQuantity=('Quantity', 'sum'),
        TotalValue=('UnitPrice', lambda x: (x * database.loc[x.index, 'Quantity']).sum())
    )
    summary.to_csv(output_path)
    print(f"Rapport généré avec succès : {output_path}")

def show_data():
    global database
    if database.empty:
        print("La base consolidée est vide.")
    else:
        print("Données consolidées :")
        print(database)

def interactive_mode():
    """
    Démarre un mode interactif pour exécuter les commandes.
    """
    print("=== Mode interactif : Gestion d'inventaire ===")
    print("Entrez une commande ou 'help' pour voir les options.")
    while True:
        command = input(">>> ").strip()
        if command in ["exit", "quit"]:
            print("Fin du mode interactif.")
            break
        elif command == "help":
            print("""
Commandes disponibles :
  - import <fichier1> <fichier2> ... : Importer et consolider des fichiers CSV.
  - search <colonne> <valeur>        : Rechercher des produits dans l'inventaire.
  - report <fichier_output>          : Générer un rapport récapitulatif.
  - show                             : Afficher les données consolidées.
  - exit / quit                      : Quitter le mode interactif.
  - help                             : Afficher cette aide.
            """)
        elif command.startswith("import "):
            files = command.split()[1:]
            consolidate_files([Path(file) for file in files])
        elif command.startswith("search "):
            try:
                _, criteria, value = command.split(maxsplit=2)
                search_inventory(criteria, value)
            except ValueError:
                print("Usage : search <colonne> <valeur>")
        elif command.startswith("report "):
            output_path = command.split(maxsplit=1)[1]
            generate_report(output_path)
        elif command == "show":
            show_data()
        else:
            print("Commande inconnue. Tapez 'help' pour voir les options.")

def main():
    """
    Point d'entrée principal du programme.
    Gère les commandes interactives ou non.
    """
    parser = argparse.ArgumentParser(description="Gestion d'inventaire consolidée.")
    parser.add_argument('--interactive', action='store_true', help="Lancer le programme en mode interactif.")
    args = parser.parse_args()

    load_database()

    if args.interactive:
        interactive_mode()
    else:
        print("Utilisez l'option '--interactive' pour lancer le mode interactif ou passez des commandes via argparse.")
        print("Exemple : python script.py --interactive")

if __name__ == "__main__":
    main()
