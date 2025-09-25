from django.test import TestCase
from nvdagen.models import Participant, Program, TeamMember

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
        self.assertEqual(self.team_member_1.name, "NotFoo")

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
