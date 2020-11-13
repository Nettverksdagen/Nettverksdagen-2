from rest_framework import serializers
from .models import Listing, Business, Sponsor, TeamMember, Form, Participant


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    send_email = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'



    def send_email(self, request):
        response = {'message': 'It works!!'}
        return Response(response, status = status.HTTP_200_OK)
        
        try:
            #email, event, authentication
            if request.method == 'POST':
                #initialize
                data = {'email': request.data.get('email'), 'name': request.data.get('name')}
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

        