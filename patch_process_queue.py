import re

with open('src/pages/Billing.tsx', 'r') as f:
    content = f.read()

# Add check and state update in processQueue loop
loop_start = """      for (let i = 0; i < clients.length; i++) {
        const client = clients[i];
        setSendingProgress({ current: i + 1, total: clients.length });"""

loop_replacement = """      const todayStr = new Date().toLocaleDateString('pt-BR');

      for (let i = 0; i < clients.length; i++) {
        const client = clients[i];
        setSendingProgress({ current: i + 1, total: clients.length });
        
        // Skip if already billed today
        if (billedClients[client.id] === todayStr) {
          successCount++; // count as success to skip
          continue;
        }"""

content = content.replace(loop_start, loop_replacement)


# Also we need to update billedClients state at the end of the success block inside processQueue
success_block = """          if (waSettings.useMetaApi) {
            await sendMetaMessage(client, message);
          } else {
            await sendEvolutionMessage(client, message);
          }
          setSentClients(prev => ({ ...prev, [client.id]: 'success' }));
          successCount++;"""

success_replacement = """          if (waSettings.useMetaApi) {
            await sendMetaMessage(client, message);
          } else {
            await sendEvolutionMessage(client, message);
          }
          setSentClients(prev => ({ ...prev, [client.id]: 'success' }));
          
          setBilledClients(prev => {
            const newBilled = { ...prev, [client.id]: todayStr };
            localStorage.setItem('gestaopro_billed_clients', JSON.stringify(newBilled));
            return newBilled;
          });
          
          successCount++;"""

content = content.replace(success_block, success_replacement)

with open('src/pages/Billing.tsx', 'w') as f:
    f.write(content)
