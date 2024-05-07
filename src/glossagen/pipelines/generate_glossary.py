"""Module for extracting and generating glossaries from research documents."""

from typing import Any

import dspy

from glossagen.utils import ResearchDoc, ResearchDocLoader, init_dspy


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
        self.glossary_predictor = dspy.Predict("text -> glossary")

    def generate_glossary(self) -> Any:
        """
        Generate the glossary based on the research document.

        Returns
        -------
            Any: The generated glossary.

        """
        init_dspy()
        total_text = self.research_doc.paper
        part_length = len(total_text) // 100
        print("Total Text Length:", len(total_text))
        print("Part Length:", part_length)
        glossary = self.glossary_predictor(text=total_text[:part_length])
        return glossary


def main() -> None:
    """Demonstrate the usage of the ResearchDoc class."""
    document_directory = "/Users/magdalenalederbauer/projects/glossagen/data/"
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
    glossary = glossary_generator.generate_glossary()
    print("Generated Glossary:")
    print(glossary)


if __name__ == "__main__":
    main()
