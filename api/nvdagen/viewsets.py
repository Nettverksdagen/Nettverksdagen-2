from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant, Program
from .serializers import ListingSerializer, BusinessSerializer, SponsorSerializer, TeamMemberSerializer, FormSerializer, ParticipantSerializer, ProgramSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from time import gmtime, strftime
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time


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
                    data['waitingListIndex'] = waitingListIndex
                    data['place'] = program.place
                    # OBS! Første test av overføring fra epoch til datetime
                    data['timeStart'] = strftime('%. %B klokken %H:%M', gmtime(program.timeStart+3600))
                    
                    data['header'] = program.header
                    html_message = render_to_string('on_waiting_list.html', context=data)
                    plain_message = strip_tags(html_message)
                    send_mail('Nettverksdagene - Du står på venteliste',
                        plain_message,
                        'do-not-reply@nettverksdagene.no',
                        [data['email']],
                        fail_silently=False,
                        html_message=html_message)
                # If program not full, send confirmation email
                else:
                    data['place'] = program.place
                    #data['timeStart'] = strftime('%d. %b klokken %H:%M', gmtime(program.timeStart+3600))
                    #Ny formatering av dato
                    data['timeStart'] = format_datetime(datetime.fromtimestamp(program.timeStart+3600), "EEEE dd. MMMM, 'klokken' H:MM ", locale='nb_NO')
                    data['header'] = program.header
                    html_message = render_to_string('registered_email.html', context=data)
                    plain_message = strip_tags(html_message)
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data['name'],
                        plain_message,
                        'do-not-reply@nettverksdagene.no',
                        [data['email']],
                        fail_silently=False,
                        html_message=html_message)
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
            data = {}
            data['name'] = participant.name
            data['header'] = program.header
            data['code'] = participant.code
            html_message = render_to_string('deregister_code.html', context=data)
            plain_message = strip_tags(html_message)
            send_mail('Nettverksdagene - Avmeldingskode for ' + participant.name,
                plain_message,
                'do-not-reply@nettverksdagene.no',
                [participant.email],
                fail_silently=False,
                html_message=html_message)
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
                        data = {}
                        data['name'] = lastParticipant.name
                        data['header'] = program.header
                        data['timeStart'] = strftime('%d. %b klokken %H:%M', gmtime(program.timeStart+3600))
                        data['place'] = program.place
                        html_message = render_to_string('off_waiting_list.html', context=data)
                        plain_message = strip_tags(html_message)
                        send_mail('Nettverksdagene - Påmelding bekreftet for ' + lastParticipant.name,
                            plain_message,
                            'do-not-reply@nettverksdagene.no',
                            [lastParticipant.email],
                            fail_silently=False,
                            html_message=html_message)
                    except:
                        print("ERROR: Could not send email. Is mail_settings.py correct?")
                        response = {'message': 'Could not send email'}
                        return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
