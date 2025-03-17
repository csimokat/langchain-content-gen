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
            label="Enter Topic (max 100 characters)",
            placeholder="e.g., AI for healthcare",
            max_lines=1,
        )
        topic_counter = gr.Markdown("0 / 100")

    with gr.Row():
        content_type = gr.Radio(["blog", "social media"], label="Select Content Type")

    # Advanced collapsible section
    with gr.Accordion("⚙️ Advanced Settings: Customize Prompts", open=False):
        gr.Markdown(
            "💡 **Tip:** If you customize the human prompt, be sure to include `{topic}` where you want the user's topic to be inserted."
        )

        system_prompt_input = gr.Textbox(
            label="System Prompt (Optional, max 400 characters)",
            placeholder="Leave empty for default system prompt",
            lines=3,
        )
        system_counter = gr.Markdown("0 / 400")

        human_prompt_input = gr.Textbox(
            label="Human Prompt (Optional, max 400 characters)",
            placeholder="Leave empty for default human prompt",
            lines=3,
        )
        human_counter = gr.Markdown("0 / 400")

    with gr.Row():
        generate_btn = gr.Button("Generate Content")
        clear_btn = gr.Button("Clear All")

    with gr.Row():
        md_output = gr.Markdown(label="Markdown Preview")

    with gr.Row():
        download_output = gr.File(label="Download Generated Content (.txt)")

    # Live char counters:
    topic_input.change(
        fn=lambda t: count_chars(t, 100), inputs=topic_input, outputs=topic_counter
    )
    system_prompt_input.change(
        fn=lambda s: count_chars(s, 400),
        inputs=system_prompt_input,
        outputs=system_counter,
    )
    human_prompt_input.change(
        fn=lambda h: count_chars(h, 400),
        inputs=human_prompt_input,
        outputs=human_counter,
    )


# Handle click event
# Generation logic with filename auto-generator
def process_and_create_file(topic, content_type, system_prompt, human_prompt):
    # Input length validation
    if len(topic.strip()) > 100:
        return "⚠️ Error: Topic must be under 100 characters.", None
    if system_prompt and len(system_prompt.strip()) > 400:
        return "⚠️ Error: System prompt must be under 400 characters.", None
    if human_prompt and len(human_prompt.strip()) > 400:
        return "⚠️ Error: Human prompt must be under 400 characters.", None

    # Validate that {topic} exists in custom human prompt (if provided)
    if human_prompt and "{topic}" not in human_prompt:
        return (
            "⚠️ Error: Your custom human prompt must include `{topic}` somewhere!",
            None,
        )

    content = generate_content(topic, content_type, system_prompt, human_prompt)
    if "Error" in content:
        return content, None

    sanitized_topic = sanitize_filename(topic)
    filename = f"{sanitized_topic}_{content_type.replace(' ', '_')}.txt"

    with open(filename, "w") as f:
        f.write(content)
    return content, filename


# Clear/reset logic
def reset_fields():
    return "", None, None, "", "", "0 / 100", "0 / 400", "0 / 400"


def count_chars(text, max_len):
    return f"{len(text)}/{max_len}"

    generate_btn.click(
        fn=process_and_create_file,
        inputs=[topic_input, content_type, system_prompt_input, human_prompt_input],
        outputs=[md_output, download_output],
    )

    clear_btn.click(
        fn=reset_fields,
        inputs=[],
        outputs=[
            topic_input,
            md_output,
            download_output,
            system_prompt_input,
            human_prompt_input,
        ],
    )


if __name__ == "__main__":
    demo.launch()
