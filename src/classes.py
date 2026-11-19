from dataclasses import dataclass, replace
from datetime import date
from typing import Optional, Tuple


@dataclass(frozen=True)
class Livro:
    id: int
    titulo: str
    autor: str
    categoria: str


@dataclass(frozen=True)
class Usuario:
    id: int
    nome: str
    matricula: str


@dataclass(frozen=True)
class Emprestimo:
    id: int
    livro: Livro
    usuario: Usuario
    data_emprestimo: date
    data_prevista_devolucao: date
    data_devolucao: Optional[date] = None


class Biblioteca:
    def __init__(self) -> None:
        self._livros: Tuple[Livro, ...] = ()
        self._usuarios: Tuple[Usuario, ...] = ()
        self._emprestimos: Tuple[Emprestimo, ...] = ()

    @property
    def livros(self) -> Tuple[Livro, ...]:
        return self._livros

    @property
    def usuarios(self) -> Tuple[Usuario, ...]:
        return self._usuarios

    @property
    def emprestimos(self) -> Tuple[Emprestimo, ...]:
        return self._emprestimos

    def cadastrar_livro(self, livro: Livro) -> None:
        if any(item.id == livro.id for item in self._livros):
            raise ValueError("Já existe um livro com esse identificador")
        self._livros = self._livros + (livro,)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        if any(item.id == usuario.id or item.matricula == usuario.matricula for item in self._usuarios):
            raise ValueError("Já existe um usuário com esse identificador ou matrícula")
        self._usuarios = self._usuarios + (usuario,)

    def consultar_livro(self, livro_id: int) -> Livro:
        for livro in self._livros:
            if livro.id == livro_id:
                return livro
        raise LookupError("Livro não encontrado")

    def consultar_usuario(self, usuario_id: int) -> Usuario:
        for usuario in self._usuarios:
            if usuario.id == usuario_id:
                return usuario
        raise LookupError("Usuário não encontrado")

    def consultar_emprestimo(self, emprestimo_id: int) -> Emprestimo:
        for emprestimo in self._emprestimos:
            if emprestimo.id == emprestimo_id:
                return emprestimo
        raise LookupError("Empréstimo não encontrado")

    def livro_disponivel(self, livro_id: int) -> bool:
        self.consultar_livro(livro_id)
        return not any(
            emprestimo.livro.id == livro_id and emprestimo.data_devolucao is None
            for emprestimo in self._emprestimos
        )

    def registrar_emprestimo(self, emprestimo: Emprestimo) -> None:
        if emprestimo.data_prevista_devolucao < emprestimo.data_emprestimo:
            raise ValueError("A data prevista não pode ser anterior ao empréstimo")
        if any(item.id == emprestimo.id for item in self._emprestimos):
            raise ValueError("Já existe um empréstimo com esse identificador")
        if any(item.livro.id == emprestimo.livro.id and item.data_devolucao is None
               for item in self._emprestimos):
            raise ValueError("O livro já está emprestado")
        if emprestimo.livro not in self._livros:
            raise ValueError("O livro não está cadastrado")
        if emprestimo.usuario not in self._usuarios:
            raise ValueError("O usuário não está cadastrado")
        self._emprestimos = self._emprestimos + (emprestimo,)

    def registrar_devolucao(self, emprestimo_id: int, data_devolucao: date) -> None:
        emprestimo = self.consultar_emprestimo(emprestimo_id)
        if emprestimo.data_devolucao is not None:
            raise ValueError("O empréstimo já foi devolvido")
        if data_devolucao < emprestimo.data_emprestimo:
            raise ValueError("A data de devolução não pode ser anterior ao empréstimo")
        atualizado = replace(emprestimo, data_devolucao=data_devolucao)
        self._emprestimos = tuple(
            atualizado if item.id == emprestimo_id else item
            for item in self._emprestimos
        )
