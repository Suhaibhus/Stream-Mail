from imap_tools import MailBox

mail_username = "testeremailsummarizer@gmail.com"
mail_password = "bkmh ziyf gijl gzix"  


with MailBox("imap.gmail.com").login(mail_username, mail_password) as mb:
    for msg in mb.fetch(limit=1, reverse=True, mark_seen=False):
        print(f"Subject: {msg.subject} \n Date: {msg.date_str} \n Text: {msg.text} ")

    # mb.move({msg.uid}, "Testing")