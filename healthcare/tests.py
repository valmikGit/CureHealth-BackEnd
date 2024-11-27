from rest_framework.test import APITestCase, APIClient
from .models import NewUser, Patient, Doctor, Intermediate, Appointment
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.contrib.auth.hashers import make_password
class PatientsAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user (not a patient)
        self.user = NewUser.objects.create(
            username="testuser",
            email="testuser@example.com",
            type=NewUser.Types.USER,
            password=make_password("password123")
        )
        
        # Create a test patient user
        self.patient_user = NewUser.objects.create(
            username="patientuser",
            email="patientuser@example.com",
            type=NewUser.Types.PATIENT,
            password=make_password("password123")
        )
        
        self.patient = Patient.objects.create(
            id=self.patient_user.id,
            blood_Group="O+",
            gender="Male",
            disease="Flu",
            user=self.patient_user
        )
        
        self.client = APIClient()

    def test_get_patient_by_id(self):
        response = self.client.get(f'/patients/', {'id': self.patient_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['blood_Group'], 'O+')
        self.assertEqual(response.data['gender'], 'Male')
        self.assertEqual(response.data['disease'], 'Flu')

    def test_get_all_patients(self):
        response = self.client.get('/patients/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one patient exists

    def test_post_patient(self):
        data = {
            "username": "newpatient",
            "email": "newpatient@example.com",
            "type": NewUser.Types.PATIENT,
            "password": "securepassword",
            "blood_Group": "A+",
            "gender": "Female",
            "disease": "COVID-19"
        }
        response = self.client.post('/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Patient added to database, GET to check whether database was updated.")

    def test_put_patient(self):
        data = {
            "id": self.patient.id,
            "blood_Group": "B+",
            "gender": "Male",
            "disease": "UpdatedDisease"
        }
        response = self.client.put('/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_patient = Patient.objects.get(id=self.patient.id)
        self.assertEqual(updated_patient.blood_Group, "B+")
        self.assertEqual(updated_patient.disease, "UpdatedDisease")

    def test_patch_patient(self):
        data = {
            "id": self.patient.id,
            "disease": "NewDisease"
        }
        response = self.client.patch('/patients/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_patient = Patient.objects.get(id=self.patient.id)
        self.assertEqual(updated_patient.disease, "NewDisease")

    def test_delete_patient(self):
        response = self.client.delete('/patients/', {'id': self.patient.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Patient.objects.filter(id=self.patient.id).exists())

class DoctorsAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user (not a doctor)
        self.user = NewUser.objects.create(
            username="testuser",
            email="testuser@example.com",
            type=NewUser.Types.USER,
            password=make_password("password123")
        )
        
        # Create a test doctor user
        self.doctor_user = NewUser.objects.create(
            username="doctortest",
            email="doctortest@example.com",
            type=NewUser.Types.DOCTOR,
            password=make_password("password123")
        )
        
        # Create doctor profile
        self.doctor = Doctor.objects.create(
            id=self.doctor_user.id,
            about="Experienced general physician.",
            specialization="Cardiologist",
            is_Free=True,
            user=self.doctor_user
        )
        
        # Initialize client
        self.client = APIClient()

    def test_get_doctor_by_id(self):
        response = self.client.get(f'/doctors/', {'id': self.doctor_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['about'], "Experienced general physician.")
        self.assertEqual(response.data['specialization'], "Cardiologist")
        self.assertEqual(response.data['is_Free'], True)

    def test_get_doctors_by_specialization(self):
        response = self.client.get('/doctors/', {'specialization': 'Cardiologist'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one Cardiologist exists
        self.assertEqual(response.data[0]['specialization'], "Cardiologist")

    def test_get_all_doctors(self):
        response = self.client.get('/doctors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one doctor exists

    def test_post_doctor(self):
        data = {
            "username": "newdoctor",
            "email": "newdoctor@example.com",
            "type": NewUser.Types.DOCTOR,
            "password": "securepassword",
            "about": "Specialist in Orthopedics.",
            "specialization": "Orthopedic",
            "is_Free": False
        }
        response = self.client.post('/doctors/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Doctor added to database, GET to check whether database was updated.")
        new_doctor = Doctor.objects.filter(user__username="newdoctor").first()
        self.assertIsNotNone(new_doctor)
        self.assertEqual(new_doctor.specialization, "Orthopedic")

    def test_put_doctor(self):
        data = {
            "id": self.doctor.id,
            "about": "Updated description",
            "specialization": "Neurologist",
            "is_Free": False
        }
        response = self.client.put('/doctors/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(updated_doctor.about, "Updated description")
        self.assertEqual(updated_doctor.specialization, "Neurologist")
        self.assertEqual(updated_doctor.is_Free, False)

    def test_patch_doctor(self):
        data = {
            "id": self.doctor.id,
            "is_Free": False
        }
        response = self.client.patch('/doctors/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_doctor = Doctor.objects.get(id=self.doctor.id)
        self.assertEqual(updated_doctor.is_Free, False)

    def test_delete_doctor(self):
        response = self.client.delete('/doctors/', {'id': self.doctor.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Doctor.objects.filter(id=self.doctor.id).exists())

    def test_get_nonexistent_doctor_by_id(self):
        response = self.client.get(f'/doctors/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User with this ID does not exist.')

    def test_get_non_doctor_user_by_id(self):
        response = self.client.get(f'/doctors/', {'id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User exists but is not of Doctor type.')

    def test_get_doctors_with_no_free_specialists(self):
        self.doctor.is_Free = False
        self.doctor.save()
        response = self.client.get('/doctors/', {'specialization': 'Cardiologist'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Cardiologists are not free right now.")

class NewUsersAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user = NewUser.objects.create(
            username="testuser",
            email="testuser@example.com",
            type=NewUser.Types.USER,
            password=make_password("password123")
        )
        
        self.another_user = NewUser.objects.create(
            username="anotheruser",
            email="anotheruser@example.com",
            type=NewUser.Types.USER,
            password=make_password("password456")
        )
        
        # Initialize client
        self.client = APIClient()

    def test_get_user_by_id(self):
        response = self.client.get(f'/new_users/', {'id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser")
        self.assertEqual(response.data['email'], "testuser@example.com")

    def test_get_nonexistent_user_by_id(self):
        response = self.client.get(f'/new_users/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User with this ID does not exist.')

    def test_get_all_users(self):
        response = self.client.get('/new_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two users exist
        usernames = [user['username'] for user in response.data]
        self.assertIn("testuser", usernames)
        self.assertIn("anotheruser", usernames)

    def test_post_new_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "type": NewUser.Types.USER,
            "password": "securepassword"
        }
        response = self.client.post('/new_users/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_user = NewUser.objects.filter(username="newuser").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.email, "newuser@example.com")

    def test_put_update_user(self):
        data = {
            "id": self.user.id,
            "username": "updateduser",
            "email": "updateduser@example.com",
            "type": NewUser.Types.USER
        }
        response = self.client.put('/new_users/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = NewUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, "updateduser")
        self.assertEqual(updated_user.email, "updateduser@example.com")

    def test_patch_update_user(self):
        data = {
            "id": self.user.id,
            "email": "patchedemail@example.com"
        }
        response = self.client.patch('/new_users/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = NewUser.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, "patchedemail@example.com")

    def test_delete_user(self):
        response = self.client.delete('/new_users/', {'id': self.another_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(NewUser.objects.filter(id=self.another_user.id).exists())

    def test_delete_nonexistent_user(self):
        response = self.client.delete('/new_users/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Error is", response.data['message'])

class IntermediatesAPITestCase(APITestCase):
    def setUp(self):
        # Create test users of type 'INTERMEDIATE' and others for testing
        self.intermediate_user = NewUser.objects.create(
            username="intermediateuser",
            email="intermediateuser@example.com",
            type=NewUser.Types.INTERMEDIATE,
            password=make_password("password123")
        )

        self.intermediate = Intermediate.objects.create(
            id=self.intermediate_user.id,
            specialization="Teaching",
            user=self.intermediate_user
        )

        self.other_user = NewUser.objects.create(
            username="regularuser",
            email="regularuser@example.com",
            type=NewUser.Types.USER,
            password=make_password("password456")
        )

        self.client = APIClient()

    def test_get_intermediate_by_id(self):
        response = self.client.get(f'/intermediates/', {'id': self.intermediate_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], "intermediateuser")
        self.assertEqual(response.data[0]['email'], "intermediateuser@example.com")

    def test_get_nonexistent_intermediate_by_id(self):
        response = self.client.get(f'/intermediates/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User with this ID does not exist.')

    def test_get_non_intermediate_user_by_id(self):
        response = self.client.get(f'/intermediates/', {'id': self.other_user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User exists but is not of Intermediate type.')

    def test_get_all_intermediates(self):
        response = self.client.get('/intermediates/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one intermediate user exists
        self.assertEqual(response.data[0]['specialization'], "Teaching")

    def test_post_intermediate(self):
        data = {
            "username": "newintermediate",
            "email": "newintermediate@example.com",
            "type": NewUser.Types.INTERMEDIATE,
            "password": "securepassword",
            "specialization": "Counseling"
        }
        response = self.client.post('/intermediates/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        created_user = NewUser.objects.filter(username="newintermediate").first()
        self.assertIsNotNone(created_user)
        self.assertEqual(created_user.type, NewUser.Types.INTERMEDIATE)

    def test_put_intermediate(self):
        data = {
            "id": self.intermediate.id,
            "specialization": "Mentorship"
        }
        response = self.client.put('/intermediates/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_intermediate = Intermediate.objects.get(id=self.intermediate.id)
        self.assertEqual(updated_intermediate.specialization, "Mentorship")

    def test_patch_intermediate(self):
        data = {
            "id": self.intermediate.id,
            "specialization": "Leadership"
        }
        response = self.client.patch('/intermediates/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_intermediate = Intermediate.objects.get(id=self.intermediate.id)
        self.assertEqual(updated_intermediate.specialization, "Leadership")

    def test_delete_intermediate(self):
        response = self.client.delete('/intermediates/', {'id': self.intermediate.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Intermediate.objects.filter(id=self.intermediate.id).exists())

    def test_delete_nonexistent_intermediate(self):
        response = self.client.delete('/intermediates/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Error is", response.data['message'])

class AppointmentsAPITestCase(APITestCase):
    def setUp(self):
        # Create a doctor and intermediate users for testing
        self.doctor_user = NewUser.objects.create(
            username="doctoruser",
            email="doctor@example.com",
            type=NewUser.Types.DOCTOR,
            password=make_password("password123")
        )
        self.doctor = Doctor.objects.create(
            id=self.doctor_user.id,
            specialization="General",
            is_Free=True,
            user=self.doctor_user
        )

        # Create an appointment
        self.appointment = Appointment.objects.create(
            patient_name="John Doe",
            appointment_date=now() + timedelta(days=1),
            doctor_Intermediate_ID=self.doctor.id,
            type="videocall"
        )

        self.client = APIClient()

    def test_get_all_appointments(self):
        response = self.client.get('/appointments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One appointment exists
        self.assertEqual(response.data[0]['patient_name'], "John Doe")

    def test_get_upcoming_appointments(self):
        response = self.client.get('/appointments/', {'filter': 'upcoming'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One upcoming appointment
        self.assertEqual(response.data[0]['patient_name'], "John Doe")

    def test_get_past_appointments(self):
        # Modify the appointment to be in the past
        self.appointment.appointment_date = now() - timedelta(days=1)
        self.appointment.save()
        response = self.client.get('/appointments/', {'filter': 'past'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One past appointment
        self.assertEqual(response.data[0]['patient_name'], "John Doe")

    def test_get_chat_appointments(self):
        # Change the type of appointment to "chat"
        self.appointment.type = "chat"
        self.appointment.save()
        response = self.client.get('/appointments/', {'filter': 'chat'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One chat appointment
        self.assertEqual(response.data[0]['type'], "chat")

    def test_get_videocall_appointments(self):
        response = self.client.get('/appointments/', {'filter': 'videocall'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # One videocall appointment
        self.assertEqual(response.data[0]['type'], "videocall")

    def test_post_appointment(self):
        data = {
            "patient_name": "Jane Doe",
            "appointment_date": str(now() + timedelta(days=2)),
            "doctor_Intermediate_ID": self.doctor.id,
            "type": "chat"
        }
        response = self.client.post('/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Appointment.objects.filter(patient_name="Jane Doe").exists())

    def test_put_appointment(self):
        data = {
            "id": self.appointment.id,
            "patient_name": "Updated Name",
            "type": "chat"
        }
        response = self.client.put('/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(updated_appointment.patient_name, "Updated Name")
        self.assertEqual(updated_appointment.type, "chat")

    def test_patch_appointment(self):
        data = {
            "id": self.appointment.id,
            "type": "chat"
        }
        response = self.client.patch('/appointments/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_appointment = Appointment.objects.get(id=self.appointment.id)
        self.assertEqual(updated_appointment.type, "chat")

    def test_delete_appointment(self):
        response = self.client.delete('/appointments/', {'id': self.appointment.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())

    def test_delete_nonexistent_appointment(self):
        response = self.client.delete('/appointments/', {'id': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Error is", response.data['message'])