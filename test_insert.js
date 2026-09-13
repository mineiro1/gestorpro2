import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
dotenv.config();

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseKey = process.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function test() {
  const { data, error } = await supabase.from('chat_sessions').insert({
    visit_id: '123',
    admin_id: '123',
    client_id: '123',
    employee_id: '123',
    status: 'open'
  });
  console.log("Error:", error);
}
test();
