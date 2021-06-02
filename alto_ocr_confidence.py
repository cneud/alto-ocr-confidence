#!/usr/bin/env python
# Usage: python alto_ocr_confidence.py <inputdir>

import os
import sys
import xml.etree.ElementTree as ET

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
             'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
             'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}

def parse_alto(fpath, f):
    try:
        tree = ET.parse(fpath)
    except ET.ParseError as e:
        print(f"Parser Error in file '{fpath}': {e}")
    else:
        score = 0
        count = 0
        xmlns = tree.getroot().tag.split('}')[0].strip('{')  # extract namespace from root
        if xmlns in namespace.values():
            for elem in tree.iterfind('.//{%s}String' % xmlns):
                    wc = elem.attrib.get('WC')
                    if wc is not None:   
                        score += float(wc)
                        count += 1
            if count > 0:
                confidence = score / count
                result = round(100 * confidence, 2)
                sys.stdout.write(f'\nFile: {f}, Confidence: {result}')
                return result
            else:
                sys.stdout.write(f'\nFile: {f}, Confidence: 00.00')
                return 0
        else:
            sys.stdout.write(f'\nERROR: File "{f}" does not appear to be a valid ALTO file (namespace declaration missing)')
            return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python %s <inputdir>" % os.path.basename(__file__))
        sys.exit(-1)
    files = [f for f in os.listdir(sys.argv[1]) if f.endswith('xml') or f.endswith('.alto')]
    conf = []
    for f in files:
        fpath = os.path.join(sys.argv[1], f)
        conf.append(parse_alto(fpath, f))
    
    print(f"\n\nConfidence of folder: {round(sum([e for e in conf if e is not None])/len(files), 2)}")
