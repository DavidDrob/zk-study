from py_ecc.bn128 import G1, multiply, add, eq, neg, curve_order, field_modulus, is_on_curve, is_inf, Z1
from py_ecc.fields import bn128_FQ

print(bn128_FQ(3))
print(G1)

print(multiply(G1, 2))
print(add(G1, G1) == multiply(G1, 2))

# Modulus != curve order
print(curve_order)
print(field_modulus)
print(field_modulus-curve_order)

# Homomorphism between modular addition
# and EC addition

x = 2 ** 300 + 21
y = 3 ** 50 + 11

# mulitplication takes modulus before doing the multiplication
# so it doesn't matter if multiplier overflows
print(x + y > field_modulus)

# (x + y)G == xG + yG
assert eq(multiply(G1, (x + y)), add(multiply(G1, x), multiply(G1, y)))
assert eq(multiply(G1, (x + y) % curve_order), add(multiply(G1, x), multiply(G1, y)))

# Division

# rational numbers are not "supported"
# however in a finite field you can compute the rationals
# using the modulo of the inverse
five_over_two = (5 * pow(2, -1, curve_order))
one_half = pow(2, -1, curve_order)

# 5/2 + 0.5 = 3
assert eq(add(multiply(G1, five_over_two), multiply(G1, one_half)), multiply(G1, 3))


# Associativity
x = 5
y = 10
z = 15

# (G1*x + G1*y) + G1*z
lhs = add(add(multiply(G1, x), multiply(G1, y)), multiply(G1, z))

# G1*x + (G1*y + G1*z)
rhs = add(multiply(G1, x), add(multiply(G1, y), multiply(G1, z)))

assert eq(lhs, rhs)


# Inverses

random_point = multiply(G1, x)
inverse = (random_point[0], random_point[1] * -1)

assert inverse == neg(random_point)

our_curve = bn128_FQ(3)
assert is_on_curve(inverse, our_curve)

# add inverse to original point will return point at infinity
assert is_inf(add(random_point, neg(random_point)))

# points at infinity == Z1 == identity of group
assert add(random_point, neg(random_point)) == Z1
