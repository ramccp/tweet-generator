import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

tweet_template = '''Generate exactly {number}-tweet(s) about {topic} with appropriate hashtags and suggest the details to be posted in the image for that tweet, separate the tweets with a divider and follow the following format:
### Tweet 1

Content to be posted in the tweet

#### Image Suggestion

Suggest the details to be posted in the image for that tweet

Divider

And do not include any other text in your response.'''

tweet_prompt = PromptTemplate(template=tweet_template, input_variables=["number", "topic"])

llm = ChatGroq(model_name="meta-llama/llama-4-maverick-17b-128e-instruct")

chain = tweet_prompt | llm

# Frontend
st.header("Tweet Generator 🐥")
st.subheader("Generate tweets using Generative AI")

topic = st.text_input("Topic")
number = st.number_input(
    "Number of tweets", 
    min_value=1, 
    max_value=10, 
    value=1, 
    step=1,
    format="%d",  # Integer format only
    help="Enter a number between 1 and 20"
)

button = st.button("Generate")

if button:
    # Validate both topic and number
    if not topic or topic.strip() == "":
        st.error("Please enter a topic for the tweets.")
    elif int(number) < 1:
        st.error("Please enter a number greater than 0.")
    else:
        # Show generating message
        if int(number) == 1:
            st.write("Generating tweet...")
        else:
            st.write("Generating tweets...")
        
        try:
            # Generate tweets
            response = chain.invoke({"number": int(number), "topic": topic.strip()})
            st.write(response.content)
        except Exception as e:
            st.error(f"An error occurred while generating tweets: {str(e)}")