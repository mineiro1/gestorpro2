import re

with open('src/pages/SuppliesForm.tsx', 'r') as f:
    content = f.read()

# Add states
content = content.replace(
    "const [waSettings, setWaSettings] = useState<any>(null);",
    """const [waSettings, setWaSettings] = useState<any>(null);
  const [showPartnerModal, setShowPartnerModal] = useState(false);
  const [selectedPartners, setSelectedPartners] = useState<string[]>([]);
  const [lastSentData, setLastSentData] = useState<{ products: SupplyItem[] } | null>(null);"""
)

# New handlers
new_handlers = """
  const handleSendToPartners = async () => {
    if (selectedPartners.length === 0) {
      alert('Selecione pelo menos uma loja parceira.');
      return;
    }
    
    if (!lastSentData || !client) return;
    
    const settings = waSettings || userProfile?.whatsappSettings || {};
    const companyName = settings.companyName || 'nossa empresa';
    const partnerStores = settings.partnerStores || [];
    
    const storesToSend = partnerStores.filter((p: any) => selectedPartners.includes(p.phone));
    
    const message = `Olá, aqui é a empresa ${companyName}, enviei para você uma lista de produtos que solicitei ao meu cliente, caso deseje enviar um orçamento para ele(a) estou deixando a lista e o contato dele logo abaixo.\\n\\n` +
      lastSentData.products.map(s => `• ${s.name}: ${s.quantity} ${s.unit}`).join('\\n') +
      `\\n\\nCliente: ${client.name.split(' ')[0]}\\nContato: ${client.phone}`;
      
    // Send to each selected partner
    for (const store of storesToSend) {
      if (!settings.useMetaApi && !settings.useEvolutionApi) {
        openWhatsApp(store.phone, message);
      } else {
        try {
          if (settings.useMetaApi) {
            await sendMetaMessage(store.phone, message, settings);
          } else if (settings.useEvolutionApi) {
            await sendEvolutionMessage(store.phone, message, settings);
          }
        } catch (err) {
          console.error('Erro ao enviar para loja parceira:', err);
        }
      }
    }
    
    setShowPartnerModal(false);
    setSelectedPartners([]);
    setLastSentData(null);
    navigate('/clients');
    
    if (settings.useMetaApi || settings.useEvolutionApi) {
      alert('Lista enviada para as lojas parceiras com sucesso!');
    }
  };

  const closePartnerModal = () => {
    setShowPartnerModal(false);
    setSelectedPartners([]);
    setLastSentData(null);
    navigate('/clients');
  };

  const handleSend = async () => {
    if (!client) {
      alert('Cliente não encontrado.');
      return;
    }
    const selected = supplies.filter(s => s.quantity && Number(s.quantity) > 0);
    if (selected.length === 0) {
      alert('Preencha a quantidade de pelo menos um insumo.');
      return;
    }
    const number = client.phone;
    if (!number) {
      alert('O cliente não possui um número de telefone cadastrado.');
      return;
    }
    const message = `Olá *${client.name}*, estamos precisando de alguns insumos para a manutenção da sua piscina:\\n\\n` + 
      selected.map(s => `• ${s.name}: ${s.quantity} ${s.unit}`).join('\\n') + 
      `\\n\\nPor favor, providencie assim que possível para não interrompermos o tratamento.`;
      
    const settings = waSettings || userProfile?.whatsappSettings || {};
    const partnerStores = settings.partnerStores || [];
    
    setLastSentData({ products: selected });
    
    if (!settings.useMetaApi && !settings.useEvolutionApi) {
       openWhatsApp(number, message);
       if (partnerStores.length > 0) {
         setShowPartnerModal(true);
       } else {
         navigate('/clients');
       }
       return;
    }

    setSendingMessage(true);
    try {
      if (settings.useMetaApi) {
        await sendMetaMessage(number, message, settings);
        alert('Mensagem de insumos enviada com sucesso via Meta API!');
      } else if (settings.useEvolutionApi) {
        await sendEvolutionMessage(number, message, settings);
        alert('Mensagem de insumos enviada com sucesso via Evolution API!');
      }
      
      if (partnerStores.length > 0) {
        setShowPartnerModal(true);
      } else {
        navigate('/clients');
      }
    } catch (error: any) {
      console.error(error);
      alert('Falha ao enviar mensagem: ' + error.message);
    } finally {
      setSendingMessage(false);
    }
  };
"""

# Replace handleSend
start_idx = content.find('  const handleSend = async () => {')
end_idx = content.find('  if (loading) {', start_idx)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_handlers + content[end_idx:]

# Add JSX
modal_jsx = """
      {showPartnerModal && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md flex flex-col overflow-hidden">
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h2 className="text-xl font-bold text-gray-800">Enviar para Lojas Parceiras?</h2>
              <button onClick={closePartnerModal} className="text-gray-400 hover:text-gray-600">
                <X size={24} />
              </button>
            </div>
            
            <div className="p-6 overflow-y-auto">
              <p className="text-gray-600 mb-4">
                Deseja enviar a lista de produtos solicitada para suas lojas parceiras cadastradas?
              </p>
              
              <div className="space-y-3">
                {(waSettings?.partnerStores || (userProfile?.whatsappSettings as any)?.partnerStores || []).map((store: any, idx: number) => (
                  <label key={idx} className="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                    <input
                      type="checkbox"
                      className="w-5 h-5 rounded border-gray-300 text-primary focus:ring-primary mr-3"
                      checked={selectedPartners.includes(store.phone)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedPartners([...selectedPartners, store.phone]);
                        } else {
                          setSelectedPartners(selectedPartners.filter(p => p !== store.phone));
                        }
                      }}
                    />
                    <div>
                      <div className="font-medium text-gray-800">{store.name}</div>
                      <div className="text-sm text-gray-500">{store.phone}</div>
                    </div>
                  </label>
                ))}
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-100 flex justify-between bg-gray-50 shrink-0">
              <button
                onClick={closePartnerModal}
                className="px-4 py-2 text-gray-600 hover:bg-gray-200 rounded-lg transition-colors font-medium"
              >
                Não, obrigado
              </button>
              <button
                onClick={handleSendToPartners}
                disabled={selectedPartners.length === 0}
                className="flex items-center px-6 py-2 bg-primary text-white font-bold rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50"
              >
                <Send size={18} className="mr-2" />
                Enviar ({selectedPartners.length})
              </button>
            </div>
          </div>
        </div>
      )}
"""

# Replace `    </div>\n  );\n}` at the end of the file
content = content.replace("    </div>\n  );\n}", modal_jsx + "    </div>\n  );\n}")

with open('src/pages/SuppliesForm.tsx', 'w') as f:
    f.write(content)
