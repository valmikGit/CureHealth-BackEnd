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

# class IntermediatesAPITestCase(APITestCase):
#     def setUp(self):
#         # Create test users of type 'INTERMEDIATE' and others for testing
#         self.intermediate_user = NewUser.objects.create(
#             username="intermediateuser",
#             email="intermediateuser@example.com",
#             type=NewUser.Types.INTERMEDIATE,
#             password=make_password("password123")
#         )

#         self.intermediate = Intermediate.objects.create(
#             id=self.intermediate_user.id,
#             specialization="Teaching",
#             user=self.intermediate_user
#         )

#         self.other_user = NewUser.objects.create(
#             username="regularuser",
#             email="regularuser@example.com",
#             type=NewUser.Types.USER,
#             password=make_password("password456")
#         )

#         self.client = APIClient()

#     def test_get_intermediate_by_id(self):
#         response = self.client.get(f'/intermediates/', {'id': self.intermediate_user.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data[0]['username'], "intermediateuser")
#         self.assertEqual(response.data[0]['email'], "intermediateuser@example.com")

#     def test_get_nonexistent_intermediate_by_id(self):
#         response = self.client.get(f'/intermediates/', {'id': 999})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'User with this ID does not exist.')

#     def test_get_non_intermediate_user_by_id(self):
#         response = self.client.get(f'/intermediates/', {'id': self.other_user.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], 'User exists but is not of Intermediate type.')

#     def test_get_all_intermediates(self):
#         response = self.client.get('/intermediates/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # Only one intermediate user exists
#         self.assertEqual(response.data[0]['specialization'], "Teaching")

#     def test_post_intermediate(self):
#         data = {
#             "username": "newintermediate",
#             "email": "newintermediate@example.com",
#             "type": NewUser.Types.INTERMEDIATE,
#             "password": "securepassword",
#             "specialization": "Counseling"
#         }
#         response = self.client.post('/intermediates/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         created_user = NewUser.objects.filter(username="newintermediate").first()
#         self.assertIsNotNone(created_user)
#         self.assertEqual(created_user.type, NewUser.Types.INTERMEDIATE)

#     def test_put_intermediate(self):
#         data = {
#             "id": self.intermediate.id,
#             "specialization": "Mentorship"
#         }
#         response = self.client.put('/intermediates/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_intermediate = Intermediate.objects.get(id=self.intermediate.id)
#         self.assertEqual(updated_intermediate.specialization, "Mentorship")

#     def test_patch_intermediate(self):
#         data = {
#             "id": self.intermediate.id,
#             "specialization": "Leadership"
#         }
#         response = self.client.patch('/intermediates/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_intermediate = Intermediate.objects.get(id=self.intermediate.id)
#         self.assertEqual(updated_intermediate.specialization, "Leadership")

#     def test_delete_intermediate(self):
#         response = self.client.delete('/intermediates/', {'id': self.intermediate.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(Intermediate.objects.filter(id=self.intermediate.id).exists())

#     def test_delete_nonexistent_intermediate(self):
#         response = self.client.delete('/intermediates/', {'id': 999})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("Error is", response.data['message'])

# class AppointmentsAPITestCase(APITestCase):
#     def setUp(self):
#         # Create a doctor and intermediate users for testing
#         self.doctor_user = NewUser.objects.create(
#             username="doctoruser",
#             email="doctor@example.com",
#             type=NewUser.Types.DOCTOR,
#             password=make_password("password123")
#         )
#         self.doctor = Doctor.objects.create(
#             id=self.doctor_user.id,
#             specialization="General",
#             is_Free=True,
#             user=self.doctor_user
#         )

#         # Create an appointment
#         self.appointment = Appointment.objects.create(
#             patient_name="John Doe",
#             appointment_date=now() + timedelta(days=1),
#             doctor_Intermediate_ID=self.doctor.id,
#             type="videocall"
#         )

#         self.client = APIClient()

#     def test_get_all_appointments(self):
#         response = self.client.get('/appointments/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # One appointment exists
#         self.assertEqual(response.data[0]['patient_name'], "John Doe")

#     def test_get_upcoming_appointments(self):
#         response = self.client.get('/appointments/', {'filter': 'upcoming'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # One upcoming appointment
#         self.assertEqual(response.data[0]['patient_name'], "John Doe")

#     def test_get_past_appointments(self):
#         # Modify the appointment to be in the past
#         self.appointment.appointment_date = now() - timedelta(days=1)
#         self.appointment.save()
#         response = self.client.get('/appointments/', {'filter': 'past'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # One past appointment
#         self.assertEqual(response.data[0]['patient_name'], "John Doe")

#     def test_get_chat_appointments(self):
#         # Change the type of appointment to "chat"
#         self.appointment.type = "chat"
#         self.appointment.save()
#         response = self.client.get('/appointments/', {'filter': 'chat'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # One chat appointment
#         self.assertEqual(response.data[0]['type'], "chat")

#     def test_get_videocall_appointments(self):
#         response = self.client.get('/appointments/', {'filter': 'videocall'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)  # One videocall appointment
#         self.assertEqual(response.data[0]['type'], "videocall")

#     def test_post_appointment(self):
#         data = {
#             "patient_name": "Jane Doe",
#             "appointment_date": str(now() + timedelta(days=2)),
#             "doctor_Intermediate_ID": self.doctor.id,
#             "type": "chat"
#         }
#         response = self.client.post('/appointments/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(Appointment.objects.filter(patient_name="Jane Doe").exists())

#     def test_put_appointment(self):
#         data = {
#             "id": self.appointment.id,
#             "patient_name": "Updated Name",
#             "type": "chat"
#         }
#         response = self.client.put('/appointments/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_appointment = Appointment.objects.get(id=self.appointment.id)
#         self.assertEqual(updated_appointment.patient_name, "Updated Name")
#         self.assertEqual(updated_appointment.type, "chat")

#     def test_patch_appointment(self):
#         data = {
#             "id": self.appointment.id,
#             "type": "chat"
#         }
#         response = self.client.patch('/appointments/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_appointment = Appointment.objects.get(id=self.appointment.id)
#         self.assertEqual(updated_appointment.type, "chat")

#     def test_delete_appointment(self):
#         response = self.client.delete('/appointments/', {'id': self.appointment.id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())

#     def test_delete_nonexistent_appointment(self):
#         response = self.client.delete('/appointments/', {'id': 999})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("Error is", response.data['message'])