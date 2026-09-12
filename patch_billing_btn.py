import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

# Add billedClients state
state_code = """  const [billedClients, setBilledClients] = useState<Record<string, string>>(() => {
    try {
      const stored = localStorage.getItem('gestaopro_billed_clients');
      return stored ? JSON.parse(stored) : {};
    } catch {
      return {};
    }
  });"""

content = content.replace("const [sentClients, setSentClients] = useState<Record<string, 'success'|'error'>>({});",
                          "const [sentClients, setSentClients] = useState<Record<string, 'success'|'error'>>({});\n" + state_code)

# Add save logic in handleSendWhatsApp
handle_start = """  const handleSendWhatsApp = async (client: ClientBilling) => {
    if (!client.phone) {
      alert(`O cliente ${client.name} não possui telefone cadastrado.`);
      return;
    }"""

handle_replacement = handle_start + """

    const todayStr = new Date().toLocaleDateString('pt-BR');
    const newBilled = { ...billedClients, [client.id]: todayStr };
    setBilledClients(newBilled);
    localStorage.setItem('gestaopro_billed_clients', JSON.stringify(newBilled));"""

content = content.replace(handle_start, handle_replacement)

# Replace the button
btn_regex = re.compile(
    r"<button\s*onClick=\{\(\) => handleSendWhatsApp\(client\)\}\s*className=\{`flex items-center px-4 py-2 rounded-lg transition-colors font-semibold shadow-sm border \$\{\s*client\.status === 'delayed'\s*\?\s*'bg-red-50 text-red-700 border-red-200 hover:bg-red-100'\s*:\s*'bg-\[#25D366\] text-white border-transparent hover:bg-\[#20b858\]'\s*\}\`\}\s*>\s*<MessageCircle size=\{18\} className=\"mr-2\" />\s*\{client\.status === 'delayed' \? 'Cobrar' : 'Lembrete'\}\s*</button>"
)

new_btn = """                        {(() => {
                          const today = new Date().toLocaleDateString('pt-BR');
                          const alreadyBilled = billedClients[client.id] === today;
                          
                          return (
                            <button
                              onClick={() => handleSendWhatsApp(client)}
                              disabled={alreadyBilled}
                              className={`flex items-center px-4 py-2 rounded-lg transition-colors font-semibold shadow-sm border ${
                                alreadyBilled 
                                  ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                                  : client.status === 'delayed' 
                                    ? 'bg-red-50 text-red-700 border-red-200 hover:bg-red-100 cursor-pointer' 
                                    : 'bg-[#25D366] text-white border-transparent hover:bg-[#20b858] cursor-pointer'
                              }`}
                            >
                              <MessageCircle size={18} className="mr-2" />
                              {alreadyBilled ? 'Enviado Hoje' : (client.status === 'delayed' ? 'Cobrar' : 'Lembrete')}
                            </button>
                          );
                        })()}"""

content = btn_regex.sub(new_btn, content)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
