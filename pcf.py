"""
Periodic Continued Fractions

To obtain continued fraction representation for the value
((sqrt(17) - 19)/21) we write

>>> PCF(17, -19, 21)
[-1; 3, <period start> 2, 3, 18, 1, 20, 1, 2, 3, 5, 8, 1, 12]

for the value (1/5-sqrt(13)) we write

>>> PCF(13 * 5**2, -1, -5)
[-4; 1, 1, <period start> 2, 6, 1, 4, 7, 180, 7, 4, 1, 6, 2]

>>> PCF(13 * 5**2, -1, -5).repr_combining()
'[-4; 1, 1, 2̅,̅ ̅6̅,̅ ̅1̅,̅ ̅4̅,̅ ̅7̅,̅ ̅1̅8̅0̅,̅ ̅7̅,̅ ̅4̅,̅ ̅1̅,̅ ̅6̅,̅ ̅2̅]'

The latter string uses unicode combining characters, and should look
pretty enough after inserting in some Word-like editor.

for the value 123456/100500 we write

>>> FCF(123456, 100500)
[1; 4, 2, 1, 1, 1, 4, 1, 2, 4, 1, 2]

resolve_pcf and resolve_fcf should be self-descriptive:

>>> resolve_pcf([1, 5], [2, 3])
(15, -24, -17)
>>> PCF(15, -24, -17)
[1; 5, <period start> 2, 3]

>>> resolve_fcf([1, 5, 2, 3])
(45, 38)
>>> FCF(45, 38)
[1; 5, 2, 3]

"""

from fractions import gcd

__all__ = ['PCF', 'FCF', 'resolve_pcf', 'resolve_fcf']

def int_sqrt(A):
    x, y = A-1, A
    while not x**2 < A < y**2:
        y = (x + A // -x // -1) // -2 // -1
        x = y - 1
        if A == y**2:
            return y
    return x, y

class PCF:
    """
    Periodic continued fraction.
    """
    def __new__(cls, A, B=0, C=1):
        # \frac{\sqrt{A} + B}{C}
        if not all(isinstance(x, int) for x in (A, B, C)):
            raise TypeError("int arguments required")
        if C == 0:
            raise ValueError("nonzero C required")
        if A <= 1:
            raise ValueError("A > 1 required")

        if isinstance(int_sqrt(A), int):
            return FCF(int_sqrt(A) + B, C)
        # the alternative is a tuple of two ints, which means
        # non-integral \sqrt{A}

        return super().__new__(cls)

    def __init__(self, A, B=0, C=1):
        if (A - B**2) % C:
            q = abs(C)
            A *= q**2; B *= q; C *= q
        assert (A - B**2) % C == 0, (A, B, C)

        self.origin = (A, B, C)
        self.nextmap = nextmap = {}
        sqrtA_down, sqrtA_up = int_sqrt(A)
        while True:
            if (A, B, C) in nextmap:
                self.periodstart = (A, B, C)
                break
            if C > 0:
                quotient = (sqrtA_down + B) // C
            else:
                quotient = (- sqrtA_up - B) // -C
            B1 = C * quotient - B
            C1 = (A - B1**2) // C
            nextmap[A, B, C] = quotient, (A, B1, C1)
            B = B1
            C = C1

    @property
    def preperiod(self):
        return list(self.iter_preperiod())

    @property
    def period(self):
        return list(self.iter_period())

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

    def __iter__(self):
        value = self.origin
        nextmap = self.nextmap
        while True:
            quotient, value = nextmap[value]
            yield quotient

    def __repr__(self, combining=False):
        preperiod = []
        delimiter = ';'
        for i in self.iter_preperiod():
            preperiod.append(str(i))
            preperiod.append(delimiter)
            delimiter = ','
            preperiod.append(' ')
        preperiod = ''.join(preperiod)

        period = []
        for i in self.iter_period():
            period.append(str(i))
            period.append(delimiter)
            delimiter = ','
            period.append(' ')
        else:
            del period[-2:]
        if combining:
        # This produce a mess in the terminal
            period = list(''.join(period))
            for i in range(len(period)):
                period[2*i+1:2*i+1] = '\N{COMBINING OVERLINE}'
        period = ''.join(period)
        return ('['
            + preperiod
            + ('<period start> ' if not combining else '')
            + period + ']')

    def repr_combining(self):
        return self.__repr__(combining=True)

class FCF:
    """
    Finite continued fraction.
    """
    def __new__(cls, A, B):
        # \frac{A}{B}
        if not all(isinstance(x, int) for x in (A, B)):
            raise TypeError("int arguments required")
        if B == 0:
            raise ValueError("nonzero B required")

        return super().__new__(cls)

    def __init__(self, A, B):
        if B < 0:
            A = -A
            B = -B

        self.quotients = quotients = []
        while B > 0:
            quotient = A // B
            quotients.append(quotient)
            A, B = B, A - B * quotient

    def __iter__(self):
        return iter(self.quotients)

    def __repr__(self):
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

        return '[' + quotients + ']'

def resolve_fcf(quotients, return_two_last=False):
    # TODO: function argument checks
    p0 = 0; q0 = 1
    p1 = 1; q1 = 0;
    for a in quotients:
        (p1, q1), (p0, q0) = (p1 * a + p0, q1 * a + q0), (p1, q1)
    if not return_two_last:
        return (p1, q1)
    else:
        return (p0, q0), (p1, q1)

def resolve_pcf(preperiod, period, return_latex=False):
    # TODO: function argument checks
    preperiod = list(preperiod)
    period = list(period)

    (p0, q0), (p1, q1) = resolve_fcf(period, return_two_last=True)
    a = q1; b = q0 - p1; c = -p0
    g = abs(gcd(b, 2 * gcd(a, c)))
    A = (b**2 - 4 * a * c) // g**2
    B = -b // g
    C = 2 * a // g

    for a in reversed(preperiod):
        assert (A - B**2) % C == 0
        C = (A - B**2) // C
        B = a * C - B

    if not return_latex:
        return (A, B, C)
    else:
        return r"\frac{{\sqrt{{{A}}}{B:+}}}{{{C}}}".format(A=A, B=B, C=C)

