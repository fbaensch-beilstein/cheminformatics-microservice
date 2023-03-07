from fastapi import Request, APIRouter, Depends, HTTPException
from typing import Optional
from rdkit import Chem

# from ..database import db
from fastapi_pagination import Page, add_pagination, paginate
from rdkit.Chem.EnumerateStereoisomers import (
    EnumerateStereoisomers,
    StereoEnumerationOptions,
)
from chembl_structure_pipeline import standardizer
from fastapi.responses import JSONResponse
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem.QED import properties
from rdkit.Chem.rdMolDescriptors import Properties
from STOUT import translate_forward, translate_reverse
from app.modules.npscorer import getnp_score
from app.modules.descriptor_calculator import GetBasicDescriptors

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
async def standardise_mol(request: Request):
    body = await request.json()
    query = body["query"]
    if query:
        return translate_reverse(query)


@router.get("/{smiles}/npscore")
async def nplikeliness_score(smiles: Optional[str]):
    if smiles:
        np_score = getnp_score(smiles)
        return np_score


# @app.get("/molecules/", response_model=List[schemas.Molecule])
# def read_molecules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     molecules = crud.get_molecules(db, skip=skip, limit=limit)
#     return molecules
