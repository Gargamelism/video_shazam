import requests
import os


QUOTA_EXCEEDED_ERROR = "You have exceeded the MONTHLY quota for Requests on your current plan"


def identify_song(audio_file: str):
    response = requests.post(
        "https://shazam-api6.p.rapidapi.com/shazam/recognize",
        headers={
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapid-api-host": "shazam-api6.p.rapidapi.com",
        },
        files={"upload_file": (open(audio_file, "rb"))},
    )

    response_json = response.json()

    if "status" in response_json and response_json["status"] == False:
        print(f"Could not identify song for {audio_file}")
        return False

    if "message" in response_json and QUOTA_EXCEEDED_ERROR in response_json["message"]:
        print(f"Error: {response_json['message']}")
        exit(1)

    return response_json
