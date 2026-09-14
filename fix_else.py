with open('server.ts', 'r') as f:
    content = f.read()
content = content.replace('else console.log("Webhook message inserted successfully!");', '')
with open('server.ts', 'w') as f:
    f.write(content)
