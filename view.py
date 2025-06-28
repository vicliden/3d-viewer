import matplotlib.pyplot as plt
from typing import Union, List, Tuple
import numpy as np
from typing import Any
from needed_math import rot_x, rot_y, rot_z, project_on_vector, project_to_plane, get_plane_base
from matplotlib.animation import FuncAnimation
from shapes import Shape, Cube, Axis

class View():

    def __init__(self, width = 5, z_angle = 0, x_angle = 0):
        """Initializes the View with a specified width and angle.
        Args:
            width (float, optional): The width of the view. Defaults to 5.
            z_angle (float, optional): The rotation angle around the Z-axis (in degrees). Defaults to 0.
            x_angle (float, optional): The rotation angle around the X-axis (in degrees). Defaults to 0.
        """
        self.width = width
        self.z_angle = -np.deg2rad(z_angle)
        self.x_angle = -np.deg2rad(x_angle)
        self.fig, self.ax = plt.subplots(figsize=(width, width))
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.shapes : dict[Any, Shape]= {}
        self.n_vector = self.define_n_vector()
        self.ax.set_xlim(-self.width / 2, self.width / 2)
        self.ax.set_ylim(-self.width / 2, self.width / 2)  
        self.text = self.fig.text(0.02, 0.98 , f"z-rot = {self.z_angle:.3f}, xy-rot = {self.x_angle:.3f}", ha='left', va='top')

    def add_shape(self, shape: Shape):
        """Adds a shape to the view."""
        self.shapes[shape.id] = shape

    def remove_shape(self, shape_id: Any):
        """Removes a shape from the view by its ID."""
        if shape_id in self.shapes:
            del self.shapes[shape_id]
        else:
            print(f"Shape with ID {shape_id} not found in the view.")

    def define_n_vector(self) -> np.ndarray:
        """Defines the normal vector of the view plane based on the specified angles."""
        angle_x, angle_z = self.x_angle, self.z_angle

        n = np.array([0, 1, 0])
        R = rot_z(angle_z) @ rot_x(angle_x)
        n = R @ n
        self.n_vector = n / np.linalg.norm(n)  # Normalize the normal vector
        return self.n_vector

    def get_view_plane_base_vectors(self) -> Tuple[np.ndarray, np.ndarray]:
        n = self.define_n_vector()  
        
        v = np.cross(n, np.array([0, 0, 1]))
        v = v / np.linalg.norm(v)  # Normalize v


        u = -np.cross(n, v)
        u = u / np.linalg.norm(u)  # Normalize u


        return v, u


    def project_to_2d(self):
        pass

    def get_view(self,):
        plt.show()

    def create_shape_view(self, shape : Shape):
        """create a 2D view of a shape in the view plane."""
        self.n_vector = self.define_n_vector()  # Update the normal vector of the view plane
        
        edges = shape.get_lines()  #[(x, y, z), ...]
        edges = [np.array(edge) for edge in edges] #[np.array((x, y, z)), ...]
        # Project each edge onto the view plane
        projected_edges = [project_to_plane(edge, self.n_vector) for edge in edges]
        # Unzip the projected edges into x, y, z coordinates

        v, u = self.get_view_plane_base_vectors()

        test = [np.array([0, 1, 0]), np.array([0, -1, 0])]

        projected_edges_in_plane_base = [np.array([np.dot(edge, v), np.dot(edge, u)]) for edge in projected_edges]
        

        x, y = zip(*projected_edges_in_plane_base)

        return shape.id, x, y

    def draw(self):
        
        for shape in self.shapes.values():
            shape_id, x, y = self.create_shape_view(shape)
            self.ax.plot(x, y, color=shape.color, marker='', ls='-')
        plt.draw()


    def animate_revolution(self):
        """Animates the revolution of the shapes around the view plane."""
        # This method can be implemented to create an animation of the shapes revolving around the view plane.
        plots = {}
        for shape in self.shapes.values():
            shape_id, x, y = self.create_shape_view(shape)
            plots[shape_id], = self.ax.plot(x, y, color=shape.color, marker='', ls='-')
        dt = 0.006  # Time step for the animation
        STEPS_PER_FRAME = 10
        interval = dt * 1000 / STEPS_PER_FRAME  # Convert to milliseconds for FuncAnimation 

        #debug
        self.ax.plot
        
        def update(frame):
            self.z_angle -= dt   # Rotate around the z-axis
            self.n_vector = self.define_n_vector()  # Update the view plane normal vector

            for _ in range(STEPS_PER_FRAME):
                for shape in self.shapes.values():
                    shape_id, x, y = self.create_shape_view(shape)
                    plots[shape_id].set_data(x, y)
                    self.text.set_text(f"z-rot = {np.rad2deg(self.z_angle):.3f}, xy-rot = {np.rad2deg(self.x_angle):.3f}")
            return plots

        animation = FuncAnimation(self.fig, update, frames=10000, interval=interval, blit=False)

        plt.show()


if __name__ == "__main__":
    view = View(z_angle=12, x_angle=20)
    cube = Cube(id=2, side_length=2, color='green', center=(0, 0, 1))
    view.add_shape(cube)
    axis = Axis(id=3, color='red')
    view.add_shape(axis)
    # view.draw()
    # view.get_view()
    view.animate_revolution()
    

