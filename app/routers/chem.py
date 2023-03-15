import os
import requests
import selfies as sf
from fastapi import Request, APIRouter
from typing import Optional
from rdkit import Chem

from urllib.request import urlopen
from urllib.parse import urlsplit

# from ..database import db
# from fastapi_pagination import Page, add_pagination, paginate
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers,
)
from chembl_structure_pipeline import standardizer
from fastapi.responses import Response, JSONResponse
from rdkit.Chem.Scaffolds import MurckoScaffold
from STOUT import translate_forward, translate_reverse
from app.modules.npscorer import getnp_score
from app.modules.descriptor_calculator import GetBasicDescriptors
from app.modules.classyfire import classify, result
from app.modules.cdkmodules import getCDKSDGMol
from app.modules.depict import getRDKitDepiction, getCDKDepiction
from app.modules.decimermodules import getPredictedSegments

router = APIRouter(
    prefix="/chem",
    tags=["chem"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def chem_index():
    return {"message": "Hello Chem Router!"}


@router.get("/{smiles}/mol")
async def smiles_mol(smiles: str):
    if smiles:
        m = Chem.MolFromSmiles(smiles)
        return Chem.MolToMolBlock(m)
    else:
        return None


@router.get("/{smiles}/convert")
async def smiles_convert(smiles: str):
    if smiles:
        m = Chem.MolFromSmiles(smiles)
        response = {}
        response["mol"] = Chem.MolToMolBlock(m)
        response["cannonicalsmiles"] = Chem.MolToSmiles(m)
        response["inchi"] = Chem.inchi.MolToInchi(m)
        response["inchikey"] = Chem.inchi.MolToInchiKey(m)
        return response
    else:
        return None


@router.get("/{smiles}/stereoisomers")
async def smiles_stereoisomers(smiles: Optional[str]):
    m = Chem.MolFromSmiles(smiles)
    isomers = tuple(EnumerateStereoisomers(m))
    smilesArray = []
    for smi in sorted(Chem.MolToSmiles(x, isomericSmiles=True) for x in isomers):
        smilesArray.append(smi)
    return smilesArray


"""
@router.get("/search/{smiles}")
async def smiles_search(smiles: Optional[str]):
    if smiles:
        curs = db.connect().cursor()
        curs.execute(
            "select id, standard_inchi from mols where smiles@>'"
            + smiles
            + "' limit 5;"
        )
        rows = paginate(curs.fetchall())
        return rows
"""


@router.post("/standardise")
async def standardise_mol(request: Request):
    body = await request.json()
    mol = body["mol"]
    if mol:
        standardised_mol = standardizer.standardize_molblock(mol)
        rdkit_mol = Chem.MolFromMolBlock(standardised_mol)
        smiles = Chem.MolToSmiles(rdkit_mol)
        response = {}
        response["standardised_mol"] = standardised_mol
        response["cannonical_smiles"] = smiles
        response["inchi"] = Chem.inchi.MolToInchi(rdkit_mol)
        response["inchikey"] = Chem.inchi.MolToInchiKey(rdkit_mol)
        core = MurckoScaffold.GetScaffoldForMol(rdkit_mol)
        response["murcko_scaffold"] = Chem.MolToSmiles(core)
        return response


@router.get("/{smiles}/descriptors")
async def smiles_descriptors(smiles: Optional[str]):
    if smiles:
        return GetBasicDescriptors(smiles)


@router.get("/{smiles}/iupac")
async def smiles_iupac(smiles: Optional[str]):
    if smiles:
        iupac = translate_forward(smiles)
        return iupac


@router.post("/iupac/smiles")
async def iupac_smiles(request: Request):
    body = await request.json()
    query = body["query"]
    if query:
        return translate_reverse(query)


@router.get("/{smiles}/npscore")
async def nplikeliness_score(smiles: Optional[str]):
    if smiles:
        np_score = getnp_score(smiles)
        return np_score


@router.get("/{smiles}/selfies")
async def encodeselfies(smiles: Optional[str]):
    if smiles:
        selfies_e = sf.encoder(smiles)
        return selfies_e


@router.get("/{selfies}/smiles")
async def decodeselfies(selfies: Optional[str]):
    if selfies:
        selfies_d = sf.decoder(selfies)
        return selfies_d


@router.get("/classyfire/{smiles}/classify")
async def classyfire_classify(smiles: Optional[str]):
    if smiles:
        data = await classify(smiles)
        return data


@router.get("/classyfire/{id}/result")
async def classyfire_result(id: Optional[str]):
    if id:
        data = await result(id)
        return data


@router.get("/{smiles}/cdk2d")
async def cdk2d_coordinates(smiles: Optional[str]):
    if smiles:
        return getCDKSDGMol(smiles)


@router.get("/depict/{smiles}")
async def depick_molecule(
    smiles: Optional[str],
    generator: Optional[str] = "cdksdg",
    width: Optional[int] = 512,
    height: Optional[int] = 512,
    rotate: Optional[int] = 0,
):
    if generator:
        if generator == "cdksdg":
            return Response(
                content=getCDKDepiction(smiles, [width, height], rotate),
                media_type="image/svg+xml",
            )
        else:
            return Response(
                content=getRDKitDepiction(smiles, [width, height], rotate),
                media_type="image/svg+xml",
            )


@router.post("/process")
async def extract_chemicalinfo(request: Request):
    body = await request.json()
    image_path = body["path"]
    reference = body["reference"]
    split = urlsplit(image_path)
    filename = "/tmp/" + split.path.split("/")[-1]
    if "img" in body:
        imgDataURI = body["img"]
        if imgDataURI:
            response = urlopen(imgDataURI)
            with open(filename, "wb") as f:
                f.write(response.file.read())
                smiles = getPredictedSegments(filename)
                os.remove(filename)
                return JSONResponse(
                    content={"reference": reference, "smiles": smiles.split(".")}
                )
    else:
        response = requests.get(image_path)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
                smiles = getPredictedSegments(filename)
                os.remove(filename)
                return JSONResponse(
                    content={"reference": reference, "smiles": smiles.split(".")}
                )


# @app.get("/molecules/", response_model=List[schemas.Molecule])
# def read_molecules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     molecules = crud.get_molecules(db, skip=skip, limit=limit)
#     return molecules
