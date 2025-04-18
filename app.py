import os
from getpass import getpass
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OpenAI API key from env file
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Set your OpenAI API key
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass("Enter your OpenAI API key: ")

# Initialize the OpenAI chat model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# Default system + human templates
DEFAULT_BLOG_SYSTEM = (
    "You are a skilled writer who creates engaging and informative blog posts."
)
DEFAULT_BLOG_HUMAN = (
    "Write a detailed blog post about {topic}.\n\n"
    "Then, provide the following:\n"
    "1. A comma-separated list of SEO tags\n"
    "2. A short focus keyphrase (1 line)\n"
    "3. A meta description (1–2 sentences)"
)

DEFAULT_SOCIAL_SYSTEM = (
    "You are a creative writer who crafts catchy and concise social media posts."
)
DEFAULT_SOCIAL_HUMAN = (
    "Write a compelling social media post about {topic}.\n\n"
    "Then, provide the following:\n"
    "1. A comma-separated list of SEO tags\n"
    "2. A short focus keyphrase (1 line)\n"
    "3. A meta description (1–2 sentences)"
)


def generate_content(topic, content_type, system_prompt=None, human_prompt=None):
    if content_type == "blog":
        system_prompt = system_prompt or DEFAULT_BLOG_SYSTEM
        human_prompt = human_prompt or DEFAULT_BLOG_HUMAN
    elif content_type == "social media":
        system_prompt = system_prompt or DEFAULT_SOCIAL_SYSTEM
        human_prompt = human_prompt or DEFAULT_SOCIAL_HUMAN
    else:
        raise ValueError("Invalid content type. Choose 'blog' or 'social media'.")

    # Create the prompt dynamically
    custom_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("human", human_prompt)]
    )

    chain = custom_template | llm
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
