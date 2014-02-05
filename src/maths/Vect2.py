import math

class Vect2:
    def __init__(self, d):
        self.d = list(d)
    
    def __getitem__(self, n):
        return self.d[n]
    def __setitem__(self, index, value):
        self.d[index] = value

    def __add__(self, v):
        return Vect2((self.d[0]+v.d[0], self.d[1]+v.d[1]))
    
    def __sub__(self, v):
        return Vect2((self.d[0]-v.d[0], self.d[1]-v.d[1]))
        
    def __mul__(self, v):
        if v.__class__ == Vect2: # dot product
            return self.d[0]*v.d[0] + self.d[1]*v.d[1]
        return Vect2((self.d[0]*v, self.d[1]*v))
        
    def __div__(self, s):
        return Vect2((self.d[0]/s, self.d[1]/s))

    def __eq__(self, v):
        return self.d == v.d
 
    def magnitude_squared(self):
        return self.d[0]**2.0 + self.d[1]**2.0

    def magnitude(self):
        return math.sqrt(self.magnitude_squared())
    
    def distance(self, v):
        return (v-self).magnitude()
    
    def distance_squared(self, v):
        return (v-self).magnitude_squared()
    
    def normalize(self, length=1.0):
        return self/self.magnitude() * length

    def perp(self):
        return Vect2([-self.d[1], self.d[0]])

    def tuple(self): return tuple(self.d)
        
    def __str__(self):
        return "( %g %g )"%(self.d[0], self.d[1])

if __name__ == "__main__":
    assert Vect2((1, 0))+Vect2((0, 1)) == Vect2((1, 1))
    assert Vect2((2, 3)) * 2 == Vect2((4, 6))
    assert Vect2((5, 6)).normalize().magnitude() == 1
