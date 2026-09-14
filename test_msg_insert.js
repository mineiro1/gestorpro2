import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);

async function run() {
  const { data, error } = await supabaseAdmin.from('chat_messages').insert({
    session_id: '00000000-0000-0000-0000-000000000000',
    sender_type: 'client',
    content: 'teste'
  }).select().single();
  console.log("Msg insert result:", data, error);
}
run();
