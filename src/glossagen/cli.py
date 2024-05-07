"""CLI for GlossaGen."""

import argparse


def hello_world(smiles: str) -> str:
    """Return a greeting message with the provided SMILES notation."""
    return f"Hello {smiles}"


def main() -> None:
    """CLI for GlossaGen."""
    parser = argparse.ArgumentParser(description="Process some smiles.")
    parser.add_argument(
        "smiles",
        type=str,
        help="A text string representing a SMILES notation or any string.",
    )

    args = parser.parse_args()
    print(hello_world(args.smiles))


if __name__ == "__main__":
    main()
