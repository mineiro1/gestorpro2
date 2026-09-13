import re

with open('server.ts', 'r') as f:
    content = f.read()

# Make the webhook more resilient
old_webhook = """  // Webhook for incoming messages
  app.post("/api/webhook/evolution", async (req, res) => {
    try {
      const body = req.body;
      
      // Evolution API format usually comes in body.data for messages
      // This varies by version, let's handle the typical structure
      const msgData = body.data || body;"""

new_webhook = """  // Webhook for incoming messages
  app.post("/api/webhook/evolution", async (req, res) => {
    try {
      console.log("Evolution Webhook Received:", JSON.stringify(req.body));
      const body = req.body;
      
      // Evolution API format usually comes in body.data for messages
      // This varies by version, let's handle the typical structure
      const msgData = body.data || body;"""

content = content.replace(old_webhook, new_webhook)

with open('server.ts', 'w') as f:
    f.write(content)
