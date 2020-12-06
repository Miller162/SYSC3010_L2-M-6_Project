import smtplib

#Login Credentials
emailAddress = 'hemas.assistant@gmail.com'
emailPassword = 'TheEarthIsFlat'
server = 'smtp.gmail.com'
port = 587

class EmailNotification:
    def notifyUser(self, recipient, subject, message):
        
        headers = ["From: " + emailAddress, "Subject: " + subject, "To: " + recipient, "MIME-Version: 1.0", "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        
        # Establish connection to Gmail server
        session = smtplib.SMTP(server, port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(emailAddress, emailPassword)
        
        # Combine email contents and send
        session.sendmail(emailAddress, recipient, headers + "\r\n\r\n" + message)
        
        session.quit   # end the session

# The following code tests the email notifcation system
# This is one example of its implementation
if __name__ == "__main__":
    email = EmailNotification()
    recipient = 'hemas.assistant@gmail.com'
    subject = "WARNING: High Temperature"
    message = "The current temperature in the house exceeds the set threshold. User action is required."
    email.notifyUser(recipient, subject, message)
