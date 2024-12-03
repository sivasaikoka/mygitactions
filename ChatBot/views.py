from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation
from .serializers import ConversationSerializer
from .bot_logic import get_bot_response

class ChatBotView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'ChatBot/Chat.html')

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('user_input')  # Fetch data from request body
        if not user_input:
            return Response({"error": "No user input provided."}, status=status.HTTP_400_BAD_REQUEST)

        bot_response = get_bot_response(user_input)
        conversation = Conversation.objects.create(user_input=user_input, bot_response=bot_response)
        serializer = ConversationSerializer(conversation)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
