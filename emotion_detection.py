import requests
import json

WATSON_URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
    "Content-Type": "application/json"
}

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(WATSON_URL, json=payload, headers=HEADERS)

        if response.status_code == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        response.raise_for_status()
        response_dict = response.json()
        emotions = response_dict.get("emotionPredictions", [{}])[0].get("emotion", {})

        if not emotions:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        result = {
            "anger": emotions.get("anger", 0),
            "disgust": emotions.get("disgust", 0),
            "fear": emotions.get("fear", 0),
            "joy": emotions.get("joy", 0),
            "sadness": emotions.get("sadness", 0),
        }

        result["dominant_emotion"] = max(result, key=result.get) if any(result.values()) else None

        return result

    except requests.exceptions.RequestException:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None
        }

if __name__ == "__main__":
    sample_text = "I love this new technology."
    print(emotion_detector(sample_text))