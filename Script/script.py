import argparse
import pandas as pd
from pathlib import Path
from tabulate import tabulate

# Module de gestion de la base consolidée
database = pd.DataFrame()

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Charge un fichier CSV en DataFrame.

    PRE: file_path est un chemin valide vers un fichier CSV.
    POST: Retourne un DataFrame contenant les données du fichier CSV.
    """
    try:
        print(f"Tentative de chargement du fichier : {file_path}")
        data = pd.read_csv(file_path)
        print(f"Contenu chargé :\n{data}")
        return data
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
    except pd.errors.ParserError:
        print(f"Erreur de format dans le fichier CSV : {file_path}")
    except Exception as e:
        print(f"Erreur inattendue lors du chargement : {e}")
    return pd.DataFrame()

def consolidate_files(file_paths: list[Path]):
    """
    Consolide plusieurs fichiers CSV en une base de données unique.

    PRE: file_paths est une liste de chemins vers des fichiers CSV.
    POST: Met à jour la base de données consolidée et la sauvegarde.
    """
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
    """
    Sauvegarde la base de données consolidée dans un fichier CSV.

    PRE: La base de données peut être vide ou non.
    POST: Sauvegarde la base dans un fichier "consolidated_database.csv".
    """
    global database
    if not database.empty:
        database.to_csv("consolidated_database.csv", index=False)
        print("Base consolidée sauvegardée.")
    else:
        print("La base consolidée est vide, aucune sauvegarde effectuée.")

def load_database():
    """
    Charge la base de données consolidée à partir d'un fichier CSV.

    PRE: Le fichier "consolidated_database.csv" peut exister ou non.
    POST: Charge la base de données dans le programme ou initialise une base vide.
    """
    global database
    try:
        database = pd.read_csv("consolidated_database.csv")
        print("Base consolidée chargée avec succès.")
    except FileNotFoundError:
        print("Aucune base consolidée trouvée, démarrage avec une base vide.")
        database = pd.DataFrame()

def search_inventory(criteria: str, value: str):
    """
    Recherche des éléments dans la base de données selon un critère et une valeur donnés.

    PRE: criteria est une colonne existante dans la base de données.
    POST: Affiche les résultats correspondants à la recherche.
    """
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

def generate_report(output_path: str = None):
    """
    Génère un rapport récapitulatif sous forme de tableau.

    PRE: La base de données contient les colonnes 'Product', 'Category', 'Quantity', et 'UnitPrice'.
    POST: Affiche un tableau dans la console et sauvegarde un fichier CSV si un chemin est fourni.
    """
    global database
    if database.empty:
        print("La base consolidée est vide. Aucun rapport à générer.")
        return

    summary = database.groupby(['Category', 'Product']).agg(
        TotalQuantity=('Quantity', 'sum'),
        TotalValue=('UnitPrice', lambda x: (x * database.loc[x.index, 'Quantity']).sum())
    ).reset_index()

    print("\n=== Rapport Récapitulatif ===")
    print(tabulate(summary, headers='keys', tablefmt='grid', showindex=False))

    if output_path:
        summary.to_csv(output_path, index=False)
        print(f"Rapport sauvegardé avec succès : {output_path}")

def show_data():
    """
    Affiche les données consolidées.

    PRE: La base consolidée peut être vide ou non.
    POST: Affiche les données dans la console.
    """
    global database
    if database.empty:
        print("La base consolidée est vide.")
    else:
        print("Données consolidées :")
        print(database)

def interactive_mode():
    """
    Lancer le programme en mode interactif pour une interaction utilisateur.
    """
    while True:
        print("""
        Veuillez choisir une option :
        1. Consolider les fichiers CSV
        2. Afficher le CSV consolidé
        3. Rechercher dans le CSV consolidé
        4. Générer un rapport
        5. Quitter
        """)
        choice = input("Votre choix (1-5) : ").strip()

        if choice == "1":
            files = input("Entrez les chemins des fichiers CSV à consolider (séparés par des espaces) : ").strip().split()
            consolidate_files([Path(file) for file in files])
        elif choice == "2":
            show_data()
        elif choice == "3":
            criteria = input("Entrez le nom de la colonne pour la recherche : ").strip()
            value = input("Entrez la valeur à rechercher : ").strip()
            search_inventory(criteria, value)
        elif choice == "4":
            output_path = input("Entrez le chemin du fichier de rapport à générer : ").strip()
            generate_report(output_path)
        elif choice == "5":
            break
        else:
            print("Choix invalide. Veuillez entrer un chiffre entre 1 et 5.")

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
