"""
Utilities for the neon-gpt package.
"""

import json
from pathlib import Path

from rdflib import Graph


def load_prompts(prompts_file: str | Path) -> list:
    """
    Load the prompts from the prompts file.
    :param prompts_file: The path to the prompts file.
    :return: A list of prompts.
    """
    if isinstance(prompts_file, str):
        prompts_file = Path(prompts_file)

    with prompts_file.open("r") as f:
        prompts = json.load(f)

    return prompts


def convert_ontology(ontology_file: str | Path,
                     output_serialisation: str) -> Path:
    """
    Load the ontology from the ontology file.
    :param ontology_file: The path to the ontology file.
    :type ontology_file: str | Path
    :param output_serialisation: The output serialisation format.
    :type output_serialisation: str
    :return: The ontology as a string.
    :rtype: Path
    """
    if isinstance(ontology_file, str):
        ontology_file = Path(ontology_file)

    with ontology_file.open("r") as f:
        ontology = f.read()

    # parse the ontology and return the graph
    try:
        ontology = Graph().parse(data=ontology, format="ttl")
    except Exception as e:
        raise Exception(f"Error parsing the ontology: {e}") from e

    # get the output path, which is the input path with the new extension
    output_path = ontology_file.with_suffix(f".{output_serialisation.lower()}")
    # convert the ontology to the desired serialisation
    ontology.serialize(format=output_serialisation,
                                  destination=output_path)
    return Path(output_path)
