import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);

async function run() {
  const { data, error } = await supabaseAdmin.from('chat_messages').select('*').order('created_at', { ascending: false }).limit(5);
  if (error) console.error(error);
  else console.log("Recent chat_messages:", data);
  
  const { data: sessions } = await supabaseAdmin.from('chat_sessions').select('*').order('created_at', { ascending: false }).limit(5);
  console.log("Recent chat_sessions:", sessions);
}
run();
