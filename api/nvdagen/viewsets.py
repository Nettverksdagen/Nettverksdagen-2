from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant, Program
from .serializers import ListingSerializer, BusinessSerializer, SponsorSerializer, TeamMemberSerializer, FormSerializer, ParticipantSerializer, ProgramSerializer, ParticipantListSerializer, ParticipantAttendanceSerializer
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, time
from babel.dates import format_datetime, format_time
import qrcode
import io
import base64
from django.utils import timezone


def generate_qr_code(data):
    """Generate QR code as base64 encoded image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    # Convert to base64 for embedding in email
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"


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
                    # Create participant first to get attendance_token
                    participant = super().create(request)
                    created_participant = Participant.objects.get(id=participant.data['id'])

                    data['place'] = program.place
                    #data['timeStart'] = strftime('%d. %b klokken %H:%M', gmtime(program.timeStart+3600))
                    #Ny formatering av dato
                    data['timeStart'] = format_datetime(datetime.fromtimestamp(program.timeStart+3600), "EEEE dd. MMMM, 'klokken' H:MM ", locale='nb_NO')
                    data['header'] = program.header

                    # Generate QR code for attendance
                    qr_data = str(created_participant.attendance_token)
                    data['qr_code'] = generate_qr_code(qr_data)

                    html_message = render_to_string('registered_email.html', context=data)
                    plain_message = strip_tags(html_message)
                    send_mail('Nettverksdagene - Påmelding bekreftet for ' + data['name'],
                       plain_message,
                       'do-not-reply@nettverksdagene.no',
                       [data['email']],
                       fail_silently=False,
                       html_message=html_message)

                    return participant
            except Exception as e:
                print("ERROR: Could not send email. Is mail_settings.py correct?", e)
                response = {'message': 'Could not send email'}
                return Response(response, status = status.HTTP_500_INTERNAL_SERVER_ERROR)                

            # Create participant for waiting list too
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

        # The request is authorized if either a matching code is provided or
        # the user making the request is logged as the admin and no code is provided.
        if not (participant.code == code or code == None and request.user.is_staff):
            response = {'message': 'Invalid code'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def checkin(self, request):
        """Check in a participant using their attendance token"""
        token = request.data.get('token')
        if not token:
            return Response({'message': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(attendance_token=token)

            if participant.attended:
                return Response({
                    'message': 'Participant already checked in',
                    'participant': ParticipantAttendanceSerializer(participant).data
                }, status=status.HTTP_200_OK)

            participant.attended = True
            participant.check_in_time = timezone.now()
            participant.save()

            return Response({
                'message': 'Check-in successful',
                'participant': ParticipantAttendanceSerializer(participant).data
            }, status=status.HTTP_200_OK)

        except Participant.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def undo_checkin(self, request):
        """Undo check-in for a participant"""
        token = request.data.get('token')
        if not token:
            return Response({'message': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(attendance_token=token)

            if not participant.attended:
                return Response({
                    'message': 'Participant was not checked in',
                    'participant': ParticipantAttendanceSerializer(participant).data
                }, status=status.HTTP_200_OK)

            participant.attended = False
            participant.check_in_time = None
            participant.save()

            return Response({
                'message': 'Check-in undone successfully',
                'participant': ParticipantAttendanceSerializer(participant).data
            }, status=status.HTTP_200_OK)

        except Participant.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def verify(self, request):
        """Verify an attendance token and return participant info"""
        token = request.query_params.get('token')
        if not token:
            return Response({'message': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participant = Participant.objects.get(attendance_token=token)
            return Response({
                'valid': True,
                'participant': ParticipantAttendanceSerializer(participant).data
            }, status=status.HTTP_200_OK)

        except Participant.DoesNotExist:
            return Response({'valid': False, 'message': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def attendance_stats(self, request):
        """Get attendance statistics for all events"""
        program_id = request.query_params.get('program_id')

        if program_id:
            # Statistics for specific program
            participants = Participant.objects.filter(event_id=program_id)
            total = participants.count()
            attended = participants.filter(attended=True).count()
            not_attended = total - attended

            return Response({
                'program_id': program_id,
                'total_registered': total,
                'attended': attended,
                'not_attended': not_attended,
                'attendance_rate': (attended / total * 100) if total > 0 else 0
            })
        else:
            # Overall statistics
            all_participants = Participant.objects.all()
            total = all_participants.count()
            attended = all_participants.filter(attended=True).count()

            # Per-program breakdown
            programs = Program.objects.all()
            program_stats = []
            for program in programs:
                program_participants = all_participants.filter(event=program)
                program_total = program_participants.count()
                program_attended = program_participants.filter(attended=True).count()

                program_stats.append({
                    'program_id': program.id,
                    'program_name': program.header,
                    'total_registered': program_total,
                    'attended': program_attended,
                    'not_attended': program_total - program_attended,
                    'attendance_rate': (program_attended / program_total * 100) if program_total > 0 else 0
                })

            return Response({
                'overall': {
                    'total_registered': total,
                    'attended': attended,
                    'not_attended': total - attended,
                    'attendance_rate': (attended / total * 100) if total > 0 else 0
                },
                'by_program': program_stats
            })

    #Not tested and not implemented properly in /api
    def get_participant(self, request, email):
        participant = Participant.objects.get(email=email)
        return Response({'participant:', participant})

