with open('src/pages/ClientForm.tsx', 'r') as f:
    content = f.read()

# Add import if missing
if "normalizePhoneNumber" not in content:
    content = content.replace(
        "import { openMap } from '../lib/maps';",
        "import { openMap } from '../lib/maps';\nimport { normalizePhoneNumber } from '../lib/whatsapp';"
    )

content = content.replace("phone: formData.phone,", "phone: normalizePhoneNumber(formData.phone),")
content = content.replace("local_phone: formData.localPhone,", "local_phone: normalizePhoneNumber(formData.localPhone),")

with open('src/pages/ClientForm.tsx', 'w') as f:
    f.write(content)
