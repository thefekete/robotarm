import operator
from math import sqrt, sin, cos, acos


class vector(tuple):
    """A simple vector class/type implementation"""

    def __new__(self, *args):
        if len(args) == 3:
            xyz = args
        else:
            xyz = args[0]
        xyz = map(float, xyz)
        return tuple.__new__(self, xyz)

    def __init__(self, *args):
        self.x = self[0]
        self.y = self[1]
        self.z = self[2]
        self.mag = sqrt(reduce(operator.add, map(operator.mul, self, self)))
        self.mag = sqrt( sum( ( x*x for x in self )))

    def __getattr__(self, attr):
        if attr == 'unit':
            # Calculate unit vector when called the first time
            self.unit = self.__class__([ x/self.mag for x in self ])
            return self.unit

    def __repr__(self):
        return "%s(%s, %s, %s)" % \
               (self.__class__.__name__, self[0], self[1], self[2])

    # Addition Operators
    def __add__(self, other):
        try:
            return self.__class__(map(operator.add, self, other))
        except:
            return self.__class__([ x+other for x in self ])

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        return self + other
        
    # Subtraction Operators
    def __sub__(self, other):
        try:
            return self.__class__(map(operator.sub, self, other))
        except:
            return self.__class__([ x-other for x in self ])

    def __isub__(self, other):
        return self - other

    def __rsub__(self, other):
        try:
            return self.__class__(map(operator.sub, other, self))
        except:
            return self.__class__([ other-x for x in self ])

    # Multiplication Operators
    def __mul__(self, other):
        try:
            return self.__class__(map(operator.mul, self, other))
        except:
            return self.__class__([ x*other for x in self ])

    def __imul__(self, other):
        return self*other

    def __rmul__(self, other):
        return self*other

    # Division Operators
    def __div__(self, other):
        try:
            return self.__class__(map(operator.div, self, other))
        except:
            return self.__class__([ x/other for x in self ])

    def __idiv__(self, other):
        return self / other

    def __rdiv__(self, other):
        try:
            return self.__class__(map(operator.div, other, self))
        except:
            return self.__class__([ other/x for x in self ])

    # Unary Operators
    def __neg__(self):
        return self.__class__([ -x for x in self ])

    def __pos__(self):
        return self

    def __abs__(self):
        return self.mag



def dotproduct(v1, v2):
    """Calculate the dot product between vectors v1 and v2 => float"""
    return sum(map(operator.mul, v1, v2))


def angle(v1, v2):
    """Calculate the angle between vectors v1 and v2 => radians"""
    return acos(dotproduct(v1, v2) / (v1.mag*v2.mag))


def crossproduct(v1, v2):
    """Calculate cross product between vectors v1 and v2 => vec()"""
    return vector([
        (v1.y*v2.z - v1.z*v2.y), # x component
        -(v1.x*v2.z - v1.z*v2.x), # y component
        (v1.x*v2.y - v1.y*v2.x) # z component
    ])


def rotate(v1, v2, theta):
    """Rotate vector v1 about v2 by the angle theta in radians.
The right hand rule applies."""
    # Adapted from equations published by Glenn Murray - Thanks Glenn!!!
    # http://inside.mines.edu/~gmurray/ArbitraryAxisRotation/ArbitraryAxisRotation.html
    x, y, z = v1
    u, v, w = v2
    newx = (
            (
                u*(u*x + v*y + w*z)
                + (x*(v**2 + w**2) + u*(-v*y - w*z))*cos(theta)
                + sqrt(u**2 + v**2 + w**2)*(-w*y + v*z)*sin(theta)
            )
            / (u**2 + v**2 + w**2)
        )
    newy = (
            (
                v*(u*x + v*y + w*z)
                + (y*(u**2 + w**2) + v*(-u*x - w*z))*cos(theta)
                + sqrt(u**2 + v**2 + w**2)*(w*x - u*z)*sin(theta)
            )
            / (u**2 + v**2 + w**2)
        )
    newz = (
            (
                w*(u*x + v*y + w*z)
                + (z*(u**2 + v**2) + w*(-u*x - v*y))*cos(theta)
                + sqrt(u**2 + v**2 + w**2)*(-v*x + u*y)*sin(theta)
            )
            / (u**2 + v**2 + w**2)
        )
    return vector([newx,newy,newz])


# Some usefull vectors:
X = vector(1, 0, 0)
Y = vector(0, 1, 0)
Z = vector(0, 0, 1)



if __name__ == '__main__':
    from math import degrees, radians, pi
    
    v = vector(-2, 5, 6.4)
    v2 = vector([1, 2, 3])
    print "v.mag:", v.mag
    print "v.unit:", v.unit
    print "v + v1:", v + v2
    print "v+5:", v + 5
    print "dotproduct:", dotproduct(v, v2)
    print "angle:", degrees(angle(v, v2))
    print "crossproduct:", crossproduct(v, v2)
    print "rotate:", rotate(v, v2, 60)
