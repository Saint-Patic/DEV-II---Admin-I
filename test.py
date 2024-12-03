import unittest
from fraction import Fraction


class TestFraction(unittest.TestCase):
    def setUp(self):
        """Initialisation des fractions pour les tests."""
        self.fract1 = Fraction(5, 4)  # 5/4
        self.fract2 = Fraction(1, 2)  # 1/2

    # ------------------ Test Constructor ------------------

    def test_zero_denominator(self):
        """Test si la création d'une fraction avec un dénominateur de 0 lève une exception."""
        with self.assertRaises(ValueError) as context:
            Fraction(1, 0)
        self.assertEqual(str(context.exception), "Le dénominateur ne peut pas être égal à zéro.")

    def test_zero_numerator(self):
        """Test si la fraction avec un numérateur 0 est correcte."""
        zero_fraction = Fraction(0, 5)
        self.assertEqual(zero_fraction.numerator, 0)
        self.assertEqual(zero_fraction.denominator, 5)
        self.assertTrue(zero_fraction.is_zero())

    # ------------------ Test Textual representations ------------------

    def test_str(self):
        """Test la représentation en chaîne de caractères de la fraction."""
        self.assertEqual(str(self.fract1), "5/4")
        self.assertEqual(str(self.fract2), "1/2")

    def test_as_mixed_number(self):
        """Test la représentation en nombre mixte."""
        self.assertEqual(self.fract1.as_mixed_number(), "Partie entière : 1 | Reste : 1/4")
        self.assertEqual(self.fract2.as_mixed_number(), "Partie entière : 0 | Reste : 1/2")

    # ------------------ Test Operators overloading ------------------

    def test_addition(self):
        """Test la surcharge de l'opérateur +."""
        result = self.fract1 + self.fract2
        self.assertEqual(str(result), "7/4")

    def test_subtraction(self):
        """Test la surcharge de l'opérateur -."""
        result = self.fract1 - self.fract2
        self.assertEqual(str(result), "3/4")

    def test_multiplication(self):
        """Test la surcharge de l'opérateur *."""
        result = self.fract1 * self.fract2
        self.assertEqual(str(result), "5/8")

    def test_division(self):
        """Test la surcharge de l'opérateur /."""
        result = self.fract1 / self.fract2
        self.assertEqual(str(result), "5/2")

    def test_power(self):
        """Test la surcharge de l'opérateur **."""
        result = self.fract1 ** 2
        self.assertEqual(str(result), "25/16")

    def test_equality(self):
        """Test la surcharge de l'opérateur ==."""
        self.assertTrue(self.fract1 == Fraction(5, 4))
        self.assertFalse(self.fract1 == self.fract2)

    def test_float(self):
        """Test la conversion de la fraction en nombre flottant."""
        self.assertAlmostEqual(float(self.fract1), 1.25)
        self.assertAlmostEqual(float(self.fract2), 0.5)

    # ------------------ Test Properties checking ------------------

    def test_is_zero(self):
        """Test si la fraction est nulle."""
        zero_fraction = Fraction(0, 1)
        self.assertTrue(zero_fraction.is_zero())
        self.assertFalse(self.fract1.is_zero())

    def test_is_integer(self):
        """Test si la fraction est un entier."""
        integer_fraction = Fraction(4, 2)
        self.assertTrue(integer_fraction.is_integer())
        self.assertFalse(self.fract1.is_integer())

    def test_is_proper(self):
        """Test si la fraction est propre (|num| < |den|)."""
        proper_fraction = Fraction(1, 3)
        self.assertTrue(proper_fraction.is_proper())
        self.assertFalse(self.fract1.is_proper())

    def test_is_unit(self):
        """Test si la fraction est une unité (numérateur = 1)."""
        unit_fraction = Fraction(1, 4)
        self.assertTrue(unit_fraction.is_unit())
        self.assertFalse(self.fract1.is_unit())

    def test_is_adjacent_to(self):
        """Test si deux fractions sont adjacentes (diffèrent d'une unité)."""
        adjacent_fraction = Fraction(4, 4)
        self.assertTrue(self.fract1.is_adjacent_to(adjacent_fraction))
        self.assertFalse(self.fract1.is_adjacent_to(self.fract2))


if __name__ == "__main__":
    unittest.main()
