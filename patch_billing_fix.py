import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

# 1. Fix handleSendWhatsApp
old_handle = """  const handleSendWhatsApp = async (client: ClientBilling) => {
    if (!client.phone) {"""

new_handle = """  const handleSendWhatsApp = async (client: ClientBilling) => {
    let currentSettings = waSettings;
    if (userProfile?.uid) {
      const adminId = userProfile.role === 'admin' ? userProfile.uid : userProfile.adminId;
      const { data } = await supabase.from('users').select('whatsapp_settings').eq('id', adminId).single();
      if (data && data.whatsapp_settings) {
        currentSettings = { ...waSettings, ...data.whatsapp_settings };
      }
    }

    if (!client.phone) {"""

content = content.replace(old_handle, new_handle)

# 2. Fix useEffect for auto schedule
old_effect = """  useEffect(() => {
    if (!currentSettings.useEvolutionApi && !currentSettings.useMetaApi) return;"""

new_effect = """  useEffect(() => {
    if (!waSettings.useEvolutionApi && !waSettings.useMetaApi) return;"""
content = content.replace(old_effect, new_effect)

# 3. Replace all remaining currentSettings with waSettings EXCEPT in handleSendWhatsApp and processQueue
# Let's be smart. The JSX part is below line 800. We can just replace currentSettings with waSettings in the bottom half.
idx = content.find('return (')
if idx != -1:
    top = content[:idx]
    bottom = content[idx:]
    bottom = bottom.replace('currentSettings.', 'waSettings.')
    content = top + bottom

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
