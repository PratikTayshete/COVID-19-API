from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api
from data.covid_data import CovidData


covid_data = CovidData()


class CovidOverallStats(Resource):
    def get(self):
        """
        Returns a json response that contains overall statistics for COVID-19 as mentioned at https://www.mohfw.gov.in/

        :return: response - Json data that contains statistics with specific header type and status code.
        """
        json_response = jsonify({"active-cases": covid_data.get_total_active_cases(),
                                 "cured-discharged-cases": covid_data.get_total_cured_discharged_cases(),
                                 "death-cases": covid_data.get_total_death_cases()})
        response = make_response(json_response)
        response.headers["Content-Type"] = "application/json"
        response.status_code = 200
        return response


class CovidContactInfo(Resource):
    def get(self):
        """
        Returns a json response that contains contact information for COVID-19 as mentioned at https://www.mohfw.gov.in/

        :return: response - Json data that contains contact information with specific header and status code.
        """
        json_response = jsonify({"contact-information": covid_data.get_contact_information()})
        response = make_response(json_response)
        response.headers["Content-Type"] = "application/json"
        response.status_code = 200
        return response


class VaccinationInfo(Resource):
    def get(self):
        """
        Returns a json response that contains contact information for COVID-19 as mentioned at https://www.mohfw.gov.in/

        :return: response - Json data that contains the vaccination count with specific header and status code.
        """
        json_response = jsonify(({"vaccination-count": covid_data.get_vaccination_count()}))
        response = make_response(json_response)
        response.headers["Content-Type"] = "application/json"
        response.status_code = 200
        return response


app = Flask(__name__)
api = Api(app)
api.add_resource(CovidOverallStats, "/covid-overall-stats")
api.add_resource(CovidContactInfo, "/covid-contact-info")
api.add_resource(VaccinationInfo, "/covid-vaccination-info")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
