"""
==================
Visualize surfaces
==================
Test
"""

import numpy as np


from fury import window

# Conditional import machinery for vtk
# Allow import, but disable doctests if we don't have vtk
import vtk


reader = vtk.vtkPolyDataReader()

dname = '/home/elef/Data/brain_surface_hcp/'

fname = dname + '100307_white_lh.vtk'

print(fname)

reader.SetFileName(fname)


subdivider = vtk.vtkLoopSubdivisionFilter()
subdivider.SetNumberOfSubdivisions(2)
subdivider.SetInputConnection(reader.GetOutputPort())


mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(subdivider.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().BackfaceCullingOn()
# actor.SetScale(0.08, 0.08, 0.08)
actor.GetProperty().SetColor(1, 0.5, 0)




# geom_shader_file = open("fury/shaders/line.geom", "r")
# geom_shader_code = geom_shader_file.read()

# poly_mapper.SetGeometryShaderCode(geom_shader_code)

# @vtk.calldata_type(vtk.VTK_OBJECT)
# def vtkShaderCallback(caller, event, calldata=None):
#     program = calldata
#     if program is not None:
#         program.SetUniformf("linewidth", linewidth)

# poly_mapper.AddObserver(vtk.vtkCommand.UpdateShaderEvent,
#                         vtkShaderCallback)

mapper.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    if (df > 0.50) discard;
    //    fragOutput0 = vec4(1, 1, 1, 1);
    ''',
    False
)

# debug block
# mapper.AddShaderReplacement(
#     vtk.vtkShader.Fragment,
#     '//VTK::Coincident::Impl',
#     True,
#     '''
#     //VTK::Coincident::Impl
#     foo = abs(bar);
#     ''',
#     False
# )



# renderer and scene
scene = window.Scene()
scene.background((1, 1, 1))
scene.add(actor)
# renderer.set_camera(position=(10, 5, 7), focal_point=(0.5, 0.5, 0.5))
# renderer.zoom(3)

# display
window.show(scene, size=(600, 600), reset_camera=False)
# window.record(renderer, out_path='cube.png', size=(600, 600))