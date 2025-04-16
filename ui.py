# ui.py
import re
import gradio as gr
import json
from app import generate_content


# Sanitize filesnames
def sanitize_filename(text):
    # Basic sanitization to make a filesystem-friendly filename
    return re.sub(r"\W+", "_", text.strip().lower())[:50]


# Parse output into content and SEO fields
def parse_output(full_text):
    # Simple parsing based on line breaks
    parts = full_text.strip().split("\n")

    # Heuristically separate sections (works for GPT output with 1., 2., 3.)
    tags = ""
    keyphrase = ""
    meta_description = ""
    content_lines = []

    for line in parts:
        if line.strip().startswith("1."):
            tags = line.split("1.", 1)[-1].strip()
        elif line.strip().startswith("2."):
            keyphrase = line.split("2.", 1)[-1].strip()
        elif line.strip().startswith("3."):
            meta_description = line.split("3.", 1)[-1].strip()
        else:
            if not any(x in line for x in ["1.", "2.", "3."]):
                content_lines.append(line)

    main_content = "\n".join(content_lines).strip()
    return main_content, tags, keyphrase, meta_description


def generate(topic, content_type):
    try:
        result = generate_content(topic, content_type)
        return result, result  # One for Markdown preview, one for file download
    except Exception as e:
        err = f"❌ Error: {str(e)}"
        return err, None


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
    main_content, tags, keyphrase, meta_description = parse_output(content)

    # Save content and metadata
    sanitized_topic = sanitize_filename(topic)
    filename = f"{sanitized_topic}_{content_type.replace(' ', '_')}.txt"
    metadata_filename = f"{sanitized_topic}_{content_type.replace(' ', '_')}.meta.json"

    with open(filename, "w") as f:
        f.write(content)

        metadata = {
            "title": topic,
            "content_type": content_type,
            "tags": [tag.strip() for tag in tags.split(",")],
            "focus_keyphrase": keyphrase,
            "meta_description": meta_description,
        }

    with open(metadata_filename, "w") as meta_file:
        json.dump(metadata, meta_file, indent=2)

    return content, filename, tags, keyphrase, meta_description


# Clear/reset logic
def reset_fields():
    return "", None, None, "", "", "0 / 100", "0 / 400", "0 / 400", "", "", ""


# character count helper
def count_chars(text, max_len):
    return f"{len(text)}/{max_len}"


# Build the gradio UI
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

    md_output = gr.Markdown(label="Markdown Preview")

    with gr.Row():
        download_output = gr.File(
            label="Download Generated Content (.txt)", file_types=[".txt"]
        )

    with gr.Row():
        tags_output = gr.Textbox(label="Tags", interactive=False, lines=1)
        keyphrase_output = gr.Textbox(
            label="Focus Keyphrase", interactive=False, lines=1
        )
        meta_output = gr.Textbox(label="Meta Description", interactive=False, lines=1)

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
    generate_btn.click(
        fn=process_and_create_file,
        inputs=[topic_input, content_type, system_prompt_input, human_prompt_input],
        outputs=[
            md_output,
            download_output,
            tags_output,
            keyphrase_output,
            meta_output,
        ],
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
            topic_counter,
            system_counter,
            human_counter,
            tags_output,
            keyphrase_output,
            meta_output,
        ],
    )


if __name__ == "__main__":
    demo.launch()
