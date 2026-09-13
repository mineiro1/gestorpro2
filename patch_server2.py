import re

with open('server.ts', 'r') as f:
    content = f.read()

old_send = """  app.post("/api/chat/send", async (req, res) => {
    try {
      const { sessionId, text, clientPhone, waSettings } = req.body;
      if (!sessionId || !text || !clientPhone) return res.status(400).json({error: "Missing fields"});

      // Save to db first
      const { data: msg, error } = await supabaseAdmin
        .from('chat_messages')
        .insert({
           session_id: sessionId,
           sender_type: 'tech',
           content: text
        }).select().single();
      
      if (error) console.error("Error saving message", error);

      // Now send via Evolution API"""

new_send = """  app.post("/api/chat/send", async (req, res) => {
    try {
      const { text, clientPhone, waSettings } = req.body;
      if (!text || !clientPhone) return res.status(400).json({error: "Missing fields"});

      // Now send via Evolution API"""

content = content.replace(old_send, new_send)

with open('server.ts', 'w') as f:
    f.write(content)
