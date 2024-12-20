import smtplib

email = "testeremailsummarizer@gmail.com"
receiver_email = "testeremailsummarizer@gmail.com"

subject = input("Subject: ")
message = input("Message: ")

text = f'Subject: {subject}\n\n{message}'

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

server.login(email,"bkmh ziyf gijl gzix")

server.sendmail(email, receiver_email, text)

server.quit()

print("Email was successful.")