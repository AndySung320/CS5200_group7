# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import openai  
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(['POST'])
@permission_classes([IsAuthenticated])  #login required
def get_hint_from_llm(request):
    prompt = request.data.get("prompt")

    if not prompt:
        return Response({"error": "Prompt is required."}, status=400)

    response_text = call_llm(prompt)

    return Response({
        "hint": response_text
    })

def call_llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides SQL hints."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()