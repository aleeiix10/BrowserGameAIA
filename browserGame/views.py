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


from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


def enviar_email(request):
    template = render_to_string('browserGame/email_template.html', {'user': 'Andres'})

    email = EmailMessage(
        'Bienvenido a BrowserGame',
        template,
        settings.EMAIL_HOST_USER,
        ['evillcatunari.cf@iesesteveterradas.cat']
    )

    email.fail_silently = False
    email.send()  

    return  render(request, 'browserGame/email_sent.html')