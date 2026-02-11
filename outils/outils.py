from importlib.resources import read_text
import requests
from typing import List, Annotated, Optional, Dict
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.tools import tool
import os


@tool
def scrape_website(urls: list[str]) -> str:
    """Utilise requests et bs4 pour scraper les pages web fournies"""
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name ="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
            for doc in docs
        ]
    )


@tool
def create_outline(
        points: Annotated[List[str], "Liste des points ou sections principaux"],
        file_name: Annotated[str, "Chemin du fichier pour enregistrer le plan"],
) -> Annotated[str, "Chemin du fichier plan enregistré"]:
    """Créer et enregistrer un plan"""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "w") as file:
        for i, point in enumerate(points):
            file.write(f"{i + 1}. {point}\n")
    return f'plan enregistré dans {file_name}'


@tool
def read_document(
        file_name: Annotated[str, "Chemin du fichier à lire"],
        start: Annotated[Optional[int], "La ligne de début, Par défaut 0"] = None,
        end: Annotated[Optional[int], "La ligne de fin, Par défaut None"] = None,
) -> str:
    """Lire le document spécifié"""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "r") as file:
        lines = file.readlines()
    if start is None:
        start = 0
    return "\n".join(lines[start:end])


@tool
def write_document(
        content: Annotated[str, "Contenu texte à écrire dans le document"],
        file_name: Annotated[str, "Chemin du fichier pour enregistrer le document"],
) -> str:
    """Créer et enregistrer un document"""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "w") as file:
        file.write(content)
    return f'document enregistré dans {file_name}'


@tool
def edit_document(
        file_name: Annotated[str, "Chemin du fichier à éditer"],
        insert: Annotated[
            Dict[int, str], "Dictionnaire où la clé est le numéro de ligne et la valeur le texte à insérer"],
) -> str:
    """Éditer le document en insérant du texte à des numéros de ligne spécifiés"""
    file_to_use = os.path.join(os.getcwd(), "temp", file_name)
    with open(file_to_use, "r") as file:
        lines = file.readlines()

    sorted_insert = sorted(insert.items())
    for line_number, text in sorted_insert:
        if 1 <= line_number <= len(lines) + 1:
            lines.insert(line_number - 1, text + "\n")
        else:
            return f"Erreur: le numéro de ligne {line_number} est hors limites"

    with open(file_to_use, "w") as file:
        file.writelines(lines)
    return f'document édité et enregistré dans {file_name}'