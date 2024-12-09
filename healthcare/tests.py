from rest_framework.test import APITestCase, APIClient
from .models import NewUser, Patient, Doctor, Intermediate, Appointment
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.urls import reverse
from django.contrib.auth.hashers import make_password
import json

class PatientsAPITestCase(APITestCase):
    def setUp(self):
        self.patient = Patient(
            email="patient@example.com",
            username="patientuser",
            phone_number="+1234567890",
            password="securepassword123",  # Plain text; will be hashed by `set_password`.
            blood_Group="O+",
            ailments="None",
            severity=Patient.SeverityType.MILD,
            disease="Common Cold",
            gender=Patient.Gender.FEMALE
        )
        self.patient.set_password(self.patient.password)  # Hash the password
        self.patient.type = NewUser.Types.PATIENT
        self.patient.save()

        self.client = APIClient()
        self.url = reverse('patients')

    def test_get_all_patients(self):
        response = self.client.get(self.url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # There should be 1 patient in the database.

    def test_get_patient_by_id(self):
        response = self.client.get(f'{self.url}?id={self.patient.id}')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['blood_Group'], 'O+')
        self.assertEqual(response.data['gender'], 'FEMALE')
        self.assertEqual(response.data['disease'], 'Common Cold')

    def test_get_patient_not_found(self):
        # Test with an invalid patient id
        response = self.client.get(f'{self.url}?id=9999')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'User with this ID does not exist')

    def test_get_patient_wrong_type(self):
        # Create a user with type "DOCTOR" to test the wrong type scenario
        doctor_user = NewUser.objects.create(
            email="doctor@example.com",
            username="doctoruser",
            password=make_password("password123"),
            type=NewUser.Types.DOCTOR
        )
        response = self.client.get(f'{self.url}?id={doctor_user.id}')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'User exists but is not of type Patient.')

class DoctorsAPITestCase(APITestCase):
    def setUp(self):
        # Create doctor profile
        self.doctor = Doctor(
            about="Experienced general physician.",
            specialization=Doctor.Specialization.CARDIOLOGIST,
            is_Free=True,
            username="doctortest",
            email="doctortest@example.com",
            password='password123'
        )
        self.doctor.type = NewUser.Types.DOCTOR
        self.doctor.set_password(self.doctor.password)
        self.doctor.save()

        # Initialize client
        self.client = APIClient()

        self.url = reverse('doctors')

    def test_get_doctor_by_id(self):
        response = self.client.get(f'{self.url}', {'id': self.doctor.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['about'], "Experienced general physician.")
        self.assertEqual(response.data['specialization'], "CARDIOLOGIST")
        self.assertEqual(response.data['is_Free'], True)

    def test_get_doctors_by_specialization(self):
        response = self.client.get(f'{self.url}', {'specialization': 'CARDIOLOGIST'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one Cardiologist exists
        self.assertEqual(response.data[0]['specialization'], "CARDIOLOGIST")

    def test_get_all_doctors(self):
        response = self.client.get(f'{self.url}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one doctor exists

    def test_post_doctor(self):
        data = {
            "username": "newdoctor",
            "email": "newdoctor@example.com",
            "type": NewUser.Types.DOCTOR,
            "password": "securepassword",
            "about": "Specialist in Orthopedics.",
            "specialization": Doctor.Specialization.ORTHOPEDIC,
            "is_Free": False
        }
        response = self.client.post(f'{self.url}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Doctor added to database, GET to check whether database was updated.")
        new_doctor = Doctor.objects.filter(username="newdoctor").first()
        self.assertIsNotNone(new_doctor)
        self.assertEqual(new_doctor.specialization, "ORTHOPEDIC")

    def test_put_doctor(self):
        data = {
            "id": self.doctor.id,
            "password": self.doctor.password,
            "email": self.doctor.email,
            "username": self.doctor.username,
            "about": "Updated description",
            "specialization": Doctor.Specialization.NEUROLOGIST,  # Use internal enum value
            "is_Free": False
        }
        # Serialize the data manually to ensure it's in proper JSON format
        json_data = json.dumps(data)
        # response = self.client.put(f'{self.url}', data, content_type='application/json')
        response = self.client.put(f'{self.url}', json_data, content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(updated_doctor.about, "Updated description")
        self.assertEqual(updated_doctor.specialization, Doctor.Specialization.NEUROLOGIST)  # Match enum
        self.assertEqual(updated_doctor.is_Free, False)

    def test_patch_doctor(self):
        data = {
            "id": self.doctor.id,
            "is_Free": False
        }
        response = self.client.patch(f'{self.url}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(updated_doctor.is_Free, False)

    def test_delete_doctor(self):
        response = self.client.delete(f'{self.url}', {'id': self.doctor.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Doctor.objects.filter(id=self.doctor.id).exists())

    def test_get_nonexistent_doctor_by_id(self):
        response = self.client.get(f'{self.url}', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User with this ID does not exist.')

    # def test_get_non_doctor_user_by_id(self):
    #     response = self.client.get(f'{self.url}', {'id': self.user.id})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['message'], 'User exists but is not of Doctor type.')

    def test_get_doctors_with_no_free_specialists(self):
        self.doctor.is_Free = False
        self.doctor.save()
        response = self.client.get(f'{self.url}', {'specialization': 'CARDIOLOGIST'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "CARDIOLOGISTs are not free right now.")

class NewUsersAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user = NewUser.objects.create(
            username="testuser",
            email="testuser@example.com",
            password=make_password("password123")
        )
        
        self.another_user = NewUser.objects.create(
            username="anotheruser",
            email="anotheruser@example.com",
            password=make_password("password456")
        )
        
        # Initialize client
        self.client = APIClient()
        self.url = reverse('users')

    def test_get_user_by_id(self):
        response = self.client.get(f'{self.url}', {'id': self.user.id})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_get_nonexistent_user_by_id(self):
        response = self.client.get(f'{self.url}', {'id': 999})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User with this ID does not exist.')

    def test_get_all_users(self):
        response = self.client.get(f'{self.url}')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), 2)  # Two users exist
        usernames = [user['username'] for user in response.data]
        self.assertIn("testuser", usernames)
        self.assertIn("anotheruser", usernames)

    def test_post_new_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword"
        }
        response = self.client.post(f'{self.url}', data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_user = NewUser.objects.filter(username="newuser").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, "newuser@example.com")

    def test_put_update_user(self):
        data = {
            "id": self.user.id,
            "username": "updateduser",
            "email": "updateduser@example.com",
            "password": "new_password123"  # Raw password
        }
        json_data = json.dumps(data)  # Serialize the dictionary to a JSON string
        response = self.client.put(
            f'{self.url}', 
            data=json_data, 
            content_type='application/json'  # Ensure content type is application/json
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch the updated user
        updated_user = NewUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updateduser@example.com")
        self.assertTrue(updated_user.check_password("new_password123"))  # Check if the password is hashed correctly

    def test_patch_update_user(self):
        data = {
            "id": self.user.id,
            "email": "patchedemail@example.com"
        }
        response = self.client.patch(f'{self.url}', data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = NewUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, "patchedemail@example.com")

    def test_delete_user(self):
        response = self.client.delete(f'{self.url}', {'id': self.another_user.id})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(NewUser.objects.filter(id=self.another_user.id).exists())

    def test_delete_nonexistent_user(self):
        response = self.client.delete(f'{self.url}', {'id': 999})
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Error is", response.data['message'])

class IntermediateAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        # Create a sample Intermediate user
        self.intermediate_user = Intermediate.objects.create(
            username="intermediate_user",
            email="intermediate@example.com",
            password=make_password("password123"),
            about="I am an intermediate user.",
        )
        self.valid_data = {
            "username": "new_intermediate",
            "email": "new_intermediate@example.com",
            "password": "securepassword",
            "about": "New intermediate user"
        }
        self.invalid_data = {
            "username": "",
            "email": "invalid_email",
            "password": "123",
        }

        self.client = APIClient()
        self.url = reverse('intermediates')

    def test_get_all_intermediates(self):
        """
        Test GET method to retrieve all intermediate users.
        """
        response = self.client.get(f"{self.url}")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_get_single_intermediate_valid_id(self):
        """
        Test GET method with a valid intermediate ID.
        """
        response = self.client.get(f"{self.url}?id={self.intermediate_user.id}")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], self.intermediate_user.id)

    def test_get_single_intermediate_invalid_id(self):
        """
        Test GET method with an invalid intermediate ID.
        """
        response = self.client.get(f"{self.url}?id=999")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "User with this ID does not exist.")

    def test_post_valid_intermediate(self):
        """
        Test POST method with valid data.
        """
        response = self.client.post(f"{self.url}", data=self.valid_data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Intermediate added to database, GET to check whether database was updated.")

    def test_post_invalid_intermediate(self):
        """
        Test POST method with invalid data.
        """
        response = self.client.post(f"{self.url}", data=self.invalid_data)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("errors", response.data)

    def test_patch_intermediate(self):
        """
        Test PATCH method to update an intermediate user partially.
        """
        update_data = {"id": self.intermediate_user.id, "about": "Updated about information"}
        response = self.client.patch(f"{self.url}", data=update_data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.intermediate_user.refresh_from_db()
        self.assertEqual(self.intermediate_user.about, "Updated about information")

    def test_delete_intermediate(self):
        """
        Test DELETE method to delete an intermediate user.
        """
        delete_data = {"id": self.intermediate_user.id}
        response = self.client.delete(f"{self.url}", data=delete_data)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Intermediate.objects.filter(id=self.intermediate_user.id).exists())
        self.assertIn("deleted successfully", response.data['message'])

    def test_delete_invalid_intermediate(self):
        """
        Test DELETE method with an invalid ID.
        """
        response = self.client.delete(f"{self.url}", data={"id": 999}, format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("User with ID", response.data['message'])

class AppointmentAPITestCase(APITestCase):

    def setUp(self):
        # Set up initial data
        self.appointment1 = Appointment.objects.create(
            patient_ID=1,
            doctor_Intermediate_ID=101,
            meeting_Type=Appointment.MeetingType.CHAT,
            disease="Flu",
            video_URL="http://example.com/meet1"
        )
        self.appointment2 = Appointment.objects.create(
            patient_ID=2,
            doctor_Intermediate_ID=102,
            meeting_Type=Appointment.MeetingType.VIDEOCALL,
            disease="Cough",
            video_URL="http://example.com/meet2"
        )
        self.valid_payload = {
            "patient_ID": 3,
            "doctor_Intermediate_ID": 103,
            "meeting_Type": "CHAT",
            "disease": "Fever",
            "video_URL": "http://example.com/meet3"
        }
        self.invalid_payload = {
            "patient_ID": None,
            "doctor_Intermediate_ID": None,
            "meeting_Type": "UNKNOWN",
            "disease": "",
        }
    
    def test_get_all_appointments(self):
        url = reverse('appointments')  # Replace with the actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_filtered_appointments(self):
        url = f"{reverse('appointments')}?filter=chat"  # Replace with the actual URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['meeting_Type'], "CHAT")

    def test_create_valid_appointment(self):
        url = reverse('appointments')  # Replace with the actual URL name
        response = self.client.post(url, data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Appointment.objects.count(), 3)
        self.assertEqual(Appointment.objects.last().disease, "Fever")
    
    # def test_create_invalid_appointment(self):
    #     url = reverse('appointments')  # Replace with the actual URL name
    #     response = self.client.post(url, data=self.invalid_payload, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertIn('errors', response.data)

    def test_update_appointment(self):
        url = reverse('appointments')  # Replace with the actual URL name
        payload = {"id": self.appointment1.id, "disease": "Updated Flu"}
        response = self.client.patch(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.disease, "Updated Flu")

    def test_delete_appointment(self):
        url = reverse('appointments')  # Replace with the actual URL name
        payload = {"id": self.appointment1.id}
        response = self.client.delete(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Appointment.objects.count(), 1)  # Ensure one appointment remains
