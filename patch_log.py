import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_code = "export const sendMetaMessage = async (phone: string, text: string, waSettings: any) => {"
new_code = """export const sendMetaMessage = async (phone: string, text: string, waSettings: any) => {
  console.log("SEND META MESSAGE CALLED");
  console.log("Phone:", phone);
  console.log("Base URL raw:", waSettings.metaServerUrl);
  console.log("Token:", waSettings.metaToken);"""

content = content.replace(old_code, new_code)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
