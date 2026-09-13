import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

# Replace sendMetaMessage
old_send = """  const sendMetaMessage = async (client: ClientBilling, text: string) => {
    if (!waSettings.metaToken || !waSettings.metaPhoneNumberId) {
      throw new Error("Credenciais da API Oficial (Meta) incompletas nas configurações.");
    }
    
    const cleanPhone = client.phone.replace(/\\D/g, '');
    const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
    
    const url = `https://graph.facebook.com/v19.0/${waSettings.metaPhoneNumberId}/messages`;"""

new_send = """  const sendMetaMessage = async (client: ClientBilling, text: string) => {
    if (!waSettings.metaToken) {
      throw new Error("O Token/Key da API Oficial (Meta) é obrigatório.");
    }
    
    const cleanPhone = client.phone.replace(/\\D/g, '');
    const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
    
    const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
    const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
    const url = `${baseUrl}${phoneId}/messages`;"""

content = content.replace(old_send, new_send)

# Replace validation in processQueue
old_val = """      if (waSettings.useMetaApi && (!waSettings.metaToken || !waSettings.metaPhoneNumberId)) {
        if(!silent) alert("Credenciais da API Oficial (Meta) incompletas nas configurações.");
        return;
      }"""

new_val = """      if (waSettings.useMetaApi && !waSettings.metaToken) {
        if(!silent) alert("Credenciais da API Oficial (Meta) incompletas nas configurações. O Token/Key é obrigatório.");
        return;
      }"""

content = content.replace(old_val, new_val)

# Replace UI
old_ui = """                    <h5 className="text-sm font-bold text-blue-900">Credenciais Meta Cloud API</h5>
                    <p className="text-xs text-blue-700 mb-2 font-medium">Aviso: Textos livres só chegam se o cliente acionou você nas últimas 24h. Use templates aprovados para o 1º contato (não incluso na demo de texto livre).</p>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Access Token (Temporário ou Permanente)</label>"""

new_ui = """                    <h5 className="text-sm font-bold text-blue-900">Credenciais Meta Cloud API</h5>
                    <p className="text-xs text-blue-700 mb-2 font-medium">Aviso: Textos livres só chegam se o cliente acionou você nas últimas 24h. Use templates aprovados para o 1º contato (não incluso na demo de texto livre).</p>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Server URL (Opcional - deixe vazio para oficial)</label>
                      <input
                        type="text"
                        placeholder="https://graph.facebook.com/v19.0 ou https://us.api-wa.me"
                        value={waSettings.metaServerUrl || ''}
                        onChange={e => setWaSettings({...waSettings, metaServerUrl: e.target.value})}
                        className="w-full px-3 py-2 border border-blue-200 rounded-md focus:ring-blue-500 focus:border-blue-500 outline-none text-sm bg-white mb-3"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 mb-1">Access Token (ou Key)</label>"""

content = content.replace(old_ui, new_ui)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
