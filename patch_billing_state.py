import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

old_state = """      setWaSettings({
        evolutionApiUrl: userProfile.whatsappSettings.evolutionApiUrl || '',
        evolutionApiKey: userProfile.whatsappSettings.evolutionApiKey || '',
        evolutionInstanceName: userProfile.whatsappSettings.evolutionInstanceName || '',
        useMetaApi: userProfile.whatsappSettings.useMetaApi || false,
        metaToken: userProfile.whatsappSettings.metaToken || '',
        metaPhoneNumberId: userProfile.whatsappSettings.metaPhoneNumberId || ''
      });"""

new_state = """      setWaSettings({
        evolutionApiUrl: userProfile.whatsappSettings.evolutionApiUrl || '',
        evolutionApiKey: userProfile.whatsappSettings.evolutionApiKey || '',
        evolutionInstanceName: userProfile.whatsappSettings.evolutionInstanceName || '',
        useMetaApi: userProfile.whatsappSettings.useMetaApi || false,
        metaToken: userProfile.whatsappSettings.metaToken || '',
        metaPhoneNumberId: userProfile.whatsappSettings.metaPhoneNumberId || '',
        metaServerUrl: userProfile.whatsappSettings.metaServerUrl || ''
      });"""

content = content.replace(old_state, new_state)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
