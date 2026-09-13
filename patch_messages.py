import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_code = """      if (waSettings?.useMetaApi) {
        if (!waSettings || !waSettings.metaToken || !waSettings.metaPhoneNumberId) {
          throw new Error("Credenciais da API Oficial (Meta) incompletas nas configurações.");
        }
        
        const cleanPhone = clientPhone.replace(/\\D/g, '');
        const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
        
        const url = `https://graph.facebook.com/v19.0/${waSettings.metaPhoneNumberId}/messages`;"""

new_code = """      if (waSettings?.useMetaApi) {
        if (!waSettings || !waSettings.metaToken) {
          throw new Error("Credenciais da API Oficial (Meta) incompletas nas configurações.");
        }
        
        const cleanPhone = clientPhone.replace(/\\D/g, '');
        const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
        
        const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
        const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
        const url = `${baseUrl}${phoneId}/messages`;"""

content = content.replace(old_code, new_code)

old_code2 = """    } else if (waSettings?.useMetaApi) {
       if (!waSettings.metaToken || !waSettings.metaPhoneNumberId) {
         setSendingStatus('error');
         return;
       }"""
       
new_code2 = """    } else if (waSettings?.useMetaApi) {
       if (!waSettings.metaToken) {
         setSendingStatus('error');
         return;
       }"""

content = content.replace(old_code2, new_code2)

with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)
