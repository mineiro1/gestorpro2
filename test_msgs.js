const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();
async function run() {
  const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);
  // test if we can select messages by joining sessions
  // not possible without view. 
  // we can select chat_sessions by visit_id, then get their ids
}
