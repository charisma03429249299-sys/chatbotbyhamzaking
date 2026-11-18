
import re


def generate_adaptive_response(
    user_text: str,
    emotion: str,
    confidence: float
) -> str:
    """
    Generate a response using the user's words
    and the predicted emotion.
    """

    text = user_text.lower().strip()
    emotion = emotion.lower().strip()

    # Check whether the user describes feeling okay or fine
    okay_pattern = (
        r"\b(?:i am|i'm|im|i feel|feeling|doing)\s+"
        r"(?:okay|ok|fine|alright|all right)\b"
    )

    negative_cues = [
        "sad", "lonely", "angry", "frustrated",
        "afraid", "scared", "worried", "anxious",
        "upset", "hurt", "terrible", "not happy",
        "not okay", "not fine"
    ]

    # Ask for clarification when model confidence is low
    if confidence < 0.70:   

        return (
            "I am not completely sure I understood "
            "your message. Would you like to tell me "
            "a little more about how you feel?"
        )

    # Handle okay/fine messages using their actual words
    if (
        re.search(okay_pattern, text)
        and not any(word in text for word in negative_cues)
    ):

        return (
            "I'm glad things feel okay. "
            "Is there anything you'd like help with?"
        )

    # Responses based on predicted emotion
    responses = {

        "joy": (
            "That's wonderful to hear! "
            "What is making you feel happy today?"
        ),

        "anger": (
            "I'm sorry this is frustrating. "
            "Tell me what happened, and I'll try to help."
        ),

        "disgust": (
            "It sounds like something has bothered you. "
            "Would you like to tell me more?"
        ),

        "fear": (
            "That sounds worrying. "
            "Let's take things one step at a time."
        ),

        "sadness": (
            "I'm sorry you're having a difficult day. "
            "Would you like to talk about it?"
        ),

        "neutral": (
            "Hello! How can I help you today?"
        ),

        "surprise": (
            "That sounds unexpected! "
            "Would you like to tell me more?"
        )
    }

    return responses.get(
        emotion,
        "I'm here to help. Please tell me more."
    )


# Test the adaptive response system
if __name__ == "__main__":

    message = "I am feeling okay now!"

    test_response = generate_adaptive_response(
        message,
        "joy",
        0.88
    )

    print("User:", message)
    print("Predicted emotion: Joy")
    print("Adaptive response:", test_response)
