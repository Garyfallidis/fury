import numpy as np
import os
from fury.io import load_image
from tempfile import TemporaryDirectory
from vtk.util import numpy_support


def matplotlib_figure_to_numpy(fig, dpi=100, fname=None, flip_up_down=True,
                               transparent=False):
    r""" Convert a Matplotlib figure to a 3D numpy array with RGBA channels
    Parameters
    ----------
    fig : obj,
        A matplotlib figure object
    dpi : int
        Dots per inch
    fname : str
        If ``fname`` is given then the array will be saved as a png to this
        position.
    flip_up_down : bool
        The origin is different from matlplotlib default and VTK's default
        behaviour (default True).
    transparent : bool
        Make background transparent (default False).
    Returns
    -------
    arr : ndarray
        a numpy 3D array of RGBA values
    Notes
    ------
    The safest way to read the pixel values from the figure was to save them
    using savefig as a png and then read again the png. There is a cleaner
    way found here http://www.icare.univ-lille1.fr/drupal/node/1141 where
    you can actually use fig.canvas.tostring_argb() to get the values directly
    without saving to the disk. However, this was not stable across different
    machines and needed more investigation from what time permited.
    """
    if fname is None:
        with TemporaryDirectory() as tmpdir:
            fname = os.path.join(tmpdir, 'tmp.png')
            fig.savefig(fname, dpi=dpi, transparent=transparent,
                        bbox_inches='tight', pad_inches=0)
            arr = load_image(fname, use_imageio=True)
    else:
        fig.savefig(fname, dpi=dpi, transparent=transparent,
                    bbox_inches='tight', pad_inches=0)
        arr = load_image(fname, use_imageio=True)

    if flip_up_down:
        arr = np.flipud(arr)
    return arr


def set_polydata_texture_coords(polydata, tex_coords):
    """Set polydata normals with a numpy array (ndarrays Nx3 int).

    Parameters
    ----------
    polydata : vtkPolyData
    tex_coords : tex_coords, represented as 2D ndarrays (Nx3) (one per vertex)
    """

    vtk_tcoords = numpy_support.numpy_to_vtk(tex_coords, deep=True)
    polydata.GetPointData().SetTCoords(vtk_tcoords)
    return polydata
