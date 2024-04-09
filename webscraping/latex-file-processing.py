import os
import re

def find_bib_files(directory):
    bib_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".bib", ".bbl", ".cbx", ".bbx")):  # Added support for .bbl, .cbx, .bbx
                bib_files.append(os.path.join(root, file))
    return bib_files

def extract_references_from_bib(bib_file):
    references = []
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_data = f.read()
        # Check file extension to determine parsing logic
        if bib_file.endswith('.bib'):
            # Regular expression to find reference entries
            pattern = r"@.*?{.*?,\n.*?}"
            matches = re.findall(pattern, bib_data, re.DOTALL)
            for match in matches:
                references.append(match.strip())
        elif bib_file.endswith(('.bbl', '.cbx', '.bbx')):
            # Implement parsing logic for .bbl, .cbx, .bbx files
            # Example parsing logic for .bbl files:
            references.extend(parse_bbl(bib_data))  # You'll need to implement parse_bbl function
        else:
            print(f"Unsupported file format: {bib_file}")
    return references

def parse_bbl(bbl_data):
    references = []
    # Regular expression to find formatted references
    pattern = r"\\bibitem{.*?}(.*?)(?=\\bibitem|\Z)"
    matches = re.findall(pattern, bbl_data, re.DOTALL)
    for match in matches:
        # Clean up the reference and append it to the list
        reference = match.strip().replace('\n', ' ')
        references.append(reference)
    return references


def find_references_in_tex(tex_file):
    references = []
    with open(tex_file, 'r', encoding='utf-8') as f:
        tex_data = f.read()
        # Regular expression to find reference section
        pattern = r"\\bibliography{.*?}"
        match = re.search(pattern, tex_data)
        if match:
            bib_file = match.group(0).split("{")[1].split("}")[0]
            bib_file_path = os.path.join(os.path.dirname(tex_file), bib_file + ".bib")
            if os.path.exists(bib_file_path):
                bib_references = extract_references_from_bib(bib_file_path)
                references.extend(bib_references)
            else:
                print(f"Warning: Bib file '{bib_file_path}' not found.")
    return references

def find_references(directory):
    bib_files = find_bib_files(directory)
    print(bib_files)

    if bib_files:
        references = []
        for bib_file in bib_files:
            references.extend(extract_references_from_bib(bib_file))
        return references
    else:
        references = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".tex"):
                    tex_file = os.path.join(root, file)
                    tex_references = find_references_in_tex(tex_file)
                    references.extend(tex_references)
        return references

# Example usage:
directory = "extracted_latex"
references = find_references(directory)
for ref in references:
    print(ref)
