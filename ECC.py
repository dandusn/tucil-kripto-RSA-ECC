import math
import random

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
    if x<y:
        return find_inverse(y,x)
    inv = eea(x,y)[0]
    if inv < 1: inv += y #we only want positive values
    return inv

def gcd(x, y):
    while y != 0:
        (x, y) = (y, x % y)
    return x

class EllipCurve(object):
    #y^2 = x^3 + ax + b
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
      
    def isPointOnCurve(self, point):
        res1 = (point.y*point.y)%self.p
        res2 = (point.x*point.x*point.x + self.a*point.x + self.b)%self.p
        return (res1 == res2)
    
    def findY(self, x):
        return x*x*x+self.a*x+self.b
    
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

        if Xp==Xq:
            lam = ((3*Xp*Xp + self.curve.a)*find_inverse(2*Yp, self.curve.p))
        else:
            lam = (Yp - Yq)*find_inverse((Xp - Xq)%self.curve.p, self.curve.p)
        Xr = (lam*lam - Xp - Xq) % self.curve.p
        Yr = (lam*Xp - lam*Xr - Yp) % self.curve.p
        
        return Point(Xr, Yr, self.curve)
      
    def __mul__(self, k):
        if k==0:
            return Point(0, 1, self.curve)
        if k==1:
            return self
        q = Point(0, 1, self.curve)
        i = 1 << (int(math.log(k,2)))
        while i > 0:
            q = q + q
            if k&i==i:
                q = q + self
            i = i >> 1
        return q
    
    def __str__(self):
        return '(%s, %s)' % (self.x,self.y)
    
def generateKey(curve,pt):
    privatekey = random.randint(0,curve.p-1)
    publickey = pt*privatekey
    return (privatekey,publickey)

#di sini m cuma 1 char, kalau mau encrypt banyak perlu iterasi
def encrypt(publickey, m, curve, pt):
    k = random.randint(0,curve.p-1)
    cx = (publickey*k).x+ord(m)
    cy = curve.findY(cx)
    c1 = Point(cx,cy,curve)
    c2 = pt*k
    print(str(c1))
    print(str(c2))
    return (c1,c2)
    
def decrypt(privatekey, c1, c2):
    return c1.x - (c2*privatekey).x

crv = EllipCurve(7, 4, 9)
pt = Point(7,crv.findY(7),crv)
p = generateKey(crv,pt)
yyy = encrypt(p[1],'c',crv,pt)
print(chr(decrypt(p[0],yyy[0],yyy[1])))