import os
from getpass import getpass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OpenAI API key from env file
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project directory explicitly
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# temporary debugging print
# print(f"OPENAI_API_KEY from .env: {os.getenv('OPENAI_API_KEY')}")

# Set your OpenAI API key
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API key: ")

# Initialize the OpenAI chat model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Define prompt templates for blog and social media posts
blog_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a skilled writer who creates engaging and informative blog posts.",
        ),
        ("human", "Write a detailed blog post about {topic}."),
    ]
)

social_media_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a creative writer who crafts catchy and concise social media posts.",
        ),
        ("human", "Write a compelling social media post about {topic}."),
    ]
)


def generate_content(topic, content_type):
    if content_type == "blog":
        chain = blog_prompt_template | llm
    elif content_type == "social media":
        chain = social_media_prompt_template | llm
    else:
        raise ValueError("Invalid content type. Choose 'blog' or 'social media'.")

    response = chain.invoke({"topic": topic})
    return response.content


def main():
    # Get user input for the topic
    topic = input("Enter the topic you want to create content about: ")

    # Get user input for the type of content
    content_type = (
        input("Enter the type of content to create ('blog' or 'social media'): ")
        .strip()
        .lower()
    )

    # Generate and display the content
    try:
        content = generate_content(topic, content_type)
        print("\nGenerated Content:\n")
        print(content)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
