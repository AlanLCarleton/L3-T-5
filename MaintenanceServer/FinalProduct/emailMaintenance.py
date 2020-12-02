import smtplib, ssl
from email.message import EmailMessage

def send_alert(bin_num, WS_num):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "maintenancecrewcarleton@gmail.com"
    receiver_email = "maintenancecrewcarleton@gmail.com"


    msg = EmailMessage()
    content =  "Bin {} at Waste Station {} is almost full.".format(bin_num, WS_num)
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


