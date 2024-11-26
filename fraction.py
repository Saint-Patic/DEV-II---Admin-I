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
        POST : self.num declarer avec la valeur de num
               self.den declarer avec la valeur de den
        """
        if den == 0:
            raise ValueError("Le dénominateur ne peut pas être égale à zéro.")
        self.num = num
        self.den = den


    @property
    def numerator(self):
        return self.num
    @property
    def denominator(self):
        return self.den

# ------------------ Textual representations ------------------

    def __str__(self):
        """Return a textual representation of the reduced form of the fraction

        PRE : /
        POST : Retourne une chaine au format "num/den" après réduction
        """
        # trouver le PGCD
        a, b = abs(self.num), abs(self.den)
        while b != 0:
            a, b = b, a % b
        gcd = a

        reduced_num = self.num // gcd
        reduced_den = self.den // gcd

        return f"{reduced_num}/{reduced_den}"

    def as_mixed_number(self) :
        """Return a textual representation of the reduced form of the fraction as a mixed number

        A mixed number is the sum of an integer and a proper fraction

        PRE : /
        POST : Retourne une chaine au format "entier positif(reste en fraction)"
        """
        if self.num%self.den == 0:
            return f"{self.num // self.den}"
        return f"Partie entière : {self.num//self.den} | Reste : {self.num%self.den}/{self.den}"

    
# ------------------ Operators overloading ------------------

    def __add__(self, other):
        """Overloading of the + operator for fractions"""
        a, b = self.den, other.den
        while b != 0:
            a, b = b, a % b
        gcd = a
        lcm = (self.den * other.den) // gcd

        num1 = self.num * (lcm // self.den)
        num2 = other.num * (lcm // other.den)

        return Fraction(num1 + num2, lcm)



    def __sub__(self, other):
        """Overloading of the - operator for fractions"""
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

        PRE : ?
        POST : ?
        """
        return Fraction(self.num * other.num, self.den * other.den)


    def __truediv__(self, other):
        """Overloading of the / operator for fractions

        PRE : ?
        POST : ?
        """
        return Fraction(self.num * other.den, self.den * other.num)


    def __pow__(self, other):
        """Overloading of the ** operator for fractions

        PRE : ?
        POST : ?
        """
        return Fraction(self.num ** other, self.den ** other)
    
    
    def __eq__(self, other) : 
        """Overloading of the == operator for fractions
        
        PRE : ?
        POST : ? 
        
        """
        return self.num == other.num and self.den == other.den
        
    def __float__(self) :
        """Returns the decimal value of the fraction

        PRE : ?
        POST : ?
        """
        return self.num/self.den
    
# TODO : [BONUS] You can overload other operators if you wish (ex : <, >, ...)




# ------------------ Properties checking  ------------------

    def is_zero(self):
        """Check if a fraction's value is 0

        PRE : Une instance de Fraction
        POST : Retourne True si la fraction =0 sinon False
        """
        return self.num/self.den == 0


    def is_integer(self):
        """Check if a fraction is integer (ex : 8/4, 3, 2/2, ...)

        PRE : Une instance de Fraction
        POST : Retourne True si la fraction est un entier positif sinon False
        """
        return self.num % self.den == 0

    def is_proper(self):
        """Check if the absolute value of the fraction is < 1

        PRE : Une instance de Fraction
        POST : Retourne True si |num| < |den| sinon False
        """
        return abs(self.num) < abs(self.den)

    def is_unit(self):
        """Check if a fraction's numerator is 1 in its reduced form

        PRE : Une instance de Fraction
        POST : Retourne True si num == 1 sinon False
        """
        return self.num == 1

    def is_adjacent_to(self, other) :
        """Check if two fractions differ by a unit fraction

        Two fractions are adjacents if the absolute value of the difference is a unit fraction

        PRE : deux instances de Fraction
        POST : Retourne True si les deux fractions sont adjacentes sinon False
        """
        pass

if __name__ == "__main__":
    fract1 = Fraction(5, 7)
    fract2 = Fraction(1, 4)
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