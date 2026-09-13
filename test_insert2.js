import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseKey = process.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function test() {
  const { data: clients } = await supabase.from('clients').select('id, admin_id').limit(1);
  const { data: visits } = await supabase.from('visits').select('id').limit(1);
  
  if (clients.length > 0 && visits.length > 0) {
      const { data, error } = await supabase.from('chat_sessions').insert({
        visit_id: visits[0].id,
        admin_id: clients[0].admin_id,
        client_id: clients[0].id,
        status: 'open'
      }).select();
      console.log("Session Insert Result:", data, "Error:", error);
  }
}
test();
