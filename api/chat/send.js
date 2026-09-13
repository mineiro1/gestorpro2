export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const { text, clientPhone, waSettings } = req.body;
    if (!text || !clientPhone) return res.status(400).json({error: "Missing fields"});

    // Send via Evolution API
    if (waSettings?.useEvolutionApi && waSettings?.evolutionApiUrl && waSettings?.evolutionApiKey && waSettings?.evolutionInstanceName) {
      const cleanPhone = clientPhone.replace(/\D/g, '');
      const response = await fetch(`${waSettings.evolutionApiUrl}/message/sendText/${waSettings.evolutionInstanceName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'apikey': waSettings.evolutionApiKey
        },
        body: JSON.stringify({
          number: `55${cleanPhone}`,
          text: text,
          options: { delay: 1200, presence: 'composing' },
          textMessage: { text: text }
        })
      });
      if (!response.ok) {
         const errText = await response.text();
         console.error("Evolution Send Error:", errText);
      }
    }
    
    res.json({ success: true });
  } catch(e) {
    console.error(e);
    res.status(500).json({ error: e.message });
  }
}
