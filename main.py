import math
import random


def is_prime_basic(n: int) -> bool:
    if n in [1, 2, 3]:
        return True

    if n % 2 == 0:
        return False
    if n % 3 == 0:
        return False

    k = 1
    p1 = 6*k - 1
    while p1 <= math.sqrt(n):
        p1 = 6 * k - 1
        if n % p1 == 0:
            return False

        p2 = 6 * k + 1
        if n % p2 == 0:
            return False

        k += 1

    return True


def is_prime_primat(n: int) -> bool:
    if n == 0:
        return False

    if n in [1, 2, 3]:
        return True

    K = 3
    for i in range(K):
        a = random.randint(2, n-2)
        if pow(a, n-1, n) != 1:
            return False
    return True


def test_is_prime_primat():
    basic = [is_prime_basic(i) for i in range(100)]
    primat = [is_prime_basic(i) for i in range(100)]
    assert basic == primat


def next_prime(n: int) -> int:
    if is_prime_primat(n):
        return n

    if n % 2 == 0:
        return next_prime(n + 1)

    return next_prime(n + 2)


def test_next_prime():
    assert next_prime(6) == 7


def generate_two_random_primes() -> (int, int):
    magnitude = random.randint(4, 7)
    margin = random.randint(2, 4)
    low = next_prime(random.randint(10 ** magnitude, 10 ** (magnitude + margin)))
    high = next_prime(random.randint(10 ** (magnitude + margin), 10 ** (magnitude + 2 * margin)))
    p = random.choice([low, high])
    q = low if low != p else high

    return p, q


def euclidian_gcd(low: int, high: int) -> int:
    remainder = high % low
    if remainder == 0:
        return low
    return euclidian_gcd(low=high % low, high=low)


def charmichael_of_product_of_primes(p: int, q: int) -> int:
    lambda_p = p - 1
    lambda_q = q - 1
    low, high = sorted([lambda_p, lambda_q])
    gcd = euclidian_gcd(low=low, high=high)
    return lambda_p * lambda_q // gcd


def test_charmichael():
    seq = [	1, 1, 2, 2, 4, 2, 6, 2, 6, 4, 10, 2, 12, 6, 4, 4, 16, 6, 18, 4, 6, 10, 22, 2, 20, 12, 18, 6, 28, 4, 30, 8, 10, 16, 12, 6, 36, 18, 12, 4, 40, 6, 42, 10, 12, 22, 46, 4, 42, 20, 16, 12, 52, 18, 20, 6, 18, 28, 58, 4, 60, 30, 6, 16, 12, 10, 66, 16, 22, 12, 70, 6, 72, 36, 20, 18, 30, 12, 78, 4, 54]
    P = 19
    Q = 3
    N = P * Q
    if N > 81:
        raise ValueError("the truth values stop a 81")
    print(charmichael_of_product_of_primes(P, Q))
    assert seq[N-1] == charmichael_of_product_of_primes(P, Q)


def extendended_euclidian_algo(low: int, high: int, old_s: int = 1, old_t: int = 0, s: int = 0, t: int = 1)\
        -> (int, int, int):
    remainder = high % low
    if remainder == 0:
        return low, t, s

    quotient = high // low
    old_s, s = s, old_s - quotient*s
    old_t, t = t, old_t - quotient*t
    return extendended_euclidian_algo(low=remainder, high=low, old_s=old_s, old_t=old_t, s=s, t=t)


def test_extended_euclidian_algo():
    LOW = 46
    HIGH = 240
    gcd, x, y = extendended_euclidian_algo(LOW, HIGH)
    print("gcd: {} \n{}*{} + {}*{} = {}".format(gcd, x, LOW, y, HIGH, gcd))
    assert LOW * x + HIGH * y == gcd


def compute_private_exponent(e: int, lambda_n: int) -> int:
    if e >= lambda_n:
        raise ValueError("e should be less than lambda_n")

    gcd, x, y = extendended_euclidian_algo(e, lambda_n)
    return x


def test_compute_private_exponent():
    e = 65537
    p, q = generate_two_random_primes()
    lambda_n = charmichael_of_product_of_primes(p, q)
    pk_exp = compute_private_exponent(e, lambda_n)

    assert pk_exp*e % lambda_n == 1


def rsa_gen(e: int = 65137) -> ((int, int), int):
    p, q = generate_two_random_primes()
    n = p * q
    lambda_n = charmichael_of_product_of_primes(p, q)
    d = compute_private_exponent(e, lambda_n)
    public_key = (n, e)
    private_key = d

    return public_key, private_key


def rsa_encryption(message: int, public_key: (int, int)) -> int:
    m = message
    n, e = public_key
    return pow(m, e, n)


def rsa_decryption(encoded_message: int, public_key: (int, int), private_key: int) -> int:
    c = encoded_message
    n, _ = public_key
    d = private_key

    return pow(c, d, n)


def test_rsa():
    message = 12345
    e = 65537
    public_key, private_key = rsa_gen(e)
    encoded_message = rsa_encryption(message, public_key)
    decoded_message = rsa_decryption(encoded_message, public_key, private_key)
    assert message == decoded_message


if __name__ == '__main__':
    test_rsa()


