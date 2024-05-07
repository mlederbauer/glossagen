"""init dspy."""

import os

import dsp
import dspy
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

system_prompt = """
You are GlossaGen, a helpful AI that generates glossaries from scholarly
articles. You're an expert in the field of materials and chemistry and
give concise, structured, helpful answers whenever instructed."""


def init_dspy(
    language_model_class: dsp.GPT3 = dspy.OpenAI,
    max_tokens: int = 3000,
    model: str = "gpt-4-turbo",
) -> None:
    """
    Initialize the dspy library with the specified parameters.

    Args:
        language_model_class: The class of the language model to use.
        max_tokens (int): The maximum number of tokens to generate.
        model (str): The name of the language model to use.

    Returns
    -------
        None
    """
    language_model = language_model_class(
        max_tokens=max_tokens, model=model, system_prompt=system_prompt
    )

    dspy.settings.configure(lm=language_model)
