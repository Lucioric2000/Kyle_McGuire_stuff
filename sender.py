from ruamel.yaml import YAML
import logging, smtplib, os
import traceback, ssl
context = ssl.create_default_context()
yaml = YAML(typ="safe")
with open("emails_private.yml", "r") as opf:
    configuration = yaml.load(opf)
def err_raiser():
    print("this function will raise an exception")
    s = 5/0
def correct_executor():
    print("this function will execute without exceptions")

def traceback_str(exc):
    """Use this function to get the traceback string for an exception"""
    return "".join(traceback.format_tb(exc.__traceback__))
def traceback_and_err_str(exc):
    """Use this function to get the traceback string for an exception"""
    return "\n".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    #return "".join(traceback.format_tb(exc.__traceback__))+"\n"+"\n".join(traceback.format_exception_only(type(exc), emailexception))
def smtplib_email(emailconfig, smtpconfig, exception):
    #If exception is None, this function is deemed to be reporting a succesful run, else it is deemed to
    #be reportingh an error
    if exception is None:
        email_body = emailconfig['body']
    else:
        email_body = emailconfig['body'].format(traceback_and_err_str(exception))
    with smtplib.SMTP_SSL(smtpconfig['server'], smtpconfig['port'], context=context) as smtp:
    #with smtplib.SMTP(smtpconfig['server'], smtpconfig['port']) as smtp:
        smtp.login(smtpconfig["username"], smtpconfig["password"])
        #smtp.starttls()
        if isinstance(emailconfig["receivers"], str):
            receivers = (emailconfig["receivers"], )#Create a singleton tuple, tuple because tuples are more efficient than lists
        else:
            receivers = emailconfig["receivers"]
        for receiver in receivers:
            message = f"Subject: {emailconfig['subject']}\n\n{email_body}"
        smtp.sendmail(smtpconfig["username"], receiver, message)

def handle_success():
    smtplib_email(configuration["success"], configuration["smtp"], None)

def handle_exception(err):
    smtplib_email(configuration["error"], configuration["smtp"], err)

def Connect():
    #replace this function with your code.
    #here, to test error execution call err_raiser(), and to test correct execution test correct_executor()
    #err_raiser()
    correct_executor()
try:
    Connect()
except Exception as exc:
    logging.exception("An exception occured during Connect():")
    #raise ValueError(2)
    try:
        handle_exception(exc)
    except Exception as emailexception:
        logging.exception("An exception occured during the report e-mail sending:")
        assert 0, traceback_and_err_str(emailexception)
else:
    handle_success()
