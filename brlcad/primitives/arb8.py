"""
Python wrapper for the ARB8 primitive of BRL-CAD.
This covers in fact the whole ARB4-ARB8 series of primitives, as all those are
saved internally as ARB8.
"""

from base import Primitive
import numpy as np


class ARB8(Primitive):

    def __init__(self, name, points, copy=False):
        Primitive.__init__(self, name=name)
        self.point_mat = np.matrix(points, copy=copy)

    def __repr__(self):
        return "ARB8({0}, {1})".format(self.name, self.point_mat)

    def _get_points(self):
        # returns tuple because it should be immutable
        return tuple(self.point_mat.flat)

    points = property(_get_points)

    def copy(self):
        return ARB8(self.name, self.point_mat, copy=True)

    def has_same_data(self, other):
        return np.allclose(self.point_mat, other.point_mat)

    def update_params(self, params):
        params.update({
            "points": self.points,
        })

    @staticmethod
    def from_wdb(name, data):
        return ARB8(
            name=name,
            points=np.ctypeslib.as_array(data.pt)
        )