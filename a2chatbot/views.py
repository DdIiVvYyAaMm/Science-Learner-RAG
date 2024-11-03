from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from a2chatbot.models import *
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.core.files import File
from django.utils import timezone

from openai import OpenAI
import os
import json
import csv
import threading

# include the api key 
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
topic = 'mutation'
question = "what is mutation?"


userid_list = ['student1', 'student2', 'test1', 'test2']

@ensure_csrf_cookie
@login_required
def home(request):
    print("homehome")
    context = {}
    user = request.user
    participant = get_object_or_404(Participant, user=  user)
    context['user'] = user
    print(user.username)

    interaction_mode =  participant.interaction_mode

    if not Assistant.objects.filter(user = user).filter(video_name = topic).exists():
        initialize_assistant(user, interaction_mode)

    context["question"] = question
    # Retrieve conversation history
    messages = Message.objects.filter(participant=participant).order_by('timestamp')
    context['messages'] = messages

    # Get interaction mode
    interaction_mode = participant.interaction_mode
    context['interaction_mode'] = interaction_mode

    # List of predefined questions
    context['questions'] = [
        "What is a mutation?",
        "What organisms are affected by genetic mutations?",
        "Are the results of mutation good or bad?",
        "What factors can make mutations more likely to occur?",
        "What’s the difference between gene and chromosomal mutations?",
        "Why are insertions and deletions dangerous?",
        "When are mutations most likely to occur?",
        "How can mutations be passed to offspring?"
    ]

    return render(request, 'a2chatbot/welcome.html', context)


@login_required
def ask_question(request):
    user = request.user
    participant = get_object_or_404(Participant, user=user)
    if request.method == "POST":
        question = request.POST.get('question')

        # Save the assistant's message (the question)
        Message.objects.create(
            participant=participant,
            sender='assistant',
            content=question
        )

        # Return the question as the assistant's message
        response = {'bot_message': question}
        return JsonResponse(response)
    else:
        return HttpResponse(status=405)


@login_required
def sendmessage(request):
    user = request.user
    participant = get_object_or_404(Participant, user=user)

    if request.method == "POST":
        student_message = request.POST["message"]

        # Save the student's message to the database
        Message.objects.create(
            participant=participant,
            sender='user',
            content=student_message
        )

        # Retrieve all previous messages in the conversation
        conversation = Message.objects.filter(participant=participant).order_by('timestamp')

        # Prepare messages for the OpenAI API
        messages = []

        # Get the interaction mode
        interaction_mode = participant.interaction_mode

        # Get the system prompt based on the interaction mode
        system_prompt = get_system_prompt(interaction_mode)

        # Include the system prompt as an initial assistant message if it's the first message
        if conversation.count() == 1:  # Only the user's first message exists
            messages.append({
                "role": "assistant",
                "content": system_prompt
            })

        # Add conversation messages to the messages list
        for msg in conversation:
            role = 'user' if msg.sender == 'user' else 'assistant'
            messages.append({"role": role, "content": msg.content})

        # Create the thread and run
        thread = client.beta.threads.create(messages=messages)

        assistant = get_object_or_404(Assistant, user=user, video_name=topic)

        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.assistant_id,
            temperature=0
        )

        # Get the assistant's reply
        responses = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
        assistant_reply = responses[-1].content[0].text.value

        # Save the assistant's message to the database
        Message.objects.create(
            participant=participant,
            sender='assistant',
            content=assistant_reply
        )

        # Return the assistant's reply as a JSON response
        response_text = [{'bot_message': assistant_reply}]
        response = json.dumps(response_text)
        return HttpResponse(response, 'application/javascript')
    else:
        return HttpResponseBadRequest('Invalid request method')
    

def get_system_prompt(interaction_mode):
    if interaction_mode == 'tutor_asks':
        return f"""
You are a helpful tutor teaching the student about "{topic}". The student has just answered a question. Provide feedback on their answer, correcting any misconceptions and encouraging them. Ask a new question from the context['questions'] unless all have been asked once. Use a variety of question formats such as open-ended questions, multiple-choice, and fill-in-the-blank to engage the student. Adapt the difficulty based on the student's responses but keep the questions strictly from the context['questions'].
When providing feedback or explanations:

- Use **bullet points** to list key information.
- Include relevant **emojis** to make the conversation engaging (e.g., 😊, 🧬, 💡).
- Highlight important terms by wrapping them with **<strong>** tags for bold text.
- Keep sentences concise and paragraphs short.
"""
    else:  # 'student_asks' mode
        return f"""
You are a helpful tutor assisting the student with their questions about "{topic}". Provide clear explanations and encourage the student. Keep the answers informative and short to help read them quick and understand better. If possible, give examples to help the student understand better.When answering, provide concise explanations that encourage the student to think critically. Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in. Ask follow-up questions to check for understanding and keep the student engaged.
When answering:

- Structure your responses with **bullet points**.
- Use **emojis** to highlight important points and make learning fun.
- Emphasize key concepts by wrapping them in **<strong>** tags.
- Provide examples where possible to aid understanding.
- Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in. 
- Encourage critical thinking by asking follow-up questions.

Keep the tone friendly and engaging.
"""

def initialize_assistant(user, interaction_mode):
    if user.username == 'test1':
        # Advanced student persona
        student_description = 'an advanced student preparing for an exam on mutations'
        persona_instructions = """
        - Provide in-depth explanations with technical language and advanced concepts.
        - Challenge the student with complex questions and problems.
        - Encourage critical thinking and analysis.
        - Use academic terminology and reference recent research.
        """
    elif user.username == 'test2':
        # Beginner student persona
        student_description = 'a beginner learning about mutations for fun'
        persona_instructions = """
        - Provide simple, clear explanations using everyday language.
        - Keep the content engaging and fun with interesting facts and examples.
        - Use analogies and relatable scenarios to explain concepts.
        - Encourage curiosity and exploration with open-ended questions.
        - Include emojis to make the conversation lively.
        """
    else:
        # Default persona
        student_description = 'a student learning about mutations'
        persona_instructions = """
        - Provide balanced explanations.
        - Adjust complexity based on the student's responses.
        - Keep the interaction engaging and informative.
        """


    if interaction_mode == 'tutor_asks':
        interaction_instructions = f"""
You are a helpful tutor who asks the {student_description} questions about "{topic}". Use a variety of question formats such as open-ended questions, multiple-choice, and fill-in-the-blank to engage the student. Adapt the difficulty based on the student's responses.
When providing feedback or explanations:

- Use **bullet points** to list key information.
- Include relevant **emojis** to make the conversation engaging (e.g., 😊, 🧬, 💡).
- Highlight important terms by wrapping them with **<strong>** tags for bold text.
- Keep sentences concise and paragraphs short.
"""
    else:
        interaction_instructions = f"""
You are a helpful tutor assisting the {student_description} with their questions about "{topic}". Provide thorough explanations, encourage the student, and check for understanding. When answering, provide concise explanations that encourage the student to think critically. Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in. Ask follow-up questions to check for understanding and keep the student engaged.
When answering:

- Structure your responses with **bullet points**.
- Use **emojis** to highlight important points and make learning fun.
- Emphasize key concepts by wrapping them in **<strong>** tags.
- Provide examples where possible to aid understanding.
- Hide key terminologies or concepts in your responses by replacing them with blanks or hints, prompting the student to fill them in.
- Encourage critical thinking by asking follow-up questions.

Keep the tone friendly and engaging.
"""
        
    instructions = f""" {persona_instructions}  {interaction_instructions} """

    assistant = client.beta.assistants.create(
        name="Middle school teacher",
        instructions=instructions,
        model="gpt-4o",
        temperature=0,
        tools=[{"type": "file_search"}],
    )

    vector_store = client.beta.vector_stores.create(name="video transcripts")

    file = client.files.create(
    file=open('mutation.txt', 'rb'), purpose='assistants')

    client.beta.vector_stores.files.create(vector_store_id=vector_store.id, file_id=file.id)
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    new_assistant = Assistant(
        video_name=topic,
        assistant_id=assistant.id,
        vector_store_id=vector_store.id,
        file_id=file.id,
        user=user
    )
    new_assistant.save()


@login_required
def set_interaction_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mode = data.get('mode')
        if mode not in ['tutor_asks', 'student_asks']:
            return HttpResponseBadRequest('Invalid mode')
        participant = get_object_or_404(Participant, user=request.user)
        participant.interaction_mode = mode
        participant.save()

        # Delete existing assistant
        try:
            assistant = Assistant.objects.get(user=request.user, video_name=topic)
            delete_agent(assistant)
            assistant.delete()
        except Assistant.DoesNotExist:
            pass  # No assistant to delete

        # Re-initialize assistant with new interaction_mode
        initialize_assistant(request.user, mode)

        # Clear conversation history if desired
        Message.objects.filter(participant=participant).delete()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@login_required
def end_conversation(request):
    if request.method == 'POST':
        user = request.user
        participant = get_object_or_404(Participant, user=user)
        assistant = get_object_or_404(Assistant, user=user)

        # Delete the assistant
        delete_agent(assistant)

        # Clear messages
        Message.objects.filter(participant=participant).delete()

        # Delete assistant record
        assistant.delete()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

# def delete_agent(participant):
#     assistant = get_object_or_404(Assistant, video_name=topic)
#     vector_store_id = assistant.vector_store_id

#     # Delete files from vector store
#     client.beta.vector_stores.files.delete(vector_store_id=vector_store_id)

#     # Delete the vector store
#     client.beta.vector_stores.delete(vector_store_id=vector_store_id)

#     # Delete the assistant
#     client.beta.assistants.delete(assistant_id=assistant.assistant_id)

#     # Delete assistant from database
#     assistant.delete()

#     # Delete messages
#     Message.objects.filter(participant=participant).delete()

def delete_agent(assistant):
    # Delete files from vector store
    client.beta.vector_stores.files.delete(
        vector_store_id=assistant.vector_store_id,
        file_id=assistant.file_id
    )

    # Delete the file
    client.files.delete(assistant.file_id)

    # Delete vector store
    client.beta.vector_stores.delete(assistant.vector_store_id)

    # Delete assistant
    client.beta.assistants.delete(assistant.assistant_id)
    



def register_new_users():
	for i in range(len(userid_list)):
		user= User.objects.create_user(username=userid_list[i], password = userid_list[i])
		user.save()        
		participant = Participant(user = user)
		participant.save()
	print("new users registered")


		
