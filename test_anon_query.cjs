require('dotenv').config();
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.VITE_SUPABASE_URL, process.env.VITE_SUPABASE_ANON_KEY);
async function run() {
  const { data, error } = await supabase.from('clients').select('id, name');
  console.log("Error:", error);
  console.log("Data length:", data ? data.length : 0);
}
run();
