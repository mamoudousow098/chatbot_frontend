from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import requests

BASE_URL ="http://localhost:5000/"

def chatbot_view(request):
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        user_input = request.POST.get('user_input')

        response = requests.get( BASE_URL + 'test',  data= { "query" : user_input} )
        print(response.json())

        data = response.json()['message']
        print(data)


        # Define your chatbot's predefined prompts
        prompts = []

        # Append user input to the conversation
        if user_input:
            conversation.append({"role": "user", "content": user_input})

        # Append conversation messages to prompts
        prompts.extend(conversation)

        # Extract chatbot replies from the response

        chatbot_replies = [ data ]

        # Append chatbot replies to the conversation
        for reply in chatbot_replies:
            conversation.append({"role": "assistant", "content": reply})

        # Update the conversation in the session
        request.session['conversation'] = conversation

        return render(request, 'chat.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        request.session.clear()
        return render(request, 'chat.html', {'conversation': conversation})


