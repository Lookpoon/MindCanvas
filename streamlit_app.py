import streamlit as st
import openai
from PIL import Image

# Display title and description
st.title("🖼️ Image Emotion Prediction")
st.write(
    "Upload an image and provide a brief description – GPT will predict the emotion it conveys! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask the user for their OpenAI API key
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Set OpenAI API key
    openai.api_key = openai_api_key

    # Let the user upload an image file
    uploaded_image = st.file_uploader("Upload an image (JPG, JPEG, or PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Ask the user to provide a description of the image
        image_description = st.text_area(
            "Describe the image briefly for better context (e.g., 'A cat sitting in the snow looking calm')",
            placeholder="Enter a brief description of the image"
        )

        # List of emotions to classify
        emotions = ["awe", "amusement", "contentment", "excitement", "disgust", "fear", "sadness"]

        if image_description:
            # Prepare the prompt for the GPT model
            prompt = (
                f"Based on the following description of an image, classify the emotion it conveys "
                f"from these options: {', '.join(emotions)}.\n\n"
                f"Description: {image_description}\n\nEmotion:"
            )

            # Generate an emotion prediction using the GPT API
            with st.spinner("Analyzing emotion..."):
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=10,
                    temperature=0.5
                )
                predicted_emotion = response.choices[0].text.strip()

            # Display the predicted emotion
            st.success(f"Predicted Emotion: {predicted_emotion}")

