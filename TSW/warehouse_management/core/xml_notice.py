import uuid
from lxml import etree as ET
from .models import *
from io import BytesIO
from .my_func import *

"""Модуль позволяет работать с xml по уведомлениям"""


# https://ru.stackoverflow.com/questions/1064514/Как-создать-xml-на-python-используя-xml-etree-elementtree

def notice_to_xml(idnotice):
    """функция выдает xml файл по id уведомления согласно Постановлению гос там ком РБ № 6 от 12 января 2024 года"""
    try:
        notice = Notice.objects.get(id=idnotice)
    except notice.DoesNotExist:
        notice = None
    if notice:
        UVD = ET.Element('UVD_ZTK', nsmap={'xsi': 'http://www.w3.org/2001/XMLSchema-instance'})
        ET.ElementTree(UVD)
        # SubElement(родительский, тег, attrib = {}, ** дополнительный).
        # Источник: https: // tonais.ru / file / rabota - xml - python - elementtree
        GUID_file = str(uuid.uuid4()).upper()
        dec = ET.SubElement(UVD, 'Declarant', ID=GUID_file)
        notice.GUID = GUID_file
        notice.save()
        # < INFO_D >
        info_d = ET.SubElement(dec, 'INFO_D')
        doc_id = ET.SubElement(info_d, 'DOC_ID')
        doc_id.text = notice.NumberOut
        nom_lic = ET.SubElement(info_d, 'NOM_LIC')
        nom_lic.text = notice.Number[0:14]  # Number - первые 15 символов
        nomu = ET.SubElement(info_d, 'NOMU')
        nomu.text = str_6digits(notice.NumberOut)
        yearreg = ET.SubElement(info_d, 'YEARREG')
        yearreg.text = notice.Number[16]
        journ = ET.SubElement(info_d, 'JOURN')
        journ.text = notice.Number[17]
        napravl = ET.SubElement(info_d, 'NAPRAVL')
        if notice.Direction_of_travel:
            napravl.text = '1'
        else:
            napravl.text = '2'
        pr_tov = ET.SubElement(info_d, 'PR_TOV')
        if notice.Goods_Presence:
            pr_tov.text = 'Т'
        else:
            pr_tov.text = 'П'
        pr_stz = ET.SubElement(info_d, 'PR_STZ')
        pr_stz.text = notice.STZ
        # < / INFO_D >
        # < G_A > # регистрация в месте хранения
        G_A = ET.SubElement(dec, 'G_A')
        DATEU = ET.SubElement(G_A, 'DATEU')
        only_date, only_time = notice.EntryDateTime.date(), notice.EntryDateTime.time()
        DATEU.text = str(only_date)
        TIMEU = ET.SubElement(G_A, 'TIMEU')
        TIMEU.text = str(only_time)
        NUMBERU = ET.SubElement(G_A, 'NUMBERU')
        NUMBERU.text = notice.Number
        UNP = ET.SubElement(G_A, 'UNP')
        UNP.text = notice.UNP
        FIO_ZL = ET.SubElement(G_A, 'FIO_ZL')
        FIO_ZL.text = notice.FIO
        # < /G_A >
        # < G01_N >
        G01_N = ET.SubElement(dec, 'G01_N')
        VES_BR = ET.SubElement(G01_N, 'VES_BR')
        VES_BR.text = str(notice.Gross)
        CELL = ET.SubElement(G01_N, 'CELL')
        CELL.text = notice.Purpose_placement

        # < G01 > # транспортные средства
        G01 = ET.SubElement(G01_N, 'G01')
        TR_NOMER = ET.SubElement(G01, 'TR_NOMER')
        TR_NOMER.text = notice.Truck
        TR_TYPE = ET.SubElement(G01, 'TR_TYPE')
        TR_TYPE.text = notice.Truck_Type
        REG_COUNTRY = ET.SubElement(G01, 'REG_COUNTRY')
        REG_COUNTRY.text = notice.Trailer_Country
        # добавляем прицеп и контейнера, если есть
        if notice.Trailer:
            G01_Trailer = ET.SubElement(G01_N, 'G01')
            TR_NOMER_Trailer = ET.SubElement(G01_Trailer, 'TR_NOMER')
            TR_NOMER_Trailer.text = notice.Trailer
            TR_TYPE_Trailer = ET.SubElement(G01_Trailer, 'TR_TYPE')
            TR_TYPE_Trailer.text = notice.Trailer_Type
            REG_COUNTRY_Trailer = ET.SubElement(G01_Trailer, 'REG_COUNTRY')
            REG_COUNTRY_Trailer.text = notice.Trailer_Country
        if notice.Container1:
            G01_Container1 = ET.SubElement(G01_N, 'G01')
            TR_NOMER_Container1 = ET.SubElement(G01_Container1, 'TR_NOMER')
            TR_NOMER_Container1.text = notice.Container1
            TR_TYPE_Container1 = ET.SubElement(G01_Container1, 'TR_TYPE')
            TR_TYPE_Container1.text = notice.Container1_Type
            REG_COUNTRY_Container1 = ET.SubElement(G01_Container1, 'REG_COUNTRY')
            REG_COUNTRY_Container1.text = notice.Container1_Country
        if notice.Container2:
            G01_Container2 = ET.SubElement(G01_N, 'G01')
            TR_NOMER_Container2 = ET.SubElement(G01_Container2, 'TR_NOMER')
            TR_NOMER_Container2.text = notice.Container1
            TR_TYPE_Container2 = ET.SubElement(G01_Container2, 'TR_TYPE')
            TR_TYPE_Container2.text = notice.Container1_Type
            REG_COUNTRY_Container2 = ET.SubElement(G01_Container2, 'REG_COUNTRY')
            REG_COUNTRY_Container2.text = notice.Container2_Country
        # < /G01_N >

        # < G02 > # документы
        try:
            docs = Doc.objects.filter(NoticeID=idnotice)
        except Doc.DoesNotExist:
            docs = None
        if docs:  # есть документы
            for d in docs:  # бежим по всем документам
                G02 = ET.SubElement(dec, 'G02')
                KOD_DOC = ET.SubElement(G02, 'KOD_DOC')
                KOD_DOC.text = d.Doc_code
                NOM_DOC = ET.SubElement(G02, 'NOM_DOC')
                NOM_DOC.text = d.Doc_number
                DATE_DOC = ET.SubElement(G02, 'DATE_DOC')
                DATE_DOC.text = str(d.Doc_date)
        # < / G02  >
        # < G03 > # получатель товара
        try:
            reps = Recipient.objects.filter(NoticeID=idnotice)
        except Recipient.DoesNotExist:
            reps = None
        if reps:  # есть документы
            for r in reps:  # бежим по всем документам
                G03 = ET.SubElement(dec, 'G03')
                # <G081> УНП - не обязательный
                G082 = ET.SubElement(G03, 'G082')
                G082.text = r.Name
                G083 = ET.SubElement(G03, 'G083')
                G083.text = r.CountryCode
        # < / G03 >
        # < / Declarant >
        # < / UVD_ZTK >

        # выдаем сформированный файл, но в потоке
        # xml_file = BytesIO()
        # tree.write(xml_file, pretty_print=True, encoding='utf-8', xml_declaration=True, standalone='yes')

        # сохранение в файл
        # file_path = '1_.xml'
        # with open(file_path, 'wb') as file:
        #     # Записываем байты из BytesIO в файл
        #     file.write(xml_file.getvalue())

        # возвращение строкой
        return GUID_file, ET.tostring(UVD, pretty_print=True, encoding='utf-8', xml_declaration=True, standalone='yes').decode(
            'utf-8')
    else:
        return False
