"""
Free numbers provide a convenient way to form and solve linear systems.

>>> n1 = FreeFloat()
>>> n2 = FreeFloat()
>>> solve(n1 + n2)
>>> solve(n1 - 2 * n2, 12)

>>> n1.value
4.0
>>> n2.value
-4.0

>>> n3 = FreeComplex()
>>> solve(n3 * (1-2j), -3-4j)
>>> n3.refine().value
(1-2j)

"""

from collections import OrderedDict
from functools import total_ordering
from numbers import Real, Complex

__all__ = ['FreeComplex', 'FreeFloat', 'solve']

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class UndefinedError(ValueError):
    pass
class OverdefinedError(ValueError):
    pass

class FreeComplex:
    """
    Base class for free numbers.

    Never instantiated. Calling constructor returns sum of two
    FreeFloat's.
    """
    __slots__ = []

    def __new__(cls):
        if cls is FreeComplex:
            return FreeFloat() + FreeFloat() * 1j
        return super().__new__(cls)

    def __bool__(self):
        return not self.defined or self.value != 0

    def __add__(self, other):
        return SumComplex(nums=(self, other), weights=(1, 1))

    __radd__ = __add__

    def __sub__(self, other):
        return SumComplex(nums=(self, other), weights=(1, -1))

    def __rsub__(self, other):
        return SumComplex(nums=(self, other), weights=(-1, 1))

    def __mul__(self, other):
        if isinstance(other, FreeComplex):
            if not other.defined:
                return other * self.value
            other = other.value
        elif isinstance(other, Real):
            other = float(other)
        elif isinstance(other, Complex):
            other = complex(other)
        return SumComplex(nums=(self,), weights=(other,))

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self * (1.0 / other)

    def __rtruediv__(self, other):
        return other / self.value

    def __neg__(self):
        return SumComplex(nums=(self,), weights=(-1,))

    def __pos__(self):
        return self

class FreeFloat(FreeComplex):
    __slots__ = ['_value']

    def __init__(self):
        self._value = None

    @property
    def value(self):
        if self._value is None:
            raise UndefinedError
        return self._value

    @property
    def defined(self):
        return self._value is not None

    def define(self, value):
        if self._value is not None:
            raise OverdefinedError
        if not isinstance(value, Real):
            raise TypeError(value)
        logger.info('defined something')
        self._value = float(value)

    @property
    def real(self):
        return self

    @property
    def imag(self):
        return 0.0

class SumComplex(FreeComplex):
    __slots__ = ['nums', 'weights', 'absolute']

    def __new__(cls, *, nums=(), weights=(), absolute=0.0):
        self = super().__new__(cls)
        self.nums = []
        self.weights = []
        self.absolute = 0.0
        return self

    def __init__(self, *, nums=(), weights=(), absolute=0.0):
        if (nums, weights, absolute) == ((), (), 0.0):
            return
        self.nums.extend(nums)
        self.weights.extend(weights)
        self.absolute += absolute
        self.refine()

    @classmethod
    def normalize_nums_weights(cls, nums, weights, absolute):
        the_nums = {}
        the_weights = {}
        for num, weight in cls.flatten_nums_weights(nums, weights):
            if isinstance(num, (float, complex)):
                absolute += num * weight
                continue;
            assert not isinstance(num, SumComplex)
            assert isinstance(num, FreeFloat)
            num_id = id(num)
            if num_id not in the_nums:
                the_nums[num_id] = num
                the_weights[num_id] = weight
            else:
                the_weights[num_id] += weight

        nums = []; weights = [];
        for num_id in the_nums:
            num = the_nums[num_id]
            weight = the_weights[num_id]
            if not weight:
                continue;
            nums.append(num)
            weights.append(weight)
        return nums, weights, absolute

    @classmethod
    def flatten_nums_weights(cls, nums, weights):
        nums = list(nums); weights = list(weights)
        if len(nums) != len(weights):
            raise ValueError

        for num, weight in zip(nums, weights):
            if isinstance(weight, Real):
                weight = float(weight)
            elif isinstance(weight, Complex):
                weight = complex(weight)
            else:
                raise TypeError(weight)
            if weight == 0:
                continue
            if isinstance(num, Real):
                yield float(num), weight
                continue;
            elif isinstance(num, Complex):
                yield complex(num), weight
                continue;

            if not isinstance(num, FreeComplex):
                raise TypeError(num)
            if num.defined:
                yield num.value, weight
                continue;

            if isinstance(num, SumComplex):
                for subnum, subweight in num:
                    yield subnum, subweight * weight
                continue;

            yield num, weight

    def __iter__(self):
        yield from self.flatten_nums_weights(self.nums, self.weights)
        yield self.absolute, 1.0

    def refine(self):
        self.nums, self.weights, self.absolute = self.normalize_nums_weights(
            self.nums, self.weights, self.absolute)
        return self

    @property
    def defined(self):
        return not self.nums

    def define(self, value):
        raise TypeError("Can't define {!r} directly".format(self))

    @property
    def value(self):
        if self.nums:
            raise UndefinedError
        return self.absolute

    @property
    def real(self):
        return type(self)(
            nums=self.nums,
            weights=(weight.real for weight in self.weights),
            absolute=self.absolute.real)

    @property
    def imag(self):
        return type(self)(
            nums=self.nums,
            weights=(weight.imag for weight in self.weights),
            absolute=self.absolute.imag)

    def get_weight(self, num):
        nums = self.nums
        try:
            index = nums.index(num)
        except ValueError:
            return 0.0
        return self.weights[index]

    def __repr__(self):
        return (
            '{self.__class__.__name__}(\n'
                '\tnums={self.nums!r},\n'
                '\tweights={self.weights!r},\n'
                '\tabsolute={self.absolute} )'
            .format(self=self) )

class Equation:
    __slots__ = ['zero']

    zeros = []

    _defined_counter = 0

    def __init__(self, lhs, rhs=0):
        self.zero = zero = lhs - rhs
        if not isinstance(zero, SumComplex):
            raise TypeError(lhs, rhs)

    def __bool__(self):
        """
        Return True if self.zero is, well, zero.
        """
        return self.zero.defined and self.zero.value == 0.0

    def solve(self):
        self.add_zero(self.zero)

    @classmethod
    def add_zero(cls, zero):
        zero, imag = zero.real, zero.imag
        if cls.trivial_add(zero):
            return
        zero = cls.substitute(zero)
        if cls.trivial_add(zero):
            return
        zero /= zero.weights[0]
        cls.zeros.append(zero)
        cls.back_substitute()
        if imag:
            cls.add_zero(imag)

    @classmethod
    def trivial_add(cls, zero):
        if zero.defined:
            if zero.value:
                raise OverdefinedError("Inconsistent equation")
            else:
                raise OverdefinedError("Redundant equation")
        if len(zero.nums) == 1:
            num, = zero.nums
            weight, = zero.weights
            num.define(- zero.absolute / weight)
            zero.refine()
            cls.refine()
            return True
        return False

    @classmethod
    def substitute(cls, zero):
        zero.refine()
        for z in cls.zeros:
            num, *nums = z.nums
            weight = zero.get_weight(num)
            if not weight:
                continue
            zero -= weight * z
        return zero

    @classmethod
    def back_substitute(cls):
        zeros = []
        trivial_zeros = []
        zero = cls.zeros[-1]
        num, *nums = zero.nums

        needs_refine = False
        for z in cls.zeros[:-1]:
            weight = z.get_weight(num)
            if weight:
                z = z - weight * zero
            if len(z.nums) > 1:
                zeros.append(z)
            else:
                trivial_zeros.append(z)
        zeros.append(zero)
        cls.zeros = zeros
        for z in trivial_zeros:
            if not cls.trivial_add(z):
                raise AssertionError

    @classmethod
    def refine(cls):
        zeros = cls.zeros
        if not zeros:
            return
        zeros = [zero.refine() for zero in zeros]
        cls.zeros = []
        for zero in zeros:
            cls.add_zero(zero)

def solve(lhs, rhs=0):
    Equation(lhs, rhs).solve()

if __name__ == '__main__':
    import doctest
    doctest.testmod()

