from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def generate_read_query(request):
    prompt = request.data.get("prompt")

    if not prompt:
        return Response({"error": "Prompt is required."}, status=400)

    query = call_llm_for_read_query(prompt)
    return Response({"query": query})


def call_llm_for_read_query(prompt):
    system_prompt = (
        "You are a SQL assistant that only generates SELECT queries. "
        "Do NOT provide INSERT, UPDATE, DELETE or DDL statements. "
        "If the user asks for anything other than reading data, respond with a warning."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()