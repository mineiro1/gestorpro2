import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_send = """  const sendMetaMessage = async (client: any, text: string) => {
    const waSettings = userProfile?.whatsappSettings;
    if (!waSettings || !waSettings.metaToken || !waSettings.metaPhoneNumberId) {
      throw new Error("Credenciais da API Oficial (Meta) incompletas nas configurações.");
    }
    
    const cleanPhone = client.phone.replace(/\\D/g, '');
    const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
    
    const url = `https://graph.facebook.com/v19.0/${waSettings.metaPhoneNumberId}/messages`;"""

new_send = """  const sendMetaMessage = async (client: any, text: string) => {
    const waSettings = userProfile?.whatsappSettings;
    if (!waSettings || !waSettings.metaToken) {
      throw new Error("O Token/Key da API Oficial (Meta) é obrigatório.");
    }
    
    const cleanPhone = client.phone.replace(/\\D/g, '');
    const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
    
    const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
    const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
    const url = `${baseUrl}${phoneId}/messages`;"""

content = content.replace(old_send, new_send)

old_check = """       if (!waSettings.metaToken || !waSettings.metaPhoneNumberId) {
          alert("Credenciais da API Oficial (Meta) incompletas nas configurações.");
          setSending(false);
          return;
       }"""
       
new_check = """       if (!waSettings.metaToken) {
          alert("O Token/Key da API Oficial (Meta) é obrigatório.");
          setSending(false);
          return;
       }"""

content = content.replace(old_check, new_check)

with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)
