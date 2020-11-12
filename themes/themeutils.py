import xml.etree.ElementTree as ET

def consume_xml_sheet(filename):
    root = ET.parse(filename).getroot()
    sheet_dict = {}
    for child in root.getchildren():
        elem = {}
        for key in ["x", "y", "width", "height"]:
            elem[key] = int(child.get(key))
        sheet_dict[child.get("name").split(".")[0]] = elem
    return sheet_dict

def consume_txt_sheet(filename):
    file = open(filename, "r").read()
    sheet_dict = {}
    for line in file.split("\n"):
        if len(line) == 0:
            continue
        key, elems = line.split("=")
        key = key.rstrip(" ")
        elems = elems.lstrip(" ")
        x, y, width, height = elems.split(" ")
        sheet_dict[key] = {"x": int(x), "y": int(y), "width": int(width), "height": int(height)}
    return sheet_dict
