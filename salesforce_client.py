# for dataframe functionality
import pandas as pd
import requests
# For interaction with Salesforce data
from simple_salesforce import Salesforce, format_soql

class salesforceAPIClient:
    def __init__(self, token_url=None, client_id=None, client_secret=None, refresh_token=None):
        # set up Oauth params
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        refresh_params = 'grant_type=refresh_token&refresh_token=' + refresh_token + '&client_id=' + client_id + '&client_secret=' + client_secret
        refresh_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'charset': 'utf-8'}
        
        # get refreshed token and instance information and use to create sf object
        token = requests.post(token_url, headers=refresh_headers, params=refresh_params).json()
        self.sf = Salesforce(instance_url=token["instance_url"],
            session_id=token["access_token"],
            version="47.0")
    """
        post takes a dataframe with unique salesforce IDs for each row, as well as a string indicating the related object and performs a bulk update of those objects in Salesforce
        :param df: dataframe containing unique object IDs along with the values that need updated for each
        :param object: string which is used to indicate the object you are attempting to update
        :return: void
    """   
    def post(self, object, df):
        # Turn data into a dictionary which is accessable for a bulk update
        data = df.to_dict('records')
        if object == "Lead":                    
            self.sf.bulk.Lead.update(data,batch_size=10000,use_serial=True)
            print("Success! Leads updated with ML score and Auto Persona")
        elif object == "Account":
            self.sf.bulk.Account.update(data,batch_size=10000,use_serial=True)
            print("Success! Leads updated with ML score and Auto Persona")
        elif object == "Application":
            self.sf.bulk.Application.update(data,batch_size=10000,use_serial=True)
            print("Success! Leads updated with ML score and Auto Persona")
        else:
            print("invalid object selection")
    """
        get takes a SOQL query in the form of a string, executes that query, and returns the requested data as a dataframe
        :query: a string representing a SOQL query
        :return: results of that SOQL query in a dataframe
    """
    def get(self, query):
        try:
            # SOQL Query
            data = self.sf.query_all(query)
            print("Success: Query successfully executed.")
            # Transform from JSON to dataframe
            return pd.DataFrame(data['records']).drop(columns='attributes')
        except:
            print("Unable to complete request: " + query + "is malformed. Request can not be completed.")
