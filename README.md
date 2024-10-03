# RSA implementation

This is an implementation of the RSA algorithm written in Python. It was created
as a learning exercise to better understand how the algorithm works. It can
generate key pairs, encrypt and decrypt messages.

## Installation

1. Ensure [Python](https://www.python.org) is installed
2. Clone the repository
```
git clone https://github.com/mattiarmston/RSA_implementation.git
```
3. Navigate to the installation directory
```
cd RSA_implementation
```
4. Run the program
```
python rsa_clone.py
```

## Design

This program was written mainly as a teaching tool and as such many of the
algorithms were chosen for their simplicity rather than their performance.

### Flaws

The program is very inefficient due to the naive methods used for primality
tests and exponentiation as well as, to a lesser extent, the choice of language.
This means that it struggles to generate large key pairs and then encrypt and
decrypt messages with such large keys. When testing, 3 digit primes should be
used to ensure performance and this program should not be used for actual
security.

### Improvements

The RSA paper mentions several more efficient algorithms that would be obvious
improvements including:
1. Using the "probabilistic" algorithm for testing primality
2. Computing "exponentiation by repeated squaring and multiplication"
