from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def pagina_inicio(request):
    if request.user.is_authenticated:
        return render(request, 'browserGame/index_protected.html')
    else:
        return render(request, 'browserGame/index.html')
         
@login_required
def profile(request):
    return render(request,"browserGame/profile.html")

