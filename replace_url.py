with open('server.ts', 'r') as f:
    content = f.read()

content = content.replace('https://gestaopro.com', 'https://www.rspiscinas.app.br')

with open('server.ts', 'w') as f:
    f.write(content)
