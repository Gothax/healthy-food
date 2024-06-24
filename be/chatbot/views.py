from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatRequestSerializer
import requests
from decouple import AutoConfig
import json
from django.http import JsonResponse
config = AutoConfig(search_path='C:/nonoo/workspace_dj/healthy-food/be/config')
OPENAI_API_KEY = config('API_KEY')

FINE_TUNED_MODEL = 'ft:gpt-3.5-turbo-0125:::9cxyGbRc'  

class ChatWithGpt(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {OPENAI_API_KEY}',
            }

            payload = {
                "model": FINE_TUNED_MODEL,
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }

            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)

            if response.status_code == 200:
                reply = response.json()['choices'][0]['message']['content']
                return Response({'reply': reply})
            else:
                return Response({'error': 'Failed to get response from ChatGPT'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_faq_data(request):
    try:
        with open('chatbot/faq.jsonl', 'r', encoding='utf-8') as f:
            faq_list = [json.loads(line) for line in f]
        return JsonResponse(faq_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
