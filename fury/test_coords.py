import numpy as np
import numpy.testing as npt
from fury.utils import vtk, rotate
from fury import window, utils, actor
from fury.convert import set_polydata_texture_coords


def test_polydata_texture_coords2(interactive=False):
    # Create a cube
    my_triangles = np.array([[0, 6, 4],
                             [0, 2, 6],
                             [0, 3, 2],
                             [0, 1, 3],
                             [2, 7, 6],
                             [2, 3, 7],
                             [4, 6, 7],
                             [4, 7, 5],
                             [0, 4, 5],
                             [0, 5, 1],
                             [1, 5, 7],
                             [1, 7, 3]], dtype='i8')
    my_vertices = np.array([[0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 1.0, 1.0],
                            [1.0, 0.0, 0.0],
                            [1.0, 0.0, 1.0],
                            [1.0, 1.0, 0.0],
                            [1.0, 1.0, 1.0]])

    colors = my_vertices * 255
    my_polydata = vtk.vtkPolyData()

    utils.set_polydata_vertices(my_polydata, my_vertices)
    utils.set_polydata_triangles(my_polydata, my_triangles)



def _square(scale=1):
    polydata = vtk.vtkPolyData()

    vertices = np.array([[0.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [1.0, 1.0, 0.0],
                         [1.0, 0.0, 0.0]])

    vertices -= np.array([0.5, 0.5, 0])

    vertices = scale * vertices

    triangles = np.array([[0, 1, 2], [2, 3, 0]], dtype='i8')

    utils.set_polydata_vertices(polydata, vertices)
    utils.set_polydata_triangles(polydata, triangles)
    return polydata


def test_polydata_texture_coords(interactive=False):
    # utils.set_polydata_colors(my_polydata, colors)
    # utils.update_polydata_normals(my_polydata)
    # normals = utils.get_polydata_normals(my_polydata)
    # npt.assert_equal(len(normals), len(my_vertices))

    https://vtk.org/Wiki/VTK/Examples/Cxx/Visualization/TextureMapQuad

    my_polydata = _square()

    rgb = (255 * np.ones((40, 40, 3))).astype('uint8')
    rgb[:, :, 0] = 0
    tex_actor = actor.texture(rgb)

    tcoords = np.array([[0., 0., 0.],
                        [1., 0., 0.],
                        [1., 1., 0.],
                        [0., 2., 0.]], dtype='f4')

    print(tcoords.shape)
    print(tcoords.dtype)
    print(tcoords)
    # print(rgb[:10])

    set_polydata_texture_coords(my_polydata, tcoords)
    pd_actor = utils.get_actor_from_polydata(my_polydata)

    target_texture = tex_actor.GetTexture()
    # target_texture.CubeMapOn()
    # target_texture.PremultipliedAlphaOn()
    # target_texture.UseSRGBColorSpaceOn()
    # target_texture.MipmapOn()
    pd_actor.SetTexture(target_texture)

    pd_actor.GetMapper().SetInputData(my_polydata)
    pd_actor.GetMapper().Update()
    pd_actor.GetProperty().BackfaceCullingOff()
    # pd_actor.GetProperty().FrontfaceCullingOn()
    print(target_texture)

    scene = window.Scene()
    scene.add(pd_actor)
    #scene.add(tex_actor)

    if interactive:
        window.show(scene)
    arr = window.snapshot(scene)

    report = window.analyze_snapshot(arr)
    npt.assert_equal(report.objects, 1)


if __name__ == '__main__':
    # npt.run_module_suite()
    test_polydata_texture_coords(True)
