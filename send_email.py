from msal import ConfidentialClientApplication
import requests
from login_credentials import CLIENT_ID, TENANT_ID, CLIENT_SECRET

# Azure AD app credentials
SCOPES = ["https://graph.microsoft.com/.default"]


# Authenticate and acquire token
def get_access_token():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )
    token_response = app.acquire_token_for_client(scopes=SCOPES)
    print(token_response["access_token"])
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception("Failed to obtain access token")


# Send email using Microsoft Graph API
def send_email(sender_email, to_email, subject, body):
    access_token = get_access_token()
    url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to_email}}],
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 202:
        print(f"Email sent successfully to {to_email}!")
    else:
        print(f"Failed to send email: {response.status_code}, {response.json()}")

# Example usage
# send_email("nochum.paltiel@anchorhc.org", "nochum.paltiel@anchorhc.org", "Subject",
#            "This is a test email sent via Microsoft Graph API.")
