from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, QED, Lipinski, rdMolDescriptors, rdmolops


def checkRo5Violations(mol):
    """Takes a molecules and checks whether the molecule violates
    the Lipinski's Rule of Five.
    Args : molecules rdkit.Chem.rdmol.Mol: rdkit_mol Objects
    Returns (int): A number of violations on Lipinski Rules.
    """
    num_of_violations = 0
    if Descriptors.MolLogP(mol) > 5:
        num_of_violations += 1
    if Descriptors.MolWt(mol) > 500:
        num_of_violations += 1
    if Lipinski.NumHAcceptors(mol) > 10:
        num_of_violations += 1
    if Lipinski.NumHDonors(mol) > 5:
        num_of_violations += 1
    return num_of_violations


def getDescriptors(smiles):
    """Take an input SMILES and generates a selected set of molecular
    descriptors as a dictionary
    Args (str): SMILES string
    Returns (dict): a dictionary of calculated descriptors
    """
    mol = Chem.MolFromSmiles(smiles)
    AtomC = rdMolDescriptors.CalcNumAtoms(mol)
    HeavyAtomsC = rdMolDescriptors.CalcNumHeavyAtoms(mol)
    MolWt = "%.2f" % Descriptors.MolWt(mol)
    ExactMolWt = "%.2f" % Descriptors.ExactMolWt(mol)
    ALogP = "%.2f" % QED.properties(mol).ALOGP
    NumRotatableBonds = rdMolDescriptors.CalcNumRotatableBonds(mol)
    PSA = "%.2f" % rdMolDescriptors.CalcTPSA(mol)
    HBA = Descriptors.NumHAcceptors(mol)
    HBD = Descriptors.NumHDonors(mol)
    Lipinski_HBA = Lipinski.NumHAcceptors(mol)
    Lipinski_HBD = Lipinski.NumHDonors(mol)
    Ro5Violations = checkRo5Violations(mol)
    AromaticRings = rdMolDescriptors.CalcNumAromaticRings(mol)
    QEDWeighted = "%.2f" % QED.qed(mol)
    FormalCharge = "%.2f" % rdmolops.GetFormalCharge(mol)
    fsp3 = "%.3f" % rdMolDescriptors.CalcFractionCSP3(mol)
    NumRings = rdMolDescriptors.CalcNumRings(mol)

    return (
        AtomC,
        HeavyAtomsC,
        MolWt,
        ExactMolWt,
        ALogP,
        NumRotatableBonds,
        PSA,
        HBA,
        HBD,
        Lipinski_HBA,
        Lipinski_HBD,
        Ro5Violations,
        AromaticRings,
        QEDWeighted,
        FormalCharge,
        fsp3,
        NumRings,
    )


def get3Dconformers(smiles):
    """Convert SMILES to Mol with 3D coordinates
    Args (str): SMILES string.
    Returns (rdkil.mol): A mol object with 3D coodinates
    optimized with MMFF94 forcefield.

    """
    mol = Chem.MolFromSmiles(smiles)
    if mol:
        AllChem.Compute2DCoords(mol)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=0xF00D)
        AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
        return Chem.MolToMolBlock(mol)
    else:
        return None
