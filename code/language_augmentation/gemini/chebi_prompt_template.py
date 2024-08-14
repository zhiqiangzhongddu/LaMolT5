chebi_template = {
     "S":(
        "[SMILES string of target molecule]: {}\n"
        "[Description of the molecule]: {}\n"
        "[Task]: Rewrite the following molecule with its SMILES and caption.The new rewritten caption should be elaborate, descriptive, and concise, highlighting the key structural features and biological activities of the molecule. Only output rewritten caption without any header and linebreak.\n"
     ),
    "IF": (
        "[SMILES string of target molecule]: {}\n"
        "[Description of the molecule]: {}\n"
        "[Task]: Rewrite the description of the molecule 3 times. Captions should be elaborate, descriptive, and concise, highlighting the key structural features and biological activities of the molecule.\n"
    ),
    "IFC": (
        "[SMILES string of target molecule]: {}\n"
        "[Description of the molecule]: {}."
    ),
    "I": "Rewrite the following molecules with their SMILES and caption:\n",
    "FS": (
        "Rewrite the caption that describe the molecule noted in the SMILES format 3 times. "
        "The generated descriptions should only be written in a Python list format and nothing else. "
        "[Knowledge]: {}\n"
        "[SMILES string of target molecule]: {}. "
    ),
    "FSKnowledgePos": (
        "[Molecule SMILES string]: {}\n"
        "[Correct caption]: {}"
    ),
    "FSKnowledgeNeg": (
        "[Molecule SMILES string]: {}\n"
        "[Incorrect caption]: {}"
    ),
    "FSC": (
        "[Knowledge]: {}\n"
        "[SMILES string of target molecule]: {}. "
        "[Description target molecule]: {} "
        "[Task]: "
        "Rewrite the caption that describe the molecule noted in the SMILES format 3 times. Write the descriptions in a python list format."
    ),
    "FSCKnowledgePos": (
        "[Molecule SMILES string]: {}; "
        "[Caption]: {} "
        "This is a correct rewriting of the caption."
    ),
    "FSCKnowledgeNeg": (
        "[Molecule SMILES string]: {}; "
        "[Caption]: {} "
        "This is not a correct rewriting of the caption."
    ),
}
