import re

with open('server.ts', 'r') as f:
    content = f.read()

# Patch 1: log client query error
old_clients = "const { data: clients } = await supabaseAdmin.from('clients').select('id, phone, local_phone');"
new_clients = """const { data: clients, error: clientsErr } = await supabaseAdmin.from('clients').select('id, phone, local_phone');
      if (clientsErr) console.error("Webhook clients error:", clientsErr);"""
content = content.replace(old_clients, new_clients)

# Patch 2: log session query error
old_sessions = """const { data: sessions } = await supabaseAdmin
        .from('chat_sessions')
        .select('*')
        .eq('client_id', matchedClient.id)
        .eq('status', 'open');"""
new_sessions = """const { data: sessions, error: sessionsErr } = await supabaseAdmin
        .from('chat_sessions')
        .select('*')
        .eq('client_id', matchedClient.id)
        .eq('status', 'open');
      if (sessionsErr) console.error("Webhook sessions error:", sessionsErr);"""
content = content.replace(old_sessions, new_sessions)

# Patch 3: log insert error
old_insert = """await supabaseAdmin.from('chat_messages').insert({
         session_id: activeSession.id,
         sender_type: 'client',
         content: content,
         media_url: mediaUrl
      });"""
new_insert = """const { error: insertErr } = await supabaseAdmin.from('chat_messages').insert({
         session_id: activeSession.id,
         sender_type: 'client',
         content: content,
         media_url: mediaUrl
      });
      if (insertErr) console.error("Webhook insert message error:", insertErr);
      else console.log("Webhook message inserted successfully!");"""
content = content.replace(old_insert, new_insert)

with open('server.ts', 'w') as f:
    f.write(content)
