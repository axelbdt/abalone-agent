from math import comb

axel = comb(61, 28) * comb(28, 14)

antoine = comb(61, 14) * comb(47, 14)

def states(lost_white, lost_black):
    return comb(61, 14 - lost_white) * comb(61 - (14 - lost_white), 14 - lost_black)

# How many states are there?
s = (sum(states(i, j) for i in range(6) for j in range(6))
        + sum(states(6,j) for j in range(6)) 
        + sum(states(i, 6) for i in range(6)))
print("{:e}".format(s))
print (states(0, 0)== antoine)


# How many tera to stort all the states?
print("{:e}".format(s * 56 / 1e12))

