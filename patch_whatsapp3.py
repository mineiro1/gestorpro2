import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_code = "const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');"
new_code = "const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').trim().replace(/\\/$/, '');"

content = content.replace(old_code, new_code)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
