from rest_framework import serializers
from .models import Listing, Business, Sponsor, TeamMember, Form, Program, Participant, Infobox, FAQ


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

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class ParticipantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        exclude = ('code',)

class ParticipantAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('id', 'name', 'email', 'study', 'year', 'attendance_token', 'attended', 'check_in_time', 'event', 'allergies', 'qr_email_sent')

class InfoboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infobox
        fields = '__all__'

class FAQserializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
