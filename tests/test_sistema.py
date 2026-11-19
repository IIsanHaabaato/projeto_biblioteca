import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from classes import Biblioteca, Emprestimo, Livro, Usuario
from funcoes import (
    calcular_multa,
    emprestimos_atrasados,
    estatisticas,
    filtrar_livros_por_categoria,
    filtrar_livros_por_categoria_imperativo,
    gerar_relatorio_multas,
)


class SistemaBibliotecaTests(unittest.TestCase):
    def criar_cenario(self):
        biblioteca = Biblioteca()
        livros = (
            Livro(1, "Dom Casmurro", "Machado", "Romance"),
            Livro(2, "Python", "Autor", "Computação"),
            Livro(3, "Memórias", "Autor", "Romance"),
        )
        usuarios = (
            Usuario(1, "Ana", "001"),
            Usuario(2, "Bruno", "002"),
        )
        for livro in livros:
            biblioteca.cadastrar_livro(livro)
        for usuario in usuarios:
            biblioteca.cadastrar_usuario(usuario)
        return biblioteca, livros, usuarios

    def test_calculo_multa_puro(self):
        self.assertEqual(calcular_multa(5, 2), 10)
        self.assertEqual(calcular_multa(-2, 2), 0)

    def test_filtro_funcional_e_imperativo_sao_equivalentes(self):
        _, livros, _ = self.criar_cenario()
        funcional = filtrar_livros_por_categoria(livros, "Romance")
        imperativo = filtrar_livros_por_categoria_imperativo(livros, "Romance")
        self.assertEqual(funcional, imperativo)

    def test_livro_nao_pode_ser_emprestado_duas_vezes(self):
        biblioteca, livros, usuarios = self.criar_cenario()
        biblioteca.registrar_emprestimo(Emprestimo(
            1, livros[0], usuarios[0], date(2026, 11, 1), date(2026, 11, 10)
        ))
        with self.assertRaises(ValueError):
            biblioteca.registrar_emprestimo(Emprestimo(
                2, livros[0], usuarios[1], date(2026, 11, 2), date(2026, 11, 11)
            ))

    def test_devolucao_torna_livro_disponivel(self):
        biblioteca, livros, usuarios = self.criar_cenario()
        biblioteca.registrar_emprestimo(Emprestimo(
            1, livros[0], usuarios[0], date(2026, 11, 1), date(2026, 11, 10)
        ))
        biblioteca.registrar_devolucao(1, date(2026, 11, 12))
        biblioteca.registrar_emprestimo(Emprestimo(
            2, livros[0], usuarios[1], date(2026, 11, 13), date(2026, 11, 20)
        ))
        self.assertEqual(biblioteca.consultar_emprestimo(1).data_devolucao, date(2026, 11, 12))

    def test_livro_disponivel_muda_com_emprestimo_e_devolucao(self):
        biblioteca, livros, usuarios = self.criar_cenario()
        self.assertTrue(biblioteca.livro_disponivel(1))
        biblioteca.registrar_emprestimo(Emprestimo(
            1, livros[0], usuarios[0], date(2026, 11, 1), date(2026, 11, 10)
        ))
        self.assertFalse(biblioteca.livro_disponivel(1))
        biblioteca.registrar_devolucao(1, date(2026, 11, 10))
        self.assertTrue(biblioteca.livro_disponivel(1))

    def test_atrasados_filtram_apenas_ativos(self):
        _, livros, usuarios = self.criar_cenario()
        emprestimos = (
            Emprestimo(1, livros[0], usuarios[0], date(2026, 10, 1), date(2026, 10, 10)),
            Emprestimo(2, livros[1], usuarios[1], date(2026, 11, 1), date(2026, 11, 10), date(2026, 11, 12)),
        )
        atrasados = emprestimos_atrasados(emprestimos, date(2026, 11, 18))
        self.assertEqual(tuple(item.id for item in atrasados), (1,))

    def test_relatorio_multas_sem_alterar_dados(self):
        _, livros, usuarios = self.criar_cenario()
        emprestimos = (
            Emprestimo(1, livros[0], usuarios[0], date(2026, 11, 1), date(2026, 11, 10)),
            Emprestimo(2, livros[1], usuarios[1], date(2026, 11, 1), date(2026, 11, 20)),
        )
        original = tuple(emprestimos)
        relatorio = gerar_relatorio_multas(emprestimos, date(2026, 11, 18))
        self.assertEqual(relatorio["total"], 16)
        self.assertEqual(tuple(item.id for item in emprestimos), tuple(item.id for item in original))

    def test_estatisticas(self):
        _, livros, usuarios = self.criar_cenario()
        emprestimos = (
            Emprestimo(1, livros[0], usuarios[0], date(2026, 11, 1), date(2026, 11, 10)),
            Emprestimo(2, livros[1], usuarios[1], date(2026, 11, 1), date(2026, 11, 20)),
        )
        resultado = estatisticas(emprestimos, livros, date(2026, 11, 18))
        self.assertEqual(resultado["emprestimos_ativos"], 2)
        self.assertEqual(resultado["emprestimos_ativos_atrasados"], 1)
        self.assertEqual(resultado["valor_total_multas"], 16)


if __name__ == "__main__":
    unittest.main()
