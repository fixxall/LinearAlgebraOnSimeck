from sage.all import PolynomialRing, GF

GF2 = GF(2)

def lshift(x, base):
    ret = x[base:] + x[:base]
    return ret

# define f function
def f(x):
    return xor(dot(x, lshift(x, 5)), lshift(x,1))

# xor just in GF2
def xor(a,b):
    ret = []
    for i in range(len(a)):
        ret += [a[i]+b[i]]
    return ret

# dot function just in GF2
def dot(a,b):
    ret = []
    for i in range(len(a)):
        ret += [a[i]*b[i]]
    return ret

# int to bits in just GF2
def intToBits(x):
    ret = bin(x)[2:].zfill(16)
    return [GF2(int(i)) for i in ret]

# function for penjadwalan kunci
def keyGeneration(key, round):
    k_size = 16
    k_gen = [None for _ in range(round+1)]
    k_gen[0] = key[48: 48+k_size]
    k_gen[1] = key[32: 32+k_size]
    k_gen[2] = key[16: 16+k_size]
    k_gen[3] = key[: k_size]
    for i in range(4,round+1):
        k_gen[i] = xor(xor(k_gen[i-4] , f(k_gen[i-3])) , intToBits(i))
    return k_gen

# function for Encryption Scheme
def encryption(round, plaintext, key):
    # just handle key generation array return, for the round not changing
    keyround = round
    if(round<3): keyround = 3
    Keygen = keyGeneration(key, keyround)
    
    pt = [GF2(i) for i in plaintext]
    left, right = pt[:16], pt[16:]
    for i in range(round):
        right = xor(xor(right, Keygen[i]), f(left))
        left, right = right, left
    return left+right

if __name__ == "__main__":
    # define Variables
    vars = ['k'+str(i) for i in range(64)]
    K = PolynomialRing(GF2,vars).gens()

    # define Plaintext
    Plaintext = [0 for _ in range(32)]
    key = list(K)
    equation = encryption(5, Plaintext, key)
    print(equation)
    print(len(equation))