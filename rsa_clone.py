#!/usr/bin/env python
# The purpose of this is to write my own implementation of the RSA cryptography
# algorithm in the hopes that I can understand it better.

import random

def get_num(msg: str, min=None, max=None) -> int:
    num = None
    while num == None:
        print(msg)
        num = input()
        try:
            num = int(num)
        except ValueError:
            num = None
            continue
        if min != None and num < min:
            num = None
            continue
        if max != None and num > max:
            num = None
            continue
    return num

def find_prime(digits):
    prime = False
    while not prime:
        p = random.randint(10 ** (digits - 1), 10 ** digits - 1)
        # This is a naive way of testing whether a number is prime. This could
        # be optimised by only using a list of primes to pick the numbers to
        # check division for, but this would increase memory usage.
        # Alternatively, I could use a more efficient algorithm like the
        # 'probabilistic' method presented in the paper.
        if p == 1:
            continue
        if p % 2 == 0:
            continue
        i = 3
        prime = True
        while i*i <= p:
            if p % i == 0:
                prime = False
                break
            i += 2
    return p

def extended_euclids(x, y, z=1):
    # This solves the equation hx + ky = z, where h and k are integers, only if
    # hcf(x, y) divides z.
    # If z = 1, the equation is hx + ky = 1 which can be rearranged to give
    # hx = 1 - ky = 1 (mod y)
    terms = []
    # The above utilises terms being a reference to a mutable list. Any time
    # the list is changed, the old reference points to the updated list
    hcf = euclids(x, y, terms)
    if z % hcf != 0:
        raise Exception(
"""Argument error for Bezout's theorum:
  {} and {} have hcf {} which does not divide {}""".format(x, y, hcf, z))
    # For one iteration of the reverse of Euclid's algorithm:
    # c = b * t2 - a * t1
    # c = b * t2 - a * (t3 - a1 * t2)
    # c = (b + a * a1) * t2 - a * t3
    # c = -a * t3 + (b + a * a1) * t2
    # The new variables are:
    # b = -a
    # a = -(b + a * a1)
    # t1 = t2
    # t2 = t3
    # Another iteration can now be performed as above
    terms.pop()
    t1 = terms.pop()
    t2 = terms.pop()
    a = replace_terms(z, t1, t2)
    # Initially b is assumed to be 1
    b = 1
    while terms != []:
        t3 = terms.pop()
        a1 = replace_terms(t1, t2, t3)
        b2 = b
        b = -a
        a = -(b2 + a * a1)
        t1 = t2
        t2 = t3
    # The solution then is b * t2 - a * t1 = c
    # In terms of x and y: b * x + a * y = c
    if x == t2:
        b = int(b)
        a = int(-1 * a)
    else:
        b = int(b)
        a = int(-1 * a)
        a, b = b, a
    return b, a

def replace_terms(t1, t2, t3):
    # The goal is to write t1 in terms of t2 and t3
    # I assume that t1 = t3 - a * t2 and solve for a
    # a = (t3 - t1) / t2
    a = (t3 - t1) / t2
    return a

def euclids(a, b, terms=[]):
    if a < b:
        return euclids(b, a, terms)
    # This utilises terms being a reference to a mutable list. Any time the list
    # is changed, the old reference points to the updated list
    if terms == []:
        terms.append(a)
    terms.append(b)
    quotient = a // b
    remainder = a - quotient * b
    if remainder == 0:
        return b
    return euclids(b, remainder, terms)

def gen_keys(digits):
    p = find_prime(digits)
    q = find_prime(digits)
    n = p * q
    # This will be used as a base for modulo arithmetic and as an exponent
    phi_n = (p-1) * (q-1)
    # 2^16 + 1 is the 'standard' value for the encryption exponent in rsa
    # implementations. e and (p-1)(q-1) must be coprime and this will be the
    # case if e is prime, which 2^16 + 1 is. However, I could also use 3 which
    # is the smallest possible value of e. 2 is not the smallest value because
    # (p-1) and (q-1) will both be even and so are not coprime with 2.
    e = 2 ** 16 + 1
    # now I need to find a 'd' such that
    # de = 1 (mod (p-1)(q-1))
    # de = 1 + k(p-1)(q-1)
    # de -k(p-1)(q-1) = 1
    # de -k * phi_n = 1
    # TODO uncaught error here
    d, _ = extended_euclids(e, phi_n)
    if d < 2:
        # l is the smallest number such that
        # d + l * phi_n > 0
        l = 1
        while d + l*phi_n <= 0:
            l += 1
        # This is still valid because if
        # LaTeX:
        # $ m^{de}=m^{1+k(p-1)(q-1)}=m(\text{mod } n) $
        # $ m^{d(e + l(p-1)(q-1))}=m^{1+(k+l)(p-1)(q-1)}=m(\text{mod } n) $
        d += l * phi_n
    return n, e, d

def output_keys(n, e, d):
    with open("public_key.py", "w") as public:
        public.write("n = {}\n".format(n))
        public.write("e = {}\n".format(e))
    with open("private_key.py", "w") as private:
        private.write("n = {}\n".format(n))
        private.write("d = {}\n".format(d))

def new_key():
    digits = get_num("How many digits long do you want the keys to be?", min=1)
    print("generating keys")
    n, e, d = gen_keys(digits)
    print("writing public key to 'public_key.py'")
    print("writing private key to 'private_key.py'")
    output_keys(n, e, d)

def encrypt():
    try:
        from public_key import n, e
    except ImportError:
        print("Error could not find 'public_key.py'")
        return
    # As per the original paper the integer to be encrypted must be between 0 and n - 1
    m = get_num("Enter the number you would like to encrypt", min=0, max=n-1)
    encrypted_m = m ** e % n
    print("The encrypted number is {}".format(encrypted_m))

def decrypt():
    try:
        from private_key import n, d
    except ImportError:
        print("Error could not find 'public_key.py' and 'private_key.py'")
        return
    num = get_num("Enter the number you would like to decrypt")
    decrypted_num = num ** d % n
    print("The decrypted number is {}".format(decrypted_num))

def main():
    functions = [new_key, encrypt, decrypt, quit]
    while True:
        print()
        print("What would you like to do?")
        print("1. Generate a new RSA key pair")
        print("2. Encrypt a number")
        print("3. Decrypt a number")
        print("4. Quit")
        print()
        choice = get_num("Enter a number from 1 to 4", min=1, max=4)
        func = functions[choice - 1]
        func()

main()
