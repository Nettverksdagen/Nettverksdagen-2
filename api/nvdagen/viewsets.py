from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant, Program
from .serializers import ListingSerializer, BusinessSerializer, SponsorSerializer, TeamMemberSerializer, FormSerializer, ParticipantSerializer, ProgramSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        data = {'year': request.data.get('year'), 'study': request.data.get('study'), 'email': request.data.get('email'), 'name': request.data.get('name'), 'event': request.data.get('event'), 'code': request.data.get('code')}
        ParticipantValidationList = Participant.objects.filter(email=data['email'], event=data['event'])
        ProgramToBeAdded = Program.objects.filter(id=data['event'])[0]

        #Validates that a new Participant can enter the event
        if (len(ParticipantValidationList) == 0):
            #Using the default django-create function
            super().create(request)

            #Updating the registrationlist on event
            ProgramToBeAdded.registered += 1
            ProgramToBeAdded.save()

            try:
                # If program is full, send waiting list email
                if (ProgramToBeAdded.registered > ProgramToBeAdded.maxRegistered):
                    waitingListIndex = ProgramToBeAdded.registered - ProgramToBeAdded.maxRegistered

                    #Sending the mail
                    send_mail('Nettverksdagene - Du står på venteliste',
                    'Vi bekrefter herved at du står på venteliste til ' + ProgramToBeAdded.header + '. Din plass på ventelisten er ' + str(waitingListIndex) + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data.get('email')],
                    fail_silently=False)

                    #returning a response
                    response = {'message': 'It works!!'}
                    return Response(response, status = status.HTTP_200_OK)
                # If program not full, send confirmation email
                else:
                    #Sending the mail
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data.get('name'),
                    'Vi bekrefter herved at du er påmeldt ' + ProgramToBeAdded.header + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data.get('email')],
                    fail_silently=False)

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

    def retrieve(self, request, pk):
        participant = Participant.objects.get(id=pk)
        program_id = participant.event
        program = Program.objects.get(id=program_id)

        try:
            send_mail('Nettverksdagene - Avmeldingskode for ' + participant.name,
                'Din avmeldingskode for ' + program.header + ' er: ' + participant.code + '. Tusen takk for din interesse i Nettverksdagene!',
                'do-not-reply@nettverksdagene.no',
                [participant.email],
                fail_silently=False)
            #returning a response
            response = {'message': 'It works!!'}
            return Response(response, status = status.HTTP_200_OK)
        except:
            #An error to be raised if the send_mail function doesn't work
            print("ERROR: Konfigurer email-settings i mail_settings.py")
            raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')

    def destroy(self, request, pk):
        
        participant = Participant.objects.get(id=pk)
        program_id = participant.event

        response = super().destroy(request)

        if status.is_success(response.status_code):
            program = Program.objects.get(id=program_id)
            program.registered -= 1
            program.save()

            if program.registered >= program.maxRegistered:
                new_participant = Participant.objects.order_by('id')[program.maxRegistered-1]
                try:
                    #Sending the mail
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + new_participant.name,
                    'Du sto på ventelisten for ' + program.header + ', og har nå fått plass. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [new_participant.email],
                    fail_silently=False)

                    #returning a response
                    response = {'message': 'It works!!'}
                    return Response(response, status = status.HTTP_200_OK)
                except:
                    #An error to be raised if the send_mail function doesn't work
                    print("ERROR: Konfigurer email-settings i mail_settings.py")
                    raise Exception('ERROR: Konfigurer email-settings i mail_settings.py')
        else:
            raise Exception(f'ERROR: DELETE request returned {response.status_code}.')
        
        return response
