from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from nvdagen.models import Participant, Program, FAQ, Infobox

CONFIRMATION_WORD = "bekreftet"
WAITLIST_WORD     = "venteliste"

class ViewSetTestCase(APITestCase):

    def setUp(self):
        # See routers.py
        self.participant_url       = reverse("participant-list")
        self.participant_count_url = reverse("participant-count")
        self.faq_url = reverse("faq-list")
        self.infobox_url = reverse("infobox-list")

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
        
        self.faq1 = FAQ.objects.create(
            question_nb="Hva er NVD?",
            question_en="What is NVD?",
            answer_nb="Nettverksdagen",
            answer_en="Networking Day",
            order=1
        )
        
        self.faq2 = FAQ.objects.create(
            question_nb="Når er NVD?",
            question_en="When is NVD?",
            answer_nb="Hvert år",
            answer_en="Every year",
            order=2
        )

        self.infobox = Infobox.objects.create(
            title_nb="Viktig informasjon",
            title_en="Important information",
            paragraph_nb="Les dette nøye",
            paragraph_en="Read this carefully"
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
            "code" :  "0xcafebabe",
            "phone": "12345678"
        }
        bob_data = {
            "email": "bob@hotmail.com",
            "event": self.program.id,
            "name" : "Bob",
            "year" : "2021",
            "study": "Prompting",
            "code" : "0xdeadbeef",
            "phone": "87654321"
        }

        # Test registration
        response = self.client.post(self.participant_url, format="json", data=alice_data)

        self.assertLess(response.status_code, 300)
        self.assertEqual(Participant.objects.count(), 2)
        self.assertEqual(self.program.participant_set.count(), 2)

        mock_send_mail.assert_called_once()
        send_mail_args, _ = mock_send_mail.call_args
        self.assertIn(CONFIRMATION_WORD, send_mail_args[0].lower())

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
    
        self.assertNotIn(CONFIRMATION_WORD, send_mail_args[0].lower())
        self.assertIn(WAITLIST_WORD, send_mail_args[0].lower())

        # Check that if alice unregisters, Bob will get confirmed
        alice = Participant.objects.filter(email=alice_data["email"]).get()
        delete_url = reverse("participant-detail", args=[alice.id])
        response = self.client.delete(delete_url, format="json", data={
            "code": alice_data["code"]
        })

        send_mail_args, _ = mock_send_mail.call_args

        # Now bob should get the mail
        self.assertEqual(mock_send_mail.call_count, 3)
        self.assertIn(CONFIRMATION_WORD, send_mail_args[0])
        self.assertIn(bob_data["name"], send_mail_args[0])
        self.assertEquals(send_mail_args[-1][0], bob_data["email"])

    @patch("nvdagen.viewsets.send_mail")
    def test_participant_allergies(self, mock_send_mail):
        allergic_participant = {
            "email": "gluten@free.com",
            "event": self.program.id,
            "name" : "Allergisk deltaker",
            "year" : "2",
            "study": "Matvitenskap",
            "code" : "0xallergy",
            "allergies" : "gluten, laktose, vann uten smak",
            "phone": "11111111"
        }

        non_allergic_participant = {
            "email": "healthy@individual.com",
            "event": self.program.id,
            "name" : "Sunn norsk ungdom",
            "year" : "5",
            "study": "Medisin",
            "code" : "0xnoallergy",
            "phone": "22222222"
        }

        # Check that allergies are registered
        response = self.client.post(self.participant_url, format="json", data=allergic_participant)

        self.assertLess(response.status_code, 300)
        allergic = Participant.objects.get(email="gluten@free.com")
        self.assertEqual(allergic.allergies, "gluten, laktose, vann uten smak")

        # Check without allergies
        response = self.client.post(self.participant_url, format="json", data=non_allergic_participant)

        self.assertLess(response.status_code, 300)
        non_allergic = Participant.objects.get(email="healthy@individual.com")
        self.assertEqual(non_allergic.allergies, "")

    def test_list_faqs(self):
        response = self.client.get(self.faq_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_faqs_ordered(self):
        response = self.client.get(self.faq_url)
        
        self.assertEqual(response.data[0]["order"], 1)
        self.assertEqual(response.data[1]["order"], 2)
        
    def test_retrieve_faq(self):
        detail_url = reverse("faq-detail", args=[self.faq1.id])
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["question_nb"], "Hva er NVD?")
        self.assertEqual(response.data["answer_en"], "Networking Day")
        
    def test_retrieve_infobox(self):
        detail_url = reverse("infobox-detail", args=[self.infobox.id])
        response = self.client.get(detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_nb"], "Viktig informasjon")
        self.assertEqual(response.data["paragraph_en"], "Read this carefully")
        
    def test_update_infobox(self):
        detail_url = reverse("infobox-detail", args=[self.infobox.id])
        updated_data = {
            "title_nb": "Ny tittel",
            "title_en": "New title",
            "paragraph_nb": "Ny tekst",
            "paragraph_en": "New text"
        }
        response = self.client.put(detail_url, format="json", data=updated_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_nb"], "Ny tittel")
        self.assertEqual(response.data["title_en"], "New title")