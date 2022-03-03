import re

with open('src/input_ex.md', mode = 'r', encoding = 'utf-8') as md_file:
    md_text = md_file.read()
    
    code = re.compile(r'`{3}(?P<lang>[^\n]*?)\n(?P<code>.+?)`{3}', flags = re.DOTALL)
    
    Ms = code.finditer(md_text)
    
    for m in Ms:
        a = m.group('lang')
        '''
        if m.group('lang') != '':
            print('Linguagem: ' , )
        else:
            print('Linguagem: ' , 'SEM LINGUAGEM')
        print('Trecho de código: ', m.group('code'))
        print()
        '''