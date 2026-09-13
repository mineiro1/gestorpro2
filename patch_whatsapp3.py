import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_error = """  if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = errData.error?.message || JSON.stringify(errData);
    } catch(e) {}
    throw new Error(`Erro na API Oficial Meta (${response.status}): ${errDesc}`);
  }"""

new_error = """  if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = errData.message || errData.error?.message || JSON.stringify(errData);
    } catch(e) {}
    
    if (response.status === 409 || errDesc.includes('24h') || errDesc.includes('Janela')) {
        throw new Error("Janela de 24h fechada. A Meta (WhatsApp) bloqueou esta mensagem. Para iniciar a conversa, o cliente deve te enviar uma mensagem primeiro ou você deve usar Templates aprovados.");
    }
    
    throw new Error(`Erro na API Oficial Meta (${response.status}): ${errDesc}`);
  }"""

content = content.replace(old_error, new_error)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)

