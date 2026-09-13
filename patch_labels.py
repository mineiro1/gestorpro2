import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

old_label = '<span className="block font-semibold text-sm text-gray-800 text-blue-900">API Oficial Meta (Cloud API)</span>'
new_label = '<span className="block font-semibold text-sm text-blue-900">API WAME / Meta Cloud API</span>'
content = content.replace(old_label, new_label)

old_desc = '<span className="block text-xs text-gray-600">Conexão oficial via painel Developers Facebook. Ultra seguro, sem risco de banimento.</span>'
new_desc = '<span className="block text-xs text-gray-600">Conexão via Facebook Developers ou WAME API (Oficial e Não-Oficial via QR Code).</span>'
content = content.replace(old_desc, new_desc)

old_title = '<h5 className="text-sm font-bold text-blue-900">Credenciais Meta Cloud API</h5>'
new_title = '<h5 className="text-sm font-bold text-blue-900">Credenciais WAME / Meta API</h5>'
content = content.replace(old_title, new_title)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
