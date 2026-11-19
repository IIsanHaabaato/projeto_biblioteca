# Questões para estudar e responder à mão

Estas respostas são um roteiro de estudo. Cada integrante deve reescrever as respostas à mão e compreender o código antes da apresentação.

## 1. Onde a orientação a objetos aparece no projeto?

A orientação a objetos aparece nas classes `Livro`, `Usuario`, `Emprestimo` e `Biblioteca`. Cada classe reúne dados relacionados ao seu conceito. A classe `Biblioteca` também possui métodos para cadastrar elementos, registrar empréstimos e registrar devoluções. Assim, os dados e as operações do domínio ficam organizados em objetos.

## 2. O que é uma função pura e qual exemplo existe no projeto?

Uma função pura sempre produz o mesmo resultado para as mesmas entradas e não altera dados externos. `calcular_multa` é um exemplo: recebe a quantidade de dias de atraso e o valor da diária e devolve o resultado. Ela não depende do estado da biblioteca nem modifica listas ou objetos.

## 3. Como o projeto usa imutabilidade?

`Livro`, `Usuario` e `Emprestimo` são dataclasses com `frozen=True`, portanto seus campos não podem ser alterados diretamente depois da criação. As coleções internas da biblioteca são tuplas. Para registrar uma devolução, o sistema usa `dataclasses.replace` e cria uma nova versão do empréstimo.

## 4. Onde aparecem `filter`, `map` e `reduce`?

`filter` seleciona os empréstimos atrasados e os livros de uma categoria. `map` transforma cada empréstimo atrasado em um dicionário com usuário, livro, dias de atraso e multa. `reduce` soma as multas do relatório e também calcula algumas estatísticas. Essas operações aparecem principalmente em `funcoes.py`.

## 5. Como a multa é calculada e como a disponibilidade é controlada?

A multa é de R$ 2,00 por dia. O sistema calcula a diferença entre a data de referência e a data prevista para devolução. Se a diferença for positiva, ela é multiplicada por 2. Um livro fica indisponível quando existe um empréstimo ativo para ele, ou seja, um empréstimo cujo campo `data_devolucao` ainda é `None`. Depois da devolução, ele volta a ficar disponível.
