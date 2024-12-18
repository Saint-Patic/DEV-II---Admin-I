import unittest
import pandas as pd
import os
from pathlib import Path
from script import (
    load_csv,
    consolidate_files,
    save_database,
    load_database,
    search_inventory,
    generate_report,
    show_data
)


class TestInventoryManagement(unittest.TestCase):

    def setUp(self):
        """
        Configuration avant chaque test.
        Initialise une base de données temporaire.
        """
        global database
        database = pd.DataFrame()

    def tearDown(self):
        """
        Nettoyage après chaque test.
        Supprime les fichiers temporaires générés.
        """
        if os.path.exists("consolidated_database.csv"):
            os.remove("consolidated_database.csv")
        if os.path.exists("test_report.csv"):
            os.remove("test_report.csv")

    def test_load_csv_valid_file(self):
        """Tester le chargement d'un fichier CSV valide."""
        data = load_csv("test_data.csv")
        self.assertFalse(data.empty)
        self.assertIn("Category", data.columns)

    def test_load_csv_invalid_file(self):
        """Tester le chargement d'un fichier CSV invalide."""
        data = load_csv("invalid_file.csv")
        self.assertTrue(data.empty)

    def test_consolidate_files(self):
        """Tester la consolidation de plusieurs fichiers CSV."""
        file1 = "test_data1.csv"
        file2 = "test_data2.csv"
        pd.DataFrame({
            "Product": ["A", "B"],
            "Category": ["Tools", "Tools"],
            "Quantity": [10, 20],
            "UnitPrice": [5.0, 7.5]
        }).to_csv(file1, index=False)
        pd.DataFrame({
            "Product": ["C", "D"],
            "Category": ["Garden", "Garden"],
            "Quantity": [15, 25],
            "UnitPrice": [10.0, 12.5]
        }).to_csv(file2, index=False)

        consolidate_files([Path(file1), Path(file2)])
        self.assertEqual(len(database), 4)
        self.assertIn("Category", database.columns)

        os.remove(file1)
        os.remove(file2)

    def test_save_and_load_database(self):
        """Tester la sauvegarde et le chargement de la base consolidée."""
        pd.DataFrame({
            "Product": ["A"],
            "Category": ["Tools"],
            "Quantity": [10],
            "UnitPrice": [5.0]
        }).to_csv("consolidated_database.csv", index=False)

        load_database()
        self.assertEqual(len(database), 1)
        self.assertIn("Product", database.columns)

        save_database()
        self.assertTrue(os.path.exists("consolidated_database.csv"))

    def test_search_inventory(self):
        """Tester la recherche dans l'inventaire."""
        global database
        database = pd.DataFrame({
            "Product": ["A", "B", "C"],
            "Category": ["Tools", "Garden", "Tools"],
            "Quantity": [10, 20, 15],
            "UnitPrice": [5.0, 7.5, 10.0]
        })

        search_inventory("Category", "Tools")
        search_inventory("Category", "Nonexistent")
        search_inventory("InvalidColumn", "Tools")

    def test_generate_report(self):
        """Tester la génération d'un rapport."""
        global database
        database = pd.DataFrame({
            "Product": ["A", "B", "C"],
            "Category": ["Tools", "Garden", "Tools"],
            "Quantity": [10, 20, 15],
            "UnitPrice": [5.0, 7.5, 10.0]
        })

        generate_report("test_report.csv")
        self.assertTrue(os.path.exists("test_report.csv"))
        report = pd.read_csv("test_report.csv")
        self.assertIn("Product", report.columns)
        self.assertIn("Category", report.columns)

    def test_show_data(self):
        """Tester l'affichage des données consolidées."""
        global database
        database = pd.DataFrame({
            "Product": ["A", "B", "C"],
            "Category": ["Tools", "Garden", "Tools"],
            "Quantity": [10, 20, 15],
            "UnitPrice": [5.0, 7.5, 10.0]
        })
        show_data()
        self.assertFalse(database.empty)


if __name__ == "__main__":
    unittest.main()
