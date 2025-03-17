# ui.py
import re
import gradio as gr
from app import generate_content


def sanitize_filename(text):
    # Basic sanitization to make a filesystem-friendly filename
    return re.sub(r"\W+", "_", text.strip().lower())[:50]


def generate(topic, content_type):
    try:
        result = generate_content(topic, content_type)
        return result, result  # One for Markdown preview, one for file download
    except Exception as e:
        err = f"❌ Error: {str(e)}"
        return err, None


with gr.Blocks() as demo:
    gr.Markdown("# ✨ LangChain Content Generator UI")
    gr.Markdown(
        "Generate **Blog Posts** or **Social Media Posts** with OpenAI + LangChain 🚀"
    )

    with gr.Row():
        topic_input = gr.Textbox(
            label="Enter Topic", placeholder="e.g., AI for healthcare"
        )

    with gr.Row():
        content_type = gr.Radio(["blog", "social media"], label="Select Content Type")

    with gr.Row():
        generate_btn = gr.Button("Generate Content")
        clear_btn = gr.Button("Clear All")

    with gr.Row():
        md_output = gr.Markdown(label="Markdown Preview")

    with gr.Row():
        download_output = gr.File(label="Download Generated Content (.txt)")

    # Handle click event
    # Generation logic with filename auto-generator
    def process_and_create_file(topic, content_type):
        content, _ = generate(topic, content_type)
        if "Error" in content:
            return content, None

        sanitized_topic = sanitize_filename(topic)
        filename = f"{sanitized_topic}_{content_type.replace(' ', '_')}.txt"

        with open(filename, "w") as f:
            f.write(content)
        return content, filename

    # Clear/reset logic
    def reset_fields():
        return "", None, None

    generate_btn.click(
        fn=process_and_create_file,
        inputs=[topic_input, content_type],
        outputs=[md_output, download_output],
    )

    clear_btn.click(
        fn=reset_fields, inputs=[], outputs=[topic_input, md_output, download_output]
    )

if __name__ == "__main__":
    demo.launch()
