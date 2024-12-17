import argparse
import pandas as pd
from pathlib import Path

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
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
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

def search_inventory(criteria: str, value):
    """
    Recherche des éléments dans la base de données selon un critère et une valeur donnés.

    PRE: criteria est une colonne existante dans la base de données.
    POST: Affiche les résultats correspondants à la recherche.
    """
    global database
    if criteria not in database.columns:
        print(f"Critère '{criteria}' non valide. Colonnes disponibles : {', '.join(database.columns)}")
        return

    # Convertir `value` au type correspondant à la colonne
    column_type = database[criteria].dtype
    try:
        if column_type == 'int64':
            value = int(value)
        elif column_type == 'float64':
            value = float(value)
    except ValueError:
        print(f"Impossible de convertir la valeur '{value}' au type attendu ({column_type}).")
        return

    # Effectuer la recherche
    results = database[database[criteria] == value]
    if results.empty:
        print("Aucun résultat trouvé.")
    else:
        print(f"Résultats trouvés pour {criteria} = {value} :\n{results}")

def generate_report(output_path: str):
    """
    Génère un rapport récapitulatif de la base de données consolidée.

    PRE: La base de données contient des colonnes 'Category', 'Quantity' et 'UnitPrice'.
    POST: Sauvegarde un fichier CSV contenant le rapport.
    """
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

def main():
    """
    Point d'entrée principal du programme.

    Gère les commandes pour importer, rechercher, générer un rapport ou afficher les données.
    """
    parser = argparse.ArgumentParser(description="Gestion d'inventaire consolidée.")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande 'import'
    import_parser = subparsers.add_parser('import', help="Importer et consolider des fichiers CSV")
    import_parser.add_argument('files', nargs='+', help="Chemins vers les fichiers CSV à importer")

    # Commande 'search'
    search_parser = subparsers.add_parser('search', help="Rechercher des produits dans l'inventaire")
    search_parser.add_argument('criteria', help="Critère de recherche (par ex. 'Category')")
    search_parser.add_argument('value', help="Valeur à rechercher")

    # Commande 'report'
    report_parser = subparsers.add_parser('report', help="Générer un rapport récapitulatif")
    report_parser.add_argument('output', help="Chemin pour sauvegarder le fichier de rapport CSV")

    # Commande 'show'
    subparsers.add_parser('show', help="Afficher les données consolidées")

    args = parser.parse_args()

    if args.command == 'import':
        consolidate_files([Path(file) for file in args.files])
    elif args.command == 'search':
        search_inventory(args.criteria, args.value)
    elif args.command == 'report':
        generate_report(args.output)
    elif args.command == 'show':
        show_data()
    else:
        parser.print_help()

if __name__ == "__main__":
    load_database()
    main()
