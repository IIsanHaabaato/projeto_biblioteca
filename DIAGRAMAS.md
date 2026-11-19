# Diagramas do projeto

Os diagramas abaixo devem ser desenhados à mão em folha A4 branca para a entrega individual. Eles descrevem o sistema implementado, sem banco de dados.

## 1. Diagrama de casos de uso

Desenhe um retângulo com o título `Sistema de Biblioteca`. Fora do retângulo, coloque o ator `Bibliotecário`. Dentro do retângulo, coloque os casos de uso:

- Cadastrar livro
- Cadastrar usuário
- Consultar livro
- Consultar usuário
- Verificar disponibilidade
- Registrar empréstimo
- Registrar devolução
- Calcular multa
- Consultar empréstimos atrasados
- Gerar relatório de multas
- Consultar estatísticas

Ligue `Bibliotecário` a todos os casos de uso. Faça também estas relações:

- `Registrar empréstimo` inclui `Consultar livro`.
- `Registrar empréstimo` inclui `Consultar usuário`.
- `Registrar empréstimo` inclui `Verificar disponibilidade`.
- `Registrar devolução` inclui `Calcular multa`.
- `Gerar relatório de multas` inclui `Consultar empréstimos atrasados`.

Uma resposta possível para explicar o diagrama é: o bibliotecário é o usuário externo que inicia as operações, enquanto as relações `include` representam etapas necessárias para concluir uma operação maior.

## 2. Diagrama de classes

Desenhe quatro classes:

### Livro

- `id: int`
- `titulo: str`
- `autor: str`
- `categoria: str`

### Usuario

- `id: int`
- `nome: str`
- `matricula: str`

### Emprestimo

- `id: int`
- `livro: Livro`
- `usuario: Usuario`
- `data_emprestimo: date`
- `data_prevista_devolucao: date`
- `data_devolucao: Optional[date]`

### Biblioteca

- `livros: Tuple[Livro, ...]`
- `usuarios: Tuple[Usuario, ...]`
- `emprestimos: Tuple[Emprestimo, ...]`
- `cadastrar_livro(livro)`
- `cadastrar_usuario(usuario)`
- `consultar_livro(livro_id)`
- `consultar_usuario(usuario_id)`
- `consultar_emprestimo(emprestimo_id)`
- `livro_disponivel(livro_id)`
- `registrar_emprestimo(emprestimo)`
- `registrar_devolucao(emprestimo_id, data_devolucao)`

Relacione `Emprestimo` a `Livro` e `Usuario` com multiplicidade `1` para cada um. Relacione `Biblioteca` a `Livro`, `Usuario` e `Emprestimo` com uma agregação de uma biblioteca para vários objetos de cada tipo.

Ao apresentar, destaque que as três dataclasses usam imutabilidade com `frozen=True`. Na devolução, o empréstimo não é alterado diretamente: um novo objeto é criado com `replace`.
