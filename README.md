# custom-stack: Mock Object

Testes de unidade da `CustomStack` (Parte 1) e a classe `NumberAscOrder` (Parte 2), com pytest e pytest-mock.

## Installing Dependencies

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Test Execution

```sh
python -m pytest ./test/* --cov                                        # comando original
python -m pytest ./test/* --cov=src --cov-branch --cov-report=term-missing   # só o código, com branches
```

## Estrutura

```
src/
├── custom_stack_class.py   # CustomStack, StackEmptyException, StackFullException
└── number_asc_order.py     # Parte 2: NumberAscOrder
test/
├── custom_stack_test.py    # Parte 1
└── number_asc_order_test.py  # Parte 2
```

## Parte 1: testes da CustomStack

O teste que veio no projeto cobre 79% de `custom_stack_class.py`. Ele só exercita `push`, `top`, `size` e `is_empty` com um elemento. Nenhum caminho de erro e nenhum `pop` eram testados.

Os novos testes cobrem:

- pilha nova (vazia, com o limite informado);
- `push` mantendo a ordem e `top` devolvendo o último sem remover;
- `pop` na ordem LIFO, removendo o elemento, e liberando espaço para um novo `push`;
- `pop` e `top` em pilha vazia, e em pilha esvaziada por `pop`, com `StackEmptyException`;
- `push` até o limite (permitido) e além dele (`StackFullException`, sem alterar a pilha);
- pilha com limite zero.

**Bug encontrado.** Cobrir 100% não bastaria, porque o `push` nunca lançava `StackFullException`: a condição comparava `self.size` (o método) com o limite, e um método nunca é igual a um número. Os testes de pilha cheia falharam por isso (commit `test(parte 1) ... (red)`). A correção foi trocar `self.size` por `self.size()`, sem criar nenhum método novo (commit `fix(parte 1) ... (green)`).

## Parte 2: NumberAscOrder

`NumberAscOrder().sort(stack)` recebe uma `CustomStack` com os números sorteados da Mega Sena e devolve um `list` em ordem ascendente.

- Lê a pilha só pelos métodos públicos (`is_empty` e `pop`) e depois devolve os números à pilha na ordem original, inclusive se um `pop` falhar no meio. Assim a pilha do chamador não é alterada, e nenhum método foi adicionado a `CustomStack`.
- `TypeError` se o argumento não for uma `CustomStack`.
- `ValueError` se a pilha estiver vazia, se não tiver exatamente 6 números, se algum não for inteiro, se algum estiver fora de 1 a 60 ou se houver repetidos.

Cenários pedidos, testados com um mock de `CustomStack` (`mocker.Mock(spec=CustomStack)`) e também com a pilha real:

1. Pilha de 6 posições com os 6 números sorteados aleatoriamente: 10 sorteios diferentes, o resultado é a lista ordenada.
2. Pilha de 6 posições vazia: `ValueError`, sem nenhum `pop` no mock.

## Evidências de cobertura

```
Name                        Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------
src/__init__.py                 0      0      0      0   100%
src/custom_stack_class.py      24      0      6      0   100%
src/number_asc_order.py        31      0     20      0   100%
-----------------------------------------------------------
TOTAL                          55      0     26      0   100%
59 passed
```

Para conferir a efetividade dos testes, e não só a cobertura, foram feitas 8 alterações propositais no código (ordenação removida, limite 60 virando 59, pilha não restaurada, verificação de repetidos removida, condição de pilha cheia errada, `pop` e `top` pegando o primeiro elemento, `is_empty` errado). Os testes falharam em todas.
