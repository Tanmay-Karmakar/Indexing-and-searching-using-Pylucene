import math
# define the gumble distribution for rare turms
def gumble(x,alpha):
    return math.exp(- math.exp(-x/alpha))

# define the frechet distribution for common terms
def frechet(x,mu,alpha):
    return math.exp(-(mu/x)**alpha)

# Now make a mixture of theses
def G(x,mu,alpha,p):
    return p*gumble(x,alpha) + (1-p)*frechet(x,mu,alpha)