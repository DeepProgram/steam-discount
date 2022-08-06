import email, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendMail():
  def __init__(self,credentials):
    self.credentials = credentials
    self.subject = self.credentials["subject"]
    self.body = self.credentials["body"]
    self.sender_email = self.credentials["sender_email"]
    self.receiver_email = self.credentials["receiver_email"]
    self.password = self.credentials["gmailpass"]
    self.message = None

  def setCredentials(self,statsDict):
    # Create a multipart message and set headers
    self.message = MIMEMultipart("alternative")
    self.message["Subject"] = self.subject
    self.message["From"] = self.sender_email
    self.message["To"] = self.receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    {self.body}
    
    OverAll Stats Is Shown Below :

    Max Discount Found = {statsDict[0]["Max_Discount"]["Discount"]}, App Amount = {statsDict[0]["Max_Discount"]["Count"]}
    Lowest App Price = {statsDict[0]["Lowest_Price"]["Price"]}, App Amount = {statsDict[0]["Lowest_Price"]["Count"]}
    Highest App Price = {statsDict[0]["Highest_Price"]["Price"]}, App Amount = {statsDict[0]["Highest_Price"]["Count"]}
    Free Apps Amount = {statsDict[0]["Free_Games"]["Count"]}
    Free Apps = {"** No Free App Avaialble **" if statsDict[0]["Free_Games"]["Count"]==0 else str(statsDict[0]["Free_Games"]["Game_Names"])}

    Todays Stats Is Shown Below :

    Max Discount Found = {statsDict[1]["Max_Discount"]["Discount"]}, App Amount = {statsDict[1]["Max_Discount"]["Count"]}
    Lowest App Price = {statsDict[1]["Lowest_Price"]["Price"]}, App Amount = {statsDict[1]["Lowest_Price"]["Count"]}
    Highest App Price = {statsDict[1]["Highest_Price"]["Price"]}, App Amount = {statsDict[1]["Highest_Price"]["Count"]}
    Free Apps Amount = {statsDict[1]["Free_Games"]["Count"]}
    Free Apps = {"** No Free App Avaialble **" if statsDict[1]["Free_Games"]["Count"]==0 else str(statsDict[1]["Free_Games"]["Game_Names"])}

    Monthly Stats Is Shown Below :

    Max Discount Found = {statsDict[2]["Max_Discount"]["Discount"]}, App Amount = {statsDict[2]["Max_Discount"]["Count"]}
    Lowest App Price = {statsDict[2]["Lowest_Price"]["Price"]}, App Amount = {statsDict[2]["Lowest_Price"]["Count"]}
    Highest App Price = {statsDict[2]["Highest_Price"]["Price"]}, App Amount = {statsDict[2]["Highest_Price"]["Count"]}
    Free Apps Amount = {statsDict[2]["Free_Games"]["Count"]}
    Free Apps = {"** No Free App Avaialble **" if statsDict[2]["Free_Games"]["Count"]==0 else str(statsDict[2]["Free_Games"]["Game_Names"])}
    """
    part1 = MIMEText(text, "plain")
    self.message.attach(part1)
  def sendMail(self):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
      server.login(self.sender_email, self.password)
      server.sendmail(self.sender_email, self.receiver_email, self.message.as_string())
