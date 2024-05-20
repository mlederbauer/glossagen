"""Module for generating a knowledge graph out of a document."""

import datetime
from typing import List

# Importing all necessary classes and functions
from graph_maker import Document, GraphMaker, Neo4jGraphModel, Ontology, OpenAIClient

from glossagen.pipelines import generate_glossary
from glossagen.pipelines.glossary_to_ontology import OntologyGenerator
from glossagen.utils import ResearchDocLoader, init_dspy


def generate_ontology_from_glossary(document_directory: str):
    """Generate ontology from a glossary."""
    example_glossary = (
        generate_glossary(document_directory).set_index("Term").to_dict()["Definition"]
    )
    ontogen = OntologyGenerator(example_glossary)
    return ontogen.generate_ontology_from_glossary()


def generate_summary(text: str, llm: OpenAIClient) -> str:
    """Generate summary for a given text using a language model."""
    SYS_PROMPT = """
    Succinctly summarise the text provided by the user.
    Respond only with the summary and no other comments."""

    try:
        return llm.generate(user_message=text, system_message=SYS_PROMPT)
    except Exception as e:
        print(f"Failed to generate summary due to: {e}")
        return ""


def create_documents_from_text_chunks(text_chunks: List[str], llm: OpenAIClient) -> List[Document]:
    """Create documents from text chunks including metadata with summaries."""
    current_time = str(datetime.datetime.now())
    return [
        Document(
            text=t,
            metadata={"summary": generate_summary(t, llm), "generated_at": current_time},  # noqa
        )
        for t in text_chunks
    ]


def generate_and_save_graph(docs: List[Document], ontology: Ontology):
    """Generate a knowledge graph from documents and save to Neo4j."""
    llm = OpenAIClient(model="gpt-3.5-turbo", temperature=0.1, top_p=0.5)
    graph_maker = GraphMaker(ontology=ontology, llm_client=llm, verbose=False)

    graph = graph_maker.from_documents(docs, delay_s_between=0)
    print("Total number of Edges:", len(graph))
    for edge in graph:
        print(edge.model_dump(exclude=["metadata"]), "\n")

    neo4j_graph = Neo4jGraphModel(edges=graph, create_indices=False)
    neo4j_graph.save()


def main():
    """Orchestrate graph generation from research documents."""
    document_directory = "./data/"
    ontology = generate_ontology_from_glossary(document_directory)

    init_dspy()
    loader = ResearchDocLoader(document_directory)
    research_doc = loader.load()
    text_chunks = research_doc.paper.split("\n\n")  # Splitting the document into chunks
    docs = create_documents_from_text_chunks(text_chunks, OpenAIClient(model="gpt-3.5-turbo"))

    generate_and_save_graph(docs, ontology)


if __name__ == "__main__":
    main()
