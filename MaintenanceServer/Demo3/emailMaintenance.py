import smtplib, ssl
import getpass

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "maintenancecrewcarleton@gmail.com"
receiver_email = "maintenancecrewcarleton@gmail.com"
message = """\
Subject: Full Bin

Plastics bin at Waste Station 0 is full!"""

# Send email here

#password = getpass.getpass("Type your password and press enter: ")
password = "SYSC3010!"
# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)