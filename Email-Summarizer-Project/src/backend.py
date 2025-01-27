from imap_tools import MailBox
from groq import Groq
from flask import Flask, jsonify, request
from flask_cors import CORS
import textwrap

app = Flask(__name__)
CORS(app)

def chunk_text(text, chunk_size=15000):
    """Break text into chunks while preserving words."""
    return textwrap.wrap(text, chunk_size, break_long_words=False, replace_whitespace=False)

def classify_email_content(client, content, categories):
    """Classify email content, handling large texts by breaking into chunks."""
    if len(content) <= 15000:
        return get_classification(client, content, categories)
    
    # For longer content, analyze chunks and make a weighted decision
    chunks = chunk_text(content)
    classifications = []
    chunk_weights = []
    
    for chunk in chunks:
        classification = get_classification(client, chunk, categories)
        classifications.append(classification)
        chunk_weights.append(len(chunk))
    
    # Weighted classification: give preference to larger chunks
    weighted_classifications = {}
    for i, classification in enumerate(classifications):
        weighted_classifications[classification] = (
            weighted_classifications.get(classification, 0) + chunk_weights[i]
        )
    
    # Return the classification with the highest weight
    return max(weighted_classifications, key=weighted_classifications.get, default="primary")

def get_classification(client, content, categories):
    """Get classification for a single chunk of text."""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that classifies email text based on predefined categories. "
                        "Your task is to categorize the email text into one of these categories provided by the user. "
                        "If the text does not belong to any of the categories, say 'primary.'"
                    )
                },
                {
                    "role": "user",
                    "content": f"Classify the following email text into one word. Do not write anything except that one word. Categories: {categories}. Email text: {content}"
                }
            ],
            model="llama3-8b-8192",
        )
        classification = chat_completion.choices[0].message.content.strip()
        print(f"Model classification response: {classification}")
        return classification
    except Exception as e:
        print(f"Classification error: {str(e)}")
        return "primary"

@app.route('/')
def home():
    return "Server is running!"

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    categories = data.get("categories", "")
    username = data.get("username", "")
    password = data.get("password", "")

    print(f"Processing request for user: {username}")
    print(f"Categories: {categories}")

    client = Groq(api_key="UNKNOWN")
    
    try:
        with MailBox("imap.gmail.com").login(username, password) as mb:
            emails_processed = 0
            errors = []
            
            # Process all emails in the mailbox
            for msg in mb.fetch(mark_seen=False, reverse=False):
                try:
                    # Get email content
                    email_text = msg.text or msg.html or ""
                    if not email_text.strip():
                        print(f"Skipping empty email content for email ID {msg.uid}")
                        continue
                    
                    # Classify the email
                    organizer = classify_email_content(client, email_text, categories)
                    print(f"Email {emails_processed + 1} classified as: {organizer}")

                    # Move the email to the appropriate folder
                    try:
                        mb.move({msg.uid}, organizer)
                        emails_processed += 1
                    except Exception as e:
                        error_msg = f"Failed to move email to {organizer}: {str(e)}"
                        print(error_msg)
                        errors.append(error_msg)

                except Exception as e:
                    error_msg = f"Error processing email ID {msg.uid}: {str(e)}"
                    print(error_msg)
                    errors.append(error_msg)

            return jsonify({
                "status": "success",
                "message": f"Processed {emails_processed} emails",
                "emails_processed": emails_processed,
                "errors": errors
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5000)
