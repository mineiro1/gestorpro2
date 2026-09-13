import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_err = """    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(`Erro na Evolution API: ${JSON.stringify(errData)}`);
    }"""

new_err = """    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      const errMsg = errData?.response?.message || errData?.message || JSON.stringify(errData);
      if (response.status === 500 && errMsg.includes('Connection Closed')) {
        throw new Error(`O seu WhatsApp está desconectado da Evolution API (Connection Closed). Conecte o QR Code no seu painel da API e tente novamente.`);
      }
      throw new Error(`Erro na Evolution API: ${errMsg}`);
    }"""

content = content.replace(old_err, new_err)

with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)
