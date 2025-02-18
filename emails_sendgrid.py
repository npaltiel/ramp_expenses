import sendgrid
import base64
import os
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition
from login_credentials import API_KEY


def send_emails(email, subject, body, file_path):
    sg = sendgrid.SendGridAPIClient(api_key=API_KEY)
    from_email = Email("berry@reports.anchorhc.org")  # Change to your verified sender
    to_email = To(email)  # Change to your recipient
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)

    with open(file_path, "rb") as file:
        file_data = file.read()
        encoded_file = base64.b64encode(file_data).decode()

    # Create SendGrid attachment
    attachment = Attachment(
        FileContent(encoded_file),
        FileName(os.path.basename(file_path)),
        FileType("application/octet-stream"),  # Change based on file type
        Disposition("attachment"),
    )

    # Attach file to email
    mail.attachment = attachment

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(f'{email}: {response.status_code}')
