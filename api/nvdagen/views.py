from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


#
def send_email(email, event, authentication):
    try:
        send_mail('Nettverksdagene - Påmelding til ' + event,
        'Vennligst verifiser din påmelding ved å klikke på denne linken: ' + authentication,
        'it@nettverksdagene.no',
        [email],
        fail_silently=False)
    except:
        print("ERROR: Konfigurer email-settings i mail_settings.py")
        raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')

