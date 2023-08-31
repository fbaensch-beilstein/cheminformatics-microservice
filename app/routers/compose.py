from fastapi import APIRouter, status
from app.schemas import HealthCheck

router = APIRouter(
    prefix="/compose",
    tags=["compose"],
    dependencies=[],
    responses={404: {"description": "Not Found"}},
)


@router.get("/", include_in_schema=False)
@router.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check on Compose Module",
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


@router.get("/suggestions/{term}")
async def suggestTerms(term: str):
    if term:
        instrumentDictionary = [
            "Bruker avance III",
            "Agilent vnmrs 600",
            "Agilent vnmrs 601 / Agilent vnmrs 602",
            "Agilent vnmrs 603",
            "Bruker avancetm III",
            "Bruker avance III 700 mhz",
            "Varian 600 mhz",
            "Agilent technologies",
            "Agilent 500 54 vnmrs",
            "oxford 600",
            "Bruker 700mhz",
            "Bruker950 mhz",
            "Bruker avance drx 500",
            "thermo scientific 5600a 16 channel coulometric array ecd",
            "Bruker avance III 600 mhz",
            "Varian inova 800",
            "Varian 600 cold probe",
            "Bruker avance III 500 mhz and Bruker avance III hd 600 mhz",
            "Bruker 600 mhz avance III hd spectrometer",
            "Bruker avance drx 500 spectrometer",
            "Agilent 500 54 premium shielded vnmrs system",
            "Bruker 600 mhz",
            "Bruker avance III 850 mhz spectrometer",
            "ft nmr",
            "Bruker avance III 600 mhz spectrometer",
            "inova",
            "600 mhz Varian inova spectrometer",
            "Varian 600 mhz ar premium compact",
            "Bruker avance III hd",
            "Bruker avance III hd 600 mhz",
            "Bruker avance drx",
            "Agilent 500 54 premium shielded",
            "Bruker neo",
            "Bruker 600 mhz avance III solution nmr spectrometer",
            "Bruker avIII hd",
            "Bruker av III 600 mhz nmr spectrometer",
            "Bruker avance ii",
            "Bruker avIII hd 500",
            "Varian 500 mhz",
            "Bruker avance",
            "inova nmr spectrometer",
            "Bruker 18 8 tesla 800 mhz nmr spectrometer ascend",
            "600mhz avance III hd",
            "Varian 11 74t",
            "Bruker avance III",
            "Agilent 600",
            "Bruker avance lll",
            "Bruker avance neo 600 mhz 54mm console",
            "Bruker 500mhz spectrometer",
            "avance III 700 mhz nmr spectrometer",
            "800mhz avance III hd",
            "Bruker fallandden",
            "missing",
            "ascend hd III 600mhz Bruker",
            "Bruker neo 600mhz",
            "Bruker avance IIIhd",
            "avance III",
            "Varian inova nmr spectrometer Agilent technologies inc",
            "avance III hd 600 mhz",
            "Bruker800",
            "spectrometer Bruker avance III tm hd 500 mhz",
            "avance III tm hd 500mhz",
            "Bruker 600mhz",
            "Bruker neo 800 mhz",
            "850 mhz Bruker avance III",
            "avance 600 Bruker",
            "Bruker avance av 500 mhz spectrometer",
            "Bruker avance drx 700 mhz spectrometer",
            "Bruker avance 500 mhz spectrometer",
            "Varian unity inova 500 mhz spectrometer",
            "Bruker avance ii 600 mhz spectrometer",
            "Bruker 400 mhz spectrometer",
            "Varian unity inova 600 mhz spectrometer",
            "Bruker avance 700 mhz spectrometer",
            "Bruker avance III 500 mhz spectrometer",
            "Bruker avance III hd 700 mhz spectrometer",
            "Bruker avance III 400 mhz spectrometer",
            "Bruker avance ii 500 mhz spectrometer",
            "Bruker avance ii 800 mhz us2 spectrometer",
            "Bruker avance III 600mhz spectrometer",
            "Bruker 600 mhz spectrometer",
            "Bruker 600 mhz ultrashield spectrometer",
            "Bruker 500 mhz spectrometer",
            "Bruker avance drx 500 mhz spectrometer",
            "Varian unity inova 400 mhz spectrometer",
            "Bruker avance III hd 600 mhz spectrometer",
            "Bruker avance 900 mhz spectrometer",
            "Bruker avance drx 600 mhz spectrometer",
            "Varian vnmr 600 mhz spectrometer",
            "Bruker avance ii 800 mhz spectrometer",
            "Bruker ascend 700 mhz spectrometer",
            "Bruker avance 600 mhz spectrometer",
            "Bruker avance hd 700 mhz spectrometer",
            "Varian vnmrs directdrive 600 mhz spectrometer",
            "Bruker avance 850 mhz spectrometer",
            "Varian vnmrs 600 mhz spectrometer",
            "Bruker avance ii 700 mhz spectrometer",
            "Bruker avance neo 800 mhz spectrometer",
            "Bruker avance neo 500 mhz spectrometer",
            "Bruker avance III hd 800 mhz spectrometer",
            "Bruker avance III 800 mhz spectrometer",
            "Bruker avance ii 500 mhz ultrashield spectrometer",
            "Varian mercury as400 mhz spectrometer",
            "Agilent dd2 600 mhz spectrometer",
            "Bruker avance av 600 mhz spectrometer",
            "Bruker avance III 700 mhz spectrometer",
            "0.01 M phosphate buffered D2O",
            "0.01 M phosphate buffered D2O/H2O",
            "0.02 M phosphate buffered D2O",
            "0.04 M phosphate buffered D2O/H2O",
            "0.05 M phosphate buffered D2O",
            "0.05 M phosphate buffered D2O/H2O",
            "0.05 M phosphate sodium buffered D2O",
            "0.05 mM phosphate buffered D2O",
            "0.06 M phosphate buffered D2O",
            "0.07 M phosphate buffered D2O",
            "0.07 M phosphate buffered D2O/H2O",
            "0.07 M phosphate buffered H2O",
            "0.075 M phosphate buffered D2O/H2O",
            "0.09 M phosphate buffered D2O",
            "0.1 M phosphate buffered D2O",
            "0.1 M phosphate buffered D2O/H2O",
            "0.1 mM phosphate buffered D2O",
            "0.142 M phosphate buffer",
            "0.15 M phosphate buffered D2O",
            "0.15 M phosphate buffered D2O/H2O",
            "0.154 M saline D20",
            "0.2 M phosphate buffered D2O",
            "0.2 M potassium phosphate buffered D2O + 5 mM maleic acid",
            "0.24 M phosphate buffered D2O",
            "0.3 M saline D2O",
            "0.5 M phosphate buffered D2O/H2O",
            "0.5 M potassium phosphate buffered D2O + 0.025 mg/ml TSP",
            "0.6 M phosphate buffered D2O",
            "0.6 ml of 0.1M phosphate buffered D2O (pH=7.0) solution containing 0.5 mM 3 trimethylsilyl propionate 2, 2, 3, 3,  d4 (TMSP, δ =0.0 ppm)",
            "0.9% NaCl in D2O",
            "1.5 M phosphate buffered D2O",
            "1.5 M phosphate buffered D2O/H2O",
            "1.5 M Potassium dihydrogen phosphate",
            "1.75 M phosphate buffered D2O",
            "1 M phosphate buffered D2O/H2O",
            "10%D20",
            "10 % D2O",
            "10% D2O/0.04 mM sodium phosphate buffer/0.4 mM TMSP",
            "10% D2O in H2O",
            "100 mM phosphate  buffer in D2O + 1.0 mM TMSP",
            "540 µl sample/ 60 µl  buffer (pH 7.4, 1.5mM KH2PO4, 0.1% TSP)",
            "630 µl sample + internal standard solution",
            "90:10 H2O/D2O (99.96% atom D2O; Cambridge Isotope Labs) with 0.2 mM phosphate buffer (pH 7.4) and 0.25 mM 3 (trimethylsilyl)propionic 2,2,3,3d4 acid",
            "90% H2O, 10% D2O",
            "acetone",
            "acetone d6 + 1 drop D2O",
            "Acetone D6 ((CD3)2CO)",
            "Acetone D6 ((CD3)2CO) + Deuteriumoxide (D2O)",
            "acetonitril",
            "Acetonitrile D3(CD3CN)",
            "Benzene D6 (C6D6)",
            "BrF5",
            "CCl4",
            "(CD3)2SO",
            "CD3CN or CDCL3",
            "CD3COCD",
            "CD3OD",
            "CD3OD + phosphate sodium buffer D2O",
            "CDCl3",
            "CDCl3/CD3OD (1:1)",
            "CDCl3+CH3CN",
            "CDCL3,TMS",
            "CDCN",
            "CF3CCl3",
            "CF3COOD CD3OD (5:95)",
            "CFCl3",
            "CH2Cl2",
            "CHCl3",
            "chloroform",
            "Chloroform D1 (CDCl3)",
            "Chloroform D1 (CDCl3) + Acetone D6 (CD3COCD3)",
            "Chloroform D1 (CDCl3) + Benzene D6 (C6D6)",
            "Chloroform D1 (CDCl3) + Dimethylsulphoxide (DMSO D6, C2D6SO)",
            "Chloroform D1 (CDCl3) + Methanol D4 (CD3OD)",
            "Chloroform D1 (CDCl3) + Methanol D4 (CD3OD) (2:1)",
            "Chloroform D1 (CDCl3) + Methanol D4 (CD3OD) (4:1)",
            "Chloroform D1 (CDCl3) + Methanol D4 (CD3OD) (5:1)",
            "Chloroform D1 (CDCl3) + Methanol D4 (CD3OD) (9:1)",
            "Chloroform D1 (CDCl3) + Pyridin D5 (C5D5N)",
            "Chloroform D1 (CDCl3)+ trace Methanol D4 (CD3OD)",
            "CS2",
            "Cyclohexane",
            "cyclopentane",
            "D20",
            "D2O",
            "D2O + 0.35 mM TSP",
            "D2O and MeOD",
            "D2O/CDCl3",
            "D2O+DCl",
            "D2O+H2O",
            "D2O Phosphate buffer",
            "Deuterated chloroform",
            "Deuteriumoxide (D2O)",
            "dichloromethane",
            "diethylether",
            "Diethylether ((CH3CH2)2O)",
            "Dimethyl sulfoxide d6 (99.9% atom d6 DMSO; Cambridge Isotope Labs) containing 0.1% trimethylsilane",
            "Dimethylether D6 (CD3OCD3)",
            "Dimethylformamide D7 (DMF D7, CDON(CD3)2 )",
            "Dimethylsulphoxide D6 (DMSO D6, C2D6SO)",
            "Dimethylsulphoxide (DMSO D6, C2D6SO) + Trifluoroacetic Acid (TFA D1, C2DF3O2)",
            "DMCO d6",
            "DMF",
            "DMSO",
            "DMSO d6",
            "DMSO d6 + 0.1 mM DSS d6",
            "DMSO d6, DMCO d6, CD3OD, CDCl3",
            "DMSOd6",
            "Et2O",
            "ether",
            "EtO",
            "Formic Acid D2 (DCOOD)",
            "gas phase",
            "H20 + D20",
            "H2O:D2O",
            "H2O+D2O (10%)_salt",
            "H2O+D2O (90/10) phosphate buffer | H2O+D2O (90/10) phosphate buffer | H2O+D2O (90/10) phosphate buffer | H2O+D2O (90/10) phosphate buffer | D2O phosphate buffer | D2O phosphate buffer | D2O phosphate buffer | D2O phosphate buffer",
            "H2O+D2O (90/10) potassium buffer",
            "HBr",
            "hexane",
            "HF",
            "HI",
            "HSO3F",
            "MeCN",
            "MeOD",
            "MeOH",
            "METHANOL D1 (CH3OD)",
            "Methanol D3(CD3OH)",
            "Methanol D4 (CD3OD)",
            "Methanol D4/D2O (CD3OD/D4)",
            "Methylenchloride D2 (CD2Cl2)",
            "missing",
            "n hexane",
            "neat",
            "neat CFCl3",
            "NH3",
            "other",
            "pentane",
            "PhNO2",
            "Phosphate buffer (pH 7.2) + 2 mM EDTA + 0.5 mM DSS + 0.2% of sodium azide in deuterated environment",
            "Phosphate buffer (pH 7) + 2 mM EDTA + 0.5 mM DSS + 0.2% of sodium azide in deuterated environment",
            "phosphate buffered D2O",
            "phosphate buffered D2O/H2O",
            "phosphate buffered saline D2O",
            "Pyridin D5 (C5D5N)",
            "Pyridin D5 (C5D5N) + Methanol D4 (CD3OD)",
            "saline D2O",
            "SbF5",
            "Serum D2O Buffer",
            "SF6",
            "SO2",
            "SO2ClF",
            "Sodium phosphate buffer",
            "Sodium phosphate buffer in D2O",
            "solid phase",
            "Tetrachloro Ethanol (C2D2Cl4)",
            "TETRACHLORO METHANE (CCl4)",
            "Tetrahydrofuran D8 (THF D8, C4D4O)",
            "TFA",
            "THF",
            "toluene",
            "Toluol d8",
            "Trifluoroacetic Acid (TFA D1, C2DF3O2)",
            "Unknown",
            "Unreported",
            "Vogel's Media containing 5% D2O and 1mM DSS",
            "water",
            "Water (D2O)",
            "Water (H2O)",
        ]
        return list(
            filter(lambda x: x.lower().startswith(term.lower()), instrumentDictionary)
        )
    else:
        return None
