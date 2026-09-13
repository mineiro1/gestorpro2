import re

with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

old_body = """      body: JSON.stringify({
        number: number,
        text: text
      })"""

new_body = """      body: JSON.stringify({
        number: number,
        text: text,
        textMessage: { text: text },
        options: { delay: 1200, presence: "composing" }
      })"""

content = content.replace(old_body, new_body)

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(content)
