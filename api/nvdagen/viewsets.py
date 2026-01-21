from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant, Program
from .serializers import ListingSerializer, BusinessSerializer, SponsorSerializer, TeamMemberSerializer, FormSerializer, ParticipantSerializer, ProgramSerializer, ParticipantListSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, time
from babel.dates import format_datetime, format_time


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'message': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_count, _ = Listing.objects.filter(id__in=ids).delete()
        return Response({'message': f'{deleted_count} listings deleted successfully', 'deleted_count': deleted_count}, status=status.HTTP_200_OK)


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

    def list(self, request, *args, **kwargs):
        self.serializer_class = ParticipantListSerializer
        return super().list(request, *args, **kwargs)

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
                    data['allowDeregistration'] = program.allowDeregistration
                    html_message = render_to_string('registered_email.html', context=data)
                    plain_message = strip_tags(html_message)
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data['name'],
                       plain_message,
                       'do-not-reply@nettverksdagene.no',
                       [data['email']],
                       fail_silently=False,
                       html_message=html_message)
            except Exception as e:
                print("ERROR: Could not send email. Is mail_settings.py correct?", e)
                response = {'message': 'Could not send email'}
                return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)                

            return super().create(request)

        else:
            response = {'message': 'Invalid input. Is participant already registered?'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        participant = Participant.objects.get(id=pk)
        program = participant.event

        if not program.allowDeregistration:
            return Response({'message': 'This program does not allow deregistration'}, status=status.HTTP_400_BAD_REQUEST)

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
        except Exception as e:
            print("ERROR: Could not send email. Is mail_settings.py correct?", e)
            response = {'message': 'Could not send email'}
            return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = {'message': 'Participant code sent successfully'}
        return Response(response, status = status.HTTP_200_OK)

    def destroy(self, request, pk):
        try:
            participant = Participant.objects.get(id=pk)
        except:
            response = {'message': 'Participant not found'}
            return Response(response, status = status.HTTP_404_NOT_FOUND)

        code = request.data.get('code', None)
        program = participant.event

        # We only override validity as staff if the code is not provided
        valid_as_staff = request.user.is_staff and code is None
        valid_as_anon  = program.allowDeregistration and participant.code == code
        request_valid = valid_as_staff or valid_as_anon

        if not request_valid:
            msg = 'Program does not allow deregistration' if not program.allowDeregistration else 'Invalid code'
            return Response({'message': msg}, status = status.HTTP_400_BAD_REQUEST)

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
                        data['code'] = lastParticipant.code
                        data['header'] = program.header
                        data['place'] = program.place
                        html_message = render_to_string('off_waiting_list.html', context=data)
                        plain_message = strip_tags(html_message)
                        send_mail('Nettverksdagene - Påmelding bekreftet for ' + lastParticipant.name,
                            plain_message,
                            'do-not-reply@nettverksdagene.no',
                            [lastParticipant.email],
                            fail_silently=False,
                            html_message=html_message)
                    except Exception as e:
                        print("ERROR: Could not send email. Is mail_settings.py correct?", e)
                        response = {'message': 'Could not send email'}
                        return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response
    
    @action(detail=False, methods=['get'])
    def count(self, request):
        participant_count = Participant.objects.all().count()
        print(participant_count)
        return Response({'participant_count': participant_count})
    #Not tested and not implemented properly in /api
    def get_participant(self, request, email):
        participant = Participant.objects.get(email=email)
        return Response({'participant:', participant})

