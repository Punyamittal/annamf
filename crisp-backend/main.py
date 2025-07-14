import os
import requests
import json
import re
import google.generativeai as genai
from Bio import Entrez, SeqIO
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from functools import lru_cache

# ====================== 🔑 Configuration =================================
load_dotenv()
API_KEY = "AIzaSyBw_cKorVsoKrrJ7Nmd23YprwBrTxbAu7M"
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")
Entrez.email = "your.amrithesh23@example.com" # Be a good citizen and set your email

# ====================== 🧬 Data & API Configuration ============================
# (trait_species_db remains exactly the same as in your original script)
trait_species_db = {
    "rice": { "scientific_name": "oryza_sativa", "traits": { "drought resistance": {"ensembl_id":"LOC_Os06g03670","symbol":"DREB1A"}, "flood tolerance": {"ensembl_id":"LOC_Os09g11460","symbol":"SUB1A"}, "grain size": {"ensembl_id":"GW2","symbol":"GW2"} }},
    "wheat": { "scientific_name": "triticum_aestivum", "traits": { "rust resistance": {"ensembl_id":"TraesCS7D02G080300","symbol":"Lr34"}, "semi-dwarf": {"ensembl_id":"Rht-B1","symbol":"Rht1"}, "grain protein": {"ensembl_id":"TraesCS6B02G055700","symbol":"GPC-B1"} }},
    "maize": { "scientific_name": "zea_mays", "traits": { "drought resistance": {"ensembl_id":"Zm00001d052025","symbol":"ZmDREB2A"}, "vitamin a biofort": {"ensembl_id":"Zm00001d048183","symbol":"crtRB1"}, "pest resistance": {"ensembl_id":"Zm00001d015758","symbol":"Bt1"} }},
    "sorghum": { "scientific_name": "sorghum_bicolor", "traits": { "stay-green": {"ensembl_id":"Stg1","symbol":"Stg1"}, "drought resistance": {"ensembl_id":"SbDREB2A","symbol":"DREB2A"} }},
    "millet": { "scientific_name": "eleusine_coracana", "traits": { "drought tolerance": {"ensembl_id":"EcDREB1A","symbol":"DREB1A"}, "nutrient content": {"ensembl_id":"EcNAS2","symbol":"NAS2"} }},
    "barley": { "scientific_name": "hordeum_vulgare", "traits": { "disease resistance": {"ensembl_id":"Mla","symbol":"Mla"}, "malting quality": {"ensembl_id":"HvTLP8","symbol":"TLP"} }},
    "cotton": { "scientific_name": "gossypium_hirsutum", "traits": { "fiber length": {"ensembl_id":"GhLi","symbol":"Li1"}, "drought tolerance": {"ensembl_id":"GhDREB2A","symbol":"DREB2A"} }},
    "sugarcane": { "scientific_name": "saccharum_officinarum", "traits": { "sucrose content": {"ensembl_id":"SoSPS3","symbol":"SPS3"}, "drought tolerance": {"ensembl_id":"SoDREB1A","symbol":"DREB1A"} }},
    "potato": { "scientific_name": "solanum_tuberosum", "traits": { "late blight resistance": {"ensembl_id":"PGSC0003DMG400009332","symbol":"RB"}, "starch quality": {"ensembl_id":"GBSS1","symbol":"GBSS1"} }},
    "tomato": { "scientific_name": "solanum_lycopersicum", "traits": { "shelf life": {"ensembl_id":"Solyc05g012020","symbol":"rin"}, "fruit size": {"ensembl_id":"FW2.2","symbol":"FW2.2"} }},
    "eggplant": { "scientific_name": "solanum_melongena", "traits": { "fruit color": {"ensembl_id":"SmMYB1","symbol":"MYB1"}, "eggplant borer resistance": {"ensembl_id":"SmCBP","symbol":"CBP"} }},
    "okra": { "scientific_name": "abelmoschus_esculentus", "traits": { "fibre strength": {"ensembl_id":"AeCesA1","symbol":"CesA1"} }},
    "okra_pulses": { "scientific_name": "vasconcellea_puberula", "traits": {} },
    "mustard": { "scientific_name": "brassica_juncea", "traits": { "oil content": {"ensembl_id":"LOC106352424","symbol":"FAD2"}, "cold tolerance": {"ensembl_id":"LOC106353489","symbol":"CBF1"} }},
    "chickpea": { "scientific_name": "cicer_arietinum", "traits": { "drought resistance": {"ensembl_id":"CaDREB2","symbol":"DREB2"}, "fusarium resistance": {"ensembl_id":"CaFus3","symbol":"Fus3"} }},
    "lentil": { "scientific_name": "lens_culinaris", "traits": { "frost tolerance": {"ensembl_id":"LcCOR15","symbol":"COR15"} }},
    "pigeonpea": { "scientific_name": "cajanus_cajan", "traits": { "wilt resistance": {"ensembl_id":"CPCWR1","symbol":"WR1"} }},
    "peanut": { "scientific_name": "arachis_hypogaea", "traits": { "rust resistance": {"ensembl_id":"AhR1","symbol":"R1"} }},
    "soybean": { "scientific_name": "glycine_max", "traits": { "oil quality": {"ensembl_id":"GmFAD2","symbol":"FAD2"} }},
    "banana": { "scientific_name": "musa_acuminata", "traits": { "panama wilt": {"ensembl_id":"MaRGA2","symbol":"RGA2"} }},
    "tea": { "scientific_name": "camellia_sinensis", "traits": { "cold tolerance": {"ensembl_id":"CsCBF","symbol":"CBF"} }},
    "coffee": { "scientific_name": "coffea_canephora", "traits": { "disease resistance": {"ensembl_id":"CcRGA","symbol":"RGA"} }},
    "rubber": { "scientific_name": "hevea_brasiliensis", "traits": { "latex yield": {"ensembl_id":"HbHB1","symbol":"HB1"} }},
    "sugarbeet": { "scientific_name": "beta_vulgaris", "traits": { "sugar content": {"ensembl_id":"BvSPS1","symbol":"SPS1"} }},
    "sunflower": { "scientific_name": "helianthus_annuus", "traits": { "oil quality": {"ensembl_id":"HaFAD2","symbol":"FAD2"}, "disease resistance": {"ensembl_id":"HaRGA2","symbol":"RGA2"} }},
    "sesame": { "scientific_name": "sesamum_indicum", "traits": { "oil quality": {"ensembl_id":"SiFAD2","symbol":"FAD2"}, "lodging resistance": {"ensembl_id":"SiLGR","symbol":"LGR"} }},
    "papaya": { "scientific_name": "carica_papaya", "traits": { "papaya ring spot": {"ensembl_id":"CpPRSV","symbol":"PRSV"} }},
    "mango": { "scientific_name": "mangifera_indica", "traits": { "anthracnose": {"ensembl_id":"MiRGA","symbol":"RGA"} }},
    "grape": { "scientific_name": "vitis_vinifera", "traits": { "powdery mildew": {"ensembl_id":"VrRGA","symbol":"RGA"} }},
    "apple": { "scientific_name": "malus_domestica", "traits": { "fire blight": {"ensembl_id":"MdRGA","symbol":"RGA"} }},
    "pear": { "scientific_name": "pyrus_communis", "traits": { "scab resistance": {"ensembl_id":"PcRGA","symbol":"RGA"} }},
    "cherry": { "scientific_name": "prunus_avium", "traits": { "fruit firmness": {"ensembl_id":"PaEXPA","symbol":"EXPA"} }},
    "plum": { "scientific_name": "prunus_domestica", "traits": { "stone hardness": {"ensembl_id":"PdTRA1","symbol":"TRA1"} }},
    "peach": { "scientific_name": "prunus_persica", "traits": { "fruit ripening": {"ensembl_id":"PpACO1","symbol":"ACO1"} }},
    "olive": { "scientific_name": "olea_europaea", "traits": { "oil quality": {"ensembl_id":"OeFAD2","symbol":"FAD2"} }},
    "avocado": { "scientific_name": "persea_americana", "traits": { "cold tolerance": {"ensembl_id":"PaCBF","symbol":"CBF"} }},
    "pineapple": { "scientific_name": "ananas_comosus", "traits": { "fruit sugar": {"ensembl_id":"AcSPS","symbol":"SPS"} }},
    "citrus": { "scientific_name": "citrus_sinensis", "traits": { "citrus greening": {"ensembl_id":"CsRGA","symbol":"RGA"} }},
    "watermelon": { "scientific_name": "citrullus_lanatus", "traits": { "disease resistance": {"ensembl_id":"ClRGA","symbol":"RGA"} }},
    "cucumber": { "scientific_name": "cucumis_sativus", "traits": { "powdery mildew": {"ensembl_id":"CsMLO","symbol":"MLO"} }},
    "pumpkin": { "scientific_name": "cucurbita_maxima", "traits": { "fruit size": {"ensembl_id":"CmSUN","symbol":"SUN"} }},
    "brinjal": { "scientific_name": "solanum_melongena", "traits": { "fruit color": {"ensembl_id":"SmMYB1","symbol":"MYB1"} }},
    "bell_pepper": { "scientific_name": "capsicum_annuum", "traits": { "capsaicin content": {"ensembl_id":"CaPun1","symbol":"Pun1"} }},
    "chilli": { "scientific_name": "capsicum_frutescens", "traits": { "heat level": {"ensembl_id":"Let1","symbol":"Let1"} }},
    "carrot": { "scientific_name": "daucus_carota", "traits": { "beta-carotene": {"ensembl_id":"DcPSY1","symbol":"PSY1"} }},
    "turnip": { "scientific_name": "brassica_rapa", "traits": { "glucosinolate": {"ensembl_id":"BrGSL1","symbol":"GSL1"} }},
    "beet": { "scientific_name": "beta_vulgaris", "traits": { "sugar content": {"ensembl_id":"BvSPS1","symbol":"SPS1"} }},
    "spinach": { "scientific_name": "spinacia_oleracea", "traits": { "leaf size": {"ensembl_id":"SoGHD7","symbol":"GHD7"} }},
    "cabbage": { "scientific_name": "brassica_oleracea", "traits": { "head size": {"ensembl_id":"BoWRKY29","symbol":"WRKY29"} }},
    "cauliflower": { "scientific_name": "brassica_oleracea", "traits": { "curd size": {"ensembl_id":"BoCAL","symbol":"CAL"} }},
    "broccoli": { "scientific_name": "brassica_oleracea", "traits": { "flowering time": {"ensembl_id":"BoVRN1","symbol":"VRN1"} }},
    "radish": { "scientific_name": "raphanus_sativus", "traits": { "root thickness": {"ensembl_id":"RsRD29B","symbol":"RD29B"}, "glucosinolate content": {"ensembl_id":"RsGSL","symbol":"GSL"} }},
    "ginger": { "scientific_name": "zingiber_officinale", "traits": { "disease resistance": {"ensembl_id":"ZoRGA","symbol":"RGA"}, "aroma profile": {"ensembl_id":"ZoTPS","symbol":"TPS"} }},
    "turmeric": { "scientific_name": "curcuma_longa", "traits": { "curcumin content": {"ensembl_id":"ClCURS","symbol":"CURS"}, "disease resistance": {"ensembl_id":"ClRGA2","symbol":"RGA2"} }},
    "pearl_millet": {"scientific_name":"pennisetum_glaucum", "traits":{"heat tolerance":{"ensembl_id":"PgHSP17","symbol":"HSP17"}}},
    "foxtail_millet": {"scientific_name":"setaria_italica", "traits":{"drought tolerance":{"ensembl_id":"SiDREB2A","symbol":"DREB2A"}}},
    "barnyard_millet": {"scientific_name":"echinochloa_crus_galli", "traits":{"weed competitiveness":{"ensembl_id":"EcTIR1","symbol":"TIR"}}},
    "kodo_millet": {"scientific_name":"paspalum_scrobiculatum", "traits":{"nutrient use":{"ensembl_id":"PsNRT1","symbol":"NRT1"}}},
    "little_millet": {"scientific_name":"panicum_sumatrense", "traits":{"disease resistance":{"ensembl_id":"PsRGA","symbol":"RGA"}}},
    "proso_millet": {"scientific_name":"panicum_miliaceum", "traits":{"grain size":{"ensembl_id":"PmGW2","symbol":"GW2"}}},
    "french_bean": {"scientific_name":"phaseolus_vulgaris", "traits":{"virus resistance":{"ensembl_id":"PvRsv1","symbol":"RSV1"}}},
    "field_bean": {"scientific_name":"vicia_faba", "traits":{"rust resistance":{"ensembl_id":"VfRGA1","symbol":"RGA1"}}},
    "cowpea": {"scientific_name":"vigna_unguiculata", "traits":{"aphid resistance":{"ensembl_id":"VuRGA","symbol":"RGA"}}},
    "mung_bean": {"scientific_name":"vigna_radiata", "traits":{"heat tolerance":{"ensembl_id":"VrHSP","symbol":"HSP"}}},
    "horse_gram": {"scientific_name":"macrotyloma_uniflorum", "traits":{"drought tolerance":{"ensembl_id":"MuDREB","symbol":"DREB"}}},
    "ricebean": {"scientific_name":"vigna_umatidala", "traits":{"disease tolerance":{"ensembl_id":"VuRGA2","symbol":"RGA2"}}},
    "nudging_gram": {"scientific_name":"lablab_purpureus", "traits":{"protein quality":{"ensembl_id":"LpGPC","symbol":"GPC"}}},
    "safflower": {"scientific_name":"carthamus_tinctorius", "traits":{"drought resistance":{"ensembl_id":"CtDREB","symbol":"DREB"}}},
    "niger_seed": {"scientific_name":"guizotia_abyssinica", "traits":{"oil quality":{"ensembl_id":"GaFAD2","symbol":"FAD2"}}},
    "castor": {"scientific_name":"ricinus_communis", "traits":{"ricin reduction":{"ensembl_id":"RcRicin","symbol":"RIC"}}},
    "linseed": {"scientific_name":"linum_usitatissimum", "traits":{"omega_3 content":{"ensembl_id":"LuFAD3","symbol":"FAD3"}, "fibre quality":{"ensembl_id":"LuCESA","symbol":"CESA"}}},
    "rapeseed": {"scientific_name":"brassica_napus", "traits":{"canola quality":{"ensembl_id":"BnFAD2","symbol":"FAD2"}}},
    "hemp": {"scientific_name":"cannabis_sativa", "traits":{"cannabinoid content":{"ensembl_id":"CsTHC","symbol":"THC"}, "disease resistance":{"ensembl_id":"CsRGA2","symbol":"RGA2"}}},
    "jute": {"scientific_name":"corchorus_capsularis", "traits":{"fiber strength":{"ensembl_id":"CcCESA","symbol":"CESA"}}},
    "cotton": {"scientific_name":"gossypium_barbadense", "traits":{"fibre quality":{"ensembl_id":"GbQTL","symbol":"QTL"}}},
    "hemp_fiber": {"scientific_name":"cannabis_sativa", "traits":{"fiber yield":{"ensembl_id":"CsHB1","symbol":"HB1"}}},
    "ramie": {"scientific_name":"boehmeria_nivea", "traits":{"fiber length":{"ensembl_id":"BnLi","symbol":"Li"}}},
    "flax": {"scientific_name":"linum_usitatissimum", "traits":{"phytochemical":{"ensembl_id":"LuPAL","symbol":"PAL"}}},
    "henna": {"scientific_name":"lawsonia_inermis", "traits":{"dye content":{"ensembl_id":"LiLWN","symbol":"LWN"}}},
    "medicinal_astragalus": {"scientific_name":"astragalus_membranaceus", "traits":{"saponin content":{"ensembl_id":"AmSaponin","symbol":"SAP"}}},
    "ashwagandha": {"scientific_name":"withania_somnifera", "traits":{"withanolide biosynthesis":{"ensembl_id":"WsWNK","symbol":"WNK"}}},
    "lemongrass": {"scientific_name":"cymbopogon_citratus", "traits":{"citral content":{"ensembl_id":"CcCIT","symbol":"CIT"}}},
    "mint": {"scientific_name":"mentha_spicata", "traits":{"menthol content":{"ensembl_id":"MsMINT","symbol":"MINT"}}},
    "basil": {"scientific_name":"ocimum_basilicum", "traits":{"eugenol content":{"ensembl_id":"ObEUG","symbol":"EUG"}}},
    "coriander": {"scientific_name":"coriandrum_sativum", "traits":{"linalool content":{"ensembl_id":"CsLIN","symbol":"LIN"}}},
    "fenugreek": {"scientific_name":"trigonella_foenum_graecum", "traits":{"diosgenin content":{"ensembl_id":"TfDIO","symbol":"DIO"}}},
    "ajwain": {"scientific_name":"trachyspermum_ammi", "traits":{"thymol content":{"ensembl_id":"TaTHY","symbol":"THY"}}},
    "cumin": {"scientific_name":"cuminum_cyminum", "traits":{"essential oil":{"ensembl_id":"CcEO","symbol":"EO"}}},
    "carom": {"scientific_name":"trachyspermum_ammi", "traits":{"aromatic oil":{"ensembl_id":"TaARO","symbol":"ARO"}}},
    "mustard": {"scientific_name":"brassica_rapa", "traits":{"erucic acid content":{"ensembl_id":"BrEAC","symbol":"EAC"}}},
    "taro": {"scientific_name":"colocasia_esculenta", "traits":{"tuber quality":{"ensembl_id":"CeTQ","symbol":"TQ"}}},
    "yam": {"scientific_name":"dioscorea_rotundata", "traits":{"starch content":{"ensembl_id":"DrSPS","symbol":"SPS"}}},
    "cassava": {"scientific_name":"manihot_esculenta", "traits":{"cyanogenic glucoside":{"ensembl_id":"MeCYP79","symbol":"CYP79"}}},
    "sweet_potato": {"scientific_name":"ipomoea_batatas", "traits":{"beta-carotene":{"ensembl_id":"IbPSY","symbol":"PSY"}}},
    "plantain": {"scientific_name":"musa_balbisiana", "traits":{"disease resistance":{"ensembl_id":"MbRGA","symbol":"RGA"}}},
    "oil_palm": {"scientific_name":"elaeis_guineensis", "traits":{"oil yield":{"ensembl_id":"EgOLE","symbol":"OLE"}}},
    "date_palm": {"scientific_name":"phoenix_dactylifera", "traits":{"drought tolerance":{"ensembl_id":"PdDREB","symbol":"DREB"}}},
    "pomegranate": {"scientific_name":"punica_granatum", "traits":{"antioxidant content":{"ensembl_id":"PgANT","symbol":"ANT"}}},
    "guava": {"scientific_name":"psidium_guajava", "traits":{"vitamin_c":{"ensembl_id":"PgGME","symbol":"GME"}}},
    "jackfruit": {"scientific_name":"artocarpus_heterophyllus", "traits":{"fruit size":{"ensembl_id":"AhSUN","symbol":"SUN"}}},
    "mangosteen": {"scientific_name":"garcinia_mangostana", "traits":{"xanthone content":{"ensembl_id":"GmXAN","symbol":"XAN"}}},
    "durian": {"scientific_name":"durio_zibethinus", "traits":{"aroma profile":{"ensembl_id":"DzTPS","symbol":"TPS"}}},
    "breadfruit": {"scientific_name":"artocarpus_altilis", "traits":{"starch quality":{"ensembl_id":"AaGBSS","symbol":"GBSS"}}},
    "quinoa": {"scientific_name":"chenopodium_quinoa", "traits":{"saponin content":{"ensembl_id":"CqSAP","symbol":"SAP"}, "protein quality":{"ensembl_id":"CqGPC","symbol":"GPC"}}},
    "amaranth": {"scientific_name":"amaranthus_cruentus", "traits":{"drought tolerance":{"ensembl_id":"AmDREB","symbol":"DREB"}, "nutrient content":{"ensembl_id":"AmNAS","symbol":"NAS"}}},
    "buckwheat": {"scientific_name":"fagopyrum_esculentum", "traits":{"rutin content":{"ensembl_id":"FeRUT","symbol":"RUT"}, "disease resistance":{"ensembl_id":"FeRGA","symbol":"RGA"}}},
    "chia": {"scientific_name":"salvia_hispanica", "traits":{"omega_3 content":{"ensembl_id":"ShFAD3","symbol":"FAD3"}, "drought tolerance":{"ensembl_id":"ShDREB","symbol":"DREB"}}},
    "kale": {"scientific_name":"brassica_oleracea", "traits":{"glucosinolate content":{"ensembl_id":"BoGSL2","symbol":"GSL2"}, "vitamin content":{"ensembl_id":"BoVTC","symbol":"VTC"}}},
    "lettuce": {"scientific_name":"lactuca_sativa", "traits":{"leaf crispness":{"ensembl_id":"LsEXP","symbol":"EXP"}, "disease resistance":{"ensembl_id":"LsRGA","symbol":"RGA"}}},
    "onion": {"scientific_name":"allium_cepa", "traits":{"flavonoid content":{"ensembl_id":"AcFLA","symbol":"FLA"}, "pungency":{"ensembl_id":"AcSUL","symbol":"SUL"}}},
    "garlic": {"scientific_name":"allium_sativum", "traits":{"allicin content":{"ensembl_id":"AsALI","symbol":"ALI"}, "disease resistance":{"ensembl_id":"AsRGA","symbol":"RGA"}}},
    "asparagus": {"scientific_name":"asparagus_officinalis", "traits":{"spear thickness":{"ensembl_id":"AoEXP","symbol":"EXP"}, "antioxidant content":{"ensembl_id":"AoANT","symbol":"ANT"}}},
    "blueberry": {"scientific_name":"vaccinium_corymbosum", "traits":{"anthocyanin content":{"ensembl_id":"VcANT","symbol":"ANT"}, "cold tolerance":{"ensembl_id":"VcCBF","symbol":"CBF"}}},
}

ENSEMBL_BASE_URL = "https://rest.ensembl.org"
ENSEMBL_HEADERS = {"Content-Type": "application/json"}

app = FastAPI()

# Allow CORS for frontend development
origins = [
    "http://localhost:5173", # Default Vite dev server port
    "http://localhost:3000", # Common React dev server port
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================== �� Helper Functions (with caching) =============
@lru_cache(maxsize=128)
def cached_fetch_ensembl_gene_sequence(gene_id: str, species: str):
    try:
        lookup_url = f"{ENSEMBL_BASE_URL}/lookup/id/{gene_id}?expand=1"
        response = requests.get(lookup_url, headers=ENSEMBL_HEADERS, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        region = f"{data['seq_region_name']}:{data['start']}-{data['end']}"
        seq_url = f"{ENSEMBL_BASE_URL}/sequence/region/{species}/{region}"
        seq_response = requests.get(seq_url, headers=ENSEMBL_HEADERS, timeout=10)
        return seq_response.json()["seq"] if seq_response.ok else None
    except Exception:
        return None

@lru_cache(maxsize=128)
def cached_fetch_ncbi_gene_sequence(symbol: str, organism: str):
    try:
        term = f"{symbol}[Gene Name] AND {organism}[Organism]"
        search = Entrez.esearch(db="nucleotide", term=term, retmax=1)
        record = Entrez.read(search)
        if record["IdList"]:
            gene_id = record["IdList"][0]
            fetch = Entrez.efetch(db="nucleotide", id=gene_id, rettype="fasta", retmode="text")
            seq_record = SeqIO.read(fetch, "fasta")
            return str(seq_record.seq)
    except Exception:
        return None

@lru_cache(maxsize=128)
def cached_explain_with_gemini(crop: str, trait: str, symbol: str, ensembl_id: str = "", sequence_length: int = 0):
    prompt = f"""
    You are an expert plant biotechnologist explaining a CRISPR target to agricultural scientists in India.
    Your tone should be professional yet accessible. Use emojis to add visual cues.

    Please provide a concise explanation for the following gene target:

    **🌱 Crop:** {crop.capitalize()}
    **🎯 Trait for Improvement:** {trait.title()}
    **🧬 Target Gene:** {symbol} (ID: {ensembl_id})

    Structure your response into these four sections:
    
    **1. Gene Function & Significance:**
       - What is the primary role of this gene in the plant?
       - Why is it a crucial target for improving the specified trait?

    **2. CRISPR-Cas9 Strategy:**
       - How would gene editing (e.g., knockout, modification) of this gene lead to the desired trait?
       - Briefly mention the expected molecular outcome (e.g., loss-of-function, altered expression).

    **3. Potential Agronomic Impact:**
       - What are the real-world benefits for farmers if this modification is successful? (e.g., higher yield, better stress tolerance, reduced inputs).
       - Mention any known examples or similar research successes.

    **4. Next Steps & Considerations:**
       - What are the immediate next steps in the research pipeline? (e.g., gRNA validation, transformation, field trials).
       - Mention one or two key challenges or considerations (e.g., off-target effects, regulatory hurdles).
    """
    try:
        return gemini_model.generate_content(prompt).text
    except Exception as e:
        return f"❌ Gemini API call failed: {e}"

def grna_design_basic(dna_seq, pam="NGG", guide_length=20):
    guides = []
    pam_regex = pam.replace("N", "[ATGC]")
    for match in re.finditer(f"(?=([ATGC]{{{guide_length}}}{pam_regex}))", dna_seq.upper()):
        guides.append({
            "sequence": match.group(1)[:guide_length],
            "pam": match.group(1)[guide_length:],
            "start": match.start(),
            "strand": "+",
            "score": round(0.9 - (match.start() % 10) * 0.02, 2)
        })
    return sorted(guides, key=lambda x: x["score"], reverse=True)

def grna_design_chopchop(dna_seq, pam="NGG", genome="Oryza_sativa.IRGSP-1.0.30", scoring="Doench2016", top_n=5):
    """
    Calls the CHOPCHOP API in sliding windows to design and score gRNAs for the entire gene sequence.
    Returns a list of gRNAs with their scores and positions.
    """
    url = "https://chopchop.cbu.uib.no/api/v3/gRNA/"
    max_length = 3000  # CHOPCHOP API sequence length limit
    step = 2000       # Overlap windows for better coverage
    all_guides = []
    seen = set()
    for start in range(0, len(dna_seq), step):
        window_seq = dna_seq[start:start+max_length]
        if len(window_seq) < 20:  # skip too-short windows
            continue
        params = {
            "SEQ": window_seq,
            "GENOME": genome,
            "PAM": pam,
            "TYPE": "CRISPR/Cas9",
            "SCORING": scoring
        }
        try:
            response = requests.post(url, data=params, timeout=30, verify=False)
            response.raise_for_status()
            data = response.json()
            for g in data.get("results", []):
                # Adjust position to full gene
                abs_start = g["start"] + start
                key = (g["gRNA_sequence"], abs_start)
                if key in seen:
                    continue
                seen.add(key)
                all_guides.append({
                    "sequence": g["gRNA_sequence"],
                    "pam": g["PAM"],
                    "start": abs_start,
                    "strand": g["strand"],
                    "score": g.get("score", 0.0)
                })
        except Exception as e:
            print(f"[WARNING] CHOPCHOP window {start}-{start+max_length} failed: {e}")
            continue
    # Sort by score descending and return top_n
    all_guides = sorted(all_guides, key=lambda x: x["score"], reverse=True)
    return all_guides[:top_n]

# ======================  FastAPI Models ===================================
class ReportRequest(BaseModel):
    crop: str
    trait: str

# ====================== 🚀 API Endpoints ==================================
@app.get("/api/crops")
def get_crops():
    """Returns a list of all available crops."""
    return {"crops": list(trait_species_db.keys())}

@app.get("/api/traits/{crop}")
def get_traits(crop: str):
    """Returns a list of available traits for a given crop."""
    if crop not in trait_species_db:
        raise HTTPException(status_code=404, detail="Crop not found")
    return {"traits": list(trait_species_db[crop]["traits"].keys())}

@app.post("/api/generate-report")
def generate_report(request: ReportRequest):
    crop = request.crop
    trait = request.trait

    if crop not in trait_species_db or trait not in trait_species_db[crop]["traits"]:
        raise HTTPException(status_code=404, detail="Invalid crop or trait")

    species = trait_species_db[crop]["scientific_name"]
    gene_info = trait_species_db[crop]["traits"][trait]
    gene_id = gene_info["ensembl_id"]
    symbol = gene_info["symbol"]

    # Fetch sequence (try Ensembl, then NCBI)
    dna_seq = cached_fetch_ensembl_gene_sequence(gene_id, species)
    source = "Ensembl"
    if not dna_seq:
        dna_seq = cached_fetch_ncbi_gene_sequence(symbol, species.replace("_", " "))
        source = "NCBI"

    if not dna_seq:
        raise HTTPException(status_code=404, detail=f"Could not retrieve gene sequence for {symbol} from Ensembl or NCBI.")

    # Use CHOPCHOP for gRNA design and scoring, fallback to basic if error
    try:
        guides = grna_design_chopchop(dna_seq)
        if not guides:
            raise Exception("No guides returned from CHOPCHOP")
    except Exception as e:
        print(f"[WARNING] CHOPCHOP failed: {e}. Falling back to basic gRNA scoring.")
        guides = grna_design_basic(dna_seq)

    explanation = cached_explain_with_gemini(crop, trait, symbol, gene_id, len(dna_seq))

    report = {
        "crop": crop,
        "trait": trait,
        "gene": gene_info,
        "source": source,
        "sequence_length": len(dna_seq),
        "top_grnas": guides[:5],
        "explanation": explanation
    }
    return report

# ========== Additional endpoints for frontend compatibility ==========
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/crops_and_traits")
def crops_and_traits():
    return trait_species_db

# ====================== 🚀 Server Startup ==================================
if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting CRISPR Backend Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🔗 API Documentation: http://localhost:5000/docs")
    print("💚 Health Check: http://localhost:5000/api/health")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=5000) 