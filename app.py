"""Servidor local usando apenas a biblioteca padrão do Python."""

from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
import json
import unicodedata
from urllib.parse import parse_qs

from cifra import carregar_alfabeto, cifrar


PASTA = Path(__file__).resolve().parent
VALORES = carregar_alfabeto(PASTA / "config.json")
MODELO = Template((PASTA / "templates" / "index.html").read_text(encoding="utf-8"))


class Servidor(BaseHTTPRequestHandler):
    def responder(self, conteudo, tipo="text/html; charset=utf-8", status=200):
        dados = conteudo.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def mostrar_pagina(self, texto="", chave="3", resultado="", erro="", status=200):
        quantidade = len(VALORES)
        contas = []
        if resultado:
            numero = int(chave)
            sinal = "+" if numero >= 0 else "−"
            unidade = "caractere" if abs(numero) == 1 else "caracteres"
            nomes = {" ": "espaço", "\n": "quebra de linha", "\r": "retorno de carro", "\t": "tabulação"}
            for original, cifrado in zip(unicodedata.normalize("NFC", texto), resultado):
                nome = nomes.get(original, original)
                destino = nomes.get(cifrado, cifrado)
                if original in VALORES:
                    conta = f"{nome} {sinal} {abs(numero)} {unidade} = {destino}"
                else:
                    conta = f"{nome} não faz parte da lista; mantém o mesmo caractere = {destino}"
                contas.append(f"<li>{escape(conta)}</li>")
        pagina = MODELO.substitute(
            texto=escape(texto),
            chave=escape(chave),
            resultado=escape(resultado),
            contas="".join(contas),
            contas_ocultas="" if contas else "hidden",
            erro=escape(erro),
            erro_oculto="" if erro else "hidden",
            quantidade=quantidade,
            max_chave=quantidade - 1,
            alfabeto=escape(json.dumps(sorted(VALORES, key=VALORES.get), ensure_ascii=False), quote=True),
            aba_inicial="cifrar" if self.command == "POST" else "visualizar",
        )
        self.responder(pagina, status=status)

    def do_GET(self):
        if self.path == "/":
            self.mostrar_pagina()
        elif self.path == "/style.css":
            self.responder(
                (PASTA / "static" / "style.css").read_text(encoding="utf-8"),
                "text/css; charset=utf-8",
            )
        elif self.path == "/visual.js":
            self.responder(
                (PASTA / "static" / "visual.js").read_text(encoding="utf-8"),
                "text/javascript; charset=utf-8",
            )
        else:
            self.responder("Página não encontrada.", status=404)

    def do_POST(self):
        if self.path != "/":
            self.responder("Página não encontrada.", status=404)
            return

        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if not 0 <= tamanho <= 100_000:
                self.responder("Texto muito grande para esta demonstração.", status=413)
                return
            corpo = self.rfile.read(tamanho).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            self.responder("Requisição inválida.", status=400)
            return

        dados = parse_qs(corpo, keep_blank_values=True)
        texto = dados.get("texto", [""])[0]
        chave = dados.get("chave", [""])[0]

        try:
            numero = int(chave)
        except ValueError:
            self.mostrar_pagina(texto, chave, erro="Informe uma chave inteira, como 3 ou -3.", status=400)
            return
        if not texto.strip():
            self.mostrar_pagina(texto, chave, erro="Digite um texto para cifrar.", status=400)
            return

        # Unifica formas equivalentes de escrever acentos em Unicode.
        texto_normalizado = unicodedata.normalize("NFC", texto)
        resultado = cifrar(texto_normalizado, numero, VALORES)
        self.mostrar_pagina(texto, chave, resultado)


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Servidor)
    print("Cifra de César: http://127.0.0.1:8000", flush=True)
    print("Para encerrar, pressione Ctrl+C.", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()
