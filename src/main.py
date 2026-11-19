from datetime import date, datetime

from classes import Biblioteca, Emprestimo, Livro, Usuario
from funcoes import (
    emprestimos_atrasados,
    estatisticas,
    filtrar_livros_por_categoria,
    gerar_relatorio_multas,
)


def criar_biblioteca_demo() -> Biblioteca:
    biblioteca = Biblioteca()
    biblioteca.cadastrar_livro(Livro(1, "Dom Casmurro", "Machado de Assis", "Romance"))
    biblioteca.cadastrar_livro(Livro(2, "Algoritmos", "Thomas Cormen", "Computação"))
    biblioteca.cadastrar_livro(Livro(3, "O Cortiço", "Aluísio Azevedo", "Romance"))
    biblioteca.cadastrar_usuario(Usuario(1, "Ana Silva", "2026001"))
    biblioteca.cadastrar_usuario(Usuario(2, "Bruno Costa", "2026002"))
    return biblioteca


def demonstrar() -> None:
    biblioteca = criar_biblioteca_demo()
    referencia = date(2026, 11, 18)

    biblioteca.registrar_emprestimo(Emprestimo(
        1,
        biblioteca.consultar_livro(1),
        biblioteca.consultar_usuario(1),
        date(2026, 11, 1),
        date(2026, 11, 10),
    ))
    biblioteca.registrar_emprestimo(Emprestimo(
        2,
        biblioteca.consultar_livro(2),
        biblioteca.consultar_usuario(2),
        date(2026, 11, 12),
        date(2026, 11, 20),
    ))

    print("Livros encontrados:")
    for livro in filtrar_livros_por_categoria(biblioteca.livros, "Romance"):
        print(f"- {livro.titulo}")

    print("Empréstimos atrasados:")
    for emprestimo in emprestimos_atrasados(biblioteca.emprestimos, referencia):
        print(f"- ID {emprestimo.id}: {emprestimo.usuario.nome}")

    print("Relatório de multas:")
    print(gerar_relatorio_multas(biblioteca.emprestimos, referencia))

    print("Estatísticas:")
    print(estatisticas(biblioteca.emprestimos, biblioteca.livros, referencia))

    biblioteca.registrar_devolucao(2, date(2026, 11, 18))
    print("Disponibilidade após devolução:")
    livro = biblioteca.consultar_livro(2)
    emprestimo = biblioteca.consultar_emprestimo(2)
    print(f"- {livro.titulo}: {'disponível' if emprestimo.data_devolucao else 'emprestado'}")


def ler_inteiro(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")


def ler_data(mensagem: str) -> date:
    while True:
        try:
            return datetime.strptime(input(mensagem), "%d/%m/%Y").date()
        except ValueError:
            print("Digite a data no formato DD/MM/AAAA.")


def cadastrar_livro(biblioteca: Biblioteca) -> None:
    livro = Livro(
        ler_inteiro("ID do livro: "),
        input("Título: ").strip(),
        input("Autor: ").strip(),
        input("Categoria: ").strip(),
    )
    biblioteca.cadastrar_livro(livro)
    print("Livro cadastrado.")


def cadastrar_usuario(biblioteca: Biblioteca) -> None:
    usuario = Usuario(
        ler_inteiro("ID do usuário: "),
        input("Nome: ").strip(),
        input("Matrícula: ").strip(),
    )
    biblioteca.cadastrar_usuario(usuario)
    print("Usuário cadastrado.")


def listar_livros(biblioteca: Biblioteca) -> None:
    if not biblioteca.livros:
        print("Nenhum livro cadastrado.")
        return
    for livro in biblioteca.livros:
        situacao = "disponível" if biblioteca.livro_disponivel(livro.id) else "emprestado"
        print(f"{livro.id} - {livro.titulo} | {livro.autor} | {livro.categoria} | {situacao}")


def realizar_emprestimo(biblioteca: Biblioteca) -> None:
    livro = biblioteca.consultar_livro(ler_inteiro("ID do livro: "))
    usuario = biblioteca.consultar_usuario(ler_inteiro("ID do usuário: "))
    emprestimo = Emprestimo(
        ler_inteiro("ID do empréstimo: "),
        livro,
        usuario,
        ler_data("Data do empréstimo (DD/MM/AAAA): "),
        ler_data("Data prevista de devolução (DD/MM/AAAA): "),
    )
    biblioteca.registrar_emprestimo(emprestimo)
    print("Empréstimo registrado.")


def realizar_devolucao(biblioteca: Biblioteca) -> None:
    emprestimo_id = ler_inteiro("ID do empréstimo: ")
    biblioteca.registrar_devolucao(emprestimo_id, ler_data("Data da devolução (DD/MM/AAAA): "))
    print("Devolução registrada.")


def exibir_relatorio(biblioteca: Biblioteca) -> None:
    referencia = ler_data("Data de referência (DD/MM/AAAA): ")
    relatorio = gerar_relatorio_multas(biblioteca.emprestimos, referencia)
    if not relatorio["itens"]:
        print("Nenhuma multa encontrada.")
    for item in relatorio["itens"]:
        print(
            f"Empréstimo {item['emprestimo_id']} | {item['usuario']} | "
            f"{item['livro']} | {item['dias_atraso']} dias | "
            f"R$ {item['multa']:.2f}"
        )
    print(f"Total: R$ {relatorio['total']:.2f}")


def executar_menu() -> None:
    biblioteca = Biblioteca()
    opcoes = {
        "1": ("Cadastrar livro", lambda: cadastrar_livro(biblioteca)),
        "2": ("Cadastrar usuário", lambda: cadastrar_usuario(biblioteca)),
        "3": ("Listar livros", lambda: listar_livros(biblioteca)),
        "4": ("Registrar empréstimo", lambda: realizar_emprestimo(biblioteca)),
        "5": ("Registrar devolução", lambda: realizar_devolucao(biblioteca)),
        "6": ("Exibir relatório de multas", lambda: exibir_relatorio(biblioteca)),
        "7": (
            "Exibir estatísticas",
            lambda: print(estatisticas(biblioteca.emprestimos, biblioteca.livros, date.today())),
        ),
    }
    while True:
        print("\n=== SISTEMA DE BIBLIOTECA ===")
        for codigo, (nome, _) in opcoes.items():
            print(f"{codigo} - {nome}")
        print("0 - Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            print("Programa encerrado.")
            return
        if escolha not in opcoes:
            print("Opção inválida.")
            continue
        try:
            opcoes[escolha][1]()
        except (LookupError, ValueError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")


if __name__ == "__main__":
    executar_menu()
