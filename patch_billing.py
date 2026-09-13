import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

old_code = """  const processQueue = async (clients: ClientBilling[], silent = false) => {
    if (waSettings.useMetaApi || waSettings.useEvolutionApi) {
      if (waSettings.useEvolutionApi && (!waSettings.evolutionApiUrl || !waSettings.evolutionApiKey || !waSettings.evolutionInstanceName)) {
        if(!silent) alert("Credenciais da Evolution API incompletas nas configurações.");
        return;
      }
      if (waSettings.useMetaApi && !waSettings.metaToken) {
        if(!silent) alert("Credenciais da API Oficial (Meta) incompletas nas configurações. O Token/Key é obrigatório.");
        return;
      }

      const apiName = waSettings.useMetaApi ? "API Oficial do WhatsApp (Meta)" : "Evolution API";"""

new_code = """  const processQueue = async (clients: ClientBilling[], silent = false) => {
    let currentSettings = waSettings;
    if (userProfile?.uid) {
      const adminId = userProfile.role === 'admin' ? userProfile.uid : userProfile.adminId;
      const { data } = await supabase.from('users').select('whatsapp_settings').eq('id', adminId).single();
      if (data && data.whatsapp_settings) {
        currentSettings = { ...waSettings, ...data.whatsapp_settings };
      }
    }

    if (currentSettings.useMetaApi || currentSettings.useEvolutionApi) {
      if (currentSettings.useEvolutionApi && (!currentSettings.evolutionApiUrl || !currentSettings.evolutionApiKey || !currentSettings.evolutionInstanceName)) {
        if(!silent) alert("Credenciais da Evolution API incompletas nas configurações.");
        return;
      }
      if (currentSettings.useMetaApi && !currentSettings.metaToken) {
        if(!silent) alert("Credenciais da API Oficial (Meta) incompletas nas configurações. O Token/Key é obrigatório.");
        return;
      }

      const apiName = currentSettings.useMetaApi ? "API Oficial do WhatsApp (Meta)" : "Evolution API";"""

content = content.replace(old_code, new_code)

content = content.replace("waSettings.useMetaApi", "currentSettings.useMetaApi")
content = content.replace("waSettings.useEvolutionApi", "currentSettings.useEvolutionApi")
content = content.replace("await sendEvolutionMessage(client, message, waSettings);", "await sendEvolutionMessage(client, message, currentSettings);")
content = content.replace("await sendEvolutionMessage(client.phone, message, waSettings);", "await sendEvolutionMessage(client.phone, message, currentSettings);")
content = content.replace("await sendMetaMessage(client.phone, message, waSettings);", "await sendMetaMessage(client.phone, message, currentSettings);")

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
