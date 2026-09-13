import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

old_code = """    const waSettings = userProfile?.whatsappSettings;
    const isEvolution = waSettings?.useEvolutionApi;"""

new_code = """    let waSettings = userProfile?.whatsappSettings;
    if (userProfile?.uid) {
      const adminId = userProfile.role === 'admin' ? userProfile.uid : userProfile.adminId;
      const { data } = await supabase.from('users').select('whatsapp_settings').eq('id', adminId).single();
      if (data && data.whatsapp_settings) {
        waSettings = data.whatsapp_settings;
      }
    }
    
    const isEvolution = waSettings?.useEvolutionApi;"""

content = content.replace(old_code, new_code)

old_call = """await sendMetaMessage(client.phone, personalizedText, userProfile?.whatsappSettings || {});"""
new_call = """await sendMetaMessage(client.phone, personalizedText, waSettings || {});"""
content = content.replace(old_call, new_call)

with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)
