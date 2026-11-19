from datetime import date
from functools import reduce
from typing import Iterable, Sequence, Tuple

from classes import Emprestimo, Livro


MULTA_DIARIA = 2.0


def calcular_multa(dias_atraso: int, valor_diaria: float = MULTA_DIARIA) -> float:
    return max(dias_atraso, 0) * valor_diaria


def filtrar_livros_por_categoria(livros: Iterable[Livro], categoria: str) -> Tuple[Livro, ...]:
    return tuple(filter(lambda livro: livro.categoria.lower() == categoria.lower(), livros))


def calcular_dias_atraso(emprestimo: Emprestimo, data_referencia: date) -> int:
    if emprestimo.data_devolucao is not None:
        return 0
    return (data_referencia - emprestimo.data_prevista_devolucao).days


def emprestimos_atrasados(emprestimos: Iterable[Emprestimo], data_referencia: date) -> Tuple[Emprestimo, ...]:
    return tuple(filter(
        lambda emprestimo: emprestimo.data_devolucao is None
        and data_referencia > emprestimo.data_prevista_devolucao,
        emprestimos
    ))


def gerar_relatorio_multas(
    emprestimos: Iterable[Emprestimo],
    data_referencia: date,
    valor_diaria: float = MULTA_DIARIA,
) -> dict:
    atrasados = filter(
        lambda emprestimo: emprestimo.data_devolucao is None
        and data_referencia > emprestimo.data_prevista_devolucao,
        emprestimos,
    )
    itens = tuple(map(
        lambda emprestimo: {
            "emprestimo_id": emprestimo.id,
            "usuario": emprestimo.usuario.nome,
            "livro": emprestimo.livro.titulo,
            "dias_atraso": (data_referencia - emprestimo.data_prevista_devolucao).days,
            "multa": calcular_multa(
                (data_referencia - emprestimo.data_prevista_devolucao).days,
                valor_diaria,
            ),
        },
        atrasados,
    ))
    total = reduce(lambda acumulado, item: acumulado + item["multa"], itens, 0.0)
    return {"data_referencia": data_referencia, "itens": itens, "total": round(total, 2)}


def contar_livros_por_categoria(livros: Iterable[Livro]) -> dict:
    categorias = tuple(set(livro.categoria for livro in livros))
    return {
        categoria: reduce(
            lambda acumulado, livro: acumulado + (livro.categoria == categoria),
            livros,
            0,
        )
        for categoria in categorias
    }


def contar_emprestimos_por_usuario(emprestimos: Iterable[Emprestimo]) -> dict:
    usuarios = tuple(set(emprestimo.usuario.matricula for emprestimo in emprestimos))
    return {
        matricula: sum(
            1 for emprestimo in emprestimos
            if emprestimo.usuario.matricula == matricula
        )
        for matricula in usuarios
    }


def estatisticas(emprestimos: Sequence[Emprestimo], livros: Sequence[Livro], data_referencia: date) -> dict:
    ativos = tuple(filter(lambda emprestimo: emprestimo.data_devolucao is None, emprestimos))
    atrasados = emprestimos_atrasados(emprestimos, data_referencia)
    return {
        "livros_por_categoria": contar_livros_por_categoria(livros),
        "emprestimos_por_usuario": contar_emprestimos_por_usuario(emprestimos),
        "emprestimos_ativos": reduce(lambda acumulado, _: acumulado + 1, ativos, 0),
        "emprestimos_ativos_atrasados": reduce(lambda acumulado, _: acumulado + 1, atrasados, 0),
        "valor_total_multas": gerar_relatorio_multas(emprestimos, data_referencia)["total"],
    }


def filtrar_livros_por_categoria_imperativo(livros: Sequence[Livro], categoria: str) -> tuple:
    resultado = []
    for livro in livros:
        if livro.categoria.lower() == categoria.lower():
            resultado.append(livro)
    return tuple(resultado)
