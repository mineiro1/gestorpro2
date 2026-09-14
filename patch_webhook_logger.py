with open('server.ts', 'r') as f:
    content = f.read()

log_block = """      console.log("Wame/Meta Webhook Received:", JSON.stringify(req.body));
      // Save debug log to DB just so we can see it!
      try {
         await supabaseAdmin.from('chat_messages').insert({
            session_id: 'e867ca9f-d11f-4bb5-8bc6-96e1455fd260', // fake session ID just to see it in db
            sender_type: 'client',
            content: "WEBHOOK_PAYLOAD: " + JSON.stringify(req.body).substring(0, 500)
         });
      } catch(e) {}"""

content = content.replace('console.log("Wame/Meta Webhook Received:", JSON.stringify(req.body));', log_block)

with open('server.ts', 'w') as f:
    f.write(content)
