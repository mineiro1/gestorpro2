import re

with open('src/components/ChatModal.tsx', 'r') as f:
    content = f.read()

content = content.replace("userProfile.id", "userProfile.uid")
content = content.replace("userProfile?.id", "userProfile?.uid")

with open('src/components/ChatModal.tsx', 'w') as f:
    f.write(content)
