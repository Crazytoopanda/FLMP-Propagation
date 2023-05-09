# from charm.toolbox.integergroup import IntegerGroup
# from charm.schemes.pkenc.pkenc_rsa import RSA_Enc, RSA_Sig
# from charm.core.math.integer import integer, randomBits, random, randomPrime, isPrime, encode, decode, hashInt, bitsize, \
#     legendre, gcd, lcm, serialize, deserialize, int2Bytes, toInt

#-*-coding:utf-8-*-

from slt import SLT
from util import invert, powmod, getprimeover, isqrt
from CipherPub import CipherPub

from Ciphertext import Ciphertext
from Ciphertext1 import Ciphertext1

import random
from sm import SM
import time
from sad import SAD
import math
import gmpy2 as _g


try:
    from collections.abc import Mapping
except ImportError:
    Mapping = dict

DEFAULT_KEYSIZE = 1024

def divv(pair):
    a, b = pair
    return a/b

def randomPrime(n_length):
    p = q = n = None
    n_len = 0
    while n_len != n_length:
        p = getprimeover(n_length // 2)
        q = p
        while q == p:
            q = getprimeover(n_length // 2)
        n = p * q
        n_len = n.bit_length()

    if(p==q):
        raise ValueError('p and q have to be different')
    return p,q


def lcm(p_,q_):
    return (p_*q_)//_g.gcd(p_,q_)


def generate_paillier_keypair(n_length=DEFAULT_KEYSIZE):
    p, q = randomPrime(n_length)
    a = getprimeover(n_length // 2)
    x = getprimeover(n_length // 2)
    public_key = PaillierPublicKey(n_length,a ,x, p, q)
    private_key = PaillierPrivateKey(public_key, n_length, a ,x, p, q)
    return public_key, private_key


class PaillierPublicKey():
    def __init__(self, bitLengthVal = 1024,a = None,x = None,p = None, q = None):
        self.alpha = 2
        self.beta = 3
        self.bitLengthVal = bitLengthVal
        self.a = a
        self.N = p * q
        self.N2 = self.N**2
        self.g1 = 2

        self.g = (-powmod(self.a, self.g1 * self.N, self.N2)) % self.N2
        self.x = x
        self.h = powmod(self.g, self.x, self.N2)
        self.X = [None] * self.beta
        self.H = [None] * self.beta
        self.lambda1 = [None] * self.alpha
        self.Xsigma = 0
        self.Hsigma = powmod(self.g, self.Xsigma, self.N2)
        for ii in range(0, self.beta):
            self.X[ii] = getprimeover(self.bitLengthVal-12)
            self.H[ii] = powmod(self.g, self.X[ii], self.N2)
            self.Xsigma += self.X[ii]

        self.lamda = (p - 1) * (q - 1) // _g.gcd(p - 1, q - 1)
        self.KK1 = self.lamda * self.N2

        self.KKK = invert(_g.mpz(self.lamda), _g.mpz(self.N2))
        self.S = (self.lamda * self.KKK) % self.KK1
        self.lambda1[self.alpha - 1] = self.S

        for ii in range(0, self.alpha - 1):
            self.lambda1[ii] = getprimeover(self.bitLengthVal)
            self.lambda1[self.alpha - 1] = self.lambda1[self.alpha - 1] - self.lambda1[ii]


    def raw_encrypt(self, plaintext, *args):
        r = random.SystemRandom().randrange(1, 2 ** self.bitLengthVal)

        if args and len(args) > 0:
            cc = CipherPub()
            h = args[0]
            cc.PUB = h
        else:
            cc = CipherPub()
            cc.PUB = self.h
            h = cc.PUB

        cc.T1 = (((1 + plaintext * self.N) % self.N2) * powmod(h, r, self.N2)) % self.N2
        cc.T2 = powmod(self.g, r, self.N2)
        return cc


    def Encrypt(self, value,*args):#plaintext integet
        if args and len(args) > 0:
            ciphertext = self.raw_encrypt(value, *args)
        else:
            ciphertext = self.raw_encrypt(value)
        return ciphertext

    def AddPDec1(self, c, *args):  # c是 ciphertext hp integer
        if isinstance(c, Ciphertext) and args and len(args) > 0:
            hp = args[0]
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2 ** self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(hp, r, self.N2)) % self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 = powmod(cc.T1, self.lambda1[0], self.N2)
            return cc
        elif isinstance(c, CipherPub):
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2 ** self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(c.PUB, r, self.N2)) % self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 = powmod(cc.T1, self.lambda1[0], self.N2)
            return cc
        else:
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2 ** self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(self.Hsigma, r, self.N2)) % self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 = powmod(cc.T1, self.lambda1[0], self.N2)
            return cc

    def AddPDec2(self, c):  # c Ciphertext1
        cc = ((powmod(int(c.T1), int(self.lambda1[1]), self.N2) * c.T3)) % self.N2
        # if ((cc - 1) // self.N) % self.N >= self.N//2:
        #     return ((cc - 1) // self.N) % self.N - self.N
        return ((cc - 1) // self.N) % self.N

    #def PDecEncode(self, c):



    def Refreash(self,c,*args):# c Ciphertext hp integer
        if isinstance(c,Ciphertext):
            hp = args[0]
            cc = Ciphertext()
            r = random.SystemRandom().randrange(1, 2**self.bitLengthVal)
            cc.T1 = (c.T1*(powmod(hp,r,self.N2)))%self.N2
            cc.T2 = (c.T2*(powmod(self.g,r,self.N2)))%self.N2
            cc.PUB = c.PUB
            return cc
        else:
            cc = CipherPub()
            r = random.SystemRandom().randrange(1, 2 ** self.bitLengthVal)
            cc.T1 = (c.T1 * (powmod(c.PUB, r, self.N2))) % self.N2
            cc.T2 = (c.T2 * (powmod(self.g, r, self.N2))) % self.N2
            cc.PUB = c.PUB
            return cc

class PaillierPrivateKey():

    def __init__(self, public_key, bitLengthVal=1024, a = None, x = None, p = None, q = None):
        self.public_key = public_key
        self.alpha = 2
        self.beta = 3
        self.bitLengthVal = bitLengthVal

        self.lambda1 = self.public_key.lambda1
        self.N = p * q
        self.g1 = 2
        self.N2 = self.N**2
        self.a = a
        self.g = (-powmod(self.a, self.g1 * self.N, self.N2)) % self.N2
        self.g1 = 2
        self.x = x

        self.x1 = getprimeover(self.bitLengthVal // 4)
        self.lamda = (p - 1) * (q - 1) // _g.gcd(p - 1, q - 1)



        self.Hsigma = powmod(self.g, self.public_key.Xsigma, self.N2)
        self.h = powmod(self.g, self.x, self.N2)
        self.x2 = self.x - self.x1

    def WDecryption(self, c, *args):
        if args and len(args) > 0: # c ,CipherPub  x：Integer
            x = args[0]
            u = c.T1 * (invert(powmod(c.T2, x, self.N2), self.N2))
            return ((u - 1) // self.N) % self.N
        else:#c  ciphertext
            u = c.T1 * (invert(powmod(c.T2, self.x, self.N2), self.N2))
            return ((u - 1) // self.N) % self.N


    def PSDecryption1(self, c): # c Ciphertext
        cc = [None]*self.alpha
        cc[0] = powmod(c.T1,self.lambda1[0],self.N2)
        for ii in range(1,self.alpha):
            cc[ii] = powmod(c.T1,self.lambda1[ii],self.N2)
        return cc


    def DDecryption1(self,c): # c  [None]*number
        TT = 1
        for ii in range(0,self.alpha):
            TT = TT*c[ii]
        return ((TT-1)//self.N)%self.N


    def WPDecryption1(self,c,*args): #
       if isinstance(c, Ciphertext):
           cc = Ciphertext1()
           r = random.SystemRandom().randrange(1, 2**self.bitLengthVal)
           cc.T1 = (c.T1 * (powmod(self.h, r, self.N2))) % self.N2
           cc.T2 = (c.T2 * (powmod(self.g, r, self.N2))) % self.N2
           cc.T3 = powmod(cc.T2, self.x1, self.N2)
           return cc
       elif args and len(args) > 0 and isinstance(c, CipherPub):#c 是CipherPub对象 x1 Integer
           x1 = args[0]
           cc = powmod(c.T2, x1, self.N2)
           return cc
       else:# c  ,x1 Integer
            x1 = args[0]
            cc = powmod(c,x1,self.N2)
            return cc


    def WPDecryption2(self, c, *args) : #c CipherPub ccc [None]*number, integer
        if isinstance(c,CipherPub):
            ccc = args[0]
            NUM = args[1]
            x1 = args[2]
            TT = 1
            TT = powmod(c.T2,x1,self.N2)
            for ii in range(0,NUM - 1):
                TT = invert(TT*ccc[ii], self.N2)
            u = invert(c.T1*TT, self.N2)
            return ((u-1)//self.N)%self.N
        elif isinstance(c,Ciphertext):
            ccc = args[0]
            NUM = args[1]
            TT = 1
            for ii in range(0, NUM):
                TT = invert(TT * ccc[ii], self.N2)
            return ((TT - 1) // self.N) % self.N
        else:
            u1 = (c.T3 * (powmod(c.T2, self.x2, self.N2))) % self.N2
            u = c.T1 * (invert(u1, self.N2))
            return ((u - 1) // self.N) % self.N


    def SDecryption(self, c): #c ciphertext
        if isinstance(c,Ciphertext):
            u1 = invert(self.lamda, self.N)
            return (((powmod(c.T1, self.lamda, self.N2)-1)//self.N)*u1)%self.N
        elif isinstance(c,CipherPub):
            u1 = invert(_g.mpz(self.lamda), _g.mpz(self.N))
            return (((powmod(int(c.T1), int(self.lamda), self.N2) - 1) // self.N) * u1) % self.N


    def AddPDec1(self, c, *args): # c是 ciphertext hp integer
        if isinstance(c, Ciphertext) and args and len(args) > 0:
            hp = args[0]
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2**self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(hp, r, self.N2))%self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 = powmod(cc.T1,self.lambda1[0], self.N2)
            return cc
        elif isinstance(c, CipherPub):
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2**self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(c.PUB, r, self.N2)) % self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 =  powmod(cc.T1,self.lambda1[0], self.N2)
            return cc
        else:
            cc = Ciphertext1()
            r = random.SystemRandom().randrange(1, 2**self.bitLengthVal)
            cc.T1 = (c.T1 * powmod(self.Hsigma, r, self.N2)) % self.N2
            cc.T2 = (c.T2 * powmod(self.g, r, self.N2)) % self.N2
            cc.T3 = powmod(cc.T1,self.lambda1[0], self.N2)
            return cc


    def AddPDec2(self, c):#c Ciphertext1
        cc = ((powmod(int(c.T1),int(self.lambda1[1]),self.N2)*c.T3))%self.N2
        return ((cc-1)//self.N)%self.N


    def decrypt(self, encrypted_number):

        encoded = self.raw_decrypt(encrypted_number)
        if encoded <= self.public_key.N // 2:
            return encoded
        elif encoded >= self.public_key.N // 2:
           return encoded - self.public_key.N


    def raw_decrypt(self, ciphertext):
        ciphertext1 = self.AddPDec1(ciphertext)
        result = self.AddPDec2(ciphertext1)
        return result




if __name__ == "__main__":

    a = 10
    b = 5
    K = 2
    Di = []
    public_key, private_key = generate_paillier_keypair(1024)


    reg_lambda = 1

    E1 = public_key.Encrypt(b,public_key.H[1])
    E2 = public_key.Encrypt(a, public_key.H[1])

    SK17 = SAD(E1, E2, public_key)
    SK17.StepOne()
    SK17.StepTwo()
    SK17.StepThree()
    print(private_key.decrypt(SK17.FIN))

    SK18 = SM(E1, 10, public_key)
    SK18.StepOne()
    print(private_key.decrypt(SK18.FIN))

    SK11 = SLT(E1, E2, public_key)
    SK11.StepOne()
    SK11.StepTwo()
    SK11.StepThree()
    #大小比较结果U=0 x>=y ,U=1 x<y 结果U=
    print(private_key.decrypt(SK11.FIN))

















