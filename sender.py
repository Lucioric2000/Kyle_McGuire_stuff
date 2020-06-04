from ruamel.yaml import YAML
from email.mime.text import MIMEText
import logging, smtplib, os
import traceback, ssl
import pyodbc, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--emails_file", default="emails.yml")
args = parser.parse_args()

context = ssl.create_default_context()
#context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#context.options |= ssl.OP_NO_TLSv1
#context.options |= ssl.OP_NO_TLSv1_1
yaml = YAML(typ="safe")
with open(args.emails_file, "r") as opf:
    configuration = yaml.load(opf)
def traceback_str(exc):
    """Use this function to get the traceback string for an exception"""
    return "".join(traceback.format_tb(exc.__traceback__))
def traceback_and_err_str(exc):
    """Use this function to get the traceback string for an exception"""
    return "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
def smtplib_email(emailconfig, smtpconfig, exception):
    #If exception is None, this function is deemed to be reporting a succesful run, else it is deemed to
    #be reporting an error
    if exception is None:
        email_body = emailconfig['body']
    else:
        email_body = emailconfig['body'].format(traceback_and_err_str(exception))
    use_ssl = smtpconfig.get("ssl")
    if use_ssl:
        smtp = smtplib.SMTP_SSL(smtpconfig['server'], smtpconfig['port'], context=context)
    else:
        smtp = smtplib.SMTP(smtpconfig['server'], smtpconfig['port'])
    with smtp:
        smtp.set_debuglevel(1)
        if use_ssl:
            smtp.login(smtpconfig["username"], smtpconfig["password"])
            #smtp.starttls(context=context)
        if isinstance(emailconfig["receivers"], str):
            receivers = (emailconfig["receivers"], )#Create a singleton tuple, tuple because tuples are more efficient than lists
        else:
            receivers = emailconfig["receivers"]
        msg = MIMEText(email_body)
        msg['From'] = smtpconfig['username']
        msg['To'] = ','.join(receivers)
        msg['Subject'] = emailconfig['subject']
        smtp.send_message(msg)

def handle_success():
    print("handling success")
    smtplib_email(configuration["success"], configuration["smtp"], None)

def handle_exception(err):
    print("handling exception")
    smtplib_email(configuration["error"], configuration["smtp"], err)

try:
    import Connect
    con = pyodbc.connect('Driver=Amazon RedShift (x86);UID=app_r_server;PWD=GUahXz59VhP4DKVQvM9YcyJCe;Server=golda.ceefb38tkh0v.us-west-2.redshift.amazonaws.com;Database=dw')
    Connect.read(con)
except Exception as exc:
    logging.exception("An exception occurred during Connect():")
    #raise ValueError(2)
    try:
        handle_exception(exc)
    except Exception as emailexception:
        logging.exception("An exception occured during the report e-mail sending:")
else:
    handle_success()
