import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);

async function run() {
  const { data: sessions } = await supabaseAdmin.from('chat_sessions').select('*').order('created_at', { ascending: false }).limit(2);
  console.log("Sessions:", sessions);
  
  if (sessions.length > 0) {
    const clientId = sessions[0].client_id;
    const { data: client } = await supabaseAdmin.from('clients').select('id, phone, local_phone').eq('id', clientId).single();
    console.log("Client for session:", client);
  }
}
run();
