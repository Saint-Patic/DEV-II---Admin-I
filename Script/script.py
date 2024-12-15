import argparse
import pandas as pd
from pathlib import Path

# Module de gestion de la base consolidée
database = pd.DataFrame()

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Charger un fichier CSV dans un DataFrame.

    PRE : file_path est une chaîne non vide contenant un chemin valide vers un fichier CSV.
    POST : Retourne un DataFrame contenant les données du fichier CSV ou une erreur claire en cas d'échec.
    """
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return pd.DataFrame()

def consolidate_files(file_paths: list[Path]):
    """
    Consolider plusieurs fichiers CSV dans une base unique.

    PRE : file_paths est une liste de chemins valides vers des fichiers CSV.
    POST : Met à jour la base consolidée globale avec les données combinées.
    """
    global database
    frames = []
    for file_path in file_paths:
        data = load_csv(file_path)
        if not data.empty:
            frames.append(data)
    if frames:
        database = pd.concat(frames, ignore_index=True)
        print("Base consolidée mise à jour avec succès.")
    else:
        print("Aucun fichier valide à consolider.")

def search_inventory(criteria: str, value):
    """
    Rechercher dans l'inventaire selon un critère donné.

    PRE : criteria est une chaîne correspondant à une colonne de la base consolidée.
          value est la valeur à rechercher dans cette colonne.
    POST : Retourne et affiche les résultats correspondants ou un message d'erreur.
    """
    global database
    if criteria not in database.columns:
        print(f"Critère '{criteria}' non valide. Colonnes disponibles : {', '.join(database.columns)}")
        return
    results = database[database[criteria] == value]
    if results.empty:
        print("Aucun résultat trouvé.")
    else:
        print(f"Résultats trouvés pour {criteria} = {value} :\n{results}")

def generate_report(output_path: str):
    """
    Générer un rapport récapitulatif des données consolidées.

    PRE : output_path est un chemin valide pour sauvegarder le fichier CSV.
    POST : Exporte un rapport contenant les résumés par catégorie et le stock total.
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

def main():
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

    args = parser.parse_args()

    if args.command == 'import':
        consolidate_files([Path(file) for file in args.files])
    elif args.command == 'search':
        search_inventory(args.criteria, args.value)
    elif args.command == 'report':
        generate_report(args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
