"""CLI for GlossaGen."""

import argparse

from glossagen.pipelines import generate_glossary


def hello_world(smiles: str) -> str:
    """Return a greeting message with the provided SMILES notation."""
    return f"Hello {smiles}"


def main() -> None:
    """CLI for GlossaGen."""
    parser = argparse.ArgumentParser(description="Generate a glossary out of a research paper.")
    parser.add_argument(
        "document_directory",
        type=str,
        nargs="?",
        default="/Users/magdalenalederbauer/projects/glossagen/data/",
        help="The directory where the research document is stored.",
    )

    args = parser.parse_args()

    generate_glossary(args.document_directory)


if __name__ == "__main__":
    main()
