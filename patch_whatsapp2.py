import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_code = "throw new Error(`Erro na API Oficial Meta (${response.status}): ${response.statusText} at URL: ${url}`);"
new_code = "throw new Error(`Erro na API Oficial Meta (${response.status}): ${response.statusText} at URL: ${url} | Token: ${waSettings.metaToken}`);"

content = content.replace(old_code, new_code)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
