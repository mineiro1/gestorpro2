import re

with open('src/pages/Messages.tsx', 'r') as f:
    content = f.read()

# Replace sendEvolutionMessage signature
old_sig = "const sendEvolutionMessage = async (client: any, text: string, mediaBase64?: string, mimeType?: string) => {\n    const waSettings = userProfile?.whatsappSettings;"
new_sig = "const sendEvolutionMessage = async (client: any, text: string, waSettings: any, mediaBase64?: string, mimeType?: string) => {"
content = content.replace(old_sig, new_sig)

# Replace the call in the loop
old_call = "await sendEvolutionMessage(client, personalizedText, base64Media, mimeType);"
new_call = "await sendEvolutionMessage(client, personalizedText, waSettings, base64Media, mimeType);"
content = content.replace(old_call, new_call)

# Fix baseUrl in sendEvolutionMessage local to also have https auto-injection
old_base = "const baseUrl = waSettings.evolutionApiUrl.replace(/\\/$/, '');"
new_base = """let baseUrl = waSettings.evolutionApiUrl.trim().replace(/\\/$/, '');
    if (baseUrl && !baseUrl.startsWith('http')) {
      baseUrl = 'https://' + baseUrl;
    }"""
content = content.replace(old_base, new_base)

with open('src/pages/Messages.tsx', 'w') as f:
    f.write(content)
