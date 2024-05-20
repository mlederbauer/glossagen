"""CLI for GlossaGen."""

import argparse

from glossagen.pipelines import generate_glossary


def hello_world(custom_msg: str) -> str:
    """Return a greeting message with the provided custom message."""
    return f"Hello {custom_msg}"


def main() -> None:
    """CLI for GlossaGen."""
    parser = argparse.ArgumentParser(description="Generate a glossary out of a research paper.")
    parser.add_argument(
        "document_directory",
        type=str,
        nargs="?",
        default="./data",
        help="The directory where the research document is stored.",
    )

    args = parser.parse_args()

    generate_glossary(args.document_directory)


if __name__ == "__main__":
    main()
