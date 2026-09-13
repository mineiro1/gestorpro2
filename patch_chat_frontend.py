import re

with open('src/components/ChatModal.tsx', 'r') as f:
    content = f.read()

old_send = """    // Actually send to API endpoint which will forward to Meta/Evolution and save
    try {
      await fetch('/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: session.id,
          text,
          clientPhone: client.local_phone || client.phone,
          waSettings
        })
      });
    } catch (e) {"""

new_send = """    // Actually send to API endpoint which will forward to Meta/Evolution and save
    try {
      // 1. Insert into Supabase from the client (authenticated)
      await supabase.from('chat_messages').insert({
        session_id: session.id,
        sender_type: 'tech',
        content: text
      });

      // 2. Dispatch to backend to send via Evolution (bypasses CORS)
      await fetch('/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text,
          clientPhone: client.local_phone || client.phone,
          waSettings
        })
      });
    } catch (e) {"""

content = content.replace(old_send, new_send)

with open('src/components/ChatModal.tsx', 'w') as f:
    f.write(content)
