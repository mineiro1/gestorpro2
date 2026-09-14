const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
async function run() {
  const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
  const { data, error } = await supabase.from('chat_sessions').select('*').limit(1);
  console.log(data);
}
run();
