"""App to generate a glossary from a research paper PDF."""

import base64

import gradio as gr
from glossagen.pipelines import (
    GlossaryGenerator,  # Replace 'your_module' with the actual import path
)
from glossagen.utils import ResearchDocLoader


def image_to_data_uri(filepath):
    """Convert an image file to a data URI."""
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"


image_data_uri = image_to_data_uri("assets/glossagen-logo.png")
logo_html = (
    f"<img src='{image_data_uri}' alt='GlossaGen Logo' style='max-width:10%;"
    + " height:auto; display:block; margin-left:auto; margin-right:auto;'/>"
)


def process_pdf(file_path):
    """Process the uploaded PDF file."""
    # Load the PDF and generate the glossary
    # delete the last paper.pdf from the path
    file_path = file_path[:-9]
    loader = ResearchDocLoader(file_path)
    research_doc = loader.load()
    research_doc.extract_metadata()  # Optional, if you need metadata displayed or logged

    glossary_generator = GlossaryGenerator(research_doc)
    glossary_text = glossary_generator.generate_glossary_from_doc()

    with open(f"{file_path}/paper.pdf", "rb") as file:
        pdf_data = file.read()
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        pdf_html = (
            f'<embed src="data:application/pdf;base64,{base64_pdf}"'
            f' width="100%" height="600" type="application/pdf">'
        )

    return pdf_html, glossary_text


with gr.Blocks() as demo:
    gr.Markdown(logo_html)
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload PDF", type="filepath")
            pdf_viewer = gr.HTML()
        with gr.Column():
            glossary_display = gr.HTML()

    file_input.change(fn=process_pdf, inputs=file_input, outputs=[pdf_viewer, glossary_display])

demo.launch()
