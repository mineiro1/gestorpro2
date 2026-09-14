require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  // Let's check ANY messages from the last 15 minutes, ignoring the 'RAW_WEBHOOK' tag
  const fifteenMinsAgo = new Date(Date.now() - 15 * 60 * 1000).toISOString();
  const { data, error } = await supabase.from('chat_messages').select('*').gte('created_at', fifteenMinsAgo).order('created_at', { ascending: false });
  console.log("Recent DB Entries:", JSON.stringify(data, null, 2));
}
run();
