

def standard(actor, ambient_level=0.7,
             diffuse_level=0.8,
             specular_level=0.5,
             specular_power=10,
             opacity=1.,
             interpolation='phong'):

    acprop = actor.GetProperty()
    acprop.SetSpecular(specular_level)
    acprop.SetDiffuse(diffuse_level)
    acprop.SetAmbient(ambient_level)
    acprop.SetSpecularPower(specular_power)

    if interpolation.lower() == 'phong':
        acprop.SetInterpolationToPhong()
    acprop.SetOpacity(opacity)

    return acprop

