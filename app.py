from flask import Flask, render_template, request, redirect, url_for
import io
import sys

app = Flask(__name__)

# Definição dos níveis do jogo
levels = [
    {
        'number': 1,
        'concept': 'Função print',
        'instructions': (
            "O comando `print` é uma das funções mais básicas em Python e é usado "
            "para exibir mensagens na tela. Neste nível, seu objetivo é imprimir 'Olá, Mundo!' na tela."
        ),
        'solution': "print('Olá, Mundo!')",
    },
    {
        'number': 2,
        'concept': 'Variáveis e Operadores',
        'instructions': (
            "Variáveis são usadas para armazenar valores, e operadores como `*` são usados "
            "para manipular esses valores. Neste nível, você precisa declarar uma variável `x` com o valor 5 "
            "e, em seguida, multiplicar `x` por 2, exibindo o resultado."
        ),
        'solution': "x = 5\nprint(x * 2)",
    },
    {
       'number': 3,
    'concept': 'Loops',
    'instructions': (
        "Loops são usados para executar um bloco de código várias vezes. O comando <code>for</code> em Python "
        "permite iterar sobre uma sequência, como um intervalo de números. Neste nível, você deve criar "
        "um loop para imprimir números de 0 a 4.<br><br>"
        "Dica: O loop que você precisa deve ter uma estrutura como:<br><br>"
        "<pre><code>for i in range(numero):<br>    print(i)</code></pre>"
        ),
        'solution': "for i in range(5):\n    print(i)",
    },
    {
        'number': 4,
        'concept': 'Condicionais (if/else)',
        'instructions': (
            "As estruturas condicionais permitem que o código execute certas instruções apenas se uma condição "
            "for verdadeira. Neste nível, você deve criar uma variável x com o valor 15, verificar se o "
            "valor dessa variável é maior que 10 e imprimir 'Maior que 10' se a condição for verdadeira."
        ),
        'solution': "x = 15\nif x > 10:\n    print('Maior que 10')",
    },
    {
        'number': 5,
        'concept': 'Funções',
        'instructions': (
            "Funções são blocos de código que executam uma tarefa específica e podem ser reutilizadas. "
            "Neste nível, você deve definir uma função chamada `saudacao` que receba um argumento `nome` e "
            "retorne uma mensagem de saudação."
        ),
        'solution': "def saudacao(nome):\n    return 'Olá, ' + nome\nprint(saudacao('Python'))",
    },
    {
        'number': 6,
        'concept': 'Listas',
        'instructions': (
            "Listas são usadas para armazenar múltiplos itens em uma única variável. Neste nível, você deve criar "
            "uma lista chamada `frutas` contendo três frutas, e imprimir o segundo item da lista."
        ),
        'solution': "frutas = ['maçã', 'banana', 'laranja']\nprint(frutas[1])",
    },
    {
        'number': 7,
        'concept': 'Dicionários',
        'instructions': (
            "Dicionários são usados para armazenar dados em pares chave-valor. Neste nível, você deve criar um dicionário "
            "chamado `aluno` com as chaves 'nome' e 'idade', e imprimir a idade do aluno."
        ),
        'solution': "aluno = {'nome': 'Ana', 'idade': 20}\nprint(aluno['idade'])",
    }
]

def normalize_code(code):
    return "\n".join([line.strip() for line in code.strip().splitlines()])

@app.route('/')
def index():
    return redirect(url_for('game', level=1))

@app.route('/game/<int:level>', methods=['GET', 'POST'])
def game(level):
    if level > len(levels):
        return redirect(url_for('index'))  # Se o nível não existir, redireciona para o início

    current_level = levels[level - 1]
    code = ""  # Campo de código vazio ao carregar a página
    output = ""
    correct = False

    if request.method == 'POST':
        code = request.form.get('code', "")
        if not code.strip():
            output = "Nenhum código fornecido. Por favor, insira o código Python."
        else:
            try:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = io.StringIO()
                exec(code)
                output = redirected_output.getvalue()
                sys.stdout = old_stdout

                if not output.strip():
                    output = "Nenhuma saída gerada."

                # Verifica se o código corresponde à solução
                if normalize_code(code) == normalize_code(current_level['solution']):
                    correct = True
            except Exception as e:
                output = str(e)

    return render_template('game.html', 
                           level=current_level['number'], 
                           concept=current_level['concept'], 
                           instructions=current_level['instructions'], 
                           code=code, 
                           output=output, 
                           correct=correct,
                           total_levels=len(levels))

if __name__ == '__main__':
    app.run(debug=True)
