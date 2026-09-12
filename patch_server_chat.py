import re

with open('server.ts', 'r') as f:
    content = f.read()

chat_routes = """
  app.post("/api/chat/send", async (req, res) => {
    try {
      const { sessionId, text, clientPhone, waSettings } = req.body;
      if (!sessionId || !text || !clientPhone) return res.status(400).json({error: "Missing fields"});

      // Save to db first
      const { data: msg, error } = await supabaseAdmin
        .from('chat_messages')
        .insert({
           session_id: sessionId,
           sender_type: 'tech',
           content: text
        }).select().single();
      
      if (error) console.error("Error saving message", error);

      // Now send via Evolution API
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
            options: { delay: 1200, presence: 'composing' },
            textMessage: { text: text }
          })
        });
        if (!response.ok) {
           const errText = await response.text();
           console.error("Evolution Send Error:", errText);
        }
      } else if (waSettings?.useMetaApi) {
          // Meta API fallback if they use Meta instead
      }
      
      res.json({ success: true, message: msg });
    } catch(e) {
      console.error(e);
      res.status(500).json({ error: e.message });
    }
  });

  // Webhook for incoming messages
  app.post("/api/webhook/evolution", async (req, res) => {
    try {
      const body = req.body;
      
      // Evolution API format usually comes in body.data for messages
      // This varies by version, let's handle the typical structure
      const msgData = body.data || body;
      
      if (!msgData || !msgData.key || !msgData.message) {
         return res.status(200).send("OK");
      }

      // Ignore outgoing messages
      if (msgData.key.fromMe) {
         return res.status(200).send("OK");
      }

      let remoteJid = msgData.key.remoteJid || "";
      if (!remoteJid) return res.status(200).send("OK");
      
      // remoteJid is usually 5511999999999@s.whatsapp.net
      let phone = remoteJid.split('@')[0].replace('55', ''); // naive clean
      
      // Extract text content
      let content = "";
      if (msgData.message.conversation) content = msgData.message.conversation;
      else if (msgData.message.extendedTextMessage) content = msgData.message.extendedTextMessage.text;
      
      // Handle audio/media (Simplified, normally you need to download from Evolution)
      let mediaUrl = "";
      if (msgData.message.audioMessage) {
         content = "🎵 Mensagem de Áudio";
         // We would download the audio here if we had full evolution setup
      } else if (msgData.message.imageMessage) {
         content = "📷 Imagem";
      }

      if (!content && !mediaUrl) return res.status(200).send("OK");

      // Find an OPEN session for this phone number
      // Since phone can be formatted differently, we query clients where phone like %phone%
      // For safety, we query the chat_sessions matching the client.
      
      // A more robust query would search by phone or local_phone
      const { data: clients } = await supabaseAdmin.from('clients').select('id, phone, local_phone');
      if (!clients) return res.status(200).send("OK");
      
      // Find matching client
      const matchedClient = clients.find(c => {
         const cp = (c.phone || '').replace(/\D/g, '');
         const lp = (c.local_phone || '').replace(/\D/g, '');
         return cp.includes(phone) || lp.includes(phone) || phone.includes(cp) || phone.includes(lp);
      });
      
      if (!matchedClient) return res.status(200).send("OK");

      // Find open session
      const { data: sessions } = await supabaseAdmin
        .from('chat_sessions')
        .select('*')
        .eq('client_id', matchedClient.id)
        .eq('status', 'open');
        
      if (!sessions || sessions.length === 0) {
         return res.status(200).send("OK"); // No active session
      }
      
      // Check 30-min timeout
      const activeSession = sessions[0];
      const createdTime = new Date(activeSession.created_at).getTime();
      const now = new Date().getTime();
      if (now - createdTime > 30 * 60 * 1000) {
         // Auto close it
         await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
         return res.status(200).send("OK");
      }

      // Save message
      await supabaseAdmin.from('chat_messages').insert({
         session_id: activeSession.id,
         sender_type: 'client',
         content: content,
         media_url: mediaUrl
      });
      
      return res.status(200).send("OK");
    } catch(e) {
      console.error("Webhook Error:", e);
      return res.status(500).send("Error");
    }
  });
"""

import_hook = """app.all("/api/sync-payment","""

content = content.replace(import_hook, chat_routes + "\n" + import_hook)

with open('server.ts', 'w') as f:
    f.write(content)
