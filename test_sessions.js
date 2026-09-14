import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);

async function run() {
  const { data, error } = await supabaseAdmin.from('chat_sessions').select('*').limit(5);
  console.log("Anon key chat_sessions query:", data, error);
}
run();
