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

        if (notRegistered):
            currentlyRegistered = program.participant_set.all().count()
            try:
                # If program is full, send waiting list email
                if (currentlyRegistered >= program.maxRegistered):
                    waitingListIndex = currentlyRegistered - program.maxRegistered + 1
                    send_mail('Nettverksdagene - Du står på venteliste',
                    'Vi bekrefter herved at du står på venteliste til ' + program.header + '. Din plass på ventelisten er ' + str(waitingListIndex) + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data['email']],
                    fail_silently=False)
                # If program not full, send confirmation email
                else:
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data['name'],
                    'Vi bekrefter herved at du er påmeldt ' + program.header + '. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                    'do-not-reply@nettverksdagene.no',
                    [data['email']],
                    fail_silently=False)
            except:
                print("ERROR: Could not send email. Is mail_settings.py correct?")
                response = {'message': 'Could not send email'}
                return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)                

            return super().create(request)

        else:
            response = {'message': 'Invalid input. Is participant already registered?'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        participant = Participant.objects.get(id=pk)
        program = participant.event

        try:
            send_mail('Nettverksdagene - Avmeldingskode for ' + participant.name,
                'Din avmeldingskode for ' + program.header + ' er: ' + participant.code + '. Tusen takk for din interesse i Nettverksdagene!',
                'do-not-reply@nettverksdagene.no',
                [participant.email],
                fail_silently=False)
        except:
            print("ERROR: Could not send email. Is mail_settings.py correct?")
            response = {'message': 'Could not send email'}
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = {'message': 'Participant code sent successfully'}
        return Response(response, status = status.HTTP_200_OK)

    def destroy(self, request, pk):
        
        participant = Participant.objects.get(id=pk)

        response = super().destroy(request)

        if status.is_success(response.status_code):
            program = participant.event
            registered = program.participant_set.all().count()

            if registered >= program.maxRegistered: # If last participant exists
                lastParticipant = program.participant_set.all().order_by('id')[program.maxRegistered-1]
                if participant.id < lastParticipant.id: # If lastParticipant is new
                    try:
                        send_mail('Nettverksdagene - Påmelding bekreftet for ' + lastParticipant.name,
                        'Du sto på ventelisten for ' + program.header + ', og har nå fått plass. Dersom du skulle ønske å melde deg av, vennligst gjør det via nettverksdagene.no/program. Tusen takk for din interesse i Nettverksdagene!',
                        'do-not-reply@nettverksdagene.no',
                        [lastParticipant.email],
                        fail_silently=False)
                    except:
                        print("ERROR: Could not send email. Is mail_settings.py correct?")
                        response = {'message': 'Could not send email'}
                        return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
