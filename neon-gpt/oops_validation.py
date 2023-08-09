"""
Scripts to validate the produced ontology using the OOPS! APIs.
"""

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rdflib import Graph

OOPS_API = "https://oops.linkeddata.es/rest"
REQUEST_TEMPLATE = "./templates/oops_request_template.xml"


class OOPSValidation:
    """
    OOPS! validation of the produced ontology.
    """

    def __init__(self, ontology_file: str | Path | Graph):
        """
        Constructor for OOPSValidation.
        :param ontology_file: The path to the ontology file.
        :type ontology_file: str | Path | Graph
        """
        if isinstance(ontology_file, Path):
            # if file is provided, open it
            ontology_file = self._load_ontology(ontology_file)
        elif isinstance(ontology_file, str):
            try:
                # if string is provided, try to load it as a graph
                ontology_file = Graph().parse(data=ontology_file,
                                              format="RDF/XML")
            except Exception as e:
                raise Exception(f"Error parsing the ontology: {e}") from e
        elif not isinstance(ontology_file, Graph):
            raise NameError("Invalid ontology file provided."
                            "The ontology file must be a path to a file,"
                            "a string containing the ontology, or a graph.")

        self.ontology = ontology_file.serialize(format="xml")
        self.oops_api = OOPS_API

        # open the xml template
        with open(REQUEST_TEMPLATE, "r") as f:
            self.request_template = f.read()

        self.request_body = self._compose_request()

    @staticmethod
    def _load_ontology(ontology_file: str | Path) -> Graph:
        """
        Load the ontology from the ontology file.
        :param ontology_file: The path to the ontology file.
        :type ontology_file: str | Path
        :return: The ontology as a string.
        :rtype: Graph
        """
        with ontology_file.open("r") as f:
            ontology = f.read()

        # parse the ontology and return the graph
        try:
            ontology = Graph().parse(data=ontology, format="ttl")
        except Exception as e:
            raise Exception(f"Error parsing the ontology: {e}") from e

        return ontology

    def _compose_request(self,
                         output_format: str = 'XML',
                         pitfalls: str = '') -> str:
        """
        Compose the request to the OOPS! API.
        :param output_format: The output format of the OOPS! API.
        :type output_format: str
        :param pitfalls: The pitfalls to check for expressed as a string of
                            comma-separated values.
        :type pitfalls: str
        :return: The request to the OOPS! API.
        :rtype: str
        """
        # format the ontology parameter
        formatted_ontology = f'<![CDATA[ {self.ontology} ]]></OntologyContent>'
        formatted_request = self.request_template.replace('</OntologyContent>',
                                                          formatted_ontology)

        # format the output format parameter
        if output_format not in ['XML', 'RDF/XML']:
            raise ValueError(f'Invalid output format: {output_format}')
        formatted_output = f'{output_format}</OutputFormat>'
        formatted_request = formatted_request.replace('</OutputFormat>',
                                                      formatted_output)

        # format the pitfalls parameter
        if pitfalls:
            formatted_pitfalls = f'{pitfalls}</Pitfalls>'
            formatted_request = formatted_request.replace('</Pitfalls>',
                                                          formatted_pitfalls)

        return formatted_request

    def validate(self) -> str:
        """
        Validate the ontology using the OOPS! API.
        :return: The OOPS! validation results.
        :rtype: dict
        """
        print(self.request_body)
        try:
            response = requests.post(url=self.oops_api,
                                     data=self.request_body,
                                     allow_redirects=False).text
            # format the text as xml
            response = BeautifulSoup(response, features="xml").prettify()
            return response
        except Exception as e:
            raise Exception(f"Error connecting to the OOPS! API: {e}") from e


if __name__ == "__main__":
    ontology_file = Path("./test/wine_test_validated.ttl")
    oops = OOPSValidation(ontology_file)
    response = oops.validate()
    print(response)
