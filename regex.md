# re Module


doc: https://docs.python.org/3/library/re.html

HOWTO: https://docs.python.org/3/howto/regex.html

## Intro

> Regular expressions (called REs, or regexes, or regex patterns) are essentially a tiny, highly specialized programming language embedded inside Python and made available through the re module.

>Here’s a complete list of the metacharacters;

```
. ^ $ * + ? { } [ ] \ | ( )
```

## Raw Strings

Strings cruas como diz a tradução literal são strings que não contêm caracteres especiais como `\n` ou `\t`. Isso facilita na análise de strings.

## Compile

A maneira mais eficiente de realizar múltiplas busca em um arquivo de texto atrás de um padrão, é mandar a biblioteca `re` compilar o nosso padrão e guardar em um objeto `re.compile(pattern)`

## Funções para encontrar matches

> Once you have an object representing a compiled regular expression, what do you do with it? Pattern objects have several methods and attributes. Only the most significant ones will be covered here; consult the re docs for a complete listing.

| Method/Attribute | Purpose|
|-|-|
| `match()`| Determine if the RE matches at the beginning of the string.|
| `search()`| Scan through a string, looking for any location where this RE matches.|
| `findall()`| Find all substrings where the RE matches, and returns them as a list.|
| `finditer()`| Find all substrings where the RE matches, and returns them as an iterator. |

## Usando finditer

Vamos agora procurar todos os *matches* entre o padrão passado e o texto usando `finditer()`. Para isso vamos realizar a seguinte operação

```python
text = ... # Uma string representando um texto
pattern = re.compile(r'...')
matches = pattern.finditer(text)
```

`matches` será um objeto definido por ser *iterável* (`callable_iterator object`). Podemos acessar cada match usando um `for match_found in matches` de modo que cada `match_found` é um outro objeto chamado `SRE_Match`. Este objeto por sua vez tem os atributos:

E alguns métodos

| Method/Attribute | Purpose|
|-|-|
| `group(0)`| Return the string matched by the RE|
| `start()`| Return the starting position of the match|
| `end()`| Return the ending position of the match|
| `span()`| Return a tuple containing the (start, end) positions of the match |

Portanto, se eu quiser obter a string `match` do texto original eu faria

```python
for match_found in matches:
    ini = match_found.start()
    end = match_found.end()
    print( text[ini:end] )
```

## Procurando por caracteres especiais

Muitos caracteres especiais são usados pelo regex para simbolizar algo. Por exemplo, o caracter `.` dá match com todo caracter (exceto com o carácter `\n` se a tag `DOTALL` estiver desativada).

Para encontrar especificamente o caracter `.` eu tenho que usar no padrão a contrabarra `re.compile(r'\.')`

Escapando metacaracteres:

> Perhaps the most important metacharacter is the backslash, `\`. As in Python string literals, the backslash can be followed by various characters to signal various special sequences. It’s also used to escape all the metacharacters so you can still match them in patterns; for example, if you need to match a `[` or `\`, you can precede them with a backslash to remove their special meaning: `\[` or `\\`.

## Caracteres especiais na biblioteca

> Some of the special sequences beginning with '`\`' represent predefined sets of characters that are often useful, such as the set of digits, the set of letters, or the set of anything that isn’t whitespace.

|Caracter|Significado|
| :-: |-|
|`.`| Qualquer caracter|
|`\d`| Dígito `[0-9]`|
|`\w`| Caracter de palavras `[a-zA-Z0-9_]`|
|`\s`| Espaço vazio `[ \t\n\r\f\v]`|

Esses mesmos caracteres com as letras em caixa alta selecionam o oposto. Por exemplo, `\D` seleciona tudo que não é um dígito.

## Âncoras

Não selecionam um caracter em específico, mas selecionam uma condição de contorno para o padrão (algo que tem que vir antes, ou algo que tem que vir depois).

|Caracter|Significado|
| :-: |--------------------|
|`\b`| Borda de *word*|
|`^`| Começo da String|
|`$`| Fim da string|

Usando $` no final do padrão vai retornar somente o caso colado com o final, por exemplo.

## Conjunto de Caracteres

> They’re used for specifying a character class, which is a set of characters that you wish to match. Characters can be listed individually, or a range of characters can be indicated by giving two characters and separating them by a '-'. For example, `[abc]` will match any of the characters `a`, `b`, or `c`; this is the same as `[a-c]`, which uses a range to express the same set of characters. If you wanted to match only lowercase letters, your RE would be `[a-z]`.

Para indicar conjunto de caracteres usamos os colchetes e dentro colocamos todos os caracteres que desejamos. Por exemplo, se queremos selecionar somente a letra `f` ou `z` escreveríamos `re.compile(r'[fz]')`. Mas atenção, essa seleção só seleciona *um único caracter*, vai devolver todas as aparições de `f` e `z` no texto.

Se colocarmos dentro do conjunto o caracter `^`, isso equivale a estar negando o conjunto. Por exemplo, `[^123]` representa todos os caracteres, exceto 1, 2 e 3.

> You can match the characters not listed within the class by complementing the set. This is indicated by including a '`^`' as the first character of the class. For example, `[^5]` will match any character except '`5`'. If the caret appears elsewhere in a character class, it does not have special meaning. For example: `[5^]` will match either a '`5`' or a '`^`'.

Como se comportam os *metacaracteres* dentro dos conjuntos?

> Metacharacters are not active inside classes. For example, `[akm$]` will match any of the characters '`a`', '`k`', '`m`', or '`$`'; '\$' is usually a metacharacter, but inside a character class it’s stripped of its special nature.

É possível passar também sequências de caracteres como `\s` e `\d` no interior de conjuntos.

## Alcance de Caracteres

O traço pode representar um alcance de caracteres. Vamos supor que queremos somente números entre 4 e 8, então colocaremos no conjunto o `[4-8]`. Outro exemplo é: vamos supor que queremos representar somente as letras que aparecem na representação hexadecimal (não importa se é maiúscula ou minúscula), então teríamos: `[a-fA-F]`

## Utilidade em Repetir Coisas

> Being able to match varying sets of characters is the first thing regular expressions can do that isn’t already possible with the methods available on strings. However, if that was the only additional capability of regexes, they wouldn’t be much of an advance. Another capability is that you can specify that portions of the RE must be repeated a certain number of times.
>
>The first metacharacter for repeating things that we’ll look at is `*`. `*` doesn’t match the literal character '`*`'; instead, it specifies that the previous character can be matched zero or more times, instead of exactly once.
>
> For example, `ca*t` will match '`ct`' (0 '`a`' characters), '`cat`' (1 '`a`'), '`caaat`' (3 '`a`' characters), and so forth.

Sobre o caráter guloso de *regex*

> Repetitions such as `*` are greedy; when repeating a RE, the matching engine will try to repeat it as many times as possible. If later portions of the pattern don’t match, the matching engine will then back up and try again with fewer repetitions.

## Quantificadores

* {m} - contador com exatamente *m*
* {m,n} - Contador *guloso* que vai encontrar de *m* até *n* repetições do que for marcado.

Omitir *m* diz que o limite inferior é 0. Omitir *n* diz que o limite superior é infinito. 

Esse contador é considerado *guloso*, pois ele vai considerar o maior número de repetições.

Abreviações de Contadores

* `*` - Seleciona 0 ou infinitos == `{'0,}`
* `+` - Seleciona 1 ou infinitos == `{1,}`
* `?` - Seleciona 0 ou 1 == `{,1}`

> Readers of a reductionist bent may notice that the three other qualifiers can all be expressed using this notation. `{0,}` is the same as `*`, `{1,}` is equivalent to `+`, and `{0,1}` is the same as `?`. It’s better to use `*`, `+`, or `?` when you can, simply because they’re shorter and easier to read.

Todo quantificador, quando sucedido por `?` se reduz ao menor caso. Isto é, a versão não *golusa* do quantificador, como `*?`, `+?`, `??`.

Quantificador `?` visto como declarando um caracter como opcional:

> The question mark character, `?`, matches either once or zero times; you can think of it as marking something as being optional. For example, `home-?brew` matches either '`homebrew`' or '`home-brew`'.

## Grupos

Grupos são representados por *parenteses* `()`, isto é, podemos colocar diversos padrões opcionais separados pela barra vertical `|` que indica o operador `ou`. O resultado seria algo como: `(desse_jeito|ou_desse|ate_esse)`

Podemos ainda usar grupos para coletar informações diretamente do que foi comparado. Por exemplo, uma expressao como `alguma(expressao)(interessante)`, podemos acessar o conteudo de cada grupo com auxilio do metodo `.group(i)` do objeto de `Match`. Onde `i = 0` indica toda a expressao, `i = 1` indica o primeiro grupo da esquerda para direita e `i = 2` o segundo.

## Opções para grupos

* Grupos não indexados

> Sometimes you’ll want to use a group to denote a part of a regular expression, but aren’t interested in retrieving the group’s contents. You can make this fact explicit by using a non-capturing group: `(?:...)`, where you can replace the ... with any other regular expression.

* Grupos com nome

> A more significant feature is named groups: instead of referring to them by numbers, groups can be referenced by a name.
>
> The syntax for a named group is one of the Python-specific extensions: (?P<name>...). name is, obviously, the name of the group. Named groups behave exactly like capturing groups, and additionally associate a name with a group. The match object methods that deal with capturing groups all accept either integers that refer to the group by number or strings that contain the desired group’s name. Named groups are still given numbers, so you can retrieve information about a group in two ways:

```python
>>> p = re.compile(r'(?P<word>\b\w+\b)')
>>> m = p.search( '(((( Lots of punctuation )))' )
>>> m.group('word')
'Lots'
>>> m.group(1)
'Lots'
```

* Grupo com nome para identificar palavras duplicadas

> The syntax for backreferences in an expression such as `(...)\1` refers to the number of the group. There’s naturally a variant that uses the group name instead of the number. This is another Python extension: `(?P=name)` indicates that the contents of the group called name should again be matched at the current point. The regular expression for finding doubled words, `\b(\w+)\s+\1\b` can also be written as `\b(?P<word>\w+)\s+(?P=word)\b`:

## Opções de *lookahead* e *lookbehind*

* Dá match se na próxima posição estiver o que for escrito depois do `=`

`(?=...)`

> Matches if ... matches next, but doesn’t consume any of the string. This is called a lookahead assertion. For example, `Isaac (?=Asimov)` will match '`Isaac `' only if it’s followed by '`Asimov`'.

* Dá match se na próxima posição não estiver o que for escrito depois da `!`

`(?!...)`

> Matches if ... doesn’t match next. This is a negative lookahead assertion. For example, `Isaac (?!Asimov)` will match '`Isaac `' only if it’s not followed by '`Asimov`'.

As mesmas colocações funcionam para se houver um padrão antes `(?<=...)` e `(?<!...)`

* Opções de lookbehind e lookahead precisam de padrões com tamanhos fixos.

## Flags
Alguns exemplos...

# Exemplos

### Quantificadores e Visualização da Engine Gulosa

A step-by-step example will make this more obvious. Let’s consider the expression `a[bcd]*b`. This matches the letter '`a`', zero or more letters from the class `[bcd]`, and finally ends with a '`b`'. Now imagine matching this RE against the string 'abcbd'.

| Step | Matched   | Explanation|
|-|-|-|
| 1| `a`| The `a` in the RE matches.|
| 2| `abcbd`| The engine matches `[bcd]*`, going as far as it can, which is to the end of the string.|
| 3| *Failure* | The engine tries to match `b`, but the current position is at the end of the string, so it fails. |
| 4| `abcb`| Back up, so that `[bcd]*` matches one less character.|
| 5    | *Failure* | Try `b` again, but the current position is at the last character, which is a `'d'`.|
| 6    | `abc`| Back up again, so that `[bcd]*` is only matching `bc`.|
| 7| `abcb`| Try `b` again. This time the character at the current position is `'b'`, so it succeeds.          |

The end of the RE has now been reached, and it has matched '`abcb`'. This demonstrates how the matching engine goes as far as it can at first, and if no match is found it will then progressively back up and retry the rest of the RE again and again. It will back up until it has tried zero matches for `[bcd]*`, and if that subsequently fails, the engine will conclude that the string doesn’t match the RE at all.

___

### Substituindo Negritos, Itálicos

```python
texto = "*Nun64* et sem* eget ***AR+C-U*** rutrum ornare** *tipo de **pardal** et* id **lorem**, ou ainda, *caraca **bixo***. **FIM**"

# Grupo 1: (\s|^) Espaço em branco OU começo de string
# \*{N} numero N de asteriscos
# Grupo 2: (.+?) qualquer caracter com 1 ou mais (de menor tamanho possivel)
# \*{N} numero N de asteriscos
negrito_it = re.compile(r'(\s|^)\*{3}(.+?)\*{3}')
negrito = re.compile(r'(\s|^)\*{2}(.+?)\*{2}')
italico = re.compile(r'(\s|^)\*{1}(.+?)\*{1}')


novo_texto = negrito_it.sub(r'\1<strongemph>\2</strongemph>', texto)
novo_texto = negrito.sub(r'\1<strong>\2</strong>', novo_texto)
novo_texto = italico.sub(r'\1<emph>\2</emph>', novo_texto)

print(novo_texto)
```

SAÍDA: 

```
<emph>Nun64</emph> et sem* eget <strongemph>AR+C-U</strongemph> rutrum ornare** <emph>tipo de <strong>pardal</strong> et</emph> id <strong>lorem</strong>, ou ainda, <emph>caraca <strong>bixo</strong></emph>. <strong>FIM</strong>
```

___

### IDS de vídeos no youtube

```python
# Context: Will YouTube Ever Run Out Of Video IDs? [https://youtu.be/gocwRvLhDf8]

texto = "https://www.youtube.com/watch?v=K8L6KVGG-7o\nhttps://www.youtube.com/watch?v=YYXdXT2l-Gg&list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU"

# Quero extrair o ID desses vídeos : K8L6KVGG-7o e YYXdXT2l-Gg
# Os IDS do youtube usam base 64 com ultimos digitos sendo "_" e "-"

# < v= > exatamente isso
# < [\w-]+ > 1 ou mais caracteres, no conjunto "word" (= [a-zA-Z0-9_]) e "-"
padrao_id = re.compile(r'v=([\w-]+)')

padroes_encontrados = padrao_id.finditer(texto)

for padrao_encontrado in padroes_encontrados:
    print(padrao_encontrado.group(1))
```

SAÍDA:

```
K8L6KVGG-7o
YYXdXT2l-Gg
```

___

### Encontrando emails válidos

```python
texto = '''bol@uol.com.br
abc.game@email.net
OtherMail123@strange-mail.org
institutional-account@university.edu.br
notaanemail@ola
notanemail2@ponto.com.
'''

# < [\w.-]+ > um conjunto de caracteres word \w (=[a-zA-Z0-9_]), ponto e traço ocorrendo 1 ou mais vezes 
# < @ > obrigatorio
# < [a-z\-]+ > conjunto de caracteres minusculos de a até z ou um traço, ocorrendo 1 ou mais vezes
# < \.(com|edu|net|org) > um ponto obrigatorio seguido de com OU edu OU net OU org
# (\s|\.[a-z]{2}) um espaco vazio OU um ponto seguido de 2 letras minusculas
padrao_email = re.compile(r'[\w.-]+@[a-z\-]+\.(com|edu|net|org)(\s|\.[a-z]{2})')

padroes_encontrados = padrao_email.finditer(texto)

for padrao_encontrado in padroes_encontrados:
    print(padrao_encontrado)
```

SAÍDA:

```
<re.Match object; span=(0, 14), match='bol@uol.com.br'>
<re.Match object; span=(15, 34), match='abc.game@email.net\n'>
<re.Match object; span=(34, 64), match='OtherMail123@strange-mail.org\n'>
<re.Match object; span=(64, 103), match='institutional-account@university.edu.br'>
```

___

### Prefixo de senhor e senhora

```python
texto = "Mr. Incrivel\nMr Incrivel\nMister Incrivel\nMs Simpson\nMiss Pig\nMrs. Sanders\nMrsa Vodka"

# Quero encontrar todos os nomes que comecam com Mr
# Para isso vou usar o quantificador "?" que indica um caracter opcional

# < M > exatamente isso
# < (r|s|rs) > pode ser: r OU s OU rs 
# < \.? > tem um ponto opcional
# < \s > tem um espaco
# <.*> quantos caracteres seguirem até o fim da linha
padrao = re.compile(r'M(r|s|rs)\.?\s.*')

padroes_encontrados = padrao.finditer(texto)

for padrao_encontrado in padroes_encontrados:
    print(padrao_encontrado)
```

SAÍDA:

```
<re.Match object; span=(0, 12), match='Mr. Incrivel'>
<re.Match object; span=(13, 24), match='Mr Incrivel'>
<re.Match object; span=(41, 51), match='Ms Simpson'>
<re.Match object; span=(61, 73), match='Mrs. Sanders'>
```

___

### Exemplo filtrando nomes por DDD

```python
texto = 'Lista telefonica:\nAna - (11)1234-5678\nBeatriz - (11)4312-1223\nCamila - (19)3367-1234\nDebora - (15)2336-9972\nEloisa - (11)9982-2230'

# Dividir a lista em linhas
linhas = texto.split('\n')

# < \(11\) > Inicia com 11 entre parenteses,
# < \d{4} > tem 4 digitos,
# < \- > depois tem um traco,
# < \d{4} > depois mais 4 digitos.
padrao_telefone = re.compile(r'\(11\)\d{4}\-\d{4}') 

# <^> Começo da string, 
# <\w> caracteres de palavra,
# <+> com  de 1 ou mais, 
# <\s> até o espaço.
padrao_nome = re.compile(r'^\w+\s') 

# Analisar cada linha
for linha in linhas:
    
    # Procura se tem (11) seguido de um telefone.
    match_regiao = re.search(padrao_telefone, linha)
    
    # Se M for None -> (not M) == True
    if not match_regiao:
        continue
    else:
        # Significa que encontrou telefone com DDD (11)
        # Agora vou coletar o nome
        match_nome = re.search(padrao_nome, linha)
        if match_nome:
            comeco = match_nome.start()
            fim = match_nome.end() - 1 # O fator -1 desconsidera o espaço vazio
            print(linha[comeco:fim])
```

SAÍDA:

```
Ana
Beatriz
Eloisa
```

___

### Exemplos de Número de Celular

```python
texto = '235-555-0042 outros numeros 1231231241241 e coisas como 235-555-abcd\nPosso ter 235-5550042 ou ainda 235-555-004 somente.\nMas eu gosto quando tenho algo como 123-456-7890, mas tambem nao tem pr0blem4 se usar ponto 420.420.0420. Só não gosto disso quando tiver estrela 333*111*4444'

p1 = re.compile(r'\d{3}[-.]\d{3}[-.]\d{4}')
M = p1.finditer(texto)

for m in M:
    print(m)
```

SAÍDA: 

```
<re.Match object; span=(0, 12), match='235-555-0042'>
<re.Match object; span=(157, 169), match='123-456-7890'>
<re.Match object; span=(213, 225), match='420.420.0420'>
```

___

### Exemplos de Âncoras

* Usando `^`

```python
texto = 'O rato roeu a roupa do Rei de ROMa'

p1 = re.compile(r'O')
p2 = re.compile(r'^O')

M1 = p1.finditer(texto)
M2 = p2.finditer(texto)

for m1 in M1:
    print(m1)

print('-'*40)
for m2 in M2:
    print(m2)
```

SAÍDA:

```
<re.Match object; span=(0, 1), match='O'>
<re.Match object; span=(31, 32), match='O'>
----------------------------------------
<re.Match object; span=(0, 1), match='O'>
```

* Usando `$`

```python
texto = 'O rato roeu a roupa do Rei de ROMa'

p1 = re.compile(r'a')
p2 = re.compile(r'a$')

M1 = p1.finditer(texto)
M2 = p2.finditer(texto)

for m1 in M1:
    print(m1)

print('-'*40)
for m2 in M2:
    print(m2)
```

SAÍDA

```
<re.Match object; span=(3, 4), match='a'>
<re.Match object; span=(12, 13), match='a'>
<re.Match object; span=(18, 19), match='a'>
<re.Match object; span=(33, 34), match='a'>
----------------------------------------
<re.Match object; span=(33, 34), match='a'>
```

* Usando `\b`

```python
texto = 'O rato roeu a roupa do Rei de ROMa'

p1 = re.compile(r'O')
p2 = re.compile(r'O\b')

M1 = p1.finditer(texto)
M2 = p2.finditer(texto)

for m1 in M1:
    print(m1)

print('-'*40)
for m2 in M2:
    print(m2)
```

SAÍDA

```
<re.Match object; span=(0, 1), match='O'>
<re.Match object; span=(31, 32), match='O'>
----------------------------------------
<re.Match object; span=(0, 1), match='O'>
```