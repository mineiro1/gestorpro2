require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  const { data, error } = await supabase.from('chat_sessions').insert({
    admin_id: '698dfcdd-7c91-4df5-aaee-eae9e67f15ae',
    client_id: '804c35fc-53e5-400a-8795-8eb9fd7ad69b',
    employee_id: '698dfcdd-7c91-4df5-aaee-eae9e67f15ae',
    status: 'open'
  }).select().single();
  console.log(error || "Success");
}
run();
