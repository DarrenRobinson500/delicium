def set_prob(a, b, pa, pb):
    p = pa
    if (a + b) % 2 != 0: p = 1 - pb
    q = 1 - p

    if a >= 4: return 1
    if b >= 4: return 0
    return p * set_prob(a + 1, b, pa, pb) + q * set_prob(a, b + 1, pa, pb)

# for a, b in [(3,3), (3,2), (3,1), (3,0), (2, 3), (2, 2), (0, 0)]:
#     result = set_prob(a, b, 0.60, 0.55)
#     print("Result:", a, b, round(result, 2))


def game_prob(a, b, p):
    q = 1 - p
    if a >= 4: return 1
    if b >= 4: return 0
    return p * game_prob(a + 1, b, p) + q * game_prob(a, b + 1, p)

# for a, b in [(3,3), (3,2), (3,1), (3,1), (2, 3), (2, 2), (0, 0)]:
#     result = game_prob(a, b, 0.60)
#     print("Result:", a, b, round(result, 2))
