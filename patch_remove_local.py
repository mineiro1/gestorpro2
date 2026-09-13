import re

def process_billing():
    with open('src/pages/Billing.tsx', 'r') as f:
        content = f.read()

    # 1. Add import for sendMetaMessage and sendEvolutionMessage if not exists
    if 'sendEvolutionMessage' not in content:
        content = content.replace("import { Package, Send, Settings, MessageSquare } from 'lucide-react';", "import { Package, Send, Settings, MessageSquare } from 'lucide-react';\nimport { sendMetaMessage, sendEvolutionMessage } from '../lib/whatsapp';")

    # 2. Remove local sendMetaMessage
    # It starts with "const sendMetaMessage = async (client: ClientBilling, text: string) => {"
    # And ends with "return await response.json();\n  };"
    pattern = r"const sendMetaMessage = async \(client: ClientBilling, text: string\) => \{.*?return await response\.json\(\);\n  \};\n"
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 3. Remove local sendEvolutionMessage
    pattern2 = r"const sendEvolutionMessage = async \(client: ClientBilling, text: string\) => \{.*?return await response\.json\(\);\n  \};\n"
    content = re.sub(pattern2, '', content, flags=re.DOTALL)

    # 4. Update calls: sendMetaMessage(client, message) -> sendMetaMessage(client.phone, message, waSettings)
    content = content.replace("sendMetaMessage(client, message)", "sendMetaMessage(client.phone, message, waSettings)")
    content = content.replace("sendEvolutionMessage(client, message)", "sendEvolutionMessage(client.phone, message, waSettings)")

    with open('src/pages/Billing.tsx', 'w') as f:
        f.write(content)

def process_messages():
    with open('src/pages/Messages.tsx', 'r') as f:
        content = f.read()
        
    if 'sendEvolutionMessage' not in content:
        content = content.replace("import { Search, Send, Clock, AlertTriangle, CheckCircle, Image as ImageIcon, Video, X } from 'lucide-react';", "import { Search, Send, Clock, AlertTriangle, CheckCircle, Image as ImageIcon, Video, X } from 'lucide-react';\nimport { sendMetaMessage, sendEvolutionMessage } from '../lib/whatsapp';")
        
    pattern = r"const sendMetaMessage = async \(client: any, text: string\) => \{.*?return await response\.json\(\);\n  \};\n"
    content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    pattern2 = r"const sendEvolutionMessage = async \(client: any, text: string\) => \{.*?return await response\.json\(\);\n  \};\n"
    content = re.sub(pattern2, '', content, flags=re.DOTALL)

    # Calls in Messages.tsx
    # sendMetaMessage(client, personalizedText)
    content = content.replace("sendMetaMessage(client, personalizedText)", "sendMetaMessage(client.phone, personalizedText, userProfile?.whatsappSettings || {})")
    content = content.replace("sendEvolutionMessage(client, personalizedText)", "sendEvolutionMessage(client.phone, personalizedText, userProfile?.whatsappSettings || {})")

    with open('src/pages/Messages.tsx', 'w') as f:
        f.write(content)

process_billing()
process_messages()
