import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_code = "const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').trim().replace(/\\/$/, '');"
new_code = """let baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').trim().replace(/\\/$/, '');
  if (baseUrl && !baseUrl.startsWith('http')) {
    baseUrl = 'https://' + baseUrl;
  }"""

content = content.replace(old_code, new_code)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
