with open('server.ts', 'r') as f:
    content = f.read()

# Replace body.object === "whatsapp_business_account" with checking for both
old_check = 'if (body.object === "whatsapp_business_account" && body.entry && body.entry[0].changes) {'
new_check = 'if ((body.object === "whatsapp_business_account" || body.object === "wame") && body.entry && body.entry[0].changes) {'

content = content.replace(old_check, new_check)

with open('server.ts', 'w') as f:
    f.write(content)
