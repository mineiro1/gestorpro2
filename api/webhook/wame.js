import { createClient } from '@supabase/supabase-js';

export default async function handler(req, res) {
  // 1. Handle Wame/Meta GET Verification Challenge
  if (req.method === 'GET') {
    const mode = req.query["hub.mode"];
    const challenge = req.query["hub.challenge"];
    if (mode === "subscribe" && challenge) {
      return res.status(200).send(challenge);
    }
    return res.status(200).send("Wame Webhook is active!");
  }

  // 2. Handle POST Messages
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const supabaseUrl = process.env.VITE_SUPABASE_URL || '';
    const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.VITE_SUPABASE_ANON_KEY || '';
    const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey, {
      auth: { autoRefreshToken: false, persistSession: false }
    });

    const body = req.body;
    let phone = "";
    let content = "";
    let mediaUrl = "";
    
    // Parse Meta/Wame API format
    if ((body.object === "whatsapp_business_account" || body.object === "wame") && body.entry && body.entry[0].changes) {
       const value = body.entry[0].changes[0].value;
       if (value.messages && value.messages.length > 0) {
          const msg = value.messages[0];
          phone = msg.from;
          if (msg.type === "text" && msg.text) {
             content = msg.text.body;
          } else if (msg.type === "audio") {
             content = "🎵 Mensagem de Áudio";
          } else if (msg.type === "image") {
             content = "📷 Imagem";
          } else if (msg.type === "document") {
             content = "📄 Documento";
          }
       } else {
          return res.status(200).send("EVENT_RECEIVED");
       }
    } 
    // Fallback parsing for alternative raw formats
    else if (body.phone && body.message) {
        phone = body.phone;
        content = body.message;
    } else if (body.contact && body.message) {
        phone = body.contact;
        content = body.message;
    } else if (body.from && body.body) {
        phone = body.from;
        content = body.body;
    }
    
    if (!phone || !content) {
       return res.status(200).send("EVENT_RECEIVED");
    }
    
    // 3. Robust Phone Matching (Bypass 9th digit and DDD inconsistencies)
    const { data: clients, error: clientsErr } = await supabaseAdmin.from('clients').select('id, phone, local_phone, admin_id');
    if (clientsErr) console.error("Webhook clients error:", clientsErr);
    
    const matchedClient = (clients || []).find(c => {
       const cp = (c.phone || '').replace(/\D/g, '');
       const lp = (c.local_phone || '').replace(/\D/g, '');
       if (!cp && !lp) return false;
       
       const getCore = (num) => num.length >= 8 ? num.slice(-8) : num;
       const webhookCore = getCore(phone.replace(/\D/g, ''));
       
       let matchPhone = false;
       if (cp.length > 5) {
          matchPhone = cp.includes(phone) || phone.includes(cp) || getCore(cp) === webhookCore;
       }
       
       let matchLocal = false;
       if (lp.length > 5) {
          matchLocal = lp.includes(phone) || phone.includes(lp) || getCore(lp) === webhookCore;
       }
       
       return matchPhone || matchLocal;
    });
    
    if (!matchedClient) {
        console.log("Client not found for phone:", phone);
        return res.status(200).send("EVENT_RECEIVED");
    }

    // 4. Find or Create Session
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
       // Auto-close if older than 30 mins
       if (now - createdTime > 30 * 60 * 1000) {
          await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
          activeSession = null;
       }
    }
    
    if (!activeSession) {
       const { data: newSession, error: newSessionError } = await supabaseAdmin
         .from('chat_sessions')
         .insert({
            client_id: matchedClient.id,
            admin_id: matchedClient.admin_id,
            employee_id: matchedClient.admin_id, // fallback to admin
            status: 'open'
         }).select().single();
       if (newSessionError) {
          console.error("Failed to create new session:", newSessionError);
          return res.status(200).send("EVENT_RECEIVED");
       }
       activeSession = newSession;
    }
    
    // 5. Save the Message
    const { error: insertError } = await supabaseAdmin.from('chat_messages').insert({
       session_id: activeSession.id,
       sender_type: 'client',
       content: content,
       media_url: mediaUrl
    });
    
    if (insertError) {
       console.error("Error inserting message:", insertError);
    } else {
       console.log("Message successfully saved to session", activeSession.id);
    }
    
    return res.status(200).send("EVENT_RECEIVED");
    
  } catch(e) {
    console.error("Webhook Error:", e);
    return res.status(500).send("Error");
  }
}
