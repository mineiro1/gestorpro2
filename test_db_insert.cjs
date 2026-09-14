require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  const { data, error } = await supabase.from('chat_messages').insert({
    session_id: 'e867ca9f-d11f-4bb5-8bc6-96e1455fd260',
    sender_type: 'client',
    content: "TEST_INSERT"
  });
  console.log("Error:", error);
}
run();
