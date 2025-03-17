# ui.py
import gradio as gr
from app import generate_content


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

    with gr.Row():
        md_output = gr.Markdown(label="Markdown Preview")

    with gr.Row():
        download_output = gr.File(label="Download Generated Content (.txt)")

    # Handle click event
    def process_and_create_file(topic, content_type):
        content, _ = generate(topic, content_type)
        # Save to file dynamically
        if "Error" in content:
            return content, None
        filename = "generated_content.txt"
        with open(filename, "w") as f:
            f.write(content)
        return content, filename

    generate_btn.click(
        fn=process_and_create_file,
        inputs=[topic_input, content_type],
        outputs=[md_output, download_output],
    )

if __name__ == "__main__":
    demo.launch()
