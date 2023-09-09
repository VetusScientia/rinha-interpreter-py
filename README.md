# Rinha Interpreter

Olá! 👋 Welcome ao Rinha Interpreter, um projeto desenvolvido com o objetivo de interpretar a linguagem Rinha. Este interpretador foi feito para uma Rinha de Compiladores (ou interpretadores, rs), mais informações [aqui](https://github.com/aripiprazole/rinha-de-compiler/).

## Introdução

O Rinha Interpreter trabalha com árvores sintáticas abstratas (AST), que são armazenadas no formato JSON. Sua principal função é interpretar programas com base nas informações contidas nessa AST.

## Como Executar

Para executar o Rinha Interpreter, siga os passos abaixo:

### Requisitos

1. Python 3.x instalado.

### Executando um Programa Rinha

### Com Docker

1. Abra o terminal ou prompt de comando;
2. Use os seguintes comandos:

```bash
docker build -t rinha_interprete .
docker run rinha_interprete
```

### Sem Docker

1. Abra o terminal ou prompt de comando;
2. Navegue até o diretório onde o arquivo **main.py** (com os demais arquivos do interpretador) está localizado;
3. Use o seguinte comando:

```bash
python main.py -s nome_do_arquivo.rinha.json
```

Substitua **nome_do_arquivo.rinha.json** pelo nome do arquivo Rinha que você deseja executar.

## Como Testar

Você pode testar o interpretador utilizando o arquivo `var/rinha/fib.rinha` e gerando o JSON correspondente com a ferramenta fornecida nesse [repositório](https://github.com/aripiprazole/rinha-de-compiler). E em seguida rodar o JSON disponível em `var/rinha/fib.rinha.json`. Existem outros códigos que você pode testar no diretório `var/rinha/`.

## Funcionamento da Linguagem Rinha

A linguagem Rinha é uma linguagem de programação dinâmica que possui um conjunto de funcionalidades e uma sintaxe simples. Abaixo, vamos explorar algumas das principais funcionalidades da linguagem:

### Tipos de Dados

A linguagem Rinha possui três tipos de dados principais:

1. **Inteiros (Int)**: Representam números inteiros de 32 bits.
   Exemplo: `42`

2. **Texto (Str)**: Representam sequências de caracteres.
   Exemplo: `"Olá, Mundo"`

3. **Booleanos (Bool)**: Representam valores verdadeiro ou falso.
   Exemplo: `true`, `false`

### Operadores

A linguagem suporta uma variedade de operadores para realizar operações em diferentes tipos de dados. Alguns dos operadores mais comuns incluem:

- **Aritméticos**: `+` (adição), `-` (subtração), `*` (multiplicação), `/` (divisão), `%` (resto).

- **Comparação**: `==` (igual a), `!=` (diferente de), `<` (menor que), `>` (maior que), `<=` (menor ou igual a), `>=` (maior ou igual a).

- **Lógicos**: `&&` (E lógico), `||` (OU lógico).

### Estruturas de Controle

A linguagem oferece estruturas de controle de fluxo para ajudar a controlar o comportamento do programa. Sendo ela:

- **If-Else**: Permite executar diferentes blocos de código com base em uma condição.

```javascript
if (condicao) {
    // Bloco de código se a condição for verdadeira
} else {
    // Bloco de código se a condição for falsa
}
```

### Funções

A linguagem Rinha permite a definição e chamada de funções. Uma função pode receber parâmetros e retornar um valor. Aqui está um exemplo de como definir e chamar uma função:

```javascript
let soma = fn(a, b) => {
    a + b
};

let resultado = soma(10, 20);
print(resultado)
```

### Variáveis

Variáveis são usadas para armazenar valores e podem ser declaradas com a palavra-chave `let`. Elas podem ser reatribuídas com um novo valor.

```javascript
let nome = "João";
nome = "Maria"; // Agora 'nome' possui o valor "Maria"
```

### Print

A função `print` é usada para exibir mensagens no terminal.

```javascript
print("Olá, Mundo!")
```

### Tuplas

Tuplas são estruturas de dados que podem conter dois elementos. Elas são imutáveis, o que significa que seus elementos não podem ser alterados depois de criados.

```javascript
let ponto = (10, 20);
let x = first(ponto); // x terá o valor 10
let y = second(ponto); // y terá o valor 20
```

### Comentários

Comentários são utilizados para adicionar explicações ou anotações no código e não são executados. Eles começam com `//`.

```javascript
// Isto é um comentário
```

### Recursão

A linguagem Rinha suporta recursão, o que significa que uma função pode chamar a si mesma. Loucura :O

```javascript
let fatorial = fn(n) => {
    if (n <= 1) {
      1
    } else {
        n * fatorial(n - 1)
    }
};
```

## Exemplo de Código

Aqui está um exemplo de código Rinha que calcula o Fibonacci:

```javascript
let fib = fn (n) => {
  if (n < 2) {
    n
  } else {
    fib(n - 1) + fib(n - 2)
  }
};

print("fib: " + fib(10))
```

# Outros

O repositório está aberto a contribuições, então se você encontrar algum bug ou erro, por favor, abra uma nova issues e me avise, ou envie um novo pull requests, caso saiba como resolver. :)

# Licença

MIT License

Copyright (c) 2023 Emanuel Júnior

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.