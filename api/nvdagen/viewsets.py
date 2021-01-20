from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant, Program
from .serializers import ListingSerializer, BusinessSerializer, SponsorSerializer, TeamMemberSerializer, FormSerializer, ParticipantSerializer, ProgramSerializer
from django.core.mail import send_mail

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer


class FormViewSet(viewsets.ModelViewSet):
    serializer_class = FormSerializer
    queryset = Form.objects.all()

class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    queryset = Program.objects.all()

    
class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = (AllowAny,)


    def create(self, request):
        data = {'email': request.data.get('email'), 'name': request.data.get('name')}
        # queryset = Participant.objects.all()
        # print(queryset.filter(email))
        # if(not queryset.filter(email=data['email']).exists()):
        try:
            #email, event, authentication
            #if request.method == 'POST':
            #initialize

            #Sending the mail
            send_mail('Nettverksdagene - Påmelding til ' + data.get('name'),
            'Vennligst verifiser din påmelding ved å klikke på denne linken: ',
            'it@nettverksdagene.no',
            [data.get('email')],
            fail_silently=False)
            #html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"><html><head>  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>  <title>E-mail</title>  <style></style>  <script></script></head><body>Vennligst sjekk søppelfilteret</body></html>'
            response = {'message': 'It works!!'}
            return Response(response, status = status.HTTP_200_OK)
        except:
            print("ERROR: Konfigurer email-settings i mail_settings.py")
            raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')

        return super().create(request)
        # else:
        #     print("NONONONONONONONO!")
        #     return

    # @action(detail=True)
    # def post(self, request):
    #     print("HALLOOO!!!")
    #     serializer_class.send_email(request)
