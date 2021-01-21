from vector_class import Vector3D as Vec

class Cube:
    name = 'Cube'

    def __init__(self, pos, size, colour=[255, 255, 255]):
        self.pos = Vec(pos)
        self.size = Vec(size)

        self.colour = colour

    def collide_point(self, point):
        x, y, z = self.pos.x, self.pos.y, self.pos.z
        w, h, d = self.size.x, self.size.y, self.size.z

        if not (x - (w/2) > point.x and x + (w/2) < point.x) : return False
        if not (y - (h/2) > point.y and y + (h/2) < point.y) : return False
        if not (z - (d/2) > point.z and z + (d/2) < point.z) : return False

        return True

class Sphere:
    name = 'Sphere'

    def __init__(self, pos, radius, colour=[255, 255, 255]):
        self.pos = Vec(pos)
        self.r = radius

        self.r_squared = self.r**2

        self.colour = colour

    def collide_point(self, point):
        return self.pos.dist(point.pos) <= self.r_squared

objects_to_add = [

    Sphere(
        pos=(50, 20, 50),
        radius=20,
        colour=[150, 0, 0]
    ),

    Sphere(
        pos=(50, 80, 50),
        radius=20,
        colour=[0, 150, 0]
    )

]
