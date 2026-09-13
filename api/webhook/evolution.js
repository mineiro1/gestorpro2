import { createClient } from '@supabase/supabase-js';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const supabaseUrl = process.env.VITE_SUPABASE_URL || '';
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.VITE_SUPABASE_ANON_KEY || '';
    const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey, {
      auth: { autoRefreshToken: false, persistSession: false }
    });

    console.log("Evolution Webhook Received:", JSON.stringify(req.body));
    const body = req.body;
    
    // Evolution API format usually comes in body.data for messages
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
    
    let phone = remoteJid.split('@')[0].replace('55', ''); // naive clean
    
    let content = "";
    if (msgData.message.conversation) content = msgData.message.conversation;
    else if (msgData.message.extendedTextMessage) content = msgData.message.extendedTextMessage?.text || "";
    
    let mediaUrl = "";
    if (msgData.message.audioMessage) {
       content = "🎵 Mensagem de Áudio";
    } else if (msgData.message.imageMessage) {
       content = "📷 Imagem";
    }
    if (!content && !mediaUrl) return res.status(200).send("OK");

    const { data: clients } = await supabaseAdmin.from('clients').select('id, phone, local_phone');
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
      .eq('status', 'open');
      
    if (!sessions || sessions.length === 0) {
       return res.status(200).send("OK"); // No active session
    }
    
    const activeSession = sessions[0];
    const createdTime = new Date(activeSession.created_at).getTime();
    const now = new Date().getTime();
    if (now - createdTime > 30 * 60 * 1000) {
       await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
       return res.status(200).send("OK");
    }

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
}
