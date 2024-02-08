# https://developer.servicem8.com/reference/post-jobcontact-create
import requests
import os 
from dotenv import load_dotenv, find_dotenv
#from .customer import add_customer  # Relative import with . as NoModuleError was being raised
#import time
#import asyncio


load_dotenv(find_dotenv())


class ServiceM8:

    #ups = os.getenv('UPS_KEY')

    def __init__(self, name, email, mobile, address, description, servicem8_key: str) -> None:
        self.name = name
        self.email = email
        self.mobile = mobile
        self.address = address
        self.description = description
        self.servicem8_key = servicem8_key

    def create_job(self) -> str:
        """Receives flat dict from Elementor Form webhook listener"""
        
        # Create new job
        url = "https://api.servicem8.com/api_1.0/job.json"
        job_status = 'Quote'
        payload = {
            "active": 1,
            "job_address": self.address,
            "geo_country": "Australia",
            "geo_state": "Western Australia",
                "status": job_status,
                "job_description": self.description,
            }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            # Fl0 does not take Env Variables with empty spaces
            # Therefore, Basic + ' ' + key is required
            "authorization": 'Basic' + ' ' + self.servicem8_key,
            "uuid": "x-record-uuid"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f'create_job: {response.text}')
            # Get job uuid to attached contact to job
            job_uuid = response.headers['x-record-uuid']
            return job_uuid
        except Exception as e:
            raise (e)

    def create_contact(self, job_uuid: str) -> tuple:
        """Uses data from checkout session
        & job_uuid returned from create_job func
        to create new job contact on ServiceM8,
        attached to job_uuid."""

        url = "https://api.servicem8.com/api_1.0/jobcontact.json"
        # Create new job contact
        payload = {
            "active": 1,
            "job_uuid": job_uuid,
            "first": self.name,
            #"last": name2,
            "email": self.email,
            "mobile": self.mobile,
            "type": "Job Contact",
            "is_primary_contact": "yes",
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            # Fl0 does not take Env Variables with empty spaces
            # Therefore, Basic + ' ' + key is required
            "authorization": 'Basic' + ' ' + self.servicem8_key,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            print(f'create_contact: {response.text}')
            return self.mobile, self.email, job_uuid
        except Exception as e:
            raise (e)
        

if __name__ == '__main__':
    ServiceM8()