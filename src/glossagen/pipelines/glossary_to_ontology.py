"""Module to generate an ontology from a glossary."""

from typing import Any, Dict, List

import dspy
from pydantic import BaseModel, Field

from glossagen.pipelines import generate_glossary
from glossagen.utils import init_dspy


def generate_ontology_from_glossary(document_directory: str) -> Any:
    """Generate ontology from a glossary.

    Args:
        document_directory (str): The directory containing the research documents.

    Returns
    -------
        Any: The generated ontology.
    """
    glossary = generate_glossary(document_directory).set_index("Term").to_dict()["Definition"]
    ontogen = OntologyGenerator(glossary)
    return ontogen.generate_ontology_from_glossary()


class OntologyEntityLabels(BaseModel):
    """An ontology label, i.e. an entity label in materials science and chemistry."""

    label: str = Field(..., title="A string 'label: description'  describing a entity class.")


class OntologyRelation(BaseModel):
    """Ontology relation, i.e. relation between two entities."""

    relation: str = Field(..., title="A relation type of the ontology.")


class Glossary2Labels(dspy.Signature):
    """Generating a list of entities labels (general overarching classes, e.g. Material, Property, ..., Other) from glossary term and description pairs."""  # noqa

    input_text: str = dspy.InputField(desc="Glossary term and description pairs, one by line.")
    labels: list[OntologyEntityLabels] = dspy.OutputField(
        desc="List of general labels categorizing the terms."
    )


class Glossary2Relations(dspy.Signature):
    """Generating a list of relations (single verb) between entities from glossary term and description pairs."""  # noqa

    input_text: str = dspy.InputField(desc="Glossary term and description pairs, one by line.")
    relations: list[OntologyRelation] = dspy.OutputField(
        desc="""
        List of general relations between glossary terms for an ontology.
        Short terms or verbs describing the relation."""
    )


class OntologyGenerator:
    """
    A class that generates a ontology based on a glossary.

    Attributes
    ----------
        research_doc (ResearchDoc): The research document to generate the glossary from.
        glossary_predictor (dspy.Predict): The predictor used to generate the glossary.

    Methods
    -------
        generate_glossary: Generates the glossary based on the research document.

    """

    def __init__(self, glossary: Dict[str, str]):
        """
        Initialize a GlossaryGenerator object.

        Args:
            research_doc (ResearchDoc): The research document to generate the glossary from.
            chunk_size (int): The size of the chunks to split the research document into.

        """
        self.glossary_text = "\n".join(f"{key}: {value}" for key, value in glossary.items())
        self.relations_predictor = dspy.TypedPredictor(Glossary2Relations)
        self.labels_predictor = dspy.TypedPredictor(Glossary2Labels)

    def generate_ontology_from_glossary(self, verbose: bool = False) -> Any:
        """
        Generate the glossary based on the research document.

        Returns
        -------
            Any: The generated glossary.

        """
        init_dspy()
        predicted_labels = self.labels_predictor(input_text=self.glossary_text)
        predicted_relations = self.relations_predictor(input_text=self.glossary_text)

        label_dict = {
            label.label.split(":")[0].strip(): label.label.split(":")[1].strip()
            for label in predicted_labels["labels"]
        }
        relations = [relation.relation for relation in predicted_relations["relations"]]

        if verbose:
            print(label_dict)
            print(relations)

        return Ontology(labels=label_dict, relationships=relations)


class Ontology(BaseModel):
    """Represent an ontology with labels and relationships."""

    labels: Dict[str, str]
    relationships: List[str]

    def print_labels(self):
        """Print all the labels in the ontology."""
        for key, value in self.labels.items():
            print(f"{key}: {value}")

    def print_relationships(self):
        """Print all the relationships in the ontology."""
        for relation in self.relationships:
            print(relation)


if __name__ == "__main__":
    document_directory = "./data/"
    example_glossary = (
        generate_glossary(document_directory).set_index("Term").to_dict()["Definition"]
    )
    ontogen = OntologyGenerator(example_glossary)
    ontology = ontogen.generate_ontology_from_glossary()

    # Print labels and relationships if needed
    ontology.print_labels()
    ontology.print_relationships()
