from django.shortcuts import render
from django.core.mail import send_mail

# Create your views here.


#
def send_email(email, relevant_arrangement):
    try:
        #authentication = authentication_email()
        send_mail('Nettverksdagene - Påmelding til ' + relevant_arrangement,
        'Vennligst verifiser din påmelding ved å klikke på denne linken: ' + authentication,
        'it@nettverksdagene.no',
        [email],
        fail_silently=False)
    except:
        print("MÅ STÅ NOE VETTUGT HER")

    # return render(request, '')

def authentication_email():
    #Henter random streng som er generert i frontend
    #returnerer den genererte strengen