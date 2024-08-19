from py_ecc.bn128 import G1, multiply, add, eq, curve_order


# Basic proof
# prove you know two numbers that add up to 15
# without revealing them
def addition_zk_proof(s1, s2):
    z = 15  # public

    s1_c, s2_c = multiply(G1, s1), multiply(G1, s2)
    v_c = multiply(G1, z)

    return eq(v_c, add(s1_c, s2_c))


# Multiplication proof
# prove you know two numbers with the product 161
# without revealing them
def multiplication_zk_proof(s1, s2):
    z = 161  # public

    s2_c = multiply(G1, s2)
    z_over_s1_c = multiply(G1, (z * pow(s1, -1, curve_order)))

    # z / s1 == s2
    return eq(z_over_s1_c, s2_c)


# Linear equation
# prove you know the solution of a linear equation
# without revealing it
def linear_equation(s):
    # public
    k = 2
    d = 4
    f = 8

    s_c = multiply(G1, s)

    f_c = multiply(G1, f)
    d_c = multiply(G1, d)

    # `multiply` can only multiply by a scalar
    # not another curve points, so we use `k`
    # f = (k * x) + d
    return eq(add(multiply(s_c, k), d_c), f_c)


print(addition_zk_proof(7, 8))
print(multiplication_zk_proof(7, 23))
print(multiplication_zk_proof(23, 7))
print(multiplication_zk_proof(24, 7))
print(linear_equation(2))
