import xml.etree.ElementTree as ET
import json

def parse_tmx(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    tmx_data = []
    
    for tu in root.findall('.//{http://www.lisa.org/tmx14}tu'):
        tu_id = tu.attrib.get('id')
        en_text = ""
        
        for tuv in tu.findall('{http://www.lisa.org/tmx14}tuv'):
            if tuv.attrib.get('{http://www.w3.org/XML/1998/namespace}lang') == 'en':
                seg = tuv.find('{http://www.lisa.org/tmx14}seg').text
                if seg and seg.strip():  # Check if seg is not None and not just whitespace
                    en_text = seg.strip()
                    break
        
        if tu_id and en_text:
            tmx_data.append({"id": tu_id, "text": en_text})
    
    return tmx_data

def write_to_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

def main():
    input_file = './toh1-6-v3.tmx'
    output_file = 'output.jsonl'
    
    tmx_data = parse_tmx(input_file)
    write_to_jsonl(tmx_data, output_file)
    
    print(f"Conversion complete. JSONL file saved as {output_file}")

if __name__ == "__main__":
    main()
