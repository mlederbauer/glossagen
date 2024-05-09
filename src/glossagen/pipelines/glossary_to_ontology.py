import re
from typing import Any, Dict, Optional

import dspy
from pydantic import BaseModel, Field

import wandb
from glossagen.utils import ResearchDoc, ResearchDocLoader, init_dspy

class Glossary(BaseModel):
    """A research paper."""

    glossary_text: str

    # class Config:
    #     """Pydantic configuration for the ResearchDoc class."""

    #     arbitrary_types_allowed = True
    #     orm_mode=True

    @classmethod
    def from_dict(cls, glossary_dict: Dict[str,str]) -> "Glossary":
        """
        Create a ResearchDoc instance from text.

        Args:
            text (str): The text of the research paper.
            doc_src (str): The source of the document.

        Returns
        -------
            ResearchDoc: The created ResearchDoc instance.
        """
        glossary_text = "\n".join(f"{key}: {value}" for key, value in glossary_dict.items())

        glossary = cls(glossary_text=glossary_text)
        return glossary

class OntologyEntityLabels(BaseModel):
    """An ontology label, i.e. an entity label in materials science and chemistry."""

    entity: str = Field(..., title="A string label describing a entity class.")


class OntologyRelation(BaseModel):
    """An ontology relation, i.e. a relation between two entities in materials science and chemistry."""

    relation: str = Field(..., title="A relation type of the ontology.")

class Glossary2Entities(dspy.Signature):
    """Generating a list of entities labels (general overarching classes, e.g. Material, Process, Property, ...) from glossary term and description pairs."""

    input_text: str = dspy.InputField(desc="Glossary term and description pairs, one by line.")
    entities: list[OntologyEntityLabels] = dspy.OutputField(
        desc="List of general labels categorizing the terms."
    )

class Glossary2Relations(dspy.Signature):
    """Generating a list of relations (single verb) between entities from glossary term and description pairs."""

    input_text: str = dspy.InputField(desc="Glossary term and description pairs, one by line.")
    relations: list[OntologyRelation] = dspy.OutputField(
        desc="List of general relations between glossary terms for an ontology. Short terms or verbs describing the relation."
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

    def __init__(self, glossary_text: str):
        """
        Initialize a GlossaryGenerator object.

        Args:
            research_doc (ResearchDoc): The research document to generate the glossary from.
            chunk_size (int): The size of the chunks to split the research document into.

        """
        self.glossary_text = glossary_text.glossary_text
        self.relations_predictor = dspy.TypedPredictor(Glossary2Relations)
        self.entities_predictor = dspy.TypedPredictor(Glossary2Entities)


    def generate_ontology_from_glossary(self) -> Any:
        """
        Generate the glossary based on the research document.

        Returns
        -------
            Any: The generated glossary.

        """
        init_dspy()
        entities = self.entities_predictor(input_text=self.glossary_text)
        relations = self.relations_predictor(input_text=self.glossary_text)

        print(entities)

        print(relations)

        return entities

if __name__ == '__main__':

    example_glossary = {
        "Zeolite": "An aluminosilicate compound with a wide range of applications in medicine and dentistry, known for its distinct porous structure and ability to accommodate cations, hydroxyl groups, and water molecules.",
        "Ion-embedded zeolites": "Zeolites containing ions that can act as potential antibacterial agents against pathogenic oral microbes by interfering with their metabolic activity.",
        "AgZ": "Silver zeolite: Zeolite incorporating silver ions, used in restorative materials, dental liners, and root canal irrigation for its antibacterial properties.",
        "Chlorhexidine zeolite": "Zeolite combined with chlorhexidine, utilized in root canal irrigation due to its antibacterial properties.",
        "Zeolite coating": "A coating of zeolite applied to dental implants to enhance osseointegration.",
        "Glass Ionomer Cements (GIC)": "Dental cements incorporating ion-embedded zeolites for antibacterial activity, commonly used in various dental applications.",
        "Mineral Trioxide Aggregate (MTA)": "A dental material where the addition of zeolites, such as AgZ, enhances antibacterial activity against oral microorganisms.",
        "Root Canal Irrigation Solutions": "Solutions containing zeolites, like AgZ, used for their antibacterial efficacy in root canal treatments.",
        "Acrylic Resins with Zeolites": "Acrylic resins incorporating zeolites, such as AgZ and Ag-Zn-Ze, to improve antibacterial properties against oral pathogens.",
        "Implant Coatings with Zeolites": "Antibacterial coatings containing zeolites, like AgZ, applied to implants to prevent microbial growth, particularly effective against MRSA.",
        "Volatile Organic Compounds (VOCs)": "Organic chemicals emitted by the human body, used in studies for detecting medical conditions, including cancer markers.",
        "Antimicrobial Activity": "The ability of a substance to inhibit or kill microorganisms such as bacteria, viruses, or fungi.",
        "Mechanical Properties": "The characteristics of a material related to its behavior under applied forces, including strength, hardness, elasticity, and toughness.",
        "GIC": "Glass Ionomer Cement, a dental restorative material known for its fluoride release and adhesion to tooth structure.",
        "MTA": "Mineral Trioxide Aggregate, a bioactive material used in endodontic procedures for root canal treatments.",
        "AgZ Incorporation": "Incorporation of silver zeolites into materials for enhanced antimicrobial properties.",
        "Root Canal Irrigation": "The process of flushing and disinfecting the root canal system during endodontic treatment."
    }

    ontogen = OntologyGenerator(Glossary.from_dict(glossary_dict=example_glossary))

    ontogen.generate_ontology_from_glossary()


