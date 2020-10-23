from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse


# Create your views here.


#
def send_email(request):
    try:
        #email, event, authentication
        if request.method == 'POST':
            #initialize
            email = request.POST['emal_address']
            event = request.POST['event_address']
            authentication = request.POST['authentication']
            #Sending the mail
            send_mail('Nettverksdagene - Påmelding til ' + event,
            'Vennligst verifiser din påmelding ved å klikke på denne linken: ' + authentication,
            'it@nettverksdagene.no',
            [email],
            fail_silently=False)
            html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head>  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>  <title>E-mail</title>  <style></style>  <script></script></head><body>Vennligst sjekk søppelfilteret</body></html>'
            return HttpResponse(html)
    except:
        print("ERROR: Konfigurer email-settings i mail_settings.py")
        raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')

