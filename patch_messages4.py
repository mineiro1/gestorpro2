import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_error = """    if (!response.ok) {
      let errDesc = 'Desconhecido';
      try {
        const errData = await response.json();
        errDesc = errData.error?.message || JSON.stringify(errData);
      } catch(e) {}
      throw new Error(`Erro API Meta (${response.status}): ${errDesc}`);
    }"""

new_error = """    if (!response.ok) {
      let errDesc = 'Desconhecido';
      try {
        const errData = await response.json();
        errDesc = errData.message || errData.error?.message || JSON.stringify(errData);
      } catch(e) {}
      
      if (response.status === 409 || errDesc.includes('24h') || errDesc.includes('Janela')) {
         throw new Error("Janela de 24h fechada. A Meta (WhatsApp) bloqueou o envio. O cliente deve enviar uma mensagem para você antes que você possa responder com texto livre.");
      }
      
      throw new Error(`Erro API Meta (${response.status}): ${errDesc}`);
    }"""

content = content.replace(old_error, new_error)
with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)

