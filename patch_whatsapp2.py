import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_error = """    if (!response.ok) {
      let errDesc = 'Desconhecido';
      try {
        const errData = await response.json();
        errDesc = errData.error?.message || JSON.stringify(errData);
      } catch(e) {}
      throw new Error(`Erro na API Oficial Meta (${response.status}): ${errDesc}`);
    }"""

new_error = """    if (!response.ok) {
      let errDesc = 'Desconhecido';
      try {
        const errData = await response.json();
        errDesc = errData.message || errData.error?.message || JSON.stringify(errData);
      } catch(e) {}
      
      if (response.status === 409 || errDesc.includes('24h')) {
          throw new Error("Janela de 24 horas fechada. O WhatsApp (Meta) bloqueou o envio de texto livre para este cliente. O cliente precisa te mandar uma mensagem primeiro.");
      }
      
      throw new Error(`Erro API Meta (${response.status}): ${errDesc}`);
    }"""

content = content.replace(old_error, new_error)
with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_error2 = """      if (!response.ok) {
         let errDesc = 'Desconhecido';
         try {
           const errData = await response.json();
           errDesc = errData.error?.message || JSON.stringify(errData);
         } catch(e) {}
         throw new Error(`Erro API Meta (${response.status}): ${errDesc}`);
      }"""

new_error2 = """      if (!response.ok) {
         let errDesc = 'Desconhecido';
         try {
           const errData = await response.json();
           errDesc = errData.message || errData.error?.message || JSON.stringify(errData);
         } catch(e) {}
         
         if (response.status === 409 || errDesc.includes('24h')) {
             throw new Error("Janela de 24 horas fechada pelo WhatsApp. O cliente precisa responder você primeiro.");
         }
         
         throw new Error(`Erro API Meta (${response.status}): ${errDesc}`);
      }"""

content = content.replace(old_error2, new_error2)
with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)

