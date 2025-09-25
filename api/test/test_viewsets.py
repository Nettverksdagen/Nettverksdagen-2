from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from nvdagen.models import Participant, Program

class ViewSetTestCase(APITestCase):
    def setUp(self):
        # See routers.py
        self.participant_url       = reverse("participant-list")
        self.participant_count_url = reverse("participant-count")

        self.program = Program.objects.create(
            header        = "Interesting event",
            place         = "Interesting place",
            timeStart     = 69,
            timeEnd       = 420,
            registration  = True,
            maxRegistered = 2,
        )

        self.participant = Participant.objects.create(
            event = self.program,
            email = "participant@gmail.com",
        )

    def test_participant_count(self):
        response = self.client.get(self.participant_count_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("participant_count", response.data)
        self.assertEqual(response.data["participant_count"], 1)

    @patch("nvdagen.viewsets.send_mail")
    def test_program_registration(self, mock_send_mail):
        alice_data = {
            "email": "alice@gmail.com",
            "event": self.program.id,
            "name" : "Alice",
            "year" : "1918",
            "study": "Kjønnsstudier",
            "code" :  "0xcafebabe"
        }
        bob_data = {
            "email": "bob@hotmail.com",
            "event": self.program.id,
            "name" : "Bob",
            "year" : "2021",
            "study": "Prompting",
            "code" : "0xdeadbeef"
        }

        # Test registration
        response = self.client.post(self.participant_url, format="json", data=alice_data)

        self.assertLess(response.status_code, 300)
        self.assertEqual(Participant.objects.count(), 2)
        self.assertEqual(self.program.participant_set.count(), 2)

        mock_send_mail.assert_called_once()
        send_mail_args, _ = mock_send_mail.call_args
        self.assertIn("bekreftet", send_mail_args[0].lower())

        # Test registration fails if someone registers twice
        response = self.client.post(self.participant_url, format="json", data=alice_data)

        self.assertEquals(response.status_code, 400)

        # No mail should be sent
        mock_send_mail.assert_called_once()

        # Test registration that exceeds maxRegistered
        response = self.client.post(self.participant_url, format="json", data=bob_data)

        self.assertLess(response.status_code, 300)
        self.assertEqual(Participant.objects.count(), 3)
        self.assertEqual(self.program.participant_set.count(), 3)

        # An email should be sent
        self.assertEqual(mock_send_mail.call_count, 2)

        send_mail_args, _ = mock_send_mail.call_args
    
        self.assertNotIn("bekreftet", send_mail_args[0].lower())
        self.assertIn("venteliste", send_mail_args[0].lower())

        # Check that if alice unregisters, Bob will get confirmed
        alice = Participant.objects.filter(email=alice_data["email"]).get()
        delete_url = reverse("participant-detail", args=[alice.id])
        response = self.client.delete(delete_url, format="json", data={
            "code": alice_data["code"]
        })

        send_mail_args, _ = mock_send_mail.call_args

        # Now bob should get the mail
        self.assertEqual(mock_send_mail.call_count, 3)
        self.assertIn("bekreftet", send_mail_args[0])
        self.assertIn(bob_data["name"], send_mail_args[0])
        self.assertEquals(send_mail_args[-1][0], bob_data["email"])
