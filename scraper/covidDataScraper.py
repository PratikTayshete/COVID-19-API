"""
The data provided is scraped from the website: https://www.mohfw.gov.in/.
"""

from bs4 import BeautifulSoup
import requests
import re


class CovidData:
    def __init__(self):
        self.URL = "https://www.mohfw.gov.in/"

    def __get_response(self):
        """
        Generates the response from the URL to scrape the data from.

        :return: parsed_data - A BeautifulSoup class object.
        """
        response = requests.get(self.URL)
        data = response.text
        parsed_data = BeautifulSoup(data, 'html.parser')
        return parsed_data

    def get_total_active_cases(self):
        """
        Returns the total active cases from COVID-19 as mentioned in the URL.

        :return: total_active_cases - Total count of active cases.
        """
        parsed_data = self.__get_response()
        active_cases_section = parsed_data.find("div", {"class": "site-stats-count"}).find("li", {"class": "bg-blue"})
        total_active_cases = active_cases_section.find("strong").text
        return int(total_active_cases)

    def get_total_cured_discharged_cases(self):
        """
        Returns the total cured/discharged cases from COVID-19 as mentioned in the URL.

        :return: total_cured_discharged_cases - Total count of cured or discharged cases.
        """
        parsed_data = self.__get_response()
        cured_discharged_cases_section = parsed_data.find("div", {"class": "site-stats-count"}).find("li", {
            "class": "bg-green"})
        total_cured_discharged_cases = cured_discharged_cases_section.find("strong").text
        return int(total_cured_discharged_cases)

    def get_total_death_cases(self):
        """
        Returns the total death cases from COVID-19 as mentioned in the URL.

        :return: total_death_cases - Total count of death cases.
        """
        parsed_data = self.__get_response()
        death_cases_section = parsed_data.find("div", {"class": "site-stats-count"}).find("li", {"class": "bg-red"})
        total_death_cases = death_cases_section.find("strong").text
        return int(total_death_cases)

    def get_total_migrated_cases(self):
        """
        Returns the total migrated cases from COVID-19 as mentioned in the URL.

        :return: total_migrated_cases - Total count of migrated cases.
        """
        parsed_data = self.__get_response()
        migrated_cases_section = parsed_data.find("div", {"class": "site-stats-count"}).find("li",
                                                                                             {"class": "bg-orange"})
        total_migrated_cases = migrated_cases_section.find("strong").text
        return int(total_migrated_cases)

    def get_contact_information(self):
        """
        Returns the contact information for COVID-19 as provided in the URL.

        :return: contact_information - A dictionary that contains the contact information retrieved.
        """
        # The list stores the raw contact information data needed to be filtered.
        contact_raw_data = []
        # The dictionary stores the contact information to be returned.
        contact_information = {}

        parsed_data = self.__get_response()
        contact_details_section = parsed_data.find_all("div", {"class": "site-meta"})
        for index, contact_data in enumerate(contact_details_section):
            if index > 2:
                break
            contact_raw_data.append(contact_data.text)

        # Filter the raw contact data to get the specific string data.
        filtered_contact_data = []
        for contact_data in contact_raw_data:
            filter_pattern = re.compile(r'[A-Z].*')
            filter_match = filter_pattern.findall(contact_data)
            filtered_contact_data.append([match for match in filter_match][0])

        # Filter the list of contact information data and save it in a dictionary.
        for index, contact_data in enumerate(filtered_contact_data):
            # Retrieve the helpline number.
            if index == 0:
                helpline_number_pattern = re.compile(r'\+[0-9].*-[0-9].*-[0-9].*$')
                helpline_number_match = helpline_number_pattern.findall(contact_data)
                contact_information['helpline'] = [matched_number for matched_number in helpline_number_match][0]

            # Retrieve the toll-free number.
            elif index == 1:
                tollfree_number_pattern = re.compile(r'[0-9].*$')
                tollfree_number_match = tollfree_number_pattern.findall(contact_data)
                contact_information['tollfree'] = [matched_number for matched_number in tollfree_number_match][0]

            # Retrieve the email id.
            elif index == 2:
                email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
                email_pattern_match = email_pattern.findall(contact_data)
                contact_information['email'] = [matched_email for matched_email in email_pattern_match][0]

        # Retrieve technical email contact.
        technical_email_id = parsed_data.find("span", {"class": "blinking"}).find("strong").find("a").text
        contact_information['technical_query_email'] = technical_email_id

        return contact_information

    def get_states_data(self):
        """
        Returns the statistics of different states as mentioned in the URL. Each state holds a count for Active Cases,
        Cured/Discharged/Migrated cases, Deaths and Total.
        :return: states_data - A dictionary that holds information related to different states.
        """

        states_data = {}  # This dictionary stores information about all the states.
        parsed_data = self.__get_response()
        states_table_data = parsed_data.find("div", {"class": "data-table"}). \
            find("table", {"class": "table"}). \
            find_all("tr")

        # Extract data for each state. The 1st row is ignored as it contains table headers.
        # The last 6 rows are ignored as the data is not related to a specific state.
        for state_data in states_table_data[1:-6]:
            state_info = state_data.find_all("td")[1:]  # Ignore the index number

            state_info_dict = {}  # The dictionary stores the information about each state.
            for index, info in enumerate(state_info[1:]):
                if index == 0:
                    state_info_dict["active_cases"] = info.text
                elif index == 1:
                    state_info_dict["cured_discharged_migrated"] = info.text
                elif index == 2:
                    state_info_dict["deaths"] = info.text
                elif index == 3:
                    state_info_dict["total_confirmed_cases"] = info.text

            states_data[state_info[0].text] = state_info_dict

        return states_data


