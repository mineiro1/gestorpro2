with open('src/pages/ProductsPage.tsx', 'r') as f:
    content = f.read()

import re

# Find handleSend
start_idx = content.find('  const handleSend = async () => {')
# Find the end of handleSend (which ends just before `if (loading) {` or `return (`)
end_idx = content.find('  if (loading) {', start_idx)
if end_idx == -1:
    end_idx = content.find('  return (', start_idx)

new_handle_send = """  const handleSend = async () => {
    if (!selectedClient) {
      alert('Selecione um cliente primeiro.');
      return;
    }
    const selected = supplies.filter(s => s.quantity && Number(s.quantity) > 0);
    if (selected.length === 0) {
      alert('Preencha a quantidade de pelo menos um insumo.');
      return;
    }
    const number = selectedClient.phone;
    if (!number) {
      alert('O cliente não possui um número de telefone cadastrado.');
      return;
    }
    const message = `Olá *${selectedClient.name}*, estamos precisando de alguns insumos para a manutenção da sua piscina:\\n\\n` + 
      selected.map(s => `• ${s.name}: ${s.quantity} ${s.unit}`).join('\\n') + 
      `\\n\\nPor favor, providencie assim que possível para não interrompermos o tratamento.`;
      
    const settings = waSettings || userProfile?.whatsappSettings || {};
    const partnerStores = settings.partnerStores || [];
    
    setLastSentData({ client: selectedClient, products: selected });
    
    // Web WhatsApp natively (synchronous to avoid popup block if no API configured)
    if (!settings.useMetaApi && !settings.useEvolutionApi) {
       openWhatsApp(number, message);
       if (partnerStores.length > 0) {
         setShowPartnerModal(true);
       } else {
         setSupplies(supplies.map(s => ({ ...s, quantity: '' })));
         setSelectedClient(null);
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
        setSupplies(supplies.map(s => ({ ...s, quantity: '' })));
        setSelectedClient(null);
      }
    } catch (error: any) {
      console.error(error);
      alert('Falha ao enviar mensagem: ' + error.message);
    } finally {
      setSendingMessage(false);
    }
  };

"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_handle_send + content[end_idx:]
    with open('src/pages/ProductsPage.tsx', 'w') as f:
        f.write(content)
    print("Patched successfully")
else:
    print("Could not find boundaries")
