def isPrime(num):
    for i in range(3, num):
        if num % i == 0:
            return False
    return True

def eea(a,b):
	if b==0:return (1,0)
	(q,r) = (a//b,a%b)
	(s,t) = eea(b,r)
	return (t, s-(q*t) )

def find_inverse(x,y):
	inv = eea(x,y)[0]
	if inv < 1: inv += y #we only want positive values
	return inv

def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

def Encript(p,d):
    cipher = []
    for i in range(len(p)):
        c = pow(p[i], d) % n
        cipher.append(c)
    return cipher

def readFileEnkript(fl):
    with open(fl, 'rb') as f:
        words = toIntst(f.read())
    return words

def readFileDecript(fl):
    with open(fl, 'rb') as f:
        w = f.read().split( )
        w = toIntde(w)
    return w

def toIntst(w):
    res = []
    for i in range(len(w)):
        res.append(ord(w[i]))
    return res

def toIntde(w):
    res = []
    for i in range(len(w)):
        res.append(long(w[i]))
    return res

def Decript(c, e):
    plain = []
    for i in range(len(c)):
        p = pow(c[i], e) % n
        plain.append(p)

    print plain
    return plain

def writeFileEnkript(fl,w):
    f = open(fl, "wb")
    for i in range(len(w)):
        if(i != len(w)-1): f.write(str(w[i])+" ")
        else: f.write(str(w[i]))
    f.close()

def writeFileDekript(fl,w):
    f = open(fl, "wb")
    for i in range(len(w)):
        f.write(chr(w[i]))
    f.close()

#main
print("input P")
p = input()
print("input Q")
q = input()
if not isPrime(p): raise Exception("P (%i) is not prime" % (p,))
if not isPrime(q): raise Exception("Q (%i) is not prime" % (q,))
print("input E")
e = input()
on = (p-1)*(q-1)
if e < 1 or e > on: raise Exception("E must be > 1 and < 0n")
if gcd(e, on)!=1: raise Exception("E is not coprime with 0n")
n = p*q
d = find_inverse(e,on)
print "public key: (N: %i, E: %i)" % (n, e)
print "private key: (N: %i, D: %i)" % (n, d)

plain = readFileEnkript("plain.txt")
cipher = Encript(plain,d)
writeFileEnkript("encript.txt",cipher)


filedec = readFileDecript("encript.txt")
print filedec
resplain =  Decript(filedec, e)

writeFileDekript("decript.txt", resplain)