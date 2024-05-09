"""Gradio interface to display a PDF file uploaded by the user."""

import base64
import os

import gradio as gr


def display_pdf(file_path):
    """Read a PDF file and returns an HTML embed tag to display it in Gradio."""
    print("Uploaded file path:", file_path)
    if os.path.exists(file_path):
        print("File exists. Size:", os.path.getsize(file_path), "bytes")
    else:
        print("File does not exist.")
        return "File does not exist or path is incorrect."

    try:
        with open(file_path, "rb") as file:
            file_content = file.read()
            if not file_content:
                print("File is empty.")
                return "The uploaded file is empty."
            print("Read", len(file_content), "bytes.")
    except Exception as e:
        print("Failed to read file:", e)
        return "Failed to read the file."

    try:
        b64_pdf = base64.b64encode(file_content).decode("utf-8")
        pdf_html = f'<embed src="data:application/pdf;base64,{b64_pdf}" width="100%" height="600" type="application/pdf">'  # noqa
        print("PDF encoded in base64.")
    except Exception as e:
        print("Failed to encode file:", e)
        return "Failed to encode the file."

    return pdf_html


iface = gr.Interface(
    fn=display_pdf,
    inputs=gr.File(label="Drag and Drop or Click to Upload PDF", type="filepath"),
    outputs=gr.components.HTML(label="Uploaded PDF"),
)

iface.launch(debug=True)
