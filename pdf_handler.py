import os
from typing import Dict, List
import re
import unicodedata
from pdfminer.high_level import extract_text


def _p(texto: str) -> str:
    """
    Padroniza texto:
    deixa tudo minusculo,
    remove acentuacao, pontos, multiplos espacos, linhas em branco
    """

    texto = texto.lower().replace(".", " ")

    texto = re.sub(
        r"[ \t]+", " ", texto
    )  # troca multiplos espacos/tabs/quebras por 1 espaco
    texto = re.sub(r"\n\s*\n", "\n", texto)  # remove linhas em branco
    texto = texto.strip()

    texto = "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )

    return texto


def get_text(file_path: str) -> List[Dict[str, str]]:

    return _p(extract_text(file_path))


def is_simplificado(texto: str) -> bool:
    """
    Avalia se o texto eh um relatorio simplificado (retorna True) ou nao (False)
    """
    padrao = "relatorio final simplificado"
    return re.search(padrao, texto[1300:1700], re.S) is not None


def get_historico(texto: str):

    padrao = r"1\s+1\s+historico do voo(.*?)2\s+analise \(comentarios\s*/\s*pesquisas\)"
    historico_text = re.search(padrao, texto, re.S)

    return historico_text


def get_labels(texto: str, simplificado: bool) -> Dict[str, str]:
    """
    TODO:
    - levantar erro caso divida errado o label
    - extrair label de relatorio completo
    - documentacao
    """

    labels_dict = {}

    if simplificado:
        padrao = r"3 2 fatores contribuintes(.*?)4 recomendacoes de seguranca"
        labels_text = re.search(
            padrao, texto, re.S
        )  # Apenas o pedaco do texto do item 3.2

        if labels_text:

            linhas = [
                l.strip(" -;\n") for l in labels_text.group(1).splitlines() if l.strip()
            ]
            for l in linhas:
                partes = re.split(r"\s[–-]\s", l, maxsplit=1)  # aceita – ou -
                if len(partes) == 2:
                    labels_dict[partes[0]] = partes[1][:1]
                else:
                    print("ERRO nao dividiu corretamente o label")
        else:
            print("Trecho não encontrado")
    else:
        print("Relatorio Completo: em desenvolvimento")

    return labels_dict


# ============================


def pdf_handler(file, file_name):
    resumo = {}
    new_file = {}

    text_araw = get_text(file)
    simplificado = is_simplificado(text_araw)

    historico = get_historico(text_araw)

    labels = get_labels(text_araw, simplificado)
    new_file["labels"] = labels

    resumo[f"relatorio"] = (file_name, "completo/simplificado")  # ATENCAO

    return new_file  # ATENCAO, so retorna o ultimo
