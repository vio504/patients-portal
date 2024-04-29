"""Patient API Controller"""

from flask import Flask, request, jsonify
from patient_db import PatientDB


class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the pinfobase.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        try:
            patient_n = request.get_json()
            patient_id = self.patient_db.insert_patient(patient_n)
            if patient_id:
                patient = self.patient_db.fetch_patient_id_by_name(
                    patient_n["patient_name"])
                return jsonify(patient), 200
            else:
                return jsonify(message="patient already Exist :("), 400
        except Exception as e:
            return jsonify(message=str(e)), 400
        
    def get_patients(self):
        try:
            _name = request.args.get("search_name")
            if _name:
                patient = self.patient_db.fetch_patient_id_by_name(_name)
                if patient:
                    return jsonify(patient), 200
                else:
                    return jsonify({"error": "There is no Patient with this name !."}), 400
                
            patients = self.patient_db.select_all_patients()
            if patients:
                return jsonify(patients), 200
            else:
                return jsonify({"error": "Failed to retrieve patients from DB."}), 400
        except Exception:
            return jsonify({"error": "Internal Server Error."}), 500
        
    def get_patient(self, patient_id):
        try:
            patient = self.patient_db.select_patient(patient_id)
            if patient:
                return jsonify(patient), 200
            else:
                return jsonify({"error": "Patient not found."}), 400
        except Exception:
            return jsonify({"error": "Internal Server Error."}), 500
        
    def update_patient(self, patient_id):
        update_pinfo = request.json
        result = self.patient_db.update_patient(patient_id, update_pinfo)
        if result:
            return jsonify({"message": "Patient updated successfully."}), 200
        else:
            return jsonify({"error": "Failed to update patient."}), 400

    def delete_patient(self, patient_id):
        result = self.patient_db.delete_patient(patient_id)
        if result:
            return jsonify({"message": "Patient deleted successfully."}), 200
        else:
            return jsonify({"error": "Failed to delete patient."}), 400


    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()