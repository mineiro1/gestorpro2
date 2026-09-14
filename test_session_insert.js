import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseAdmin = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);

async function run() {
  const adminId = "698dfcdd-7c91-4df5-aaee-eae9e67f15ae";
  const { data: clients } = await supabaseAdmin.from('clients').select('id').eq('admin_id', adminId).limit(1);
  if (!clients || clients.length === 0) { console.log("No client"); return; }
  
  const { data: visits } = await supabaseAdmin.from('visits').select('id').eq('client_id', clients[0].id).limit(1);
  if (!visits || visits.length === 0) { console.log("No visit"); return; }
  
  const { data, error } = await supabaseAdmin.from('chat_sessions').insert({
    visit_id: visits[0].id,
    admin_id: adminId,
    client_id: clients[0].id,
    employee_id: adminId,
    status: 'open'
  }).select().single();
  
  console.log("Insert result:", data, error);
}
run();
