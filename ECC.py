import math
import random
import time
import os

def isPrime(num):
    for i in range(3, num):
        if num % i == 0:
            return False
    return True


def eea(a, b):
    if b == 0: return (1, 0)
    (q, r) = (a // b, a % b)
    (s, t) = eea(b, r)
    return (t, s - (q * t))


def find_inverse(x, y):
    if x < y:
        return find_inverse(y, x)
    inv = eea(x, y)[0]
    if inv < 1: inv += y  # we only want positive values
    return inv


def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x


class EllipCurve(object):
    # y^2 = x^3 + ax + b mod p
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b

    def isPointOnCurve(self, point):
        res1 = (point.y * point.y) % self.p
        res2 = (point.x * point.x * point.x + self.a * point.x + self.b) % self.p
        return (res1 == res2)

    def findY(self, x):
        return math.floor(math.sqrt((x * x * x) + (self.a * x) + (self.b)))


class Point(object):
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __add__(self, q):
        Xp = self.x
        Yp = self.y
        Xq = q.x
        Yq = q.y

        if Xp == Xq:
            lam = ((3 * Xp * Xp + self.curve.a) * find_inverse(2 * Yp, self.curve.p))
        else:
            lam = (Yp - Yq) * find_inverse((Xp - Xq) % self.curve.p, self.curve.p)
        Xr = (lam * lam - Xp - Xq) % self.curve.p
        Yr = (lam * Xp - lam * Xr - Yp) % self.curve.p

        return Point(Xr, Yr, self.curve)

    def __mul__(self, k):
        if k == 0:
            return Point(0, 1, self.curve)
        if k == 1:
            return self
        q = Point(0, 1, self.curve)
        i = 1 << (k)
        while i > 0:
            q = q + q
            if (k & i) == i:
                q = q + self
            i = i >> 1
        return q

    def __str__(self):
        return '(%s,%s)' % (self.x, self.y)


def generateKey(curve, pt):
    privatekey = random.randint(0, curve.p - 1)
    publickey = pt * privatekey

    writefile("eccpublic", publickey)
    writefile("eccprivate", privatekey)

    return (privatekey, publickey)


# di sini m cuma 1 char, kalau mau encrypt banyak perlu iterasi
def encrypt(publickey, m, curve, pt, k):
    cx = (publickey * k).x + ord(m)
    cy = curve.findY(cx)
    c1 = Point(cx, cy, curve)
    c2 = pt * k
#    print(str(c1))
#    print(str(c2))
    return (c2, c1)

def writefile(fl, w):
    f = open(fl, "w")
    f.write(str(w))
    f.close()

def readfile(fl):
    with open (fl, "r") as myfile:
        x = myfile.read()
    return x

def groupCipher(c):
    s = c.split()
    return s

def decrypt(privatekey, c1, c2):
    return c2.x - (c1 * privatekey).x

def encryptString(publickey, s, curve, pt):
    k = random.randint(0, curve.p - 1)
    print(k)
    start = time.time()
    res = ""
    for c in s:
        d = encrypt(publickey, c, curve, pt, k)
        res += "['" + str(d[0])
        res += "';'" + str(d[1]) + "']"
        res += " "
    res = res[:len(res)-1]
    done = time.time()
    
    print("how long encrypt: %f" % (done-start))
    print(res)
    writefile("cipherteks",res)
    print("file size")
    print(os.path.getsize("cipherteks"))
    return res


def decryptString(privatekey, c, curve):
    start = time.time()
    res = ""
    for p in c:
        print(p)
        tx = p[p.find("[")+1:p.find("]")]
        t = tx.split(";")
        t1 = t[0][t[0].find("(")+1:t[0].find(")")]
        t2 = t[1][t[1].find("(")+1:t[1].find(")")]
        p1 = t1.split(",")
        p2 = t2.split(",")
        po1 = Point(int(p1[0]),int(p1[1]),curve)
        po2 = Point(int(p2[0]),int(p2[1]),curve)
        
        res += chr(decrypt(privatekey, po1, po2))
        
    done = time.time()
    print("how long decrypt: %f" % (done-start))
    writefile("plainteks",res)
    print("file size")
    print(os.path.getsize("plainteks"))
    return res

p = int(input("input p: "))
a = int(input("input a: "))
b = int(input("input b: "))
crv = EllipCurve(p, a, b)

x = int(input("x: "))
print("y: %i" % crv.findY(x))

pt = Point(x, crv.findY(x), crv)
k = generateKey(crv, pt)

#yyy = encrypt(k[1], 'c', crv, pt)
#print(chr(decrypt(k[0], yyy[0], yyy[1])))

stu = readfile("plain.txt")

asd = encryptString(k[1], stu, crv, pt)

cip = readfile("cipherteks")
points = groupCipher(cip)

pqr = decryptString(k[0], points, crv)
print(pqr)
