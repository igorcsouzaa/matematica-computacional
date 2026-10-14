# Cifra de César

Projeto didático com frontend em **HTML, CSS e JavaScript** e backend em **Python**, sem bibliotecas externas.

A aba **Visualizar** mostra uma palavra base e anima cada letra ao mudar o deslocamento pelo número, pelos botões ou pelo controle deslizante. A aba **Cifrar texto** mantém o formulário de texto completo. Ambas usam a mesma lista do `config.json`. A animação respeita a preferência do sistema por movimento reduzido.

## Como executar

Com o Python 3 instalado, abra o PowerShell e execute:

```powershell
cd C:\faculdade\cifra-cesar
python app.py
```

Acesse **http://127.0.0.1:8000** no navegador. Escreva um texto, informe uma chave inteira e clique em **Cifrar texto**. Para encerrar o servidor, pressione `Ctrl+C` no terminal.

## Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `app.py` | Recebe o formulário, chama a cifra e devolve a página com o resultado. |
| `cifra.py` | Carrega e valida a configuração e implementa o algoritmo. |
| `config.json` | Define o número de cada caractere permitido na cifra. |
| `templates/index.html` | Estrutura da página e formulário. |
| `static/style.css` | Aparência e adaptação da página à largura da tela. |
| `static/visual.js` | Abas e animação do deslocamento das letras. |
| `test_cifra.py` | Testes do algoritmo e da configuração. |

## O caminho de um texto

1. O navegador envia o texto e a chave para o Python por um formulário `POST`.
2. O backend valida se existe texto e se a chave é inteira.
3. O Python normaliza o texto para Unicode NFC, unificando formas equivalentes de representar acentos.
4. Para cada caractere configurado, calcula uma nova posição na lista.
5. O backend devolve o HTML com o resultado. O texto é escapado antes de entrar na página, para ser exibido como texto.

## Algoritmo, passo a passo

A configuração utiliza valores de **1 até N**, sem repetir ou pular números. Nesta versão há **78 caracteres**: 26 letras minúsculas, 26 maiúsculas e 26 letras acentuadas ou com cedilha. Por exemplo, `a = 1`, `b = 2` e `A = 27`, como no enunciado.

Para cada caractere presente na configuração:

```text
novo_valor = ((valor_atual - 1 + chave) % N) + 1
```

- `valor_atual - 1`: passa a posição para o intervalo de 0 até N − 1.
- `+ chave`: desloca a posição.
- `% N`: calcula o resto da divisão inteira; isso faz a lista funcionar como um círculo.
- `+ 1`: volta à numeração de 1 até N.

Com a chave **3**, `a` tem valor 1:

```text
((1 - 1 + 3) % 78) + 1 = 4
```

O valor 4 representa `d`. Assim, **abc → def**.

No final da lista, o cálculo volta ao começo: `Ç` vale 78; com chave 1, seu novo valor é `((78 - 1 + 1) % 78) + 1 = 1`, portanto **Ç → a**.

Minúsculas, maiúsculas e acentos fazem parte de **uma única lista**. Por isso, com chave 1, `z → A` e `Z → á`. Não há um alfabeto separado para cada tipo de letra.

Espaços, quebras de linha, números, pontuação, emojis e qualquer caractere ausente da configuração são preservados. Essa escolha permite cifrar textos em português mantendo sua formatação. As letras acentuadas listadas na configuração são cifradas normalmente.

## Quantidade de caracteres e possibilidades de chave

A **cardinalidade** é a quantidade de elementos de um conjunto. Aqui, é o número **N** de caracteres configurados.

Embora possamos informar qualquer chave inteira, existem apenas **N deslocamentos distintos**, representados pelas chaves de **0 até N − 1**. Chaves que diferem por um múltiplo de N são equivalentes, pois deixam o mesmo resto na divisão por N.

| Caracteres configurados (N) | Deslocamentos distintos | Deslocamentos que não são a identidade |
| --- | --- | --- |
| 26 | 26 (0 a 25) | 25 |
| 52 | 52 (0 a 51) | 51 |
| 78, neste projeto | 78 (0 a 77) | 77 |

A chave **0**, ou qualquer múltiplo de N, mantém todos os caracteres iguais. Nesta configuração, **3, 81 e −75** produzem o mesmo deslocamento. O Python permite chaves negativas: `−3` move três posições para trás e desfaz o deslocamento de `3`.

Portanto, aumentar N aumenta **linearmente** a quantidade de chaves efetivamente distintas. Mesmo assim, a cifra de César é fraca: alguém pode testar todos os N deslocamentos. Ela serve aqui para aprender o algoritmo, não para proteger informações reais. Se o texto só tiver caracteres fora da configuração, nenhuma chave mudará seu conteúdo.

## Como alterar os caracteres

Edite `config.json` mantendo um único caractere por entrada e valores inteiros consecutivos de 1 até N. Para adicionar um caractere, use o próximo número disponível. Reinicie o servidor após alterar a configuração. O algoritmo calcula N automaticamente.

## Testes

Na pasta do projeto, execute:

```powershell
python -m unittest -v
```
