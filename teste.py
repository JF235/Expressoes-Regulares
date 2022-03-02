import re

texto = 'Lista telefonica:\nAna - (11)1234-5678\nBeatriz - (11)4312-1223\nCamila - (19)3367-1234\nDebora - (15)2336-9972\nEloisa - (11)9982-2230'



# Dividir a lista em linhas
linhas = texto.split('\n')
#print(linhas)
padrao_telefone = re.compile(r'\(11\)\d{4}\-\d{4}')
padrao_nome = re.compile(r'^\w+\s') # <^> Começo da string, <\w> caracteres de palavra,<+> com  de 1 ou mais, <\s> até o espaço

for linha in linhas:
    
    # Procura se tem (11) seguido de um telefone
    match_regiao = re.search(padrao_telefone, linha)
    
    # Se M for None -> (not M) == True
    if not match_regiao:
        continue
    else:
        match_nome = re.search(padrao_nome, linha)
        if match_nome:
            comeco = match_nome.span()[0]
            fim = match_nome.span()[1]
            print(linha[comeco:fim])