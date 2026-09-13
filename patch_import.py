import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

content = content.replace("Settings, X, Play", "Settings, X, Play, MessageSquare")

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
