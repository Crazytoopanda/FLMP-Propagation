# import pailiierT as paillierT
from sad import SAD
from util import invert, powmod, getprimeover, isqrt
from CipherPub import CipherPub
from Ciphertext import Ciphertext
from Ciphertext1 import Ciphertext1
import time
import random
import math
import gmpy2 as _g
import paillierT

def compareTo(a, b):
    return ((a > b) - (a < b))


class SMAX():
    def __init__(self,_VA,_VB,_paillier):

        self.a = CipherPub()
        self.b = CipherPub()
        self.a11 = CipherPub()
        self.a12 = CipherPub()
        self.a14 = CipherPub()
        self.b14 = CipherPub()
        self.b11 = CipherPub()
        self.b12 = CipherPub()
        self.b13 = CipherPub()
        self.l1 = CipherPub()
        self.l2 = CipherPub()
        self.l3 = CipherPub()
        self.D1 = CipherPub()
        self.D2 = CipherPub()
        self.ERr1 = CipherPub()
        self.ERr2 = CipherPub()
        self.U = CipherPub()
        self.EEone = CipherPub()
        self.FINMX = CipherPub()
        self.FINMI = CipherPub()
        self.m11 = Ciphertext1()
        self.EZERO =CipherPub()
        self.a = _VA
        self.b = _VB
        self.paillier = _paillier
        self.pub = self.paillier.Hsigma


    def StepOne(self):
        self.time_start = time.time()
        self.a1 = self.paillier.N-1
        self.TWO = 2


        self.l = random.SystemRandom().randrange(1, 2**(self.paillier.N.bit_length()//2))


        self.EEone = self.paillier.raw_encrypt(1, self.pub)
        self.EZERO = self.paillier.raw_encrypt(0, self.pub)

        self.a11 = self.a
  
        self.b11 = self.b

        self.a12.T1 = ((powmod(self.a11.T1,self.TWO, self.paillier.N2))*self.EEone.T1)%self.paillier.N2
        self.a12.T2 = ((powmod(self.a11.T2,self.TWO, self.paillier.N2))*self.EEone.T2)%self.paillier.N2

        self.a12.PUB = self.a11.PUB

        self.b12.T1 = powmod(self.b11.T1,self.TWO, self.paillier.N2)
        self.b12.T2 = powmod(self.b11.T2,self.TWO, self.paillier.N2)
        self.b12.PUB = self.b11.PUB

        self.RR1 = random.SystemRandom().randrange(1, 2**200)
        self.Rr1 = random.SystemRandom().randrange(1, 2**200)
        self.Rr2 = random.SystemRandom().randrange(1, 2**200)
        self.RRr1 = self.paillier.N - self.Rr1
        self.RRr2 = self.paillier.N - self.Rr2

        self.ERr1 = self.paillier.raw_encrypt(self.Rr1, self.pub)
        self.ERr2 = self.paillier.raw_encrypt(self.Rr2, self.pub)

        self.s = random.SystemRandom().randrange(1, 100000000) % 2

        if self.s == 1:
            self.b13.T1 = powmod(self.b12.T1, self.a1, self.paillier.N2)
            self.b13.T2 = powmod(self.b12.T2, self.a1, self.paillier.N2)

            self.a14.T1 = powmod(self.a11.T1, self.a1, self.paillier.N2)
            self.a14.T2 = powmod(self.a11.T2, self.a1, self.paillier.N2)

            self.b14.T1 = powmod(self.b11.T1, self.a1, self.paillier.N2)
            self.b14.T2 = powmod(self.b11.T2, self.a1, self.paillier.N2)
            self.l1.T1 = powmod(self.a12.T1 * self.b13.T1, self.RR1, self.paillier.N2)
            self.l1.T2 = powmod(self.a12.T2 * self.b13.T2, self.RR1, self.paillier.N2)
            self.l1.PUB = self.pub

            self.l2.T1 = self.b11.T1 * self.a14.T1 * self.ERr1.T1
            self.l2.T2 = self.b11.T2 * self.a14.T2 * self.ERr1.T2
            self.l2.PUB = self.pub

            self.l3.T1 = self.a11.T1 * self.b14.T1 * self.ERr2.T1
            self.l3.T2 = self.a11.T2 * self.b14.T2 * self.ERr2.T2
            self.l3.PUB = self.pub
        else:
            self.b13.T1 = powmod(self.a12.T1, self.a1, self.paillier.N2)
            self.b13.T2 = powmod(self.a12.T2, self.a1, self.paillier.N2)

            self.a14.T1 = powmod(self.a11.T1, self.a1, self.paillier.N2)
            self.a14.T2 = powmod(self.a11.T2, self.a1, self.paillier.N2)

            self.b14.T1 = powmod(self.b11.T1, self.a1, self.paillier.N2)
            self.b14.T2 = powmod(self.b11.T2, self.a1, self.paillier.N2)


            self.l1.T1 = powmod(self.b12.T1 * self.b13.T1, self.RR1, self.paillier.N2)
            self.l1.T2 = powmod(self.b12.T2 * self.b13.T2, self.RR1, self.paillier.N2)
            self.l1.PUB = self.pub

            self.l3.T1 = self.b11.T1 * self.a14.T1 * self.ERr2.T1
            self.l3.T2 = self.b11.T2 * self.a14.T2 * self.ERr2.T2
            self.l3.PUB = self.pub

            self.l2.T1 = self.a11.T1 * self.b14.T1 * self.ERr1.T1
            self.l2.T2 = self.a11.T2 * self.b14.T2 * self.ERr1.T2
            self.l2.PUB = self.pub


        self.m11 = self.paillier.AddPDec1(self.l1)


    def StepTwo(self):

        self.m1 = self.paillier.AddPDec2(self.m11)
        if compareTo(self.m1,self.l) == -1:
            self.U = self.paillier.raw_encrypt(0, self.pub)
            self.D1 = self.paillier.raw_encrypt(0, self.pub)
            self.D2 = self.paillier.raw_encrypt(0, self.pub)

        elif compareTo(self.m1,self.l) == 1:
             self.U = self.paillier.raw_encrypt(1, self.pub)
             self.D1 = self.paillier.Refreash(self.l2)
             self.D2 = self.paillier.Refreash(self.l3)
        else:
            self.U = self.paillier.raw_encrypt(self.a1, self.pub)



    def StepThree(self):
        if self.s == 1 :
            self.FINMX.T1 = (self.a.T1 * self.D1.T1 * powmod(self.U.T1, self.RRr1, self.paillier.N2)) % self.paillier.N2
            self.FINMX.T2 = (self.a.T2 * self.D1.T2 * powmod(self.U.T2, self.RRr1, self.paillier.N2)) % self.paillier.N2
            self.FINMX.PUB = self.pub
            self.FINMI.T1 = (self.b.T1 * self.D2.T1 * powmod(self.U.T1, self.RRr2, self.paillier.N2)) % self.paillier.N2
            self.FINMI.T2 = (self.b.T2 * self.D2.T2 * powmod(self.U.T2, self.RRr2, self.paillier.N2)) % self.paillier.N2
            self.FINMI.PUB = self.pub

        if self.s == 0:
            self.FINMX.T1 = (self.b.T1 * self.D1.T1 * powmod(self.U.T1, self.RRr1, self.paillier.N2)) % self.paillier.N2
            self.FINMX.T2 = (self.b.T2 * self.D1.T2 * powmod(self.U.T2, self.RRr1, self.paillier.N2)) % self.paillier.N2
            self.FINMX.PUB = self.pub
            self.FINMI.T1 = (self.a.T1 * self.D2.T1 * powmod(self.U.T1, self.RRr2, self.paillier.N2)) % self.paillier.N2
            self.FINMI.T2 = (self.a.T2 * self.D2.T2 * powmod(self.U.T2, self.RRr2, self.paillier.N2)) % self.paillier.N2
            self.FINMI.PUB = self.pub
        time_end = time.time()
        #print('time cost1-2', time_end - self.time_start, 's')

if __name__ == "__main__":
    a = -20000001
    b = -40000001

    PaillierPublicKey,PaillierPrivateKey = paillierT.generate_paillier_keypair(1024)


    E10 = PaillierPublicKey.Encrypt(a)

    E20 = PaillierPublicKey.Encrypt(b)


    SK111 = SMAX(E10, E20,PaillierPublicKey)
    SK111.StepOne()
    SK111.StepTwo()
    SK111.StepThree()

    print("2个数中小的是" ,PaillierPrivateKey.decrypt(SK111.FINMI))
    print("2个数中大的是" ,PaillierPrivateKey.decrypt(SK111.FINMX))
    
    if PaillierPrivateKey.decrypt(SK111.FINMX) == PaillierPrivateKey.decrypt(E10):
        print('E1')
    elif PaillierPrivateKey.decrypt(SK111.FINMX) == PaillierPrivateKey.decrypt(E20):
        print('E2')