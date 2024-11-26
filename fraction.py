class Fraction:
    """Class representing a fraction and operations on it

    Author : V. Van den Schrieck
    Date : October 2021
    This class allows fraction manipulations through several operations.
    """

    def __init__(self, num=0, den=1):
        """This builds a fraction based on some numerator and denominator.

        PRE : num est un entier positif
              den est un entier positif
        POST : self.num est initialisé avec la valeur de num
               self.den est initialisé avec la valeur de den
        """
        if den == 0:
            raise ValueError("Le dénominateur ne peut pas être égal à zéro.")
        self.num = num
        self.den = den

    @property
    def numerator(self):
        """Returns the numerator of the fraction.

        PRE : Une instance de Fraction
        POST : Retourne le numérateur de la fraction (self.num)
        """
        return self.num

    @property
    def denominator(self):
        """Returns the denominator of the fraction.

        PRE : Une instance de Fraction
        POST : Retourne le dénominateur de la fraction (self.den)
        """
        return self.den

    # ------------------ Textual representations ------------------

    def __str__(self):
        """Return a textual representation of the reduced form of the fraction

        PRE : /
        POST : Retourne une chaîne de caractères au format "num/den" après réduction de la fraction
        """
        a, b = abs(self.num), abs(self.den)
        while b != 0:
            a, b = b, a % b
        gcd = a

        numReduit = self.num // gcd
        denReduit = self.den // gcd

        return f"{numReduit}/{denReduit}"

    def as_mixed_number(self):
        """Return a textual representation of the reduced form of the fraction as a mixed number

        A mixed number is the sum of an integer and a proper fraction.

        PRE : /
        POST : Retourne une chaîne au format "Partie entière : <entier> | Reste : <reste sous forme réduite>"
        """
        # Calcul du PGCD pour réduire la fraction
        a, b = abs(self.num), abs(self.den)
        while b != 0:
            a, b = b, a % b
        gcd = a

        numReduit = self.num // gcd
        denReduit = self.den // gcd

        # Calcul de la partie entière et du reste
        partEntier = numReduit // denReduit
        resteNum = abs(numReduit % denReduit)

        if resteNum == 0:
            return f"Partie entière : {partEntier} | Reste : 0"
        return f"Partie entière : {partEntier} | Reste : {resteNum}/{denReduit}"

    # ------------------ Operators overloading ------------------

    def __add__(self, other):
        """Overloading of the + operator for fractions

        PRE : other est une instance de Fraction
        POST : Retourne une nouvelle instance de Fraction représentant la somme des deux fractions
        """
        a, b = self.den, other.den
        while b != 0:
            a, b = b, a % b
        gcd = a
        lcm = (self.den * other.den) // gcd

        num1 = self.num * (lcm // self.den)
        num2 = other.num * (lcm // other.den)

        return Fraction(num1 + num2, lcm)

    def __sub__(self, other):
        """Overloading of the - operator for fractions

        PRE : other est une instance de Fraction
        POST : Retourne une nouvelle instance de Fraction représentant la différence entre les deux fractions
        """
        a, b = self.den, other.den
        while b != 0:
            a, b = b, a % b
        gcd = a
        lcm = (self.den * other.den) // gcd

        num1 = self.num * (lcm // self.den)
        num2 = other.num * (lcm // other.den)

        return Fraction(num1 - num2, lcm)

    def __mul__(self, other):
        """Overloading of the * operator for fractions

        PRE : other est une instance de Fraction
        POST : Retourne une nouvelle instance de Fraction représentant le produit des deux fractions
        """
        return Fraction(self.num * other.num, self.den * other.den)

    def __truediv__(self, other):
        """Overloading of the / operator for fractions

        PRE : other est une instance de Fraction
        POST : Retourne une nouvelle instance de Fraction représentant le quotient des deux fractions
        """
        return Fraction(self.num * other.den, self.den * other.num)

    def __pow__(self, other):
        """Overloading of the ** operator for fractions

        PRE : other est un entier
        POST : Retourne une nouvelle instance de Fraction représentant la fraction élevée à la puissance `other`
        """
        return Fraction(self.num ** other, self.den ** other)

    def __eq__(self, other):
        """Overloading of the == operator for fractions

        PRE : other est une instance de Fraction
        POST : Retourne True si les deux fractions sont égales, sinon False
        """
        return self.num == other.num and self.den == other.den or self.num//self.den == other.num//other.den

    def __float__(self):
        """Returns the decimal value of the fraction

        PRE : /
        POST : Retourne la valeur décimale de la fraction (numérateur / dénominateur)
        """
        return self.num / self.den

    # ------------------ Properties checking ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : Une instance de Fraction
        POST : Retourne True si la fraction est égale à 0, sinon False
        """
        return self.num == 0

    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : Une instance de Fraction
        POST : Retourne True si la fraction est un entier, sinon False
        """
        return self.num % self.den == 0

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : Une instance de Fraction
        POST : Retourne True si |num| < |den|, sinon False
        """
        return abs(self.num) < abs(self.den)

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : Une instance de Fraction
        POST : Retourne True si num == 1, sinon False
        """
        return self.num == 1

    def is_adjacent_to(self, other):
        """Check if two fractions differ by a unit fraction

        Two fractions are adjacents if the absolute value of the difference is a unit fraction

        PRE : deux instances de Fraction
        POST : Retourne True si les deux fractions sont adjacentes, sinon False
        """
        pass


if __name__ == "__main__":
    fract1 = Fraction(5, 4)
    fract2 = Fraction(1, 2)
    exposant = 3

    print(fract1.as_mixed_number())
    print(fract2.as_mixed_number())
    print(f"Addition : {fract1.numerator}/{fract1.denominator} + {fract2.numerator}/{fract2.denominator} = {fract1 + fract2}")
    print(f"Soustraction : {fract1.numerator}/{fract1.denominator} - {fract2.numerator}/{fract2.denominator} = {fract1 - fract2}")
    print(f"Multiplication : {fract1.numerator}/{fract1.denominator} * {fract2.numerator}/{fract2.denominator} = {fract1 * fract2}")
    print(f"Division : {fract1.numerator}/{fract1.denominator} / {fract2.numerator}/{fract2.denominator} = {fract1 / fract2}")
    print(f"Soustraction : ({fract1.numerator}/{fract1.denominator})^{exposant} = {fract1 ** exposant}")
    print(f"Egalité : {fract1.numerator}/{fract1.denominator} == {fract2.numerator}/{fract2.denominator} = {fract1 == fract2}")
    print(f"Décimale de {fract1.numerator}/{fract1.denominator} = {fract1.__float__()}")
    print(f"Décimale de {fract2.numerator}/{fract2.denominator} = {fract2.__float__()}")