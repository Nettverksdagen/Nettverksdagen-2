from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
import uuid
import base64

from nvdagen.models import Participant, Program

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
            "allergies" : "gluten, laktose, vann uten smak"
        }

        non_allergic_participant = {
            "email": "healthy@individual.com",
            "event": self.program.id,
            "name" : "Sunn norsk ungdom",
            "year" : "5",
            "study": "Medisin",
            "code" : "0xnoallergy"
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
        """Test the generate_qr_code utility function"""
        from nvdagen.viewsets import generate_qr_code

        test_data = "test-uuid-string"
        qr_code = generate_qr_code(test_data)

        self.assertIsNotNone(qr_code)
        self.assertTrue(qr_code.startswith("data:image/png;base64,"))

        # Verify base64 string can be decoded
        base64_str = qr_code.split(',')[1]
        base64.b64decode(base64_str)  # Should not raise exception

    @patch("nvdagen.viewsets.generate_qr_code")
    @patch("nvdagen.viewsets.send_mail")
    def test_qr_code_included_in_registration_email(self, mock_send_mail, mock_generate_qr_code):
        """Verify QR code is generated and included in confirmation email"""
        mock_generate_qr_code.return_value = "data:image/png;base64,fake_qr_code"

        new_participant = {
            "email": "newuser@example.com",
            "event": self.program.id,
            "name": "New User",
            "year": "2024",
            "study": "CS",
            "code": "code123"
        }

        response = self.client.post(self.participant_url, format="json", data=new_participant)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_generate_qr_code.assert_called_once()

        # Verify the token passed to generate_qr_code matches the created participant's token
        created_participant = Participant.objects.get(email="newuser@example.com")
        call_args = mock_generate_qr_code.call_args[0][0]
        self.assertEqual(call_args, str(created_participant.attendance_token))

        # Verify email was sent
        mock_send_mail.assert_called_once()

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
        p1_1 = Participant.objects.create(event=self.program, email="p1_1@test.com", name="P1_1", year="2024", study="CS", code="code1")
        p1_2 = Participant.objects.create(event=self.program, email="p1_2@test.com", name="P1_2", year="2024", study="CS", code="code2")
        p1_1.attended = True
        p1_1.check_in_time = timezone.now()
        p1_1.save()
        p1_2.attended = True
        p1_2.check_in_time = timezone.now()
        p1_2.save()

        # Program 2: 2 registered, 1 attended
        p2_1 = Participant.objects.create(event=program2, email="p2_1@test.com", name="P2_1", year="2024", study="CS", code="code3")
        p2_2 = Participant.objects.create(event=program2, email="p2_2@test.com", name="P2_2", year="2024", study="CS", code="code4")
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
        p1 = Participant.objects.create(event=self.program, email="p1@test.com", name="P1", year="2024", study="CS", code="code1")
        p2 = Participant.objects.create(event=self.program, email="p2@test.com", name="P2", year="2024", study="CS", code="code2")

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
    @patch("nvdagen.viewsets.generate_qr_code")
    @patch("nvdagen.viewsets.send_mail")
    def test_full_attendance_workflow(self, mock_send_mail, mock_generate_qr_code):
        """Test complete workflow from registration to check-in"""
        mock_generate_qr_code.return_value = "data:image/png;base64,fake_qr_code"

        # 1. Register participant
        participant_data = {
            "email": "workflow@example.com",
            "event": self.program.id,
            "name": "Workflow User",
            "year": "2024",
            "study": "CS",
            "code": "workflow123"
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
    @patch("nvdagen.viewsets.send_mail")
    def test_send_qr_emails_success(self, mock_send_mail):
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

    @patch("nvdagen.viewsets.send_mail")
    def test_send_qr_emails_skips_already_sent(self, mock_send_mail):
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

        # send_mail should not have been called
        mock_send_mail.assert_not_called()

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