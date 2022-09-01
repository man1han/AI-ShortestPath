class nodeClass:

    def __init__(self, root, coordinates):
        self.root = root
        self.coordinates = coordinates
        self.f, self.g, self.h = 0, 0, 0

    def __eq__(self, object):
        return self.coordinates == object.coordinates

    def __lt__(self, other):
        if self.g == other.g:
            return self.h < other.h
        else: 
            return self.g > other.g