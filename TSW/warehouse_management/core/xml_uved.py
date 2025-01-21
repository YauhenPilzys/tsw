import xml.etree.ElementTree as ET

def generate_xml(notice):
    # Создаём корневой элемент
    root = ET.Element("UVD_ZTK")
    declarant = ET.SubElement(root, "Declarant", {"ID": str(notice.guid)})

    # INFO_D
    info_d = ET.SubElement(declarant, "INFO_D")
    ET.SubElement(info_d, "DOCID").text = "1"
    ET.SubElement(info_d, "NOM_LIC").text = notice.warehouse.svh_number if hasattr(notice, 'warehouse') else ""
    ET.SubElement(info_d, "NOMU").text = notice.notification or ""
    ET.SubElement(info_d, "YEARREG").text = notice.year or ""
    ET.SubElement(info_d, "JOURN").text = notice.zhurnal or ""
    ET.SubElement(info_d, "NAPRAVL").text = notice.purpose_placement
    ET.SubElement(info_d, "PR_TOV").text = "Т"
    ET.SubElement(info_d, "PR_STZ").text = notice.stz or "0"

    # G_A
    ga = ET.SubElement(declarant, "G_A")
    ET.SubElement(ga, "DATEU").text = notice.date_in.strftime("%d.%m.%Y")
    ET.SubElement(ga, "TIMEU").text = notice.time_in.strftime("%H:%M:%S")
    ET.SubElement(ga, "NUMBERU").text = notice.number_notification or ""
    ET.SubElement(ga, "UNP").text = notice.unp
    ET.SubElement(ga, "FIO_ZL").text = notice.fio or ""

    # G01_N (Transport)
    g01_n = ET.SubElement(declarant, "G01_N")
    ET.SubElement(g01_n, "VES_BR").text = f"{notice.gross_weight:.2f}"
    ET.SubElement(g01_n, "CELL").text = notice.purpose_placement
    for transport in notice.transport_notice.all():
        g01 = ET.SubElement(g01_n, "G01")
        ET.SubElement(g01, "TR_NOMER").text = transport.number
        ET.SubElement(g01, "TR_TYPE").text = transport.type
        ET.SubElement(g01, "REG_COUNTRY").text = transport.country

    # G02 (Documents)
    for doc in notice.docs.all():
        g02 = ET.SubElement(declarant, "G02")
        ET.SubElement(g02, "KOD_DOC").text = doc.doc_code
        ET.SubElement(g02, "NOM_DOC").text = doc.doc_number
        ET.SubElement(g02, "DATE_DOC").text = doc.doc_date.strftime("%Y-%m-%d")

    # G03 (Recipient)
    g03 = ET.SubElement(declarant, "G03")
    for recipient in notice.recipient.all():
        ET.SubElement(g03, "G082").text = recipient.name
        ET.SubElement(g03, "G083").text = recipient.country

    # Возвращаем сгенерированный XML
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)