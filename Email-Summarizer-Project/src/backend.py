from imap_tools import MailBox
from groq import Groq

#email log in user will input this. 
mail_username = "testeremailsummarizer@gmail.com"
mail_password = "bkmh ziyf gijl gzix"  

client = Groq(api_key="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")

chooser = input("Please enter the categories (comma-separated): ")

with MailBox("imap.gmail.com").login(mail_username, mail_password) as mb:
    for msg in mb.fetch(limit=1000, reverse=True, mark_seen=False):
        print(f"Subject: {msg.subject} \n Date: {msg.date_str} \n Text: {msg.text}")
        
        user = msg.text
        # ai groq running. 
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that classifies email text based on predefined categories. Your task is to categorize the email text into one of these categories provided by the user. If the text does not belong to any of the categories, say 'primary'."
                },
                {
                    "role": "user",
                    "content": f"Classify the following email text into one word. Do not write anything except that one word. This will be used for something it will be based on the categories: {chooser}. Email text: {user}"
                }
            ],
            model="llama3-8b-8192",
        )

        #Result of the Gpt running
        organizer = chat_completion.choices[0].message.content.strip()

        print(f"Classified Category: {organizer}")

        # Move the email to the corresponding label based on the result
        try:
            #will try to add the label to your email, if it doesnt exist will ask user to self help.
            mb.move({msg.uid}, organizer)
            print(f"Email moved to: {organizer}")
        except Exception as e:
            print(f"Failed to move email, check if label is created")
