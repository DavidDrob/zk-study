from libnum import has_sqrtmod_prime_power, sqrtmod_prime_power
import matplotlib.pyplot as plt

MODULUS = 11


def main():
    field = range(0, MODULUS)
    temp = {}
    points = []

    # BRUTE-FORCE SOLUTION
    # get temporary calculation (without sqrt) for
    # y^2 = (x^3 + 3) mod 11
    for x in field:
        temp[x] = ((x ** 3) + 3) % MODULUS

    # generate group
    for k, i in temp.items():
        bf_solutions = []

        # brute force solution
        for r in temp.values():
            if r ** 2 % MODULUS == i:
                bf_solutions.append(r)

        # Tonelli-Shanks algorithm
        # compute sqrt() mod 11
        solutions = []
        if has_sqrtmod_prime_power(i, MODULUS, 1):
            solutions = list(sqrtmod_prime_power(i, MODULUS, 1))
            print(f"Solutions for {k}: {solutions}")
        else:
            print(f"No solutions for {k}")

        assert sorted(bf_solutions) == sorted(solutions)

        for s in bf_solutions:
            points.append((k, s))

    # assert closed property
    p3 = simple_addition(points[1], points[2], MODULUS)
    assert p3 in points

    p4 = simple_addition((0, 0), points[2], MODULUS)
    assert p4 not in points

    # assert the group is cyclic
    print("cyclic group")
    generator = (4, 10)
    next_x, next_y = generator
    points_in_group = [generator]

    for i in range(2, 13):
        next_x, next_y = add_points(next_x, next_y, generator[0], generator[1], MODULUS)
        print(i, next_x, next_y)
        points_in_group.append((next_x, next_y))

    points.append((None, None))  # point at infinity

    assert set(points_in_group) == set(points)


def generate_plot(points):
    xs = [i for i, j in points]
    ys = [j for i, j in points]

    fig, (ax1) = plt.subplots(1, 1)
    fig.suptitle('y^2 = x^3 + 3 (mod p)')
    fig.set_size_inches(6, 6)
    ax1.set_xticks(range(0, MODULUS))
    ax1.set_yticks(range(0, MODULUS))
    plt.grid()
    plt.scatter(xs, ys)
    plt.savefig(f"mod-{MODULUS}.png")


# doesn't work for points that are equal (multiplication)
# because of division by zero in lambda
def simple_addition(p1, p2, MODULUS):
    lmbd = (p2[1] - p1[1]) / (p2[0] - p1[0])
    x3 = int((lmbd ** 2 - p1[0] - p2[0]) % MODULUS)
    y3 = int(((p1[0] - x3) * lmbd - p1[1]) % MODULUS)

    return (x3, y3)


def double(x, y, a, p):
    lambd = (((3 * x**2) % p ) *  pow(2 * y, -1, p)) % p
    newx = (lambd**2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    return (newx, newy)


def add_points(xq, yq, xp, yp, p, a=0):
    if xq == yq == None:
        return xp, yp
    if xp == yp == None:
        return xq, yq

    assert (xq**3 + 3) % p == (yq ** 2) % p, "q not on curve"
    assert (xp**3 + 3) % p == (yp ** 2) % p, "p not on curve"

    if xq == xp and yq == yp:
        return double(xq, yq, a, p)
    elif xq == xp:
        return None, None

    lambd = ((yq - yp) * pow((xq - xp), -1, p)) % p
    xr = (lambd**2 - xp - xq) % p
    yr = (lambd*(xp - xr) - yp) % p
    return xr, yr


if __name__ == "__main__":
    main()
