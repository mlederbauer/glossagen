"""Module for extracting and generating glossaries from research documents."""

import re
from typing import Any, Dict, Optional

import dspy
from pydantic import BaseModel, Field

import wandb
from glossagen.utils import ResearchDoc, ResearchDocLoader, init_dspy


class TerminusTechnicus(BaseModel):
    """A terminus technicus, i.e. a techincal term in materials science and chemistry."""

    term: str = Field(..., title="The technical term.")
    definition: str = Field(..., title="The definition of the technical term.")


class Text2GlossarySignature(dspy.Signature):
    """Generating a list of termini technici from a text in materials science and chemistry."""

    text: str = dspy.InputField(desc="The text to extract the termini technici from.")
    glossary: list[TerminusTechnicus] = dspy.OutputField(
        desc="The list of termini technici extracted from the text."
    )


class GlossaryGenerator:
    """
    A class that generates a glossary based on a research document.

    Attributes
    ----------
        research_doc (ResearchDoc): The research document to generate the glossary from.
        glossary_predictor (dspy.Predict): The predictor used to generate the glossary.

    Methods
    -------
        generate_glossary: Generates the glossary based on the research document.

    """

    def __init__(self, research_doc: ResearchDoc):
        """
        Initialize a GlossaryGenerator object.

        Args:
            research_doc (ResearchDoc): The research document to generate the glossary from.

        """
        self.research_doc = research_doc
        self.glossary_predictor = dspy.TypedPredictor(Text2GlossarySignature)

    def normalize_term(self, term: str) -> str:
        """Normalize a term by converting it to lowercase and removing common plural endings."""
        term = term.lower().strip()
        # Remove common plural endings
        if term.endswith("ies"):
            term = re.sub("ies$", "y", term)
        elif term.endswith("es"):
            term = re.sub("es$", "e", term)
        elif term.endswith("s"):
            term = term[:-1]
        return term

    def deduplicate_entries(self, glossary: list[TerminusTechnicus]) -> list[TerminusTechnicus]:
        """Deduplicate the glossary entries by considering plurals and similar-sounding terms."""
        normalized_terms = set()
        deduplicated_glossary = []

        for term in glossary:
            normalized = self.normalize_term(term.term)
            if normalized not in normalized_terms:
                normalized_terms.add(normalized)
                deduplicated_glossary.append(term)
        return deduplicated_glossary

    def format_nicely(self, glossary: list[TerminusTechnicus]) -> str:
        """
        Format the glossary nicely.

        Args:
            glossary (list[TerminusTechnicus]): The glossary to format.

        Returns
        -------
            str: The nicely formatted glossary.

        """
        formatted_glossary = ""
        for i, term in enumerate(glossary):
            formatted_glossary += f"{i+1}. {term.term}: {term.definition}\n"
        return formatted_glossary

    def generate_glossary_from_doc(self) -> Any:
        """
        Generate the glossary based on the research document.

        Returns
        -------
            Any: The generated glossary.

        """
        init_dspy()
        total_text = self.research_doc.paper
        parts = 100
        part_length = len(total_text) // parts
        print("Extracting glossary from the text...")
        print(f"Total text length: {len(total_text)}")
        print(f"Part length: {part_length}")
        combined_glossary = []

        for i in range(parts):
            start_index = i * part_length
            end_index = (
                (i + 1) * part_length if i < (parts - 1) else len(total_text)
            )  # Adjust the end index for the last part
            part_text = total_text[start_index:end_index]
            glossary_part = self.glossary_predictor(text=part_text)
            combined_glossary.extend(glossary_part.glossary)

        combined_glossary_deduplicate = self.deduplicate_entries(combined_glossary)

        log_to_wandb(combined_glossary_deduplicate)

        return self.format_nicely(combined_glossary_deduplicate)


def log_to_wandb(
    glossary: list[TerminusTechnicus],
    project_name: str = "GlossaGen",
    config: Optional[Dict[Any, Any]] = None,
) -> None:
    """
    Initialize wandb and log the generated glossary as a wandb.Table.

    Args:
        glossary (list[TerminusTechnicus]): The list of glossary terms to log.
        project_name (str): The name of the wandb project.
        config (dict): Configuration parameters for the wandb run.
    """
    # Initialize wandb
    wandb.init(project=project_name, config=config)

    # Prepare data for wandb.Table
    table_data = [[term.term, term.definition] for term in glossary]
    glossary_table = wandb.Table(columns=["Term", "Definition"], data=table_data)  # type: ignore

    # Log the glossary table
    wandb.log({"Generated Glossary": glossary_table})

    # Finish the wandb run
    wandb.finish()


def generate_glossary(document_directory: str, log_to_wandb_flag: bool = True) -> Any:
    """
    Generate a glossary based on a research document.

    Args:
        document_directory (str): The directory where the research document is stored.

    Returns
    -------
        str: The generated glossary.

    """
    init_dspy()

    loader = ResearchDocLoader(document_directory)
    research_doc = loader.load()
    research_doc.extract_metadata()

    print("--------------------------------------------------")
    print("Extracted Metadata:")
    for key, value in research_doc.metadata_dict.items():
        print(f"{key}: {value}")
    print("--------------------------------------------------")
    print("Paper Text:", research_doc.paper[:1000])

    glossary_generator = GlossaryGenerator(research_doc)
    glossary = glossary_generator.generate_glossary_from_doc()

    print("Generated Glossary:")
    print(glossary)

    return glossary


def main() -> None:
    """Demonstrate the generation of a glossary from a research document."""
    document_directory = "/Users/magdalenalederbauer/projects/glossagen/data/"
    generate_glossary(document_directory)


if __name__ == "__main__":
    main()
