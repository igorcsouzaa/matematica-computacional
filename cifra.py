"""Regras da cifra de César, separadas da página e do servidor."""

import json
from pathlib import Path


def carregar_alfabeto(caminho):
    """Lê os caracteres e seus valores (de 1 até N) do arquivo JSON."""
    with Path(caminho).open(encoding="utf-8") as arquivo:
        valores = json.load(arquivo)

    if not isinstance(valores, dict) or not valores:
        raise ValueError("A configuração deve ser um objeto com caracteres e valores.")
    if any(len(caractere) != 1 for caractere in valores):
        raise ValueError("Cada entrada deve representar um único caractere.")
    if any(type(valor) is not int for valor in valores.values()):
        raise ValueError("Os valores dos caracteres devem ser números inteiros.")
    if sorted(valores.values()) != list(range(1, len(valores) + 1)):
        raise ValueError("Os valores devem ir de 1 até N, sem repetições ou lacunas.")
    return valores


def cifrar(texto, chave, valores):
    """Desloca os caracteres configurados; mantém os demais como estão."""
    # Faz o caminho inverso: do número para o caractere.
    caracteres = {valor: caractere for caractere, valor in valores.items()}
    quantidade = len(valores)
    resultado = []

    for caractere in texto:
        if caractere in valores:
            valor_atual = valores[caractere]
            # Subtrair 1 adapta os valores para o intervalo 0 até N - 1.
            # O resto (%) faz a contagem voltar ao início do alfabeto.
            novo_valor = ((valor_atual - 1 + chave) % quantidade) + 1
            resultado.append(caracteres[novo_valor])
        else:
            resultado.append(caractere)

    return "".join(resultado)
