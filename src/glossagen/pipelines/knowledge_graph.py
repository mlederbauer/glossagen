"""Pipeline to generate a knowledge graph from research documents."""

import datetime
import os
from typing import List

from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI

from glossagen.utils import ResearchDocLoader

load_dotenv()
os.environ["NEO4J_URI"] = os.getenv("NEO4J_URI", "")
os.environ["NEO4J_USERNAME"] = os.getenv("NEO4J_USERNAME", "")
os.environ["NEO4J_PASSWORD"] = os.getenv("NEO4J_PASSWORD", "")


def create_documents_from_text_chunks(text: str, max_length: int = 2000) -> List[Document]:
    """Create documents from text by dividing it into chunks of max_length characters."""
    current_time = str(datetime.datetime.now())
    documents = []
    for start in range(0, len(text), max_length):
        # Extract a substring from the text starting at 'start' up to 'start+max_length'
        chunk = text[start : start + max_length]
        documents.append(Document(page_content=chunk, metadata={"generated_at": current_time}))
    # take doc 4-7 HACK FOR NOW
    documents = documents[12:16]
    # documents = documents[8:11]
    return documents


def main() -> None:
    """Orchestrate graph generation from research documents."""
    document_directory = "./papers/Chem. Rev. 2022, 122, 12207-12243"
    # ontology = generate_ontology_from_glossary(document_directory)
    labels = {
        "Material": "Various materials used in dentistry and medicine, such as zeolites, glass ionomer cements, acrylic resins, and mineral trioxide aggregate.",  # noqa
        "Process": "Procedures and methods involved in dental treatments, including root canal irrigation, implant coatings, and zeolite incorporation.",  # noqa
        "Property": "Characteristics and attributes of materials, like antimicrobial activity and mechanical properties.",  # noqa
        "Other": "General terms and concepts not falling under the specific categories of material, process, or property, such as volatile organic compounds and ion-embedded zeolites.",  # noqa
    }
    relations = [
        "contain",
        "incorporate",
        "enhance",
        "utilize",
        "apply",
        "improve",
        "prevent",
        "emit",
        "detect",
        "inhibit",
        "kill",
        "relate to",
        "be known for",
        "adhere to",
        "flush and disinfect",
    ]
    allowed_nodes = list(labels.keys())
    allowed_relationships = relations

    # Setting up the Neo4j graph instance
    graph = Neo4jGraph()

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")  # type: ignore
    llm_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=allowed_nodes,
        allowed_relationships=allowed_relationships,
        strict_mode=True,
    )

    loader = ResearchDocLoader(
        document_directory
    )  # Update this part with your method to load documents
    research_doc = loader.load()
    full_text = research_doc.paper  # Assuming `paper` is a string containing the full text
    docs = create_documents_from_text_chunks(full_text)

    graph_documents = llm_transformer.convert_to_graph_documents(docs)
    for doc in graph_documents:
        print(f"Nodes:{doc.nodes}")
        print(f"Relationships:{doc.relationships}")

    graph.add_graph_documents(graph_documents)


if __name__ == "__main__":
    main()
