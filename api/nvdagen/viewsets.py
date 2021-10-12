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
        #Data to be used
        data = {'year': request.data.get('year'), 'study': request.data.get('study'), 'email': request.data.get('email'), 'name': request.data.get('name'), 'event': request.data.get('event')}
        ParticipantValidationList = Participant.objects.filter(email=data['email'], event=data['event'])
        ProgramToBeAdded = Program.objects.filter(id=data['event'])[0]

        #Validates that a new Participant can enter the event
        if((len(ParticipantValidationList) == 0) and (ProgramToBeAdded.registered < ProgramToBeAdded.maxRegistered)):
            try:
                #Sending the mail
                send_mail('Nettverksdagene - Påmelding bekreftet for ' + data.get('name'),
                'Vi bekrefter herved at du er påmeldt. Dersom du skulle ønske å melde deg av igjen, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                'do-not-reply@nettverksdagene.no',
                [data.get('email')],
                fail_silently=False)

                #Using the default django-create function
                super().create(request)

                #Updating the registrationlist on event
                ProgramToBeAdded.registered += 1
                ProgramToBeAdded.save()

                #returning a response
                response = {'message': 'It works!!'}
                return Response(response, status = status.HTTP_200_OK)
            except:
                #An error to be raised if the send_mail function doesn't work
                print("ERROR: Konfigurer email-settings i mail_settings.py")
                raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')


        else:
            #returning a response
            response = {'message': 'Invalid input, check Participant list. Should not be duplicated'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)
