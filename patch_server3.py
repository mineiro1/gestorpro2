import re

with open('server.ts', 'r') as f:
    content = f.read()

old_webhook = """  // Webhook for incoming messages
  app.post("/api/webhook/evolution", async (req, res) => {
    try {
      console.log("Evolution Webhook Received:", JSON.stringify(req.body));
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
  });"""

new_webhook = """  // Webhook for incoming messages
  app.post("/api/webhook/evolution", async (req, res) => {
    try {
      console.log("Evolution Webhook Received:", JSON.stringify(req.body));
      const body = req.body;
      
      // Extracted payload handling (supports v1, v2 and array formats)
      let msgData = body.data || body;
      
      if (msgData.message && msgData.message.key) {
         msgData = msgData.message;
      } else if (Array.isArray(msgData) && msgData[0]?.key) {
         msgData = msgData[0];
      } else if (msgData.messages && Array.isArray(msgData.messages) && msgData.messages[0]?.key) {
         msgData = msgData.messages[0];
      }

      if (!msgData || !msgData.key || !msgData.message) {
         console.log("Not a valid message payload, ignoring.");
         return res.status(200).send("OK");
      }
      
      if (msgData.key.fromMe) return res.status(200).send("OK");
      
      let remoteJid = msgData.key.remoteJid || "";
      if (!remoteJid || remoteJid.includes('@g.us')) return res.status(200).send("OK");
      
      let phone = remoteJid.split('@')[0].replace(/^55/, ''); 
      
      let content = "";
      if (msgData.message.conversation) content = msgData.message.conversation;
      else if (msgData.message.extendedTextMessage) content = msgData.message.extendedTextMessage?.text || "";
      
      let mediaUrl = "";
      if (msgData.message.audioMessage) content = "🎵 Mensagem de Áudio";
      else if (msgData.message.imageMessage) content = "📷 Imagem";
      else if (msgData.message.documentMessage) content = "📄 Documento";
      else if (msgData.message.videoMessage) content = "🎥 Vídeo";
      else if (msgData.message.stickerMessage) content = "🖼️ Figurinha";

      if (!content && !mediaUrl) return res.status(200).send("OK");

      const { data: clients } = await supabaseAdmin.from('clients').select('id, phone, local_phone, admin_id');
      if (!clients) return res.status(200).send("OK");
      
      const matchedClient = clients.find(c => {
         const cp = (c.phone || '').replace(/\D/g, '');
         const lp = (c.local_phone || '').replace(/\D/g, '');
         return cp.includes(phone) || lp.includes(phone) || phone.includes(cp) || phone.includes(lp);
      });
      
      if (!matchedClient) return res.status(200).send("OK");

      const { data: sessions } = await supabaseAdmin
        .from('chat_sessions')
        .select('*')
        .eq('client_id', matchedClient.id)
        .eq('status', 'open')
        .order('created_at', { ascending: false });
        
      let activeSession = sessions && sessions.length > 0 ? sessions[0] : null;
      
      const now = new Date().getTime();
      if (activeSession) {
         const createdTime = new Date(activeSession.created_at).getTime();
         if (now - createdTime > 30 * 60 * 1000) {
            await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
            activeSession = null;
         }
      }

      if (!activeSession) {
         const { data: newSession } = await supabaseAdmin
           .from('chat_sessions')
           .insert({
              client_id: matchedClient.id,
              admin_id: matchedClient.admin_id,
              employee_id: matchedClient.admin_id,
              status: 'open'
           }).select().single();
         activeSession = newSession;
      }
      
      if (!activeSession) return res.status(200).send("OK");

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
  });"""

content = content.replace(old_webhook, new_webhook)

with open('server.ts', 'w') as f:
    f.write(content)
