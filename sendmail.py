import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import stats

def sendMail():
  print("\n\n\t\t**** SENDING MAIL ****\n\n")
  credentials = json.loads(open("credentials.txt","r").read())
  subject = credentials["subject"]
  body = credentials["body"]
  sender_email = credentials["sender_email"]
  receiver_email = credentials["receiver_email"]
  password = credentials["gmailpass"]

  # Create a multipart message and set headers
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject
  message["Bcc"] = receiver_email  # Recommended for mass emails

  # Add body to email
  message.attach(MIMEText(body, "plain"))
  filename = "saved.txt"  # In same directory as script
  with open(filename, "rb") as attachment:
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())

  # Encode file in ASCII characters to send by email    
  encoders.encode_base64(part)

  # Add header as key/value pair to attachment part
  part.add_header(
      "Content-Disposition",
      f"attachment; filename= {filename}",
  )

  # Add attachment to message and convert message to string
  message.attach(part)
  text = message.as_string()

  # Log in to server using secure context and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
  
  print("\n\n\t\t**** SENT MAIL.. Waiting For Next Run ****\n\n")
