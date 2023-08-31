from fastapi import APIRouter, status, Query, HTTPException
from typing import List
from app.modules.tools.surge import generateStructures
from app.modules.tools.sugarremoval import (
    getSugarInfo,
    removeLinearSugar,
    removeCircularSugar,
    removeLinearandCircularSugar,
)
from app.schemas import HealthCheck
from app.schemas.error import ErrorResponse

router = APIRouter(
    prefix="/tools",
    tags=["tools"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", include_in_schema=False)
@router.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check on Tools Module",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
    include_in_schema=False,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a health check on. This endpoint can primarily be used by Docker
    to ensure a robust container orchestration and management are in place. Other
    services that rely on the proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


@router.get(
    "/generate-structures",
    response_model=List[str],
    summary="Generates structures using the chemical structure generator",
    responses={400: {"model": ErrorResponse}},
)
async def Generate_Structures(
    molecular_formula: str = Query(
        title="Molecular Formula",
        description="Molecular Formula for the chemical structure to be generated",
        examples=[
            "C6H6",
            "C2H5OH",
        ],
    )
):
    """
    Generates structures using the chemical structure generator based on the canonical generation path method.
    For more information refer to:
    - McKay, B.D., Yirik, M.A. & Steinbeck, C. Surge: a fast open-source chemical graph generator. J Cheminform 14, 24 (2022). https://doi.org/10.1186/s13321-022-00604-9


    Parameters:
     - **Molecular_Formula**: required (str): The molecular formula of the compound.

    Returns:
    - List[str]: A list of generated structures.

    Raises:
    - HTTPException: If there was an error generating the structures.

    Example:
    - GET /generate-structures?molecular_formula=C4H10

    Note:
    - The maximum allowable count of heavy atoms is restricted to 10 to mitigate excessive utilization of this service.

    """
    try:
        structures = generateStructures(molecular_formula)
        if structures:
            return structures
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/sugars-info",
    response_model=str,
    summary="Get information whether a given molecule has circular or linear sugars",
    responses={400: {"model": ErrorResponse}},
)
async def getsugarinformation(
    smiles: str = Query(
        title="SMILES",
        description="SMILES: string representation of the molecule",
        examples=[
            "OCC(O)C(O)C(O)C(O)C1OC(CO)C(O)C(O)C1O",
            "O=C(O)C1=CC(O)C(O)C(OC(=O)C2C(=CC=3C=C(O)C(OC4OC(CO)C(O)C(O)C4O)=CC3C2C5=CC=C(O)C(O)=C5)C(=O)OCC(O)C(O)C(O)C(O)C(O)CO)C1",
        ],
    )
):
    """
    Get information on whether a given molecule has circular or linear sugars.
    For more information refer to:
    - Schaub, J., Zielesny, A., Steinbeck, C. et al. Too sweet: cheminformatics for deglycosylation in natural products. J Cheminform 12, 67 (2020). https://doi.org/10.1186/s13321-020-00467-y.

    Parameters:
    - **SMILES string**: (str): SMILES: string representation of the molecule (required, query parameter)

    Returns:
    - str: A message indicating the type of sugars present in the molecule.

    Note:
    The function `getSugarInfo` is used internally to determine the presence of linear and circular sugars in the molecule.

    The returned message indicates the types of sugars present in the molecule:
        - If both linear and circular sugars are present, it returns "The molecule contains Linear and Circular sugars."
        - If only linear sugar is present, it returns "The molecule contains only Linear sugar."
        - If only circular sugars are present, it returns "The molecule contains only Circular sugar."
        - If no sugars are found, it returns "The molecule contains no sugar."

    """
    try:
        hasLinearSugar, hasCircularSugars = getSugarInfo(smiles)
        if hasLinearSugar and hasCircularSugars:
            return "The molecule contains Linear and Circular sugars"
        if hasLinearSugar and not hasCircularSugars:
            return "The molecule contains only Linear sugar"
        if hasCircularSugars and not hasLinearSugar:
            return "The molecule contains only Circular sugar"
        else:
            return "The molecule contains no sugar"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/remove-linear-sugars",
    response_model=str,
    summary="Detect and remove linear sugars",
    responses={400: {"model": ErrorResponse}},
)
async def removelinearsugars(
    smiles: str = Query(
        title="SMILES",
        description="SMILES: string representation of the molecule",
        examples=[
            "OCC(O)C(O)C(O)C(O)C1OC(CO)C(O)C(O)C1O",
            "O=C(O)C1=CC(O)C(O)C(OC(=O)C2C(=CC=3C=C(O)C(OC4OC(CO)C(O)C(O)C4O)=CC3C2C5=CC=C(O)C(O)=C5)C(=O)OCC(O)C(O)C(O)C(O)C(O)CO)C1",
        ],
    )
):
    """
    Detect and remove linear sugars from a given SMILES string using Sugar Removal Utility.

    Parameters:
    - **SMILES string**: (str): SMILES: string representation of the molecule (required, query parameter)

    Returns:
    - str: The modified SMILES string with linear sugars removed.

    """
    try:
        removed_smiles = removeLinearSugar(smiles)
        if removed_smiles:
            return removed_smiles
        else:
            raise HTTPException(
                status_code=400,
                detail="Error reading SMILES string, please check again.",
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/remove-circular-sugars",
    response_model=str,
    summary="Detect and remove linear sugars",
    responses={400: {"model": ErrorResponse}},
)
async def removecircularsugars(
    smiles: str = Query(
        title="SMILES",
        description="SMILES: string representation of the molecule",
        examples=[
            "OCC(O)C(O)C(O)C(O)C1OC(CO)C(O)C(O)C1O",
            "O=C(O)C1=CC(O)C(O)C(OC(=O)C2C(=CC=3C=C(O)C(OC4OC(CO)C(O)C(O)C4O)=CC3C2C5=CC=C(O)C(O)=C5)C(=O)OCC(O)C(O)C(O)C(O)C(O)CO)C1",
        ],
    )
):
    """
    Detect and remove circular sugars from a given SMILES string using Sugar Removal Utility.

    Parameters:
    - **SMILES string**: (str): SMILES: string representation of the molecule (required, query parameter)

    Returns:
    - str: The modified SMILES string with circular sugars removed.

    """
    try:
        removed_smiles = removeCircularSugar(smiles)
        if removed_smiles:
            return removed_smiles
        else:
            raise HTTPException(
                status_code=400,
                detail="Error reading SMILES string, please check again.",
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/remove-sugars",
    response_model=str,
    summary="Detect and remove linear sugars",
    responses={400: {"model": ErrorResponse}},
)
async def removelinearandcircularsugars(
    smiles: str = Query(
        title="SMILES",
        description="SMILES: string representation of the molecule",
        examples=[
            "OCC(O)C(O)C(O)C(O)C1OC(CO)C(O)C(O)C1O",
            "O=C(O)C1=CC(O)C(O)C(OC(=O)C2C(=CC=3C=C(O)C(OC4OC(CO)C(O)C(O)C4O)=CC3C2C5=CC=C(O)C(O)=C5)C(=O)OCC(O)C(O)C(O)C(O)C(O)CO)C1",
        ],
    )
):
    """
    Detect and remove linear and circular sugars from a given SMILES string using Sugar Removal Utility.

    Parameters:
    - **SMILES string**: (str): SMILES: string representation of the molecule (required, query parameter)

    Returns:
    - str: The modified SMILES string with linear and circular sugars removed.

    """
    try:
        removed_smiles = removeLinearandCircularSugar(smiles)
        if removed_smiles:
            return removed_smiles
        else:
            raise HTTPException(
                status_code=400,
                detail="Error reading SMILES string, please check again.",
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
