from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class TwoDCoordinatesResponse(BaseModel):
    """Represents a response containing 2D coordinates for a molecule.

    Properties:
    - molblock (str): The generated mol block with 2D coordinates.
    """

    molblock: str = Field(
        ...,
        title="Molecule Block",
        description="The generated mol block with 2D coordinates as plain text.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CC",
                    "message": "Success",
                    "output": """
  CDK     09012308392D

  2  1  0  0  0  0  0  0  0  0999 V2000
    0.0000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
    1.5000    0.0000    0.0000 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0  0  0  0
M  END""",
                },
            ],
        }


class ThreeDCoordinatesResponse(BaseModel):
    """Represents a response containing 3D coordinates for a molecule.

    Properties:
    - molblock (str): The generated mol block with 3D coordinates.
    """

    molblock: str = Field(
        ...,
        title="Molecule Block",
        description="The generated mol block with 3D coordinates as plain text.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CC",
                    "message": "Success",
                    "output": """

     RDKit          3D

  2  1  0  0  0  0  0  0  0  0999 V2000
   -0.7044   -0.0850   -0.4900 C   0  0  0  0  0  0  0  0  0  0  0  0
   -1.9017   -0.1353    0.4322 C   0  0  0  0  0  0  0  0  0  0  0  0
  1  2  1  0
M  END""",
                },
            ],
        }


class GenerateSMILESResponse(BaseModel):
    """Represents a response containing a generated SMILES string.

    Properties:
    - smiles (str): The generated SMILES string.
    """

    smiles: str = Field(
        ...,
        title="SMILES",
        description="The generated SMILES string corresponding to the input text.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "1,3,7-trimethylpurine-2,6-dione",
                    "message": "Success",
                    "output": "CN1C=NC2=C1C(=O)N(C)C(=O)N2C",
                },
            ],
        }


class GenerateCanonicalResponse(BaseModel):
    """Represents a response containing a generated SMILES string.

    Properties:
    - smiles (str): The generated Canonical SMILES string.
    """

    smiles: str = Field(
        ...,
        title="SMILES",
        description="The generated Canonical SMILES string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "CN1C=NC2=C1C(=O)N(C)C(=O)N2C",
                },
            ],
        }


class GenerateCXSMILESResponse(BaseModel):
    """Represents a response containing a generated CXSMILES string.

    Properties:
    - smiles (str): The generated CXSMILES string.
    """

    smiles: str = Field(
        ...,
        title="SMILES",
        description="The generated CXSMILES string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "CN1C=NC2=C1C(=O)N(C)C(=O)N2C |(2.68,2.45,;2.22,1.02,;3.1,-0.19,;2.22,-1.4,;0.8,-0.94,;0.8,0.56,;-0.5,1.31,;-0.5,2.81,;-1.8,0.56,;-3.1,1.31,;-1.8,-0.94,;-3.1,-1.69,;-0.5,-1.69,;-0.5,-3.19,)|",
                },
            ],
        }


class GenerateInChIResponse(BaseModel):
    """Represents a response containing a generated InChI string.

    Properties:
    - inchi (str): The generated InChI string.
    """

    inchi: str = Field(
        ...,
        title="SMILES",
        description="The generated InChI string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "InChI=1S/C8H10N4O2/c1-10-4-9-6-5(10)7(13)12(3)8(14)11(6)2/h4H,1-3H3",
                },
            ],
        }


class GenerateInChIKeyResponse(BaseModel):
    """Represents a response containing a generated InChI Key string.

    Properties:
    - inchikey (str): The generated InChI Key string.
    """

    inchikey: str = Field(
        ...,
        title="SMILES",
        description="The generated InChI Key string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "RYYVLZVUVIJVGH-UHFFFAOYSA-N",
                },
            ],
        }


class GenerateIUPACResponse(BaseModel):
    """Represents a response containing a generated IUPAC string.

    Properties:
    - iupac (str): The generated IUPAC name.
    """

    iupac: str = Field(
        ...,
        title="SMILES",
        description="The generated IUPAC name corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "1,3,7-trimethylpurine-2,6-dione",
                },
            ],
        }


class GenerateSELFIESResponse(BaseModel):
    """Represents a response containing a generated SELFIES string.

    Properties:
    - iupac (str): The generated SELFIES string.
    """

    iupac: str = Field(
        ...,
        title="SMILES",
        description="The generated SELFIES string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "[C][N][C][=Branch1][C][=O][C][=C][Branch1][#Branch1][N][=C][N][Ring1][Branch1][C][N][Branch1][C][C][C][Ring1][N][=O]",
                },
            ],
        }


class GenerateFormatsResponse(BaseModel):
    """Represents a response containing a generated SELFIES string.

    Properties:
    - iupac (str): The generated SELFIES string.
    """

    iupac: str = Field(
        ...,
        title="SMILES",
        description="The generated SELFIES string corresponding to the input SMILES.",
    )

    class Config:
        """Pydantic model configuration.

        JSON Schema Extra:
        - Includes examples of the response structure.
        """

        json_schema_extra = {
            "examples": [
                {
                    "input": "CN1C(=O)C2=C(N=CN2C)N(C)C1=O",
                    "message": "Success",
                    "output": "molblock, SMILES, InChI and InChI-Key",
                },
            ],
        }
