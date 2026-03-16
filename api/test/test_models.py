from django.test import TestCase
from nvdagen.models import Participant, Program, TeamMember
import uuid

class ModelTestCase(TestCase):
    def setUp(self) -> None:
        self.team_member_1 = TeamMember.objects.create(
            id=1,
            name="Foo",
            email="foo@bar.baz",
            team="Bar",
            position="Baz"
        )

    def test_basic(self):
        self.assertEqual(self.team_member_1.name, "Foo")

    def test_participant_program(self):
        program = Program.objects.create(
            header       = "",
            place        = "",
            timeStart    = 0,
            timeEnd      = 1,

        )

        participant = Participant.objects.create(
            event = program,
            email = "",
        )

        self.assertEqual(Program.objects.count(), 1)
        self.assertEqual(Participant.objects.count(), 1)

        program.delete()

        self.assertEqual(Program.objects.count(), 0)

        # All participants of a program should be deleted when program is deleted
        self.assertEqual(Participant.objects.count(), 0)

    def test_participant_attendance_token_auto_generation(self):
        """Verify attendance_token is automatically generated as UUID on participant creation"""
        program = Program.objects.create(
            header="Test Event",
            place="Test Place",
            timeStart=0,
            timeEnd=1,
        )

        participant = Participant.objects.create(
            event=program,
            email="test@example.com",
            name="Test User",
            year="2024",
            study="Computer Science",
            code="testcode123"
        )

        self.assertIsNotNone(participant.attendance_token)
        self.assertIsInstance(participant.attendance_token, uuid.UUID)

    def test_participant_attendance_token_uniqueness(self):
        """Verify each participant gets a unique attendance_token"""
        program = Program.objects.create(
            header="Test Event",
            place="Test Place",
            timeStart=0,
            timeEnd=1,
        )

        participant1 = Participant.objects.create(
            event=program,
            email="test1@example.com",
            name="Test User 1",
            year="2024",
            study="Computer Science",
            code="testcode123"
        )

        participant2 = Participant.objects.create(
            event=program,
            email="test2@example.com",
            name="Test User 2",
            year="2024",
            study="Computer Science",
            code="testcode456"
        )

        self.assertNotEqual(participant1.attendance_token, participant2.attendance_token)

    def test_participant_attendance_defaults(self):
        """Verify default values for attendance fields"""
        program = Program.objects.create(
            header="Test Event",
            place="Test Place",
            timeStart=0,
            timeEnd=1,
        )

        participant = Participant.objects.create(
            event=program,
            email="test@example.com",
            name="Test User",
            year="2024",
            study="Computer Science",
            code="testcode123"
        )

        self.assertFalse(participant.attended)
        self.assertIsNone(participant.check_in_time)

    def test_participant_attendance_token_immutable(self):
        """Verify attendance_token doesn't change on subsequent saves"""
        program = Program.objects.create(
            header="Test Event",
            place="Test Place",
            timeStart=0,
            timeEnd=1,
        )

        participant = Participant.objects.create(
            event=program,
            email="test@example.com",
            name="Test User",
            year="2024",
            study="Computer Science",
            code="testcode123"
        )

        original_token = participant.attendance_token
        participant.name = "Updated Name"
        participant.save()
        participant.refresh_from_db()

        self.assertEqual(participant.attendance_token, original_token)
