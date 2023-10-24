import os
import re

import fitz


def text_remover(
    pdf_input='', pdf_output='', string_find=[''], string_replace=['']
):
    """
    Lê um arquivo PDF e salva um arquivo com o mesmo nome seguido de _censored

    Args:
        pdf_path (str, mandatory): Caminho do arquivo PDF..
        pdf_output (str, optional): Caminho para salvar o PDF. Se não for informada, automaticamente salva com o sufixo '_censored.pdf'.
        string_find (list, optional): Lista de strings a serem buscadas.
        string_replace (list, optional): Lista de strings a serem serem substituídas.

    """

    if len(string_find) > len(string_replace):
        string_replace = [string_replace[0]] * len(string_find)
        print(string_replace)

    if not os.path.exists(pdf_input):
        raise ValueError('Esse arquivo não existe.')

    doc = fitz.open(pdf_input)

    for page in doc:
        for sub in range(len(string_find)):
            print(sub)
            string_finded = string_find[sub]
            string_replaced = string_replace[sub]

            pageTextRect = page.search_for(string_finded, quads=True)
            page.get_fonts()
            if pageTextRect:
                redact = 0
                for redact in pageTextRect:
                    # print(redact)
                    # page_font = page.get_fonts()
                    page.add_redact_annot(quad=redact, text=string_replaced)
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
            # print(f"After {page.number}: \n{pageText}\n\n")
    if pdf_output == '':
        pdf_output = re.sub('[.]pdf', '', pdf_input)
        pdf_output = pdf_output + '_censored.pdf'
    doc.save(pdf_output, garbage=1, clean=True, deflate=True)
