require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.SUPABASE_SERVICE_ROLE_KEY);
async function run() {
  const { data } = await supabase.from('clients').select('id, name, phone, local_phone').like('phone', '%1907236%');
  console.log("CLIENTS:", JSON.stringify(data, null, 2));
}
run();
