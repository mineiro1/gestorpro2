import fetch from 'node-fetch';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.VITE_SUPABASE_ANON_KEY);

async function run() {
  const adminId = "698dfcdd-7c91-4df5-aaee-eae9e67f15ae";
  
  // Find a client
  const { data: clients } = await supabaseAdmin.from('clients').select('id, phone, local_phone').eq('admin_id', adminId).limit(1);
  const client = clients[0];
  let phone = (client.phone || '').replace(/\D/g, '');
  if (!phone.startsWith("55")) phone = "55" + phone;

  console.log("Client phone:", phone);

  // Is there a session?
  const { data: sessions } = await supabaseAdmin.from('chat_sessions').select('*').eq('client_id', client.id);
  console.log("Existing sessions:", sessions);

  // Send a webhook POST
  const webhookBody = {
    data: {
      key: {
        remoteJid: `${phone}@s.whatsapp.net`,
        fromMe: false
      },
      message: {
        conversation: "Teste de mensagem via Webhook (Admin Test)!"
      }
    }
  };

  const res = await fetch("http://localhost:3000/api/webhook/evolution", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(webhookBody)
  });
  
  console.log("Webhook response:", res.status, await res.text());
  
  // Check if it inserted
  const { data: msgs } = await supabaseAdmin.from('chat_messages').select('*').order('created_at', { ascending: false }).limit(2);
  console.log("Recent messages after webhook:", msgs);
}
run();
