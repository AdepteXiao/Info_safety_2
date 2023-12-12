import random


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Обратное по модулю не существует')
    else:
        return x % m


def nod(a, b):
    while b:
        a, b = b, a % b
    return a


def miller_rabin(n, test_count):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(test_count):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def ferma(num, test_count):
    if num == 1 or num == 4:
        return False
    elif num == 2 or num == 3:
        return True
    else:
        for i in range(test_count):
            a = random.randint(2, num - 2)

            if pow(a, num - 1, num) != 1:
                return False
    return True
