import re

with open('server.ts', 'r') as f:
    content = f.read()

old_body = """          body: JSON.stringify({
            number: `55${cleanPhone}`,
            options: { delay: 1200, presence: 'composing' },
            textMessage: { text: text }
          })"""

new_body = """          body: JSON.stringify({
            number: `55${cleanPhone}`,
            text: text,
            options: { delay: 1200, presence: 'composing' },
            textMessage: { text: text }
          })"""

content = content.replace(old_body, new_body)

with open('server.ts', 'w') as f:
    f.write(content)
