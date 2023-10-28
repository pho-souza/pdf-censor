import os
import re
import shutil

from pytest import raises

import pydf_text_remover.remover as remover

test_dir = os.path.abspath(os.path.dirname(__file__))
resource_dir = os.path.join(test_dir, 'resources')
wikipedia_pdf = os.path.join(resource_dir, 'PDF.pdf')
wikipedia_pdf_censored = os.path.join(resource_dir, 'PDF_censored.pdf')


def test_pdf_input_does_not_exist():
    msg_error = 'Esse arquivo não existe.'

    # Configuração do teste
    pdf_not_exist = os.path.join(resource_dir, 'NOT_EXISTS.PDF')
    with raises(ValueError) as error:
        remover.text_remover(pdf_input=pdf_not_exist)
        assert msg_error == error.value.args[0]


def test_string_replace_empty():
    msg_error = ''
    string_find = ['PDF']

    # Configuração do teste
    remover.text_remover(pdf_input=wikipedia_pdf, string_find=string_find)
    assert 1 == 1
    # os.remove(wikipedia_pdf_censored)


def test_output_path_working():
    output_name = os.path.join(resource_dir, 'NEW_PDF.pdf')
    string_find = ['PDF', '__', '__']

    # Configuração do teste
    remover.text_remover(
        pdf_input=wikipedia_pdf,
        pdf_output=output_name,
        string_find=string_find,
    )
    assert os.path.exists(output_name)
    # os.remove(wikipedia_pdf_censored)


def test_replace():
    output_name = os.path.join(resource_dir, 'PDF_SUBS.pdf')
    string_find = ['PDF', 'file', 'text']
    string_replace = ['FDP', 'ffff', 'bext']

    # Configuração do teste
    remover.text_remover(
        pdf_input=wikipedia_pdf,
        pdf_output=output_name,
        string_find=string_find,
        string_replace=string_replace,
    )
    assert os.path.exists(output_name)
    # os.remove(wikipedia_pdf_censored)
