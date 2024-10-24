import google.generativeai as genai
from chatbot_project.settings import GEMINI_KEY
import queue
from IPython.display import display
from IPython.display import Markdown
import pathlib
import textwrap
from .models import Chat
from django.contrib.auth.models import User
from django.utils import timezone

response_queue=queue.Queue()

# User.objects.last().__dict__ ---> to convert last user obj into dict 

def to_markdown(text):
    text = text.replace('> ', '')
    text=text.replace('*',' ')
    text = text.replace('**', ' ')
    formatted_text = text.replace('\n', '\n\n')
    #formatted_text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', formatted_text)
    indented_text=textwrap.indent(formatted_text, ' ', predicate=lambda _: True)
    return indented_text


genai.configure(api_key=GEMINI_KEY)

def ask_gemini(message,userID):
    model = genai.GenerativeModel('gemini-1.5-flash',system_instruction="You are a sales/marketing AI assistant named SalesSense and you help users, clients and customers in improving their company's sales and marketing and for every other query which is not relevant to this domain you polietely reply saying this is not your domain  and also prompt some sample queries which enduser can ask you and also don't give long responses keep it precise and easy to understand")
    chat=model.start_chat(
        history=get_history(userID=userID)
    )
    response=chat.send_message(message)

    print(response.text)
    chat =Chat(user=User.objects.get(id=userID),message=message,response=to_markdown(response.text),created_at=timezone.now())
    chat.save()
    response_queue.put(to_markdown(response.text))
    

def get_history(userID):
    history = Chat.objects.filter(user=User.objects.get(id=userID))
    formatted_history = []
    for item in history:
        formatted_history.append({"parts": item.message,"role": "user"})
        formatted_history.append({"parts": item.response,"role": "model"})
        
    return formatted_history
