from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from os import mkdir, chdir

def set_need_appearances_writer(writer: PdfFileWriter):
    # See 12.7.2 and 7.7.2 for more information: http://www.adobe.com/content/dam/acom/en/devnet/acrobat/pdfs/PDF32000_2008.pdf
    try:
        catalog = writer._root_object
        # get the AcroForm tree
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})

        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer


def gen_dip(jmeno, infile):
    pdf = PdfFileReader(open(infile, "rb"), strict=False)
    if "/AcroForm" in pdf.trailer["/Root"]:
        pdf.trailer["/Root"]["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    pdf2 = PdfFileWriter()
    set_need_appearances_writer(pdf2)
    if "/AcroForm" in pdf2._root_object:
        pdf2._root_object["/AcroForm"].update(
            {NameObject("/NeedAppearances"): BooleanObject(True)})

    field_dictionary = {"Jmeno": jmeno}

    pdf2.addPage(pdf.getPage(0))
    pdf2.updatePageFormFieldValues(pdf2.getPage(0), field_dictionary)
    outputStream = open("./OUT/" + jmeno+".pdf", "wb")
    pdf2.write(outputStream)



vystup = "./OUT/"
try:
    chdir(vystup)
except FileNotFoundError:
    mkdir(vystup)

with open("seznam_jmen.txt", mode="r", encoding="utf-8") as soubor:
    for jmeno in soubor:
        jmeno1 = jmeno.strip().split(" ")
        if (jmeno1[0].endswith("a")) and (jmeno1[0] != "Jirka"):
            infile = "Test_holky.pdf"
            gen_dip(jmeno.strip(), infile)
            
        else:
            infile = "Test_kluci.pdf"
            gen_dip(jmeno.strip(), infile)
