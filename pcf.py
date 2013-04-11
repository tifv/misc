"""
Periodic continued fractions.

Aimed at Python 3.

Docstrings of main classes contain examples.
Running this as a script will launch doctest.
"""

__all__ = ['PeriodicContinuedFraction', 'FiniteContinuedFraction']

import fractions
import numbers
import math
from functools import reduce

class PeriodicContinuedFraction:
    r"""
    Periodic continued fraction

    This stands for '(sqrt(17) - 19) / 21':
    >>> the_pcf = PeriodicContinuedFraction(-19, 21, 17)

    Value is converted to satisfy some internal requirements
    (see implementation):
    >>> the_pcf
    PeriodicContinuedFraction(-399, 441, 7497)
    >>> the_pcf.tex_repr()
    '\\frac{-399 + \\sqrt{7497}}{441}'

    Computation of continued fraction preperiod and period:
    >>> the_pcf.fraction
    [-1; 3, <period:> 2, 3, 18, 1, 20, 1, 2, 3, 5, 8, 1, 12]
    >>> the_pcf.fraction.__repr__()
    '[-1; 3, <period:> 2, 3, 18, 1, 20, 1, 2, 3, 5, 8, 1, 12]'
    >>> the_pcf.fraction.tex_repr()
    '[\\, -1; 3, \\overline{2, 3, 18, 1, 20, 1, 2, 3, 5, 8, 1, 12} \\,]'

    Unicode representation uses unicode combinig characters and should
    look pretty in Word or Google Docs or something:
    >>> the_pcf.fraction.unicode_repr()
    '[-1; 3, 2̅,̅ ̅3̅,̅ ̅1̅8̅,̅ ̅1̅,̅ ̅2̅0̅,̅ ̅1̅,̅ ̅2̅,̅ ̅3̅,̅ ̅5̅,̅ ̅8̅,̅ ̅1̅,̅ ̅1̅2̅]'

    Error and corner cases:
    >>> PeriodicContinuedFraction(-19, 0, 17)
    Traceback (most recent call last):
        ...
    ValueError: nonzero denominator required
    >>> PeriodicContinuedFraction(-19, 21, 0)
    FiniteContinuedFraction(-19, 21)
    >>> PeriodicContinuedFraction(-19, 21, 4)
    FiniteContinuedFraction(-17, 21)
    >>> PeriodicContinuedFraction(-19, 21, -5)
    Traceback (most recent call last):
        ...
    ValueError: non-negative sqrtbase required

    Reverse problem: having the preperiod and period, compute the value
    of periodic fraction:
    >>> the_pcf = PeriodicContinuedFraction.from_cfraction([1, 5], [2, 5])
    >>> the_pcf.tex_repr()
    '\\frac{0 + \\sqrt{35}}{5}'
    >>> the_pcf.fraction
    [1; <period:> 5, 2]
    """

    def __new__(cls, numerator=0, denominator=1, sqrtbase=0):
        if not all(
            isinstance(x, int)
            for x in (numerator, denominator, sqrtbase)
        ):
            raise TypeError("int arguments required")
        if denominator == 0:
            raise ValueError("nonzero denominator required")
        if sqrtbase < 0:
            raise ValueError("non-negative sqrtbase required")

        sqroot = int_sqrt(sqrtbase)
        if isinstance(sqroot, int):
            return FiniteContinuedFraction(numerator + sqroot, denominator)

        return super().__new__(cls)

    def __init__(self, numerator=0, denominator=1, sqrtbase=0):
        """"""
        # Convert value to satisfy the following assertion
        p = abs(denominator // gcd(numerator**2 - sqrtbase, denominator))
        numerator *= p; denominator *= p; sqrtbase *= p**2
        q = abs(gcd(
            (numerator**2 - sqrtbase) // denominator,
            numerator, denominator ))
        numerator //= q; denominator //= q; sqrtbase //= q**2
        assert (numerator**2 - sqrtbase) % denominator == 0

        self.numerator = numerator
        self.denominator = denominator
        self.sqrtbase = sqrtbase
        self.origin = (P, Q) = (numerator, denominator)
        self.nextmap = nextmap = {}
        sqroot_floor, sqroot_ceil = int_sqrt(sqrtbase)
        while True:
            if (P, Q) in nextmap:
                self.periodstart = (P, Q)
                break
            if Q > 0:
                quotient = (sqroot_floor + P) // Q
            else:
                quotient = (-sqroot_ceil - P) // -Q
            next_P = Q * quotient - P
            next_Q = (sqrtbase - next_P**2) // Q
            nextmap[P, Q] = quotient, (next_P, next_Q)
            P, Q = next_P, next_Q

    def iter_preperiod(self):
        value = self.origin
        periodstart = self.periodstart
        nextmap = self.nextmap
        while value != periodstart:
            quotient, value = nextmap[value]
            yield quotient

    def iter_period(self):
        value = periodstart = self.periodstart
        nextmap = self.nextmap
        while True:
            quotient, value = nextmap[value]
            yield quotient
            if value == periodstart:
                return

    def iter_quotients(self):
        value = self.origin
        nextmap = self.nextmap
        while True:
            quotient, value = nextmap[value]
            yield quotient

    def __repr__(self):
        return (
            '{self.__class__.__name__}'
            '({self.numerator}, {self.denominator}, {self.sqrtbase})'
            .format(self=self) )

    def tex_repr(self):
        return (
            r'\frac{{{self.numerator} + \sqrt{{{self.sqrtbase}}}}}'
            r'{{{self.denominator}}}'
            .format(self=self) )

    def __float__(self):
        """
        Return approximate value as a float.

        This operation does not make sense here really, and is shipped just
        for the sake of completeness.

        >>> float(PeriodicContinuedFraction(10, 11, 13))
        1.2368682977694536
        """
        return (self.numerator + math.sqrt(self.sqrtbase)) / self.denominator

    class _Fraction:

        def __init__(self, pcf):
            self.period = list(pcf.iter_period())
            self.preperiod = list(pcf.iter_preperiod())

        def __repr__(self, unicode=False, tex=False):
            preperiod = []
            delimiter = ';'
            for i in self.preperiod:
                preperiod.append(str(i))
                preperiod.append(delimiter)
                delimiter = ','
                preperiod.append(' ')
            preperiod = ''.join(preperiod)

            period = []
            for i in self.period:
                period.append(str(i))
                period.append(delimiter)
                delimiter = ','
                period.append(' ')
            else:
                del period[-2:]
            period = ''.join(period)

            if unicode:
                # This will produce a mess in the terminal
                period = unicode_overline(period)
                template = '[{preperiod}{period}]'
            elif tex:
                template = '[\, {preperiod}\overline{{{period}}} \,]'
            else:
                template = '[{preperiod}<period:> {period}]'
            return template.format(preperiod=preperiod, period=period)

        def unicode_repr(self):
            return self.__repr__(unicode=True)

        def tex_repr(self):
            return self.__repr__(tex=True)

    @property
    def fraction(self):
        return self._Fraction(self)

    @classmethod
    def from_cfraction(cls, preperiod, period):
        return cls(*cls.resolve_quotients(preperiod, period))

    @staticmethod
    def resolve_quotients(preperiod, period):
        """
        >>> PeriodicContinuedFraction.resolve_quotients([1, 5], [2, 5])
        (0, 5, 35)
        """
        (p0, q0), (p1, q1) = FiniteContinuedFraction.resolve_quotients(
            period, return_two_last=True )
        a = q1; b = q0 - p1; c = -p0
        g = abs(gcd(b, 2 * a, 2 * c))
        sqrtbase = (b**2 - 4 * a * c) // g**2
        numerator = -b // g
        denominator = 2 * a // g

        for a in reversed(preperiod):
            assert (numerator**2 - sqrtbase) % denominator == 0
            denominator = (sqrtbase - numerator**2) // denominator
            numerator = a * denominator - numerator

        return (numerator, denominator, sqrtbase)

class FiniteContinuedFraction:
    r"""
    Finite continued fraction

    >>> the_fcf = FiniteContinuedFraction(123456, 100500)

    Value is reduced (numerator and denominator have no common
    divisor):
    >>> the_fcf
    FiniteContinuedFraction(10288, 8375)
    >>> the_fcf.tex_repr()
    '\\frac{10288}{8375}'


    Computation of continued fraction:
    >>> the_fcf.fraction
    [1; 4, 2, 1, 1, 1, 4, 1, 2, 4, 1, 2]
    >>> the_fcf.fraction.tex_repr()
    '[\\, 1; 4, 2, 1, 1, 1, 4, 1, 2, 4, 1, 2 \\,]'

    In this case, unicode representation is the same as normal __repr__()
    >>> the_fcf.fraction.unicode_repr()
    '[1; 4, 2, 1, 1, 1, 4, 1, 2, 4, 1, 2]'

    Error and corner cases:
    >>> FiniteContinuedFraction(123456, 0)
    Traceback (most recent call last):
        ...
    ValueError: nonzero denominator required, received 0
    >>> FiniteContinuedFraction(123456, 123456)
    FiniteContinuedFraction(1, 1)
    >>> FiniteContinuedFraction(0, 1).fraction
    [0]

    Reverse problem: having the sequence of quotients, compute the value:
    >>> the_fcf = FiniteContinuedFraction.from_cfraction([1, 5, 2, 3])
    >>> the_fcf.tex_repr()
    '\\frac{45}{38}'
    >>> the_fcf.fraction
    [1; 5, 2, 3]
    """

    def __new__(cls, numerator=0, denominator=1):
        if not all(isinstance(x, int) for x in (numerator, denominator)):
            raise TypeError("int arguments required")
        if denominator == 0:
            raise ValueError(
                "nonzero denominator required, received {}".format(denominator)
            )

        return super().__new__(cls)

    def __init__(self, numerator=0, denominator=1):
        q = abs(gcd(numerator, denominator))
        if denominator < 0:
            q = -q
        numerator //= q; denominator //= q

        self.numerator = numerator
        self.denominator = denominator
        self.quotients = quotients = []
        while denominator > 0:
            quotient = numerator // denominator
            quotients.append(quotient)
            numerator, denominator = (
                denominator, numerator - denominator * quotient )

    def iter_quotients(self):
        return iter(self.quotients)

    def __repr__(self):
        return (
            '{self.__class__.__name__}({self.numerator}, {self.denominator})'
            .format(self=self) )

    def tex_repr(self):
        return (
            r'\frac{{{self.numerator}}}{{{self.denominator}}}'
            .format(self=self) )

    def __float__(self):
        return self.numerator / self.denominator

    def to_fraction(self):
        return fractions.Fraction(self.numerator, self.denominator)

    class _Fraction:
        def __init__(self, fcf):
            self.quotients = list(fcf.quotients)

        def __repr__(self, tex=False):
            quotients = []
            delimiter = ';'
            for i in self.quotients:
                quotients.append(str(i))
                quotients.append(delimiter)
                delimiter = ','
                quotients.append(' ')
            else:
                del quotients[-2:]
            quotients = ''.join(quotients)

            if tex:
                template = '[\, {quotients} \,]'
            else:
                template = '[{quotients}]'
            return template.format(quotients=quotients)

        unicode_repr = __repr__

        def tex_repr(self):
            return self.__repr__(tex=True)

    @property
    def fraction(self):
        return self._Fraction(self)

    @classmethod
    def from_cfraction(cls, quotients):
        return cls(*cls.resolve_quotients(quotients))

    @staticmethod
    def resolve_quotients(quotients, return_two_last=False):
        """
        >>> FiniteContinuedFraction.resolve_quotients([2, 5])
        (11, 5)
        >>> FiniteContinuedFraction.resolve_quotients([2, 5],
        ...     return_two_last=True )
        ((2, 1), (11, 5))
        """
        p0 = 0; q0 = 1
        p1 = 1; q1 = 0;
        for a in quotients:
            if not isinstance(a, int):
                raise TypeError(a)
            (p1, q1), (p0, q0) = (p1 * a + p0, q1 * a + q0), (p1, q1)
        if not return_two_last:
            return (p1, q1)
        else:
            return (p0, q0), (p1, q1)

def int_sqrt(A):
    """
    Square root implemented in purely integer operations.

    Return exact square root, if it is integer.
    Otherwise, return a (root_floor, root_ceil) pair.

    >>> int_sqrt(9)
    3
    >>> int_sqrt(10)
    (3, 4)
    >>> from math import sqrt
    >>> sqrt(12345678987654321**2)
    1.234567898765432e+16
    >>> int_sqrt(12345678987654321**2)
    12345678987654321
    >>> int_sqrt(12345678987654321**2 + 2)
    (12345678987654321, 12345678987654322)
    >>> int_sqrt(-1)
    Traceback (most recent call last):
        ...
    ValueError: math domain error
    >>> int_sqrt(0)
    0
    >>> int_sqrt(1)
    1

    """
    if A < 0:
        raise ValueError('math domain error')
    if A == 0 or A == 1:
        return A

    floor, ceil = A-1, A
    while not floor**2 < A < ceil**2:
        ceil = (floor + A // -floor // -1) // -2 // -1
        floor = ceil - 1
        if A == ceil**2:
            return ceil
    return floor, ceil

def gcd(*args, _gcd=fractions.gcd):
    """
    Return greatest common divisor of all arguments.

    Based on fractions.gcd().

    >>> gcd(6, 10, 15)
    1
    >>> gcd(6, 8, 20)
    2
    >>> gcd(15)
    15
    """
    return reduce(_gcd, args)

def unicode_overline(s):
    return ''.join(y for x in s for y in (x, '\N{COMBINING OVERLINE}'))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

