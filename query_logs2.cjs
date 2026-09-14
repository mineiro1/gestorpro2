require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  const { data } = await supabase.from('chat_messages').select('*').like('content', 'WEBHOOK_PAYLOAD%').order('created_at', { ascending: false }).limit(5);
  console.log("LOGS:", data);
}
run();
