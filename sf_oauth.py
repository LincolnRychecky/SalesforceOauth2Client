import json
from salesforce_client import salesforceAPIClient
import argparse

if __name__=="__main__":
    # command line arguement determines which set of credentials will be used
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", choices=['production', 'sandbox'], help="argument determines if data will be sent to sandbox or prod. Provide either <production> or <sandbox>")
    args = parser.parse_args()

    # get authorization token for request based on commandline argument
    authorization = { "Authorization": "", "content-type": "application/json","Accept-Charset": "UTF-8"}
    if args.instance == "production":
        sfCredentials = json.load(open('Credentials/production-credentials.json'))
        tokenURL = "https://login.salesforce.com/services/oauth2/token"
    elif args.instance == "sandbox" :
        sfCredentials = json.load(open('Credentials/sandbox-credentials.json'))
        token_url = "https://login.salesforce.com/services/oauth2/token"

    sfClient = salesforceAPIClient(
        token_url = tokenURL,
        client_id = sfCredentials["consumer key"],
        client_secret = sfCredentials["consumer secret"],
        refresh_token = sfCredentials["refresh token"]
        )

    # you how have an authed session with which you can query/update salesforce records
    data = sfClient.get("SELECT ID FROM LEAD LIMIT 10")
    print(data)