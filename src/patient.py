"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""
import uuid
from datetime import datetime
import requests
from patient_db_config import (
    PATIENT_ID_COLUMN,
    PATIENT_NAME_COLUMN,
    PATIENT_AGE_COLUMN,
    PATIENT_GENDER_COLUMN,
    PATIENT_CHECKIN_COLUMN,
    PATIENT_CHECKOUT_COLUMN,
    PATIENT_WARD_COLUMN,
    PATIENT_ROOM_COLUMN,
)
from config import GENDERS, API_CONTROLLER_URL, WARD_NUMBERS, ROOM_NUMBERS


class Patient:
    def __init__(self, name, gender, age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = self._validate_name(name)
        self.patient_gender = self._validate_gender(gender)
        self.patient_age = self._validate_age(age)
        self.patient_checkin = datetime.now().isoformat()
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None

    def _validate_name(self, name):
        if isinstance(name, str) and len(name) > 0:
            return name
        else:
            raise ValueError("Name must be a non-empty string.")

    def _validate_gender(self, gender):
        if gender in GENDERS:
            return gender
        else:
            raise ValueError("Invalid gender provided.")

    def _validate_age(self, age):
        if isinstance(age, int) and age > 0:
            return age
        else:
            raise ValueError("Age must be a positive integer.")

    def _validate_ward(self, ward):
        if not isinstance(ward, int) or ward not in WARD_NUMBERS:
            raise ValueError("Invalid ward number provided.")
        else:
            return ward

    def _validate_room(self, room):
         if not isinstance(room, int):
            raise ValueError("Room should be int.")
         if not any(str(room) in rooms for rooms in ROOM_NUMBERS.values()):
            raise ValueError(
                f"Room {room} does not exist in ward {self.patient_ward}.")
         return room
         

    def set_room(self, room):
        self.patient_room = self._validate_room(room) 

    def set_ward(self, ward):
        self.patient_ward = self._validate_ward(ward) 

    def get_id(self):
        return self.patient_id

    def get_name(self):
        return self.patient_name

    def get_gender(self):
        return self.patient_gender

    def get_age(self):
        return self.patient_age

    def get_checkin(self):
        return self.patient_checkin

    def get_checkout(self):
        return self.patient_checkout

    def get_ward(self):
        return self.patient_ward

    def get_room(self):
        return self.patient_room

    def commit(self):
        if None in (self.patient_ward, self.patient_room):
            raise ValueError("Both ward and room must be set before committing.")
        
        update_data = {
            PATIENT_ID_COLUMN: self.patient_id,
            PATIENT_NAME_COLUMN: self.patient_name,
            PATIENT_AGE_COLUMN: self.patient_age,
            PATIENT_GENDER_COLUMN: self.patient_gender,
            PATIENT_CHECKIN_COLUMN: self.patient_checkin,
            PATIENT_CHECKOUT_COLUMN: self.patient_checkout,
            PATIENT_WARD_COLUMN: self.patient_ward,
            PATIENT_ROOM_COLUMN: self.patient_room
        }
        response = requests.put(f"{API_CONTROLLER_URL}/patients/{self.patient_id}", json=update_data)
        if response.status_code == 200:
            print("Patient data committed successfully.")
        else:
            print("Failed to commit patient data to the database.")


   
