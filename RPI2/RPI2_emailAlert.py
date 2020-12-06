"""
Name: Gurjit Gill
Date: December 1, 2020
Description: The following program sets up a connection to the GMail server, allowing us to send email alerts to the homeowner. A simple call to the notifyUser function
                in this class would allow us to send a notification with the subject and message of our choice. This code was created as a starting point to the email
                notification system. The final product may not have this implemented the same way and instead may be incorporated within one of the pre-existing classes
                for RPI4 (Eric's RPi).
"""
smtplib

#Login Credentials
emailAddress = 'hemas.assistant@gmail.com' #Our new project email, do not change!
emailPassword = 'TheEarthIsFlat'
server = 'smtp.gmail.com'  #This program can only connect us to the Gmail servers
port = 587

class EmailNotification:
    def notifyUser(self, recipient, subject, message):
        
        headers = ["From: " + emailAddress, "Subject: " + subject, "To: " + recipient, "MIME-Version: 1.0", "Content-Type: text/html"]  #Filling in the fields of an email
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
email = EmailNotification()
recipient = 'hemas.assistant@gmail.com'  #Enter homeowner's email here
subject = "WARNING: High Temperature"
message = "The current temperature in the house exceeds the set threshold. User action is required."
email.notifyUser(recipient, subject, message)      #Calls the notifyUser function while giving it the required info to send an email

