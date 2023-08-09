"""
Validation and check for inconsistencies using the Hermit reasoner.
"""
import subprocess
from pathlib import Path

from utils import convert_ontology


def reason_ontology(ontology_file: str | Path) -> tuple[str, str]:
    """
    Reason the ontology using the Hermit reasoner.
    :param ontology_file: The path to the ontology file.
    :type ontology_file: str | Path
    :return: The reasoned ontology.
    :rtype: tuple[str, str]
    """
    # convert the ontology to OWL/XML
    ontology_path = convert_ontology(ontology_file, "xml")
    print(ontology_path)

    # open the ontology in the Hermit reasoner
    hermit = subprocess.run(["java", "-jar", "./bin/Hermit.jar", '-k',
                            f'file://{ontology_path.absolute()}'],
                            capture_output=True,
                            text=True)

    return hermit.stdout, hermit.stderr


if __name__ == '__main__':
    # reason the ontology
    reasoned_ontology = reason_ontology('./test/wine_test_validated.ttl')
    print(reasoned_ontology)
