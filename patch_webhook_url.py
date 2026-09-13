import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

old_code = "https://ais-pre-lafhr3cxydhbm5z265hztr-86812857430.us-east1.run.app/api/webhook/evolution"
new_code = "{window.location.origin}/api/webhook/evolution"

content = content.replace(old_code, new_code)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
