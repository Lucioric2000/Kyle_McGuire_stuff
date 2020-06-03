from ruamel.yaml import YAML
import sendgrid
import os
from sendgrid.helpers.mail import *
yaml = YAML(typ="safe")
with open("emails.yaml", "r") as opf:
    configuration = yaml.load(opf)

sg = sendgrid.SendGridAPIClient(api_key=configuration["sendgrid"][0]['API_KEY'])
#sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
def handle_sucess()
	from_email = Email("test@example.com")
	to_email = To("test@example.com")
	subject = "Sending with SendGrid is Fun"
	content = Content("text/plain", "and easy to do anywhere, even with Python")
	mail = Mail(from_email, to_email, subject, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)
assert 0, configuration

def handle_exception(exc):

def Connect():
	s=5/0

try:
	Connect()
except Exception as exc:
	handle_exception(exc)
else:
	handle_sucess()
