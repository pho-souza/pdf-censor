import os
import re

import fitz

from fitz import sRGB_to_rgb


def text_remover(
    pdf_input='',
    pdf_output='',
    string_find=[''],
    string_replace=[''],
    folder = ''
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
            string_finded = string_find[sub]
            string_replaced = string_replace[sub]
            
            # get textpag
            pageTextRect = page.search_for(string_finded, quads=False)
            # for block in pageTextRect['blocks']:
            
            # print(f'\n\npageTextRect: {pageTextRect}\n\n=================\n\n')
            # print(f'\n\npageTextRect: {blocks}\n\n=================\n\n')
            if pageTextRect:
                redact = 0
                for redact in pageTextRect:
                    if string_replaced:
                        blocks = blocks['blocks'][0]['lines'][0]['spans'][0]
                        font = blocks['font']
                        size = blocks['size']
                        color = sRGB_to_rgb(blocks['color'])
                        color = tuple(ti/255 for ti in color)
                        ref_fonts = page.get_fonts()
                        fonts = []
                        for f in ref_fonts:
                            update_font = re.findall(font, f[3])
                            if update_font:
                                fonts.append(f[4])
                        fonts = fonts[len(fonts)-1]
                        page.add_redact_annot(
                            quad=redact,
                            text=string_replaced,
                            fontsize=size,
                            fontname=fonts,
                            text_color=color,
                            fill=False
                        )
                    else:
                        page.add_redact_annot(
                            quad=redact,
                            fill=False
                        )
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)
    if folder == '':
        folder = os.path.dirname(input)
    elif not os.path.isdir(folder):
        folder = os.path.dirname(input)

    if pdf_output == '':
        pdf_output = os.path.basename(pdf_input)
        pdf_output = pdf_output + '_censored.pdf'

    pdf_output = os.path.join(folder, pdf_output)

    doc.save(pdf_output, garbage=1, clean=True, deflate=True)
