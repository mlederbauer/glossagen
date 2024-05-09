"""GUI for GlossaGen."""

import base64
from typing import Iterable

import gradio as gr  # type: ignore[attr-defined]
from glossagen.pipelines import GlossaryGenerator
from glossagen.utils import ResearchDocLoader
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

glossacol = colors.Color(
    name="glossacol",
    c50="#56B1D5",
    c100="#56B1D5",
    c200="#FFFFFF",
    c300="#56B1D5",
    c400="#56B1D5",
    c500="#56B1D5",
    c600="#3479A5",
    c700="#174B7B",
    c800="#174B7B",
    c900="#174B7B",
    c950="#174B7B",
)


class GlossaFoam(Base):
    """A custom theme for GlossaGen."""

    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.pink,
        secondary_hue: colors.Color | str = colors.pink,
        neutral_hue: colors.Color | str = glossacol,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Sans"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font | str | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Sans"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )


glossafoam = GlossaFoam()


def image_to_data_uri(filepath: str) -> str:
    """Convert an image file to a data URI."""
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"


image_data_uri = image_to_data_uri("assets/glossagen-logo-text.png")
logo_html = (
    f"<img src='{image_data_uri}' alt='GlossaGen Logo' style='max-width:30%;"
    + " height:auto; display:block; margin-left:auto; margin-right:auto;'/>"
)


def process_pdf(file_path: str) -> tuple[str, str]:
    """Process the uploaded PDF file."""
    loader = ResearchDocLoader(file_path[: file_path.rfind("/")])
    research_doc = loader.load()
    research_doc.extract_metadata()

    glossary_generator = GlossaryGenerator(research_doc)
    glossary_df = glossary_generator.generate_glossary_from_doc()[["Term", "Definition"]]

    # Limiting glossary_df to show the first 9 lines
    glossary_html = glossary_df.head(9).to_html(index=False)
    # Adding a scrollbar for the rest of the glossary
    glossary_html += "<style>table{height: 200px; overflow-y: scroll;}</style>"

    with open(f"{file_path}", "rb") as file:
        pdf_data = file.read()
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")
        pdf_html = (
            f'<embed src="data:application/pdf;base64,{base64_pdf}"'
            f' width="100%" height="600" type="application/pdf">'
        )

    return pdf_html, glossary_html


# Function to copy glossary to clipboard
def copy_to_clipboard(text):
    """Copy the text to the clipboard."""
    import pyperclip

    pyperclip.copy(text)


# Function to export glossary to LaTeX table
def export_to_latex(glossary_df):
    """Export the glossary to a LaTeX table."""
    latex_table = glossary_df.to_latex(index=False)
    return latex_table


# Function to export glossary to .csv
def export_to_csv(glossary_df):
    """Export the glossary to a .csv file."""
    glossary_df.to_csv("glossary.csv", index=False)
    return "glossary.csv"


def generate_knowledge_graph(glossary_df):
    """Generate a knowledge graph based on the glossary."""
    # TODO: add logic to implement graph_maker library like in notebook
    return "Foo"


with gr.Blocks(theme=glossafoam, css=".gradio-container {background-color: white}") as demo:
    gr.Markdown(logo_html)
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload PDF", type="filepath")
            pdf_viewer = gr.HTML()
        with gr.Column():
            glossary_display = gr.HTML()

            with gr.Row():
                with gr.Column():
                    # Adding buttons for actions
                    copy_button = gr.Button(
                        "Copy to Clipboard"
                    )  # , copy_to_clipboard, inputs=glossary_display)
                    latex_button = gr.Button("Export to LaTeX table")
                    # , export_to_latex, inputs=[glossary_display],
                    # outputs=gr.Textbox(label="LaTeX Table"))
                    csv_button = gr.Button("Export to .csv")
                    # , export_to_csv, inputs=[glossary_display],
                    # outputs=gr.Textbox(label="Download CSV file"))

                # Generate knowledge graph button
                generate_button = gr.Button(
                    "Generate Knowledge Graph"
                )  # , action=generate_knowledge_graph, inputs=glossary_display)

    file_input.change(fn=process_pdf, inputs=file_input, outputs=[pdf_viewer, glossary_display])

demo.launch()
