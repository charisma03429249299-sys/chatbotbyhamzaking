
from transformers import pipeline

# Name of our pretrained emotion detection model
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# This variable will store our loaded model
_classifier = None


def load_emotion_model():
    """
    Load the emotion detection model only once.
    """

    global _classifier

    if _classifier is None:
        print("Loading emotion detection model...")
        
        _classifier = pipeline(
            task="text-classification",
            model=MODEL_NAME,
            device=-1
        )

        print("Emotion model loaded successfully!")

    return _classifier


def detect_emotion(text: str) -> dict:
    """
    Analyze text and return the predicted emotion
    and confidence score.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Please enter a valid message.")

    classifier = load_emotion_model()

    # Get scores for all seven emotions
    predictions = classifier(text, top_k=None)

    # Handle different output formats
    if predictions and isinstance(predictions[0], list):
        predictions = predictions[0]

    if not predictions:
        raise RuntimeError("The model returned no predictions.")

    # Prepare emotion scores
    all_scores = [
        {
            "label": item["label"].lower(),
            "score": float(item["score"])
        }
        for item in predictions
    ]

    # Find the emotion with the highest score
    best_prediction = max(
        all_scores,
        key=lambda item: item["score"]
    )

    return {
        "emotion": best_prediction["label"],
        "confidence": best_prediction["score"],
        "all_scores": sorted(
            all_scores,
            key=lambda item: item["score"],
            reverse=True
        )
    }


# Test the emotion detector independently
if __name__ == "__main__":

    sample_text = "I am really happy today!"

    result = detect_emotion(sample_text)

    print("\nUser message:", sample_text)

    print("Predicted emotion:", result["emotion"])

    print(
        f"Confidence: {result['confidence']:.2%}"
    )

    print("\nAll emotion scores:")

    for item in result["all_scores"]:
        print(
            f"{item['label']}: {item['score']:.2%}"
        )
