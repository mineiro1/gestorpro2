require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  const { data } = await supabase.from('chat_messages').select('*').order('created_at', { ascending: false }).limit(3);
  console.log("Recent messages:", data);
  const { data: sess } = await supabase.from('chat_sessions').select('*').order('created_at', { ascending: false }).limit(3);
  console.log("Recent sessions:", sess);
}
run();
