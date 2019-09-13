import vtk
import numpy as np
from fury import actor, window, ui
from fury.utils import numpy_to_vtk_points, set_polydata_colors
from fury.utils import set_input, rotate, set_polydata_vertices
from fury.utils import get_actor_from_polydata, set_polydata_triangles


def rectangle(size = (1, 1)):

    X, Y = size

    # Setup four points
    points = vtk.vtkPoints()
    points.InsertNextPoint(-X/2, -Y/2, 0)
    points.InsertNextPoint(-X/2, Y/2, 0)
    points.InsertNextPoint(X/2, Y/2, 0)
    points.InsertNextPoint(X/2, -Y/2, 0)

    # Create the polygon
    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(4)  # make a quad
    polygon.GetPointIds().SetId(0, 0)
    polygon.GetPointIds().SetId(1, 1)
    polygon.GetPointIds().SetId(2, 2)
    polygon.GetPointIds().SetId(3, 3)

    # Add the polygon to a list of polygons
    polygons = vtk.vtkCellArray()
    polygons.InsertNextCell(polygon)

    # Create a PolyData
    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetPolys(polygons)

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    mapper = set_input(mapper, polygonPolyData)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    return actor

def square(scale=1):
    my_polydata = vtk.vtkPolyData()

    my_vertices = np.array([[0.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [1.0, 1.0, 0.0],
                            [1.0, 0.0, 0.0]])

    my_vertices -= np.array([0.5, 0.5, 0])

    my_vertices = scale * my_vertices

    my_triangles = np.array([[0, 1, 2],
                             [2, 3, 0]], dtype='i8')

    set_polydata_vertices(my_polydata, my_vertices)
    set_polydata_triangles(my_polydata, my_triangles)

    vertex_filter = vtk.vtkVertexGlyphFilter()
    vertex_filter.SetInputData(my_polydata)
    vertex_filter.Update()

    polydata = vtk.vtkPolyData()
    polydata.ShallowCopy(vertex_filter.GetOutput())

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    square_actor = vtk.vtkActor()
    square_actor.SetMapper(mapper)
    square_actor.GetProperty().SetPointSize(200)
    #square_actor.GetProperty().SetRenderPointsAsSpheres(True)

    return square_actor


def cube():
    my_polydata = vtk.vtkPolyData()

    my_vertices = np.array([[0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 1.0, 1.0],
                            [1.0, 0.0, 0.0],
                            [1.0, 0.0, 1.0],
                            [1.0, 1.0, 0.0],
                            [1.0, 1.0, 1.0]])

    my_vertices -= 0.5

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

    set_polydata_vertices(my_polydata, my_vertices)
    set_polydata_triangles(my_polydata, my_triangles)
    return get_actor_from_polydata(my_polydata)


def disk():

    np.random.seed(42)
    n_points = 1
    centers = np.random.rand(n_points, 3)
    colors = 255 * np.random.rand(n_points, 3)

    vtk_points = numpy_to_vtk_points(centers)

    points_polydata = vtk.vtkPolyData()
    points_polydata.SetPoints(vtk_points)

    vertex_filter = vtk.vtkVertexGlyphFilter()
    vertex_filter.SetInputData(points_polydata)
    vertex_filter.Update()

    polydata = vtk.vtkPolyData()
    polydata.ShallowCopy(vertex_filter.GetOutput())

    # set_polydata_colors(polydata, colors)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(polydata)

    points_actor = vtk.vtkActor()
    points_actor.SetMapper(mapper)
    points_actor.GetProperty().SetPointSize(1000)
    points_actor.GetProperty().SetRenderPointsAsSpheres(True)

    return points_actor

scene = window.Scene()
scene.add(actor.axes())
# scene.background((1, 1, 1))
showm = window.ShowManager(scene, size=(1920, 1080), order_transparent=True, interactor_style='custom')

obj = 'square'

if obj == 'square':

    sq = square()
    scene.add(sq)
    mapper = sq.GetMapper()

if obj == 'rectangle':

    rec = rectangle(size=(100, 100))
    scene.add(rec)
    mapper = rec.GetMapper()

if obj == 'cube':

    # rec.SetPosition(100, 0, 0)
    cu = cube()
    scene.add(cu)
    scene.background((1, 1, 1))
    # window.show(scene)
    mapper = cu.GetMapper()

if obj == 'disk':

    dis = disk()
    scene.add(dis)
    mapper = dis.GetMapper()



# mapper.AddShaderReplacement(
#     vtk.vtkShader.Vertex,
#     '//VTK::PositionVC::Dec',  # target the PositionVC block
#     True,
#     '''
#     // include the default
#     //VTK::PositionVC::Dec
#     // now declare our attribute
#     // in vec3 dummyAttribute;
#     ''',
#     False
# )

# mapper.AddShaderReplacement(
#     vtk.vtkShader.Vertex,
#     '//VTK::PositionVC::Impl',  # target the PositionVC block
#     True,
#     '''
#     // replace the default
#     // copy position in model coordinates
#     vec4 myVertexMC = vertexMC;
#     // modify coordinates with dummyAttribute
#     // just for fun, 'swizzle' the parameters
#     // subtract 0.5 so it stays centered
#     myVertexMC.xyz = vertexMC.xyz; // + (dummyAttribute.yzx - 0.5);
#     // this is used for lighting in the frag shader
#     // need to calculate and include since we replaced the default
#     vertexVCVSOutput = MCVCMatrix * myVertexMC;
#     // transform from model to display coordinates
#     gl_Position = MCDCMatrix * myVertexMC;
#     ''',
#     False
# )



mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Light::Dec',
    True,
    '''
    //VTK::Light::Dec
    uniform float time;
    ''',
    False
)

import itertools
counter = itertools.count(start=1)

global timer

timer = 0

def timer_callback(obj, event):

    global timer
    timer += 1.0
    # print(timer)
    showm.render()
    scene.set_camera(focal_point=(0,0,0))
    scene.azimuth(10)


@window.vtk.calldata_type(window.vtk.VTK_OBJECT)
def vtk_shader_callback(caller, event, calldata=None):
    program = calldata
    global timer
    if program is not None:
        try:
            program.SetUniformf("time", timer)
        except ValueError:
            pass


mapper.AddObserver(window.vtk.vtkCommand.UpdateShaderEvent, vtk_shader_callback)


mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Light::Impl',
    True,
    '''
    //VTK::Light::Impl
    vec3 rColor = vec3(.9, .0, .3);
    vec3 gColor = vec3(.0, .9, .3);
    vec3 bColor = vec3(.0, .3, .9);
    vec3 yColor = vec3(.9, .9, .3);

    float tm = .2; // speed
    float vcm = 5;

    float a = sin(gl_FragCoord.y * 0.01 * vcm - time * tm) / 2.;
    float b = cos(gl_FragCoord.y * 0.01 * vcm - time * tm) / 2.;
    float c = sin(gl_FragCoord.y * 0.01 * vcm - time * tm + 3.14) / 2.;
    float d = cos(gl_FragCoord.y * 0.01 * vcm - time * tm + 3.14) / 2.;

    float div = 0.01; // default 0.01

    float e = div / abs(gl_FragCoord.x * 0.01 + a);
    float f = div / abs(gl_FragCoord.x * 0.01 + b);
    float g = div / abs(gl_FragCoord.x * 0.01 + c);
    float h = div / abs(gl_FragCoord.x * 0.01 + d);

    vec3 destColor = rColor * e + gColor * f + bColor * g + yColor * h;
    fragOutput0 = vec4(destColor, 1.);
    //fragOutput0 = vec4(1 - normalVCVSOutput.x, 1 - normalVCVSOutput.y, 0, 1.);
    //fragOutput0 = vec4(normalVCVSOutput.x, 0, 0, 1.);
    //fragOutput0 = vec4(normalVCVSOutput.x, normalVCVSOutput.y, 0, 1.);
    fragOutput0 = vec4(gl_FragCoord.x, 0, 0, 1.);
    ''',
    False
)


# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Light::Impl',
#     True,
#     '''
#     //VTK::Light::Impl
#     vec3 rColor = vec3(.9, .0, .3);
#     vec3 gColor = vec3(.0, .9, .3);
#     vec3 bColor = vec3(.0, .3, .9);
#     vec3 yColor = vec3(.9, .9, .3);

#     float tm = .2; // speed
#     float vcm = 5;

#     float a = sin(normalVCVSOutput.y * vcm - time * tm) / 2.;
#     float b = cos(normalVCVSOutput.y * vcm - time * tm) / 2.;
#     float c = sin(normalVCVSOutput.y * vcm - time * tm + 3.14) / 2.;
#     float d = cos(normalVCVSOutput.y * vcm - time * tm + 3.14) / 2.;

#     float div = 0.01; // default 0.01

#     float e = div / abs(normalVCVSOutput.x + a);
#     float f = div / abs(normalVCVSOutput.x + b);
#     float g = div / abs(normalVCVSOutput.x + c);
#     float h = div / abs(normalVCVSOutput.x + d);

#     vec3 destColor = rColor * e + gColor * f + bColor * g + yColor * h;
#     fragOutput0 = vec4(destColor, 1.);
#     //fragOutput0 = vec4(1 - normalVCVSOutput.x, 1 - normalVCVSOutput.y, 0, 1.);
#     //fragOutput0 = vec4(normalVCVSOutput.x, 0, 0, 1.);
#     //fragOutput0 = vec4(normalVCVSOutput.x, normalVCVSOutput.y, 0, 1.);
#     ''',
#     False
# )

showm.initialize()
showm.add_timer_callback(True, 100, timer_callback)

showm.initialize()
showm.start()