import vtk


def light(focal_point=(0, 0, 0.), position=(10, 10, 0.),
          color=(255, 214, 170), intensity=0.8,
          attenuation=0.8):
    light = vtk.vtkLight()
    light.SetFocalPoint(focal_point)
    light.SetPosition(position)
    light.SetColor(color)
    #light.SetAmbientColor(255, 0, 0)
    light.SetIntensity(intensity)
    light.SetShadowAttenuation(attenuation)
    light.SetLightTypeToSceneLight()
    light.PositionalOn()
    light.SwitchOn()

    return light
