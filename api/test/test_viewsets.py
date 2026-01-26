from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
import uuid

from django.contrib.auth import get_user_model

from nvdagen.models import Participant, Program, FAQ, Infobox

CONFIRMATION_WORD = "bekreftet"
WAITLIST_WORD     = "venteliste"

class ViewSetTestCase(APITestCase):

    def setUp(self):
        # See routers.py
        self.participant_url       = reverse("participant-list")
        self.participant_count_url = reverse("participant-count")
        self.verify_url            = reverse("participant-verify")
        self.checkin_url           = reverse("participant-checkin")
        self.undo_checkin_url      = reverse("participant-undo-checkin")
        self.attendance_stats_url  = reverse("participant-attendance-stats")
        self.faq_url = reverse("faq-list")
        self.infobox_url = reverse("infobox-list")

        # Create admin user for authenticated endpoints
        self.admin_user = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True
        )

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
            name = "Test Participant",
            phone = "12345678",
            year = "2024",
            study = "CS",
            code = "testcode"
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

    @patch("nvdagen.viewsets.send_email_with_qr")
    @patch("nvdagen.viewsets.send_mail")
    def test_program_registration(self, mock_send_mail, mock_send_email_with_qr):
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

        # Test registration (program not full -> QR email)
        response = self.client.post(self.participant_url, format="json", data=alice_data)

        self.assertLess(response.status_code, 300)
        self.assertEqual(Participant.objects.count(), 2)
        self.assertEqual(self.program.participant_set.count(), 2)

        mock_send_email_with_qr.assert_called_once()
        call_kwargs = mock_send_email_with_qr.call_args[1]
        self.assertIn(CONFIRMATION_WORD, call_kwargs['subject'].lower())

        # Test registration fails if someone registers twice
        response = self.client.post(self.participant_url, format="json", data=alice_data)

        self.assertEquals(response.status_code, 400)

        # No additional mail should be sent
        mock_send_email_with_qr.assert_called_once()

        # Test registration that exceeds maxRegistered (waitlist -> send_mail)
        response = self.client.post(self.participant_url, format="json", data=bob_data)

        self.assertLess(response.status_code, 300)
        self.assertEqual(Participant.objects.count(), 3)
        self.assertEqual(self.program.participant_set.count(), 3)

        # Waitlist email should be sent via send_mail
        mock_send_mail.assert_called_once()
        send_mail_args, _ = mock_send_mail.call_args
        self.assertNotIn(CONFIRMATION_WORD, send_mail_args[0].lower())
        self.assertIn(WAITLIST_WORD, send_mail_args[0].lower())

        # Check that if alice unregisters, Bob will get confirmed (QR email)
        alice = Participant.objects.filter(email=alice_data["email"]).get()
        delete_url = reverse("participant-detail", args=[alice.id])
        response = self.client.delete(delete_url, format="json", data={
            "code": alice_data["code"]
        })

        # Bob should get QR email via send_email_with_qr
        self.assertEqual(mock_send_email_with_qr.call_count, 2)
        call_kwargs = mock_send_email_with_qr.call_args[1]
        self.assertIn(CONFIRMATION_WORD, call_kwargs['subject'])
        self.assertIn(bob_data["name"], call_kwargs['subject'])
        self.assertEqual(call_kwargs['recipient_email'], bob_data["email"])

    @patch("nvdagen.viewsets.send_email_with_qr")
    def test_participant_allergies(self, mock_send_email_with_qr):
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

    # QR Code Tests
    def test_qr_code_generation(self):
        """Test the generate_qr_code_bytes utility function"""
        from nvdagen.viewsets import generate_qr_code_bytes

        test_data = "test-uuid-string"
        qr_bytes = generate_qr_code_bytes(test_data)

        self.assertIsNotNone(qr_bytes)
        self.assertIsInstance(qr_bytes, bytes)
        # PNG files start with these magic bytes
        self.assertTrue(qr_bytes.startswith(b'\x89PNG'))

    @patch("nvdagen.viewsets.send_email_with_qr")
    def test_qr_code_included_in_registration_email(self, mock_send_email_with_qr):
        """Verify QR code email is sent on registration"""
        new_participant = {
            "email": "newuser@example.com",
            "event": self.program.id,
            "name": "New User",
            "year": "2024",
            "study": "CS",
            "code": "code123",
            "phone": "99999999"
        }

        response = self.client.post(self.participant_url, format="json", data=new_participant)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_send_email_with_qr.assert_called_once()

        # Verify the qr_data passed matches the created participant's token
        created_participant = Participant.objects.get(email="newuser@example.com")
        call_kwargs = mock_send_email_with_qr.call_args[1]
        self.assertEqual(call_kwargs['qr_data'], str(created_participant.attendance_token))

    # Verify Endpoint Tests
    def test_verify_valid_token(self):
        """Test verify endpoint with valid token (also verifies no auth required)"""
        response = self.client.get(self.verify_url, {'token': str(self.participant.attendance_token)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertIn('participant', response.data)
        self.assertEqual(response.data['participant']['id'], self.participant.id)
        self.assertFalse(response.data['participant']['attended'])
        self.assertIsNone(response.data['participant']['check_in_time'])

    def test_verify_invalid_token(self):
        """Test verify endpoint with invalid token"""
        invalid_token = str(uuid.uuid4())
        response = self.client.get(self.verify_url, {'token': invalid_token})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['valid'])
        self.assertIn('message', response.data)

    # Checkin Endpoint Tests
    @patch('django.utils.timezone.now')
    def test_checkin_success(self, mock_now):
        """Test successful check-in flow"""
        from datetime import datetime
        fixed_time = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
        mock_now.return_value = fixed_time

        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.checkin_url, {'token': str(self.participant.attendance_token)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('successful', response.data['message'].lower())
        self.assertTrue(response.data['participant']['attended'])
        self.assertIsNotNone(response.data['participant']['check_in_time'])

        # Verify database was updated
        self.participant.refresh_from_db()
        self.assertTrue(self.participant.attended)
        self.assertEqual(self.participant.check_in_time, fixed_time)

    def test_checkin_invalid_token(self):
        """Test check-in with invalid token"""
        self.client.force_authenticate(user=self.admin_user)
        invalid_token = str(uuid.uuid4())
        response = self.client.post(self.checkin_url, {'token': invalid_token})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Invalid token', response.data['message'])

    def test_checkin_requires_authentication(self):
        """Verify endpoint requires authentication"""
        response = self.client.post(self.checkin_url, {'token': str(self.participant.attendance_token)})

        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Verify participant was NOT checked in
        self.participant.refresh_from_db()
        self.assertFalse(self.participant.attended)

    # Undo Checkin Endpoint Test
    def test_undo_checkin_success(self):
        """Test successful undo of check-in"""
        # First check in
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(self.checkin_url, {'token': str(self.participant.attendance_token)})

        # Then undo
        response = self.client.post(self.undo_checkin_url, {'token': str(self.participant.attendance_token)})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('undone', response.data['message'].lower())
        self.assertFalse(response.data['participant']['attended'])
        self.assertIsNone(response.data['participant']['check_in_time'])

        # Verify database
        self.participant.refresh_from_db()
        self.assertFalse(self.participant.attended)
        self.assertIsNone(self.participant.check_in_time)

    # Attendance Stats Endpoint Tests
    def test_attendance_stats_overall(self):
        """Test overall statistics with multiple programs"""
        # Create second program
        program2 = Program.objects.create(
            header="Event 2",
            place="Place 2",
            timeStart=100,
            timeEnd=200,
            registration=True,
            maxRegistered=5,
        )

        # Program 1: 3 registered, 2 attended (including existing participant)
        p1_1 = Participant.objects.create(event=self.program, email="p1_1@test.com", name="P1_1", year="2024", study="CS", code="code1", phone="11111111")
        p1_2 = Participant.objects.create(event=self.program, email="p1_2@test.com", name="P1_2", year="2024", study="CS", code="code2", phone="22222222")
        p1_1.attended = True
        p1_1.check_in_time = timezone.now()
        p1_1.save()
        p1_2.attended = True
        p1_2.check_in_time = timezone.now()
        p1_2.save()

        # Program 2: 2 registered, 1 attended
        p2_1 = Participant.objects.create(event=program2, email="p2_1@test.com", name="P2_1", year="2024", study="CS", code="code3", phone="33333333")
        p2_2 = Participant.objects.create(event=program2, email="p2_2@test.com", name="P2_2", year="2024", study="CS", code="code4", phone="44444444")
        p2_1.attended = True
        p2_1.check_in_time = timezone.now()
        p2_1.save()

        response = self.client.get(self.attendance_stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('overall', response.data)
        self.assertIn('by_program', response.data)

        # Overall: 5 total (1 existing + 2 from p1 + 2 from p2), 3 attended
        self.assertEqual(response.data['overall']['total_registered'], 5)
        self.assertEqual(response.data['overall']['attended'], 3)
        self.assertEqual(response.data['overall']['not_attended'], 2)
        self.assertEqual(response.data['overall']['attendance_rate'], 60.0)

    def test_attendance_stats_single_program(self):
        """Test statistics for specific program"""
        # Add more participants to existing program
        p1 = Participant.objects.create(event=self.program, email="p1@test.com", name="P1", year="2024", study="CS", code="code1", phone="11111111")
        p2 = Participant.objects.create(event=self.program, email="p2@test.com", name="P2", year="2024", study="CS", code="code2", phone="22222222")

        # Mark 2 as attended (total 3 participants, 2 attended)
        p1.attended = True
        p1.check_in_time = timezone.now()
        p1.save()
        p2.attended = True
        p2.check_in_time = timezone.now()
        p2.save()

        response = self.client.get(self.attendance_stats_url, {'program_id': self.program.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['program_id'], str(self.program.id))
        self.assertEqual(response.data['total_registered'], 3)
        self.assertEqual(response.data['attended'], 2)
        self.assertEqual(response.data['not_attended'], 1)
        self.assertAlmostEqual(response.data['attendance_rate'], 66.67, places=1)

        # Should NOT include 'overall' or 'by_program' keys
        self.assertNotIn('overall', response.data)
        self.assertNotIn('by_program', response.data)

    # Integration Test
    @patch("nvdagen.viewsets.send_email_with_qr")
    def test_full_attendance_workflow(self, mock_send_email_with_qr):
        """Test complete workflow from registration to check-in"""
        # 1. Register participant
        participant_data = {
            "email": "workflow@example.com",
            "event": self.program.id,
            "name": "Workflow User",
            "year": "2024",
            "study": "CS",
            "code": "workflow123",
            "phone": "55555555"
        }
        response = self.client.post(self.participant_url, data=participant_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 2. Get token from response
        token = response.data['attendance_token']

        # 3. Verify token
        verify_response = self.client.get(self.verify_url, {'token': token})
        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertTrue(verify_response.data['valid'])

        # 4. Check in
        self.client.force_authenticate(user=self.admin_user)
        checkin_response = self.client.post(self.checkin_url, {'token': token})
        self.assertEqual(checkin_response.status_code, status.HTTP_200_OK)
        self.assertTrue(checkin_response.data['participant']['attended'])

        # 5. Check stats - should show 100% attendance for this program
        stats_response = self.client.get(self.attendance_stats_url, {'program_id': self.program.id})
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)
        # Program has 2 participants now (existing + new), 1 attended
        self.assertEqual(stats_response.data['total_registered'], 2)
        self.assertEqual(stats_response.data['attended'], 1)
        self.assertEqual(stats_response.data['attendance_rate'], 50.0)

    # Send QR Preview Tests
    def test_send_qr_preview_returns_correct_counts(self):
        """Test preview endpoint returns correct counts"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            reverse('participant-send-qr-preview'),
            {'program_id': self.program.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pending_qr_count', response.data)
        self.assertIn('total_confirmed', response.data)
        self.assertIn('already_sent_count', response.data)
        self.assertEqual(response.data['program_name'], self.program.header)
        # Participant hasn't received QR email yet
        self.assertEqual(response.data['pending_qr_count'], 1)
        self.assertEqual(response.data['already_sent_count'], 0)

    def test_send_qr_preview_requires_auth(self):
        """Test preview endpoint requires authentication"""
        response = self.client.get(
            reverse('participant-send-qr-preview'),
            {'program_id': self.program.id}
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_send_qr_preview_requires_program_id(self):
        """Test preview endpoint requires program_id parameter"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('participant-send-qr-preview'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Send QR Emails Tests
    @patch("nvdagen.viewsets.send_email_with_qr")
    def test_send_qr_emails_success(self, mock_send_email_with_qr):
        """Test sending QR emails marks participants as sent"""
        self.client.force_authenticate(user=self.admin_user)

        # Participant has not received QR email
        self.assertFalse(self.participant.qr_email_sent)

        response = self.client.post(
            reverse('participant-send-qr-emails'),
            {'program_id': self.program.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sent'], 1)
        self.assertEqual(response.data['failed'], 0)

        # Verify participant is now marked as sent
        self.participant.refresh_from_db()
        self.assertTrue(self.participant.qr_email_sent)

    @patch("nvdagen.viewsets.send_email_with_qr")
    def test_send_qr_emails_skips_already_sent(self, mock_send_email_with_qr):
        """Test that participants who already received QR are skipped"""
        self.client.force_authenticate(user=self.admin_user)

        # Mark participant as already having received QR email
        self.participant.qr_email_sent = True
        self.participant.save()

        response = self.client.post(
            reverse('participant-send-qr-emails'),
            {'program_id': self.program.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sent'], 0)
        self.assertEqual(response.data['failed'], 0)

        # send_email_with_qr should not have been called
        mock_send_email_with_qr.assert_not_called()

    def test_send_qr_emails_requires_auth(self):
        """Test send emails endpoint requires authentication"""
        response = self.client.post(
            reverse('participant-send-qr-emails'),
            {'program_id': self.program.id}
        )
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Verify participant was NOT marked as sent
        self.participant.refresh_from_db()
        self.assertFalse(self.participant.qr_email_sent)

    # FAQ Tests
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

    # Infobox Tests
    def test_retrieve_infobox(self):
        detail_url = reverse("infobox-detail", args=[self.infobox.id])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title_nb"], "Viktig informasjon")
        self.assertEqual(response.data["paragraph_en"], "Read this carefully")

    def test_update_infobox(self):
        User = get_user_model()
        superuser = User.objects.create_user(
            username="admin",
            password="1234",
            is_superuser=True
        )

        self.client.force_authenticate(user=superuser)
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
