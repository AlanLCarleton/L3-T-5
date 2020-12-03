import smtplib, ssl
from email.message import EmailMessage
from datetime import datetime

def send_alert(bin_num, WS_num, level):
    now = datetime.now() # sending email date & time
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "maintenancecrewcarleton@gmail.com"
    receiver_email = "maintenancecrewcarleton@gmail.com"

    #Set email content
    msg = EmailMessage()
    content =  "At {}\nBin {} at Waste Station {} is almost full. \nCurrent level: {}%".format(now, bin_num, WS_num,level)
    msg.set_content(content)

    msg['Subject'] = "Full Bin Alert"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email here
    password = "SYSC3010!"
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg)


