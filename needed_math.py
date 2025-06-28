import numpy as np

def rot_x(theta):  # rotation i yz-planet
    return np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta),  np.cos(theta)]
    ])

def rot_y(theta):  # rotation i xz-planet
    return np.array([
        [ np.cos(theta), 0, np.sin(theta)],
        [ 0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)]
    ])

def rot_z(theta):  # rotation i xy-planet
    return np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])

def project_on_vector(v,n):
    """Projects vector v onto vector n."""
    v = np.array(v)
    n = np.array(n)
    n = n / np.linalg.norm(n)  # Normalize the normal vector
    return np.dot(v, n) * n  # Project v onto n

def project_to_plane(v, n):
    """Projects vector v onto the plane defined by normal vector n."""
    v = np.array(v)
    n = np.array(n)
    return v - project_on_vector(v, n)

def get_plane_base(n: np.ndarray, z_rotation: float = 0):
    n = n / np.linalg.norm(n)

    # Choose a helper vector that is not parallel to n
    if abs(n[2]) < 0.9:
        helper = np.array([0, 0, 1])
    else:
        helper = np.array([1, 0, 0])

    # u is perpendicular to n and helper
    u = np.cross(n, helper)
    u = u / np.linalg.norm(u)

    # v completes the right-handed basis
    v = np.cross(n, u)
    v = v / np.linalg.norm(v)

    # Apply rotation within the view plane using your matrix
    R = rot_z(z_rotation)
    u_rot = R @ u
    v_rot = R @ v

    return u_rot, v_rot

# def get_plane_base(n : np.ndarray, z_rotation: float = 0) :
#     n = n / np.linalg.norm(n)

#     # Want u to be orthogonal to (0, 0, 1), meaning u is in the XY-plane: (x, y, 0)
#     # To also be orthogonal to n, we can take the cross product of n and (0, 0, 1)
#     # This gives a vector that is orthogonal to both n and the Z-axis, thus lying in the XY-plane and the plane of n.
#     xy_proj_candidate = np.cross(n, np.array([0, 0, 1]))

#     if np.linalg.norm(xy_proj_candidate) < 1e-8:
#         # Edge case: n is parallel to the Z-axis (i.e., n is (0, 0, +/-1))
#         # In this case, the cross product with (0,0,1) would be zero.
#         # We need to choose an arbitrary vector in the XY-plane that is orthogonal to n.
#         # Since n is (0,0, +/-1), any vector in the XY-plane is orthogonal to n.
#         # Let's pick [1, 0, 0] as a default.
#         u = np.array([1, 0, 0])
#     else:
#         u = xy_proj_candidate / np.linalg.norm(xy_proj_candidate)

#     # Now that we have u (in the XY-plane and orthogonal to n),
#     # we can find v by taking the cross product of n and u.
#     v = np.cross(n, u)
#     v = v / np.linalg.norm(v)

#     #test
#     u = rot_z(z_rotation) @ u
#     v = rot_z(z_rotation) @ v

#     return u, v


