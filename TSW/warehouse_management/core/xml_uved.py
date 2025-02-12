import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def generate_xml(notice):
    """Генерация XML с форматированием, чтобы корректно отображался в Блокноте"""
    # Создаём корневой элемент
    root = ET.Element("UVD_ZTK", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})
    declarant = ET.SubElement(root, "Declarant", {"ID": str(notice.guid).upper()})

    # INFO_D
    info_d = ET.SubElement(declarant, "INFO_D")
    ET.SubElement(info_d, "DOCID").text = str(notice.id).upper()
    ET.SubElement(info_d, "NOM_LIC").text = (
        getattr(notice.order.warehouse, "svh_number", "СВ-1601/0000304").upper()
    )
    ET.SubElement(info_d, "NOMU").text = (notice.notification or "").upper()
    ET.SubElement(info_d, "YEARREG").text = (notice.year or "").upper()
    ET.SubElement(info_d, "JOURN").text = (notice.zhurnal or "").upper()
    ET.SubElement(info_d, "NAPRAVL").text = (notice.direction_vehicle or "").upper()
    ET.SubElement(info_d, "PR_TOV").text = "Т".upper()
    ET.SubElement(info_d, "PR_STZ").text = (notice.stz or "0").upper()

    # G_A (Общие сведения)
    ga = ET.SubElement(declarant, "G_A")
    ET.SubElement(ga, "DATEU").text = (
        notice.date_in.strftime("%d.%m.%Y").upper() if notice.date_in else ""
    )
    ET.SubElement(ga, "TIMEU").text = (
        notice.time_in.strftime("%H:%M:%S").upper() if notice.time_in else ""
    )
    ET.SubElement(ga, "NUMBERU").text = (notice.number_notification or "").upper()
    ET.SubElement(ga, "UNP").text = (notice.unp or "").upper()
    ET.SubElement(ga, "FIO_ZL").text = (notice.fio or "").upper()

    # G01_N (Transport)
    g01_n = ET.SubElement(declarant, "G01_N")
    ET.SubElement(g01_n, "VES_BR").text = (
        f"{notice.gross_weight:.2f}".upper() if notice.gross_weight is not None else "0.00"
    )
    ET.SubElement(g01_n, "CELL").text = (notice.purpose_placement or "").upper()

    for transport in notice.transport_notice.all():
        g01 = ET.SubElement(g01_n, "G01")
        ET.SubElement(g01, "TR_NOMER").text = (transport.number or "").upper()
        ET.SubElement(g01, "TR_TYPE").text = (transport.type or "").upper()
        ET.SubElement(g01, "REG_COUNTRY").text = (transport.country or "").upper()

    # G02 (Documents)
    for doc in notice.docs.all():
        g02 = ET.SubElement(declarant, "G02")
        ET.SubElement(g02, "KOD_DOC").text = (doc.doc_code or "").upper()
        ET.SubElement(g02, "NOM_DOC").text = (doc.doc_number or "").upper()
        ET.SubElement(g02, "DATE_DOC").text = (
            doc.doc_date.strftime("%Y-%m-%d").upper() if doc.doc_date else ""
        )

    # G03 (Recipient)
    g03 = ET.SubElement(declarant, "G03")
    for recipient in notice.recipient.all():
        ET.SubElement(g03, "G082").text = (recipient.name or "").upper()
        ET.SubElement(g03, "G083").text = (recipient.country or "").upper()

    # Преобразуем XML в строку с отступами
    raw_xml = ET.tostring(root, encoding="utf-8")
    formatted_xml = parseString(raw_xml).toprettyxml(indent="  ")  # Делаем форматирование

    # Принудительно заменяем переносы строк для Windows (Блокнот)
    formatted_xml = formatted_xml.replace("\n", "\r\n")

    return formatted_xml.encode("utf-8")  # Преобразуем в байты для сохранения








# def generate_xml(notice):
#     # Создаём корневой элемент
#     root = ET.Element("UVD_ZTK", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance"})
#     declarant = ET.SubElement(root, "Declarant", {"ID": str(notice.guid).upper()})
#
#     # INFO_D
#     info_d = ET.SubElement(declarant, "INFO_D")
#     ET.SubElement(info_d, "DOCID").text = str(notice.id).upper()
#     ET.SubElement(info_d, "NOM_LIC").text = (
#         notice.warehouse.svh_number.upper() if hasattr(notice, "warehouse") and notice.warehouse.svh_number else ""
#     )
#     ET.SubElement(info_d, "NOMU").text = (notice.notification or "").upper()
#     ET.SubElement(info_d, "YEARREG").text = (notice.year or "").upper()
#     ET.SubElement(info_d, "JOURN").text = (notice.zhurnal or "").upper()
#     ET.SubElement(info_d, "NAPRAVL").text = (notice.direction_vehicle or "").upper()
#     ET.SubElement(info_d, "PR_TOV").text = "Т".upper()
#     ET.SubElement(info_d, "PR_STZ").text = (notice.stz or "0").upper()
#
#     # G_A (Общие сведения)
#     ga = ET.SubElement(declarant, "G_A")
#     ET.SubElement(ga, "DATEU").text = (
#         notice.date_in.strftime("%d.%m.%Y").upper() if notice.date_in else ""
#     )
#     ET.SubElement(ga, "TIMEU").text = (
#         notice.time_in.strftime("%H:%M:%S").upper() if notice.time_in else ""
#     )
#     ET.SubElement(ga, "NUMBERU").text = (notice.number_notification or "").upper()
#     ET.SubElement(ga, "UNP").text = (notice.unp or "").upper()
#     ET.SubElement(ga, "FIO_ZL").text = (notice.fio or "").upper()
#
#     # G01_N (Transport)
#     g01_n = ET.SubElement(declarant, "G01_N")
#     ET.SubElement(g01_n, "VES_BR").text = (
#         f"{notice.gross_weight:.2f}".upper() if notice.gross_weight is not None else "0.00"
#     )
#     ET.SubElement(g01_n, "CELL").text = (notice.purpose_placement or "").upper()
#
#     for transport in notice.transport_notice.all():
#         g01 = ET.SubElement(g01_n, "G01")
#         ET.SubElement(g01, "TR_NOMER").text = (transport.number or "").upper()
#         ET.SubElement(g01, "TR_TYPE").text = (transport.type or "").upper()
#         ET.SubElement(g01, "REG_COUNTRY").text = (transport.country or "").upper()
#
#     # G02 (Documents)
#     for doc in notice.docs.all():
#         g02 = ET.SubElement(declarant, "G02")
#         ET.SubElement(g02, "KOD_DOC").text = (doc.doc_code or "").upper()
#         ET.SubElement(g02, "NOM_DOC").text = (doc.doc_number or "").upper()
#         ET.SubElement(g02, "DATE_DOC").text = (
#             doc.doc_date.strftime("%Y-%m-%d").upper() if doc.doc_date else ""
#         )
#
#     # G03 (Recipient)
#     g03 = ET.SubElement(declarant, "G03")
#     for recipient in notice.recipient.all():
#         ET.SubElement(g03, "G082").text = (recipient.name or "").upper()
#         ET.SubElement(g03, "G083").text = (recipient.country or "").upper()
#
#     # Возвращаем сгенерированный XML
#     return ET.tostring(root, encoding="utf-8", xml_declaration=True)



# def generate_xml(notice):
#     # Создаём корневой элемент
#     root = ET.Element("UVD_ZTK")
#     declarant = ET.SubElement(root, "Declarant", {"ID": str(notice.guid).upper()})
#
#     # INFO_D
#     info_d = ET.SubElement(declarant, "INFO_D")
#     ET.SubElement(info_d, "DOCID").text = str(notice.id).upper()
#     ET.SubElement(info_d, "NOM_LIC").text = (notice.warehouse.svh_number if hasattr(notice, 'warehouse') else "").upper()
#     ET.SubElement(info_d, "NOMU").text = (notice.notification or "").upper()
#     ET.SubElement(info_d, "YEARREG").text = (notice.year or "").upper()
#     ET.SubElement(info_d, "JOURN").text = (notice.zhurnal or "").upper()
#     ET.SubElement(info_d, "NAPRAVL").text = notice.purpose_placement.upper()
#     ET.SubElement(info_d, "PR_TOV").text = "Т".upper()
#     ET.SubElement(info_d, "PR_STZ").text = (notice.stz or "0").upper()
#
#     # G_A
#     ga = ET.SubElement(declarant, "G_A")
#     ET.SubElement(ga, "DATEU").text = notice.date_in.strftime("%d.%m.%Y").upper()
#     ET.SubElement(ga, "TIMEU").text = notice.time_in.strftime("%H:%M:%S").upper()
#     ET.SubElement(ga, "NUMBERU").text = (notice.number_notification or "").upper()
#     ET.SubElement(ga, "UNP").text = notice.unp.upper()
#     ET.SubElement(ga, "FIO_ZL").text = (notice.fio or "").upper()
#
#     # G01_N (Transport)
#     g01_n = ET.SubElement(declarant, "G01_N")
#     ET.SubElement(g01_n, "VES_BR").text = f"{notice.gross_weight:.2f}".upper()
#     ET.SubElement(g01_n, "CELL").text = notice.purpose_placement.upper()
#     for transport in notice.transport_notice.all():
#         g01 = ET.SubElement(g01_n, "G01")
#         ET.SubElement(g01, "TR_NOMER").text = transport.number.upper()
#         ET.SubElement(g01, "TR_TYPE").text = transport.type.upper()
#         ET.SubElement(g01, "REG_COUNTRY").text = transport.country.upper()
#
#     # G02 (Documents)
#     for doc in notice.docs.all():
#         g02 = ET.SubElement(declarant, "G02")
#         ET.SubElement(g02, "KOD_DOC").text = doc.doc_code.upper()
#         ET.SubElement(g02, "NOM_DOC").text = doc.doc_number.upper()
#         ET.SubElement(g02, "DATE_DOC").text = doc.doc_date.strftime("%Y-%m-%d").upper()
#
#     # G03 (Recipient)
#     g03 = ET.SubElement(declarant, "G03")
#     for recipient in notice.recipient.all():
#         ET.SubElement(g03, "G082").text = recipient.name.upper()
#         ET.SubElement(g03, "G083").text = recipient.country.upper()
#
#     # Возвращаем сгенерированный XML
#     return ET.tostring(root, encoding="utf-8", xml_declaration=True)