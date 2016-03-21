#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time

def n_ary(f):
    '''
    Takes a binary function and makes it multi-nary
    '''
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))

    return n_ary_f


def field_multiply(squared_field):
    '''
    Returns a function that multiplies numbers in a given field. It is
    structured this way because the numerical value of the field must be
    determined externally, yet the function which does the evaluaton benefits
    significantly from an n_ary decorator. Can't have both ways

    Example: a squared_field parameter of 5 would yield a function in the field
    Z(sqrt5)
    '''

    @n_ary
    def fm_f(expr1, expr2):
        '''
        The following discussion assumes the specific case of the field
        Z(sqrt5). This is for explanatory purposes only. Other square roots,
        as well as imaginary numbers, can be chosen. Any number in fact, that
        squares to an integer.

        We are evaluating (w + x sqrt5) * (y + z sqrt5) in such a way as to
        never actually evaluate sqrt5, which would introduce rounding errors
        and possibly a wrong answer. This approach stems from the mathematical
        concept of fields. The field in question is Z(sqrt5), i.e., the field
        composed of all integers and integer multiples of sqrt5.

        Returns a tuple (a, b) that represents the number a + b sqrt5.

        Why do this style of multiplication rather than the seemingly simpler
        way of return (w*y + 5*x*z), (w*z + x*y)? The way I wrote it below
        requires fewer multiplications. Because multiplications are more
        difficult than additions, reducing the number of multiplications is
        advantageous. If fact, the preferred method is twice as fast as the
        simple method. (I'm surprised by this. I would have it to be at most
        25% faster because we reduce from four multiplications to three. But
        empirical evidence suggests a 50% improvement.) In any case: 'Win!'

        There is no advantage in memoizing this function based upon
        considerable empirical evidence
        '''
        (w, x), (y, z) = expr1, expr2
        u = w*y
        v = x*z
        return (u + squared_field*v, (w + x)*(y + z) - u - v)

    return fm_f


def power_recursion(expr, n, f):
    '''
    Herein we coordinate the powerful recursive action of a function f on a
    quantity expr raised to the nth power. It proceeds as O(lg n)
    '''
    if n > 1:
        recurse = power_recursion(expr, n/2, f)
        args = [recurse, recurse] # build list of args for f
        if n%2: #if there is a remaining exponent after the power is halved
            args.append(expr)
        return f(*args)
    else:
        return expr


def fibonacci(n):
    '''
    Takes an argument n, as in the nth fibonacci number

    The equation:
    F(n) = [(1 + sqrt5)^n - (1 - sqrt5)^n] / [2^n sqrt5]
    This is the equation obtained by the linear algebra approach to the
    Fibonacci sequence.

    The two eigenvalues are (1 + sqrt5) / 2 and (1 - sqrt5) / 2. When we
    exponentiate these terms and subtract one from the other as shown above,
    the natural number terms cancel out and only the sqrt5 term remains. The
    coefficient of the sqrt5 term is quantitatively the same for both
    eigenvalues, differing only by a factor of -1. Thus we need to get this
    coefficient for only one of the exponentiated eigenvalues, and then double
    it. That is the nth fibonacci number, which is returned.

    Return involves a call to the power_recursion function. The tuple (1,1)
    represents the number 1 + 1 * sqrt5. The function field_multiply(5)
    coordinates the multiplication of numbers in the field Z(sqrt5). Note that
    this return makes use of bitshifting (>>). This is an extremely quick way
    to divide by 2 over and over again.
    '''
    if n == 0: return 0
    return power_recursion((1, 1), n, field_multiply(5))[1] >> n-1


def main():
    print 'Which Fibonacci number seeketh thou? Enter 1 for 1st, 4 for 4th, 100 for 100th...'
    n = int(eval(raw_input("> ")))
    start = time.time()
    fibo_num = fibonacci(n)
    print ('Got it. It took %f seconds to calculate the %dth Fibonacci number. Well done.'
            % (time.time() - start, n))
    print 'Do you want a printout of the %dth Fibonaci number?' % n
    ans = raw_input("> ")
    if ans in ('y', 'Y', 'yes', 'Yes'): print fibo_num


main()
