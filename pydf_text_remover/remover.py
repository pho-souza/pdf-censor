import os
import re

import fitz
from fitz import Font, TextWriter, sRGB_to_rgb


def text_remover(
    pdf_input='',
    pdf_output='',
    string_find=[''],
    string_replace=[''],
    folder='',
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

            if pageTextRect:
                # Verifica se há o texto procurado na página
                page.clean_contents()
                redact = 0
                for redact in pageTextRect:
                    if string_replaced:
                        # Seleciona os blocks dentro dessa seção
                        blocks = page.get_text('dict', clip=redact)
                        blocks = blocks['blocks'][0]['lines'][0]['spans'][0]
                        font = blocks['font']
                        origin = fitz.Point(blocks['origin'])
                        ascender = blocks['ascender']
                        descender = blocks['descender']
                        size = blocks['size']
                        flags = blocks['flags']
                        color = sRGB_to_rgb(blocks['color'])
                        color = tuple(ti / 255 for ti in color)
                        ref_fonts = page.get_fonts()
                        fonts = {}
                        fonts['xref'] = []
                        fonts['ext'] = []
                        fonts['type'] = []
                        fonts['basefont'] = []
                        fonts['name'] = []
                        fonts['font'] = []
                        for f in ref_fonts:
                            update_font = re.findall(font, f[3])
                            font_name = re.sub('.*?\+', '', f[3])
                            if update_font:
                                fonts['xref'].append(f[0])
                                fonts['ext'].append(f[1])
                                fonts['type'].append(f[2])
                                fonts['basefont'].append(font_name)
                                fonts['name'].append(f[4])
                                ff = doc.extract_font(xref=f[0])
                                fontbuffer = ff[-1]
                                # myfont = fitz.Font(fontbuffer=fontbuffer)
                                fonts['font'].append(
                                    Font(fontbuffer=fontbuffer)
                                )
                        for i in fonts.keys():
                            size_fonts = 0  # len(fonts[i]) - 1
                            fonts[i] = fonts[i][size_fonts]
                        # text_length = fitz.get_text_length(
                        #     text=string_replaced,
                        #     fontname='cour',
                        #     encoding='utf-8',
                        #     fontsize=size,
                        # )
                        # textwrite method for add text
                        # font_used = fitz.Font(fontname=fonts['font'])
                        text_added = TextWriter(page_rect=page.rect)
                        size = size * (ascender - descender)
                        text_added.append(
                            pos=redact.bottom_left,
                            text=string_replaced,
                            font=fonts['font'],
                            fontsize=size,
                            small_caps=True,
                        )
                        # possible implementation
                        # text_added.fill_textbox(
                        #     rect=redact,
                        #     text=string_replaced,
                        #     font=fonts['font'],
                        #     fontsize=size
                        # )
                        page.add_redact_annot(
                            quad=redact,
                            # text=string_replaced,
                            # fontsize=size,
                            # fontname=fonts['name'],
                            # text_color=color,
                            fill=False,
                        )
                        page.apply_redactions(
                            images=fitz.PDF_REDACT_IMAGE_NONE
                        )
                        text_added.write_text(page=page, color=color)
                    else:
                        page.add_redact_annot(quad=redact, fill=False)
                    page.clean_contents()
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    if folder == '' or not os.path.isdir(folder):
        folder = os.path.dirname(pdf_input)

    if pdf_output == '':
        pdf_output = os.path.basename(pdf_input)
        pdf_output = pdf_output + '_censored.pdf'

    pdf_output = os.path.join(folder, pdf_output)
    print(f'PDF file save location: "{pdf_output}"')

    doc.save(pdf_output, garbage=3, clean=True, deflate=True)
