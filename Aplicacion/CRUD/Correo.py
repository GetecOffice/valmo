from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

def send_email(mail):
    context  = {'mail': mail}
    template  = get_template('Configuracion/Correos/correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Un Correo de prueba',
        'Hola mundo',
        settings.EMAIL_HOST_USER,
        [mail]
        
    )

    email.attach_alternative(content, 'text/html')
    email.send()

def index(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        send_email(mail)
    return render(request, "Configuracion/Correos/index.html")