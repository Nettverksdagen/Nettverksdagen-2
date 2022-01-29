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
        data = request.data
        notRegistered = Participant.objects.filter(email=data['email'], event=data['event']).count() == 0
        program = Program.objects.get(id=data['event'])

        #Validates that a new Participant can enter the event
        if (notRegistered):
            #Using the default django-create function
            super().create(request)

            #Updating the registrationlist on event
            program.registered += 1
            program.save()

            try:
                # If program is full, send waiting list email
                if (program.registered > program.maxRegistered):
                    waitingListIndex = program.registered - program.maxRegistered

                    #Sending the mail
                    send_mail('Nettverksdagene - Du står på venteliste',
                    'Vi bekrefter herved at du står på venteliste til ' + program.header + '. Din plass på ventelisten er ' + str(waitingListIndex) + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data['email']],
                    fail_silently=False)

                    #returning a response
                    response = {'message': 'It works!!'}
                    return Response(response, status = status.HTTP_200_OK)
                # If program not full, send confirmation email
                else:
                    #Sending the mail
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data['name'],
                    'Vi bekrefter herved at du er påmeldt ' + program.header + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data['email']],
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
        program = Program.objects.get(id=participant.event)

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

        response = super().destroy(request)

        if status.is_success(response.status_code):
            program = Program.objects.get(id=participant.event)
            program.registered -= 1
            program.save()

            if program.registered >= program.maxRegistered: # If last participant exists
                lastParticipant = Participant.objects.order_by('id')[program.maxRegistered-1]
                if participant.id < lastParticipant.id: # If lastParticipant is new
                    try:
                        #Sending the mail
                        send_mail('Nettverksdagene - Påmelding bekreftet for ' + lastParticipant.name,
                        'Du sto på ventelisten for ' + program.header + ', og har nå fått plass. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                        'do-not-reply@nettverksdagene.no',
                        [lastParticipant.email],
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
