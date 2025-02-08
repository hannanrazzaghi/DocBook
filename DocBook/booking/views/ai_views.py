import json
import requests
from django.db.models import Avg
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from DocBook.settings import DEEPSEEK_API_KEY
from booking.models import Doctor, Rating

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

@csrf_exempt
def get_doctor_recommendation(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        # Parse the incoming data
        data = json.loads(request.body)
        symptoms = data.get('symptoms')
        location = data.get('location')

        if not symptoms or not location:
            return JsonResponse({"error": "Symptoms and location are required"}, status=400)

        # Create the prompt for the AI model
        prompt = f"Given the symptoms '{symptoms}' and location '{location}', recommend the best doctor (including specialization and location)."

        # Call DeepSeek API
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",  # Adjust model name if needed
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response_data = response.json()

        if "error" in response_data:
            return JsonResponse({"error": response_data["error"]["message"]}, status=500)

        # Extract AI-generated response
        ai_response = response_data['choices'][0]['message']['content'].strip()
        recommended_doctor_info = ai_response.split(',')

        doctor_name = recommended_doctor_info[0].strip()
        doctor_specialization = recommended_doctor_info[1].strip()
        doctor_location = recommended_doctor_info[2].strip()

        # Look for a matching doctor in the database
        doctor = Doctor.objects.filter(
            specialization__icontains=doctor_specialization,
            location__icontains=doctor_location
        ).first()

        if not doctor:
            return JsonResponse({"error": "No doctor found matching the AI recommendation"}, status=404)

        # Get the doctor's rating (average rating if available)
        rating = Rating.objects.filter(doctor=doctor).aggregate(Avg('score'))['score__avg'] or 0

        # Return the doctor recommendation
        return JsonResponse({
            "doctor_name": doctor.user.username,
            "specialization": doctor.specialization,
            "location": doctor.location,
            "rating": rating
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
