import json
from pathlib import Path
import tempfile
import unittest

from cifra import carregar_alfabeto, cifrar


class TestCifra(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valores = carregar_alfabeto(Path(__file__).with_name("config.json"))

    def test_exemplo_basico(self):
        self.assertEqual(cifrar("abc", 3, self.valores), "def")

    def test_volta_ao_inicio(self):
        self.assertEqual(cifrar("Ç", 1, self.valores), "a")

    def test_lista_unica_com_maiusculas_e_acentos(self):
        self.assertEqual(cifrar("zZáç", 1, self.valores), "AáàÁ")

    def test_preserva_caracteres_nao_configurados(self):
        self.assertEqual(cifrar(" 123!\n🙂", 5, self.valores), " 123!\n🙂")

    def test_chaves_equivalentes(self):
        texto = "Olá, ação!"
        for chave in (81, -75):
            self.assertEqual(cifrar(texto, chave, self.valores), cifrar(texto, 3, self.valores))

    def test_ciclo_completo_e_identidade(self):
        texto = "".join(self.valores)
        for chave in (0, 78, -78):
            self.assertEqual(cifrar(texto, chave, self.valores), texto)

    def test_chave_negativa_desfaz_cifra(self):
        texto = "Olá, mundo! Ação, café e coração."
        self.assertEqual(cifrar(cifrar(texto, 9, self.valores), -9, self.valores), texto)

    def test_cardinalidade_configuravel(self):
        valores = {"a": 1, "b": 2, "c": 3}
        self.assertEqual(cifrar("abc", 1, valores), "bca")

    def test_rejeita_configuracoes_invalidas(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "config.json"
            for valores in ({}, {"ab": 1}, {"a": 2}, {"a": 1, "b": 1}, {"a": True}, []):
                with self.subTest(valores=valores):
                    caminho.write_text(json.dumps(valores), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        carregar_alfabeto(caminho)


if __name__ == "__main__":
    unittest.main()
