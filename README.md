# Sistema de Gerenciamento de Biblioteca

Projeto prático da disciplina Linguagens de Programação, integrando orientação a objetos e programação funcional.

## Integrantes

- Nome completo do integrante 1
- Nome completo do integrante 2
- Nome completo do integrante 3
- Nome completo do integrante 4

## Linguagem

Python 3.10 ou superior.

Python foi escolhido pela leitura direta do código, pela sintaxe curta e pela disponibilidade de `filter`, `map`, `reduce`, dataclasses e testes padrão.

## Funcionalidades

- Cadastro e consulta de livros e usuários
- Registro de empréstimos e devoluções
- Controle de disponibilidade de cada exemplar
- Identificação de empréstimos ativos em atraso
- Cálculo de multa fixa de R$ 2,00 por dia
- Relatório de multas
- Estatísticas por categoria e por usuário
- Comparação entre implementação imperativa e funcional

## Estrutura

- `src/classes.py`: classes `Livro`, `Usuario`, `Emprestimo` e `Biblioteca`
- `src/funcoes.py`: funções puras, imutabilidade, `filter`, `map`, `reduce` e estatísticas
- `src/main.py`: dados demonstrativos e execução pelo terminal
- `tests/test_sistema.py`: testes automatizados
- `DIAGRAMAS.md`: roteiro dos dois diagramas individuais
- `QUESTOES.md`: cinco questões para estudar e responder à mão

## Execução

No diretório do projeto:

```bash
python src/main.py
```

O programa abre um menu com cadastro, consultas, empréstimos, devoluções e relatórios. Para sair, escolha `0`.

## Testes

```bash
python -m unittest discover -s tests -v
```

## Conceitos aplicados

As classes `Livro`, `Usuario` e `Emprestimo` são dataclasses imutáveis. O estado administrativo da biblioteca é isolado na classe `Biblioteca`. Consultas e transformações funcionais recebem coleções e retornam novos resultados sem alterar os dados recebidos.

`calcular_multa`, `filtrar_livros_por_categoria`, `emprestimos_atrasados` e `gerar_relatorio_multas` são funções puras. `registrar_emprestimo`, `registrar_devolucao` e `cadastrar_livro` são operações com efeito colateral controlado pela biblioteca.

O relatório obrigatório usa `filter` para selecionar atrasos, `map` para calcular valores individuais e `reduce` para somar o total. Pelo menos uma estatística também usa `reduce`.

A função `filtrar_livros_por_categoria_imperativo` é a versão imperativa comparável à versão funcional `filtrar_livros_por_categoria`.

## Observações

Os dados são mantidos em memória. Não há banco de dados ou persistência externa.

## Entrega individual

Os arquivos `DIAGRAMAS.md` e `QUESTOES.md` servem como guia. Os dois diagramas e as cinco respostas devem ser produzidos fisicamente em papel A4 branco e entregues ao professor em sala, conforme a atividade.
