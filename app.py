
import streamlit as st
from collections import Counter

from emotion_detector import detect_emotion
from response_system import generate_adaptive_response


# Page configuration
st.set_page_config(
    page_title="EmpathyBot",
    page_icon="💙",
    layout="centered"
)


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Store detected emotions
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []


# Main heading
st.title("💙 EmpathyBot")
st.caption("Your Emotionally Aware AI Chatbot")

st.write(
    "Hello! Welcome to EmpathyBot. "
    "Share your thoughts, and let's talk."
)


# Sidebar
with st.sidebar:

    st.header("About EmpathyBot")

    st.write(
        "EmpathyBot analyzes emotional signals "
        "and provides supportive responses."
    )

    st.info(
        "Emotion predictions are estimates, "
        "not confirmed human feelings."
    )

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []
        st.session_state.emotion_history = []

        st.rerun()


# Emotion History Dashboard
st.divider()

st.subheader("📊 Emotion History Dashboard")

history = st.session_state.emotion_history

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Messages Analyzed",
        len(history)
    )

with col2:
    st.metric(
        "Emotion Categories",
        len(set(history))
    )


# Show emotion frequency without Pandas
if history:

    emotion_counts = Counter(history)

    total_messages = len(history)

    st.write("Emotion Frequency")

    for emotion, count in emotion_counts.most_common():

        col1, col2 = st.columns([1, 3])

        with col1:
            st.write(
                f"**{emotion.title()}** ({count})"
            )

        with col2:
            st.progress(
                count / total_messages
            )

else:

    st.info(
        "Your emotion history will appear here "
        "after your first message."
    )


st.divider()


# Emotion Dynamics
st.subheader("🔄 Emotion Change History")

if history:

    recent_emotions = history[-10:]

    st.write("Recent Emotion Signals")

    for index, emotion in enumerate(recent_emotions, start=1):

        st.write(
            f"Message {index}: {emotion.title()}"
        )

    # Find every change between consecutive predictions
    st.write("Emotion Changes")

    changes = []

    for previous, current in zip(history, history[1:]):

        if previous != current:
            changes.append((previous, current))

    if changes:

        for previous, current in changes:

            st.info(
                f"{previous.title()} → {current.title()}"
            )

    else:

        st.caption(
            "No emotion changes detected yet."
        )

else:

    st.info(
        "Emotion changes will appear after you start chatting."
    )


# Display previous conversation
st.subheader("💬 Chat with EmpathyBot")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and "emotion" in message:

            st.caption(
                f"Estimated Emotion: "
                f"{message['emotion'].title()} | "
                f"Model Score: {message['confidence']:.2%}"
            )


# User input
user_message = st.chat_input(
    "Write your message here..."
)

# Process user message
if user_message:

    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your emotions..."):

            try:

                # Detect emotion
                result = detect_emotion(user_message)

                emotion = result["emotion"]
                confidence = result["confidence"]

                # Generate empathetic response
                reply = generate_adaptive_response(
                        user_message,
                        emotion,
                        confidence
                )

                st.markdown(reply)

                st.caption(
                    f"Estimated Emotion: {emotion.title()} | "
                    f"Model Score: {confidence:.2%}"
                )

                # Save detected emotion
                st.session_state.emotion_history.append(emotion)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply,
                    "emotion": emotion,
                    "confidence": confidence
                })

            except Exception as error:

                reply = (
                    "Sorry, I couldn't analyze your message. "
                    "Please try again."
                )

                st.error(f"Analysis error: {error}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

    # Refresh dashboard after processing the message
    st.rerun()
