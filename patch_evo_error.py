import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_error = """    if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = JSON.stringify(errData);
    } catch(e) {}
    throw new Error(`Erro na Evolution API (${response.status}): ${errDesc}`);
  }"""

new_error = """    if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = errData?.response?.message || errData?.message || JSON.stringify(errData);
    } catch(e) {}
    
    if (response.status === 500 && errDesc.includes('Connection Closed')) {
      throw new Error(`O seu WhatsApp está desconectado da Evolution API (Connection Closed). Por favor, acesse o painel da sua API, leia o QR Code novamente para conectar o seu celular e tente novamente.`);
    }
    
    throw new Error(`Erro na Evolution API (${response.status}): ${errDesc}`);
  }"""

content = content.replace(old_error, new_error)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
