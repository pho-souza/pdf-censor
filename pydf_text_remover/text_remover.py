import fitz
import os
import pathlib as path
import PyPDF2
from fpdf import FPDF
import pdfminer.pdfparser as pdfparser
import re

# lista = "C:/Users/pedro//Downloads//thunae//constitucional/"

files = os.listdir(lista)

for i in range(len(files)):
    files[i] = lista + '/' + files[i]
    files[i] = os.path.abspath(files[i])

# substitute_text = function(pdf_path, find_str, sub_str):
string_find = ['PEDRO HENRIQUE OLIVEIRA DE SOUZA - 06587665110',
               'O conteúdo deste livro eletrônico é licenciado para',
               ', vedada, por quaisquer meios e a qualquer título,',
               'a sua reprodução, cópia, divulgação ou distribuição, sujeitando-se aos infratores à responsabilização civil e criminal.',
               'Constitucional']

string_replace = ['MEU NOME TAVA AQUI HAHAHA',
                   '',
                   '',
                   '',
                   'AAAA']

def remove_string_pdf(pdf_path ='', string_find = [''], string_replace = ['']):
    doc = fitz.open(pdf_path)
    # for page in doc:
    #    for xref in page.get_contents():
    #        stream = doc.xref_stream(xref).replace(string_find, string_replaced)
    #        doc.update_stream(xref, stream)
    # page_last_file = doc[len(doc)-1].search_for(string_find)
    for page in doc:
        for sub in range(len(string_find)):
            string_finded = string_find[sub]
            string_replaced = string_replace[sub]
            
            # print(sub)
            
            pageTextRect = page.search_for(string_finded, quads = True)
            # pageText = page.get_textbox(pageTextRect)
            page.get_fonts()
            # print(f"Before {page.number}: \n{pageText}\n\n")

            if pageTextRect:
                redact = 0
                for redact in pageTextRect:
                    # print(redact)
                    page_font = page.get_fonts()
                    page.add_redact_annot(quad = redact, text= string_replaced)
                page.apply_redactions(images = fitz.PDF_REDACT_IMAGE_NONE)

            # print(f"After {page.number}: \n{pageText}\n\n")
    
    pdf_output = re.sub("[.]pdf","",pdf_path)
    
    pdf_output = pdf_output + "_censored.pdf"

    doc.save(pdf_output, garbage = 4, clean = True, deflate = True)


i = files[0]
for i in files:
    remove_string_pdf(pdf_path=i,string_find= string_find,string_replace=string_replace)

