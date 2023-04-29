import math


class Vector:
    def __init__(self, *comp):
        if len(comp) == 1 and isinstance(comp[0], (list, tuple)):
            comp = comp[0]

        if len(comp) != 0 and not all(isinstance(i, (int, float)) for i in comp):
            raise TypeError(f'Vector components must be integers or floats')

        if len(comp) == 0:
            self.x, self.y, self.z = 0, 0, 0
        elif len(comp) == 1:
            self.x, self.y, self.z = comp[0], comp[0], comp[0]
        elif len(comp) == 2:
            self.x, self.y, self.z = comp[0], comp[1], 0
        elif len(comp) == 3:
            self.x, self.y, self.z = comp[0], comp[1], comp[2]
        else:
            raise ValueError('Vector can have only 0, 1, 2 or 3 components')

    def __len__(self):
        return 3

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        return f'Vector({self.x}, {self.y}, {self.z})'

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError('Vector index out of range')

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError('Vector index out of range')

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Cannot add non-vector to vector')
        else:
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __radd__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Cannot add vector to non-vector')
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Cannot subtract non-vector from vector')
        else:
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rsub__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Cannot subtract vector from non-vector')
        else:
            return Vector(other.x - self.x, other.y - self.y, other.z - self.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __abs__(self):
        return math.hypot(math.hypot(self.x, self.y), self.z)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            raise TypeError('Multiplication operation is only allowed between two vectors or a vector and an int/float')

    def __rmul__(self, other):
        return self * other

    def __matmul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.y * other.z - self.z * other.y,
                          self.z * other.x - self.x * other.z,
                          self.x * other.y - self.y * other.x)
        else:
            raise TypeError('Cross product can be done only between two vectors')

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            if other != 0:
                return Vector(self.x / other, self.y / other, self.z / other)
            else:
                raise ZeroDivisionError('Division by zero is not allowed when dividing a vector by a scalar')
        else:
            raise TypeError('Vector division can only be done between a vector and a scalar (int or float)')

    def dot(self, vector):
        if isinstance(vector, Vector):
            return self.x * vector.x + self.y * vector.y + self.z * vector.z
        else:
            raise TypeError('Dot product can be done only between two vectors')

    def cross(self, vector):
        if isinstance(vector, Vector):
            return Vector(self.y * vector.z - self.z * vector.y,
                          self.z * vector.x - self.x * vector.z,
                          self.x * vector.y - self.y * vector.x)
        else:
            raise TypeError('Cross product can be done only between two vectors')

    def magnitude(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.x * self.y))

    def normalize(self):
        mag = math.sqrt((self.x * self.x) + (self.y * self.y) + (self.x * self.y))
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def angle(self, vector, in_degrees=False):
        if isinstance(vector, Vector):
            if self.magnitude() == 0 or vector.magnitude() == 0:
                raise ZeroDivisionError('Angle cant be measured between a null vector and other vector')
            else:
                angle = math.acos((self.dot(vector)) / (self.magnitude() * vector.magnitude()))
                if in_degrees:
                    return math.degrees(angle)
                else:
                    return angle
        else:
            raise TypeError('Angle is calculated between two vectors')

    def project_on(self, projection_dir):
        if isinstance(projection_dir, Vector):
            if projection_dir.magnitude() == 0:
                raise ZeroDivisionError('Projection direction cant be a null vector')
            else:
                return (self.dot(projection_dir) / projection_dir.dot(projection_dir)) * projection_dir
        else:
            raise TypeError('Projection direction must be a vector')


UNIT_VECTOR = Vector(1)
NULL_VECTOR = Vector()
