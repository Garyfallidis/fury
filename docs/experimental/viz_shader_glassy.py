"""
==================
Visualize surfaces
==================
Test
"""

import numpy as np


from fury import window, actor

# Conditional import machinery for vtk
# Allow import, but disable doctests if we don't have vtk
import vtk


reader = vtk.vtkPolyDataReader()

dname = '/home/elef/Data/brain_surface_hcp/'
dname = 'C:\\Users\\elef\\Data\\'


fname = dname + '100307_white_lh.vtk'

print(fname)

reader.SetFileName(fname)


subdivider = vtk.vtkLoopSubdivisionFilter()
subdivider.SetNumberOfSubdivisions(1)
subdivider.SetInputConnection(reader.GetOutputPort())


mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(subdivider.GetOutputPort())

centers = np.array([[0, 0, 0]])
directions = np.array([[0, 1, 0]])
colors = np.array([[1, 1., 1]])


surface_actor = vtk.vtkActor()
surface_actor.SetMapper(mapper)
surface_actor.GetProperty().BackfaceCullingOn()
# surface_actor.GetProperty().SetOpacity(0.3)
# actor.SetScale(0.08, 0.08, 0.08)
# actor.GetProperty().SetColor(1, 0.5, 0)


box_actor = actor.box(centers, directions, colors, size=(40, 0.1, 2.5),
                      heights=np.array([20.]))

box_actor.SetPosition(0, -200, 0)

box_material = box_actor.GetProperty()

#box_material.SetColor(0.4, .4, .4)
box_material.SetColor(0.4, 0.4, 0.6)

# box_material.SetColor(1., 0.73, 0.82)
box_material.SetAmbient(.3)
box_material.SetDiffuse(0.3)
box_material.SetSpecular(.5)
box_material.SetSpecularPower(1.0)
#vbox_material.ShadingOn()


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
    if (df > 1) discard;

    //fragOutput0 = vec4(1, 1, 1, 1);
    //fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    ''',
    False
)


surface_material = surface_actor.GetProperty()
surface_material.SetAmbientColor(1, 0.2, 0)
surface_material.SetDiffuseColor(1, 0.6, 0)
surface_material.SetSpecularColor(1, 0.9, 0)


surface_material.SetAmbient(0.2)
surface_material.SetDiffuse(0.3)
surface_material.SetSpecular(1.0)
surface_material.SetSpecularPower(5.0)
surface_material.ShadingOn()

surface_material.SetInterpolationToPhong()

# surface_material.SetInterpolationToGouraud()
# surface_material.SetInterpolationToPhong()
# surface_material.SetRepresentationToWireframe()

###########################################################

mapper2 = vtk.vtkPolyDataMapper()
mapper2.SetInputConnection(subdivider.GetOutputPort())

mapper2.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    if (df <.8) discard;

    //fragOutput0 = vec4(1, 1, 1, 1);
    //fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    ''',
    False
)


surface_actor2 = vtk.vtkActor()
surface_actor2.SetMapper(mapper2)
surface_actor2.GetProperty().BackfaceCullingOn()

surface_actor2.SetPosition(0, -200, 0)

surface_material2 = surface_actor2.GetProperty()
surface_material2.SetAmbientColor(1, 0.2, 0)
surface_material2.SetDiffuseColor(1, 0.6, 0)
surface_material2.SetSpecularColor(1, 0.9, 0)


surface_material2.SetAmbient(0.2)
surface_material2.SetDiffuse(0.3)
surface_material2.SetSpecular(1.0)
surface_material2.SetSpecularPower(5.0)
surface_material2.ShadingOn()

surface_material2.SetInterpolationToPhong()


###########################################################

mapper3 = vtk.vtkPolyDataMapper()
mapper3.SetInputConnection(subdivider.GetOutputPort())

mapper3.AddShaderReplacement(
    vtk.vtkShader.Fragment,
    '//VTK::Coincident::Impl',
    True,
    '''
    //VTK::Coincident::Impl
    if (df > .3) discard;

    //fragOutput0 = vec4(1, 1, 1, 1);
    //fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    fragOutput0 = vec4(ambientColor + diffuse + specular, opacity);
    ''',
    False
)


surface_actor3 = vtk.vtkActor()
surface_actor3.SetMapper(mapper3)
surface_actor3.GetProperty().BackfaceCullingOn()

surface_actor3.SetPosition(0, -400, 0)

surface_material3 = surface_actor3.GetProperty()
surface_material3.SetAmbientColor(1, 0.2, 0)
surface_material3.SetDiffuseColor(1, 0.6, 0)
surface_material3.SetSpecularColor(1, 0.9, 0)


surface_material3.SetAmbient(0.2)
surface_material3.SetDiffuse(0.3)
surface_material3.SetSpecular(1.0)
surface_material3.SetSpecularPower(5.0)
surface_material3.ShadingOn()

surface_material3.SetInterpolationToPhong()



light = vtk.vtkLight()
light.SetColor(1.0, 0.0, 0.0)
light.SetPosition(-100, 0, 0)
light.SetFocalPoint(0, 0, 0)

light2 = vtk.vtkLight()
light2.SetColor(1.0, 1.0, 0.0)
light2.SetPosition(0, 100, 0)
light2.SetFocalPoint(0, 0, 0)

# renderer and scene
scene = window.Scene()
#scene.projection('parallel')
scene.background((1, 1, 1))
scene.add(surface_actor)
scene.add(surface_actor2)
scene.add(surface_actor3)
# scene.add(actor.axes(scale=(100, 100, 100)))
scene.add(box_actor)
# renderer.set_camera(position=(10, 5, 7), focal_point=(0.5, 0.5, 0.5))
# renderer.zoom(3)


#scene.AddLight(light)
#scene.AddLight(light2)


# display
window.show(scene, size=(1200, 1200), order_transparent=True,
            reset_camera=True)
# window.record(renderer, out_path='cube.png', size=(600, 600))