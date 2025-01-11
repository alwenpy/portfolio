from http.client import HTTPException
import os
import random
import requests
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
import json

from alwen import settings

GEMINI_API_KEY = "AIzaSyDWuh6JDfGppgGyKCHRKpKMfFmP0EPYpe8"
genai.configure(api_key=GEMINI_API_KEY)
TENOR_API_KEY = "AIzaSyDuN550ygThE8-A0nFuJGXcgM3eNVCwNW8"
CKEY = "Anime"
def home(request):
    file_path = os.path.join(settings.BASE_DIR, "static", "dynamic_script.js")

    with open(file_path, "w") as file:
        file.write("// Dynamic JavaScript")

    return render(request, "index.html")

def generate_js_with_gemini(command: str) -> str:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    prompt = (
        f"You are a JavaScript generator AI. Convert the following command into valid, plain JavaScript code: {command}. "
        f"Ensure the response contains only executable JavaScript without any enclosing tags or unnecessary prefixes like 'javascript:'."
        f"Also, avoid using 'console.log()' or similar functions in the response."
        f"Please provide the JavaScript code only."
        f"Try to display the implementation of the command in a div in the section with id=dynamic in the frontend."
        f"whatever you display apply some styles to it."
    )
    
    try:
        response = model.generate_content([prompt])
        print("Gemini API Response:", response.text)

        cleaned_js = (
            response.text
            .replace("```js", "")  
            .replace("```", "")
            .replace("javascript", "")  
            .strip()  
        )

        print("Cleaned JavaScript:", cleaned_js)
        return cleaned_js

    except Exception as e:
        print(f"Error in Gemini API call: {e}")
        raise HTTPException(status_code=500, detail=f"Error in Gemini API: {str(e)}")
@csrf_exempt
def apply_changes(request):
    if request.method == "POST":
        data = json.loads(request.body)
        command = data.get("command", "").strip()
        change_type = request.headers.get("X-Change-Type", "").lower()

        if not command:
            return JsonResponse({"error": "Command is empty."}, status=400)

        if change_type == "js":
            generated_js = generate_js_with_gemini(command)
            file_path = os.path.join(settings.BASE_DIR, "static", "dynamic_script.js")

            with open(file_path, "w") as file:
                file.write(generated_js)
            print(f"Writing JS to file: {file_path}")
            print(f"Generated JS Content:\n{generated_js}")


            return JsonResponse({"message": "JavaScript applied successfully.", "file": file_path, "js": generated_js}, status=200)
        else:
            return JsonResponse({"error": "Invalid change type."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_anime_of_the_day(request):
    anime_list = ["naruto", "jujutsu kaisen", "demon slayer", "one piece", "deathnote", "spy x family", "tokyo revengers"]
    random_anime = random.choice(anime_list)
    random_offset = random.randint(0, 50)
    url = f"https://tenor.googleapis.com/v2/search?q={random_anime}&key={TENOR_API_KEY}&client_key={CKEY}&limit=1&random=true&pos={random_offset}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            gif_url = data["results"][0]["media_formats"]["gif"]["url"]
            return JsonResponse({"gif_url": gif_url})
    return JsonResponse({"error": "No GIFs found."}, status=404)
