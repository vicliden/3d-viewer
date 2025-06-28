# Shapes.py
# This module defines various geometric shapes and their properties.
class Shape():
    """
    Base class for all shapes.
    
    """
    def __init__(self, id , color = "red", center = (0, 0), ):
        self.color = color
        self.center = center
        self.id = id


    def get_lines(self) -> list[tuple[float, float, float]]:
        """Returns a list of lines that define the shape.
        This method should be overridden by subclasses to provide specific line definitions.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

class Square(Shape):

    def __init__(self, id, side_length = 1, color = "red", center = (0, 0, 0)):
        super().__init__(id, color, center)
        self.side_length = side_length


    def get_edges(self) -> list[tuple[float, float, float]]:
        cx, cy, cz = self.center
        s = self.side_length / 2
        return [
            (cx - s, cy - s, 0),
            (cx + s, cy - s, 0),
            (cx + s, cy + s, 0),
            (cx - s, cy + s, 0),
            (cx - s, cy - s, 0) # Closing the square
        ]

    def get_lines(self) -> list[tuple[float, float, float]]:
        return self.get_edges()
    
class Cube(Shape):

    def __init__(self, id, side_length = 1, color = "blue", center = (0, 0, 0)):
        super().__init__(id, color, center)
        self.side_length = side_length

    def get_edges(self) -> list[tuple[float, float, float]]:
        cx, cy, cz = self.center
        s = self.side_length / 2

        # Define the 8 corners
        corners = [
            (cx - s, cy - s, cz - s),  # 0
            (cx + s, cy - s, cz - s),  # 1
            (cx + s, cy + s, cz - s),  # 2
            (cx - s, cy + s, cz - s),  # 3
            (cx - s, cy - s, cz + s),  # 4
            (cx + s, cy - s, cz + s),  # 5
            (cx + s, cy + s, cz + s),  # 6
            (cx - s, cy + s, cz + s),  # 7
        ]

        lines = [
            (0,1), (1,2), (2,3),(3,0),  # Bottom face
            (0,4),
            (4,5), (5,1), (1,5),
            (5,6), (6,2), (2,6),
            (6,7), (7,3), (3,7),
            (7,4)]
        # Flatten into a point list (for plotting)
        return [corners[i] for pair in lines for i in pair]

    def get_lines(self) -> list[tuple[float, float, float]]:
        return self.get_edges()

class Axis(Shape):
    def __init__(self, id, color = "red"):
        super().__init__(id, color, (0,0,0))

    def get_lines(self) -> list[tuple[float, float, float]]:
        cx, cy, cz = self.center
        l = 100
        return [
            (cx - l, cy, cz),
            (cx + l, cy, cz),
            (cx, cy, cz ),
            (cx, cy - l, cz),
            (cx, cy + l, cz),
            (cx, cy, cz),
            (cx, cy, cz - l),
            (cx, cy, cz + l)
        ]
    