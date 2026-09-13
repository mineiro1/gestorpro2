import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_code = """export const sendMetaMessage = async (phone: string, text: string, waSettings: any) => {
  if (!waSettings.metaToken || !waSettings.metaPhoneNumberId) {
    throw new Error("Credenciais da API Oficial (Meta) incompletas nas configurações.");
  }
  
  const cleanPhone = phone.replace(/\\D/g, '');
  const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
  
  const url = `https://graph.facebook.com/v19.0/${waSettings.metaPhoneNumberId}/messages`;"""

new_code = """export const sendMetaMessage = async (phone: string, text: string, waSettings: any) => {
  if (!waSettings.metaToken) {
    throw new Error("O Token/Key da API Oficial (Meta) é obrigatório.");
  }
  
  const cleanPhone = phone.replace(/\\D/g, '');
  const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
  
  const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
  const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
  const url = `${baseUrl}${phoneId}/messages`;"""

content = content.replace(old_code, new_code)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
