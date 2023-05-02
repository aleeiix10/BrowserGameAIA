from .utils import *

def cronDecorator(function):
    def wrapper(request, *args, **kwargs):
        response = function(request, *args, **kwargs)
        # Ejecutar la función después de que se carga la vista
        cronManaU()
        return response
    return wrapper