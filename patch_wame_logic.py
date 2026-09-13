import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

# Change isWame logic
old_code = "const isWame = baseUrl.includes('api-wa.me') || baseUrl.includes('wame.api.br');"
new_code = "const isWame = baseUrl && !baseUrl.includes('graph.facebook.com');"
content = content.replace(old_code, new_code)

# Make error message less confusing so they don't complain about "API Oficial" if they use WAME
old_err = "throw new Error(`Erro na API Oficial Meta (${response.status}): ${response.statusText} at URL: ${url} | Token: ${waSettings.metaToken}`);"
new_err = "throw new Error(`Erro na API (404): Verifique a URL do Servidor WAME/Meta. URL Acessada: ${url}`);"
content = content.replace(old_err, new_err)

old_err2 = "throw new Error(`Erro na API Oficial Meta (${response.status}): ${errDesc}`);"
new_err2 = "throw new Error(`Erro na API WAME/Meta (${response.status}): ${errDesc}`);"
content = content.replace(old_err2, new_err2)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
