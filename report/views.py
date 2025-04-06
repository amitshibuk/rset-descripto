from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chat(request):
    if request.method == "GET":
        # Render the chat interface for GET requests
        return render(request, "report/chat.html")

    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            if not prompt:
                return JsonResponse({"error": "Prompt is required."}, status=400)

            # Forward the prompt to the external API
            external_api_url = "http://127.0.0.1:5000/prompt"
            payload = {
                "input": prompt,
            }

            # Send the POST request to the external API
            external_response = requests.post(external_api_url, json=payload)

            print("External API Response Status:", external_response.status_code)
            print("External API Response Body:", external_response.text)

            # Check if the external API returned a successful response
            if external_response.status_code == 200:
                external_data = external_response.json()  # Parse the JSON response
                reply = external_response.text
                print(reply[1:-3])
                return JsonResponse({"reply": reply[1:-4]})
            else:
                return JsonResponse({"error": f"External API error: {external_response.status_code}"}, status=external_response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def report(request):
    if request.method == "GET":
        # Render the chat interface for GET requests
        return render(request, "report/report_editor.html")

    if request.method == "POST":
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            prompt = data.get("prompt", "")

            if not prompt:
                return JsonResponse({"error": "Prompt is required."}, status=400)

            # Forward the prompt to the external API
            external_api_url = "http://127.0.0.1:5000/prompt"
            payload = {
                "input": prompt,
            }

            # Send the POST request to the external API
            external_response = requests.post(external_api_url, json=payload)

            print("External API Response Status:", external_response.status_code)
            print("External API Response Body:", external_response.text)

            # Check if the external API returned a successful response
            if external_response.status_code == 200:
                external_data = external_response.json()  # Parse the JSON response
                reply = external_response.text
                print(reply[1:-3])
                return JsonResponse({"reply": reply[1:-3]})
            else:
                return JsonResponse({"error": f"External API error: {external_response.status_code}"}, status=external_response.status_code)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)