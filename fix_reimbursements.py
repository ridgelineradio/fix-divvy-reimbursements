from xml.etree import ElementTree as ET

xml_header = """<?xml version="1.0" encoding="UTF-8"?>
<?OFX OFXHEADER="200" VERSION="220" SECURITY="NONE" OLDFILEUID="NONE" NEWFILEUID="NONE"?>
"""

def modify_qbo_file(input_file_path, output_file_path):
    # Parse the QBO XML file
    tree = ET.parse(input_file_path)
    root = tree.getroot()

    # Iterate over all transaction elements
    for transaction in root.findall('.//STMTTRN'):
        # Replace TRNTYPE value with "DEBIT"
        trntype = transaction.find('TRNTYPE')
        if trntype is not None:
            trntype.text = 'DEBIT'
        
        # Change TRNAMT to a negative number if it's not already
        trnamt = transaction.find('TRNAMT')
        if trnamt is not None and float(trnamt.text) > 0:
            trnamt.text = "{:.2f}".format(-float(trnamt.text))

    # Write the modified content back to a new QBO file
    # tree.write(output_file_path, xml_declaration=True)
    xml_content = ET.tostring(root, encoding="utf-8").decode("utf-8")
    full_content = xml_header + xml_content

    with open(output_file_path, 'w') as f:
        f.write(full_content)

# Example usage
input_file_path = 'original export.qbo'
output_file_path = 'updated file.qbo'
modify_qbo_file(input_file_path, output_file_path)
