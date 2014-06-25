"""
Python wrappers for the DSP (Displacement Map) primitives of BRL-CAD.
"""
from base import Primitive
import os
import brlcad.exceptions as BRLCADException


class DSP(Primitive):

    def __init__(self, name, dsp_name, data_src="file", width=142, length=150, interpolation=False, cut_direction=1,
                 cell_size=1, unit_elevation=0.005, copy=False):
        """
        :param name:
        :param data_src: (1)file('f')/(2)object('o')
        :param dsp_name: name of file/object
        :param width: width of displacement-map
        :param length: length of displacement-map
        :param interpolation: True for normal interpolation
        :param cut_direction: (1,ad)ad(adaptive),(2,lR)llUR(lower left to upper right) or (3,Lr)ULlr(Upper Left to lower right)
        :return:
        """
        Primitive.__init__(self, name=name)
        if isinstance(data_src, str):
            if data_src[0] == "f" or data_src[0] == "F":
                self.data_src = 1
            elif data_src[0] == "o" or data_src[0] == "O":
                self.data_src = 2
            else:
                raise BRLCADException("Invalid Data")
        elif data_src == 1 or data_src == 2:
            self.data_src = data_src
        else:
            raise BRLCADException("Invalid Data")
        if self.data_src == 1:
            if not os.path.isfile(dsp_name):
                raise ValueError("File {} does not exist !".format(dsp_name))

        self.dsp_name = dsp_name
        self.width = width
        self.length = length
        self.interpolation = interpolation
        self.cell_size = cell_size
        self.unit_elevation = unit_elevation
        if isinstance(cut_direction, str):
            if cut_direction[0] == "a" or cut_direction[0] == "A":
                self.cut_direction = 1
            elif cut_direction == "llUR" or cut_direction == "l":
                self.cut_direction = 2
            elif cut_direction == "ULlr" or cut_direction == "L":
                self.cut_direction = 3
            else:
                raise BRLCADException("Invalid Data")
        elif cut_direction in range(1, 4):
            self.cut_direction = cut_direction
        else:
            raise BRLCADException("Invalid Data")


    def __repr__(self):
        result = "{}({}, dsp_name={}, data_src={}, width={}, length={}, interpolation={}, cut_direction={}, " \
                 "cell_size={}, unit_elevation={}"
        return result.format(
            self.__class__.__name__, self.name, self.dsp_name, self.get_data_src(), self.width, self.length,
            self.interpolation, self.get_cut_direction(), self.cell_size, self.unit_elevation
        )

    def get_cut_direction(self):
        if self.cut_direction == 1:
            return "Adaptive"
        elif self.cut_direction == 2:
            return "Lower Left Upper Right"
        elif self.cut_direction == 3:
            return "Upper Left Lower Right"
        else:
            return "Unknown"

    def get_data_src(self):
        if self.data_src == 1:
            return "File"
        elif self.data_src == 2:
            return "Object"
        else:
            return "Unknown"

    def update_params(self, params):
        params.update({
            "dsp_name": self.dsp_name,
            "data_src": self.data_src,
            "width": self.width,
            "length": self.length,
            "interpolation": self.interpolation,
            "cut_direction": self.cut_direction,
            "cell_size": self.cell_size,
            "unit_elevation": self.unit_elevation
        })

    def copy(self):
        return DSP(self.name, self.dsp_name, self.data_src, self.width, self.length, self.interpolation,
                   self.cut_direction, self.cell_size, self.unit_elevation, copy=True)

    def has_same_data(self, other):
        return self.dsp_name == other.dsp_name and \
               self.data_src == other.data_src and \
               self.width == other.width and  \
               self.length == other.length and \
               self.interpolation == other.interpolation and \
               self.cut_direction == other.cut_direction and \
               self.cell_size == other.cell_size and \
               self.unit_elevation == other.unit_elevation


    @staticmethod
    def from_wdb(name, data):
        if data.dsp_smooth == 1:
            interpolation = True
        else:
            interpolation = False
        if data.dsp_cuttype == 97:
            dsp_cuttype = 1
        if data.dsp_cuttype == 154:
            dsp_cuttype = 2
        if data.dsp_cuttype == 114:
            dsp_cuttype = 3
        return DSP(
            name=name,
            dsp_name= data.dsp_name.vls_str.data,
            data_src= data.dsp_datasrc,
            width=data.dsp_xcnt,
            length=data.dsp_ycnt,
            interpolation=interpolation,
            cut_direction=dsp_cuttype,
            cell_size=data.dsp_stom[5],
            unit_elevation=data.dsp_stom[10]
        )