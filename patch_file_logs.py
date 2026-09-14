import re

with open('server.ts', 'r') as f:
    content = f.read()

# Replace console.log and console.error in the webhook
old_log = 'console.log("Evolution Webhook Received:", JSON.stringify(req.body));'
new_log = """console.log("Evolution Webhook Received:", JSON.stringify(req.body));
import fs from 'fs';
fs.appendFileSync('webhook_debug.log', "Webhook Received: " + JSON.stringify(req.body) + "\\n");"""
content = content.replace(old_log, new_log)

old_clientsErr = 'if (clientsErr) console.error("Webhook clients error:", clientsErr);'
new_clientsErr = """if (clientsErr) {
    console.error("Webhook clients error:", clientsErr);
    fs.appendFileSync('webhook_debug.log', "Clients Err: " + JSON.stringify(clientsErr) + "\\n");
} else {
    fs.appendFileSync('webhook_debug.log', "Clients found: " + clients.length + "\\n");
}"""
content = content.replace(old_clientsErr, new_clientsErr)

old_match = 'if (!matchedClient) return res.status(200).send("OK");'
new_match = """if (!matchedClient) {
    fs.appendFileSync('webhook_debug.log', "No matched client for phone: " + phone + "\\n");
    return res.status(200).send("OK");
} else {
    fs.appendFileSync('webhook_debug.log', "Matched client: " + matchedClient.id + "\\n");
}"""
content = content.replace(old_match, new_match)

old_sess = 'if (!sessions || sessions.length === 0) {'
new_sess = """fs.appendFileSync('webhook_debug.log', "Sessions error: " + JSON.stringify(sessionsErr) + " | Found: " + (sessions ? sessions.length : 0) + "\\n");
      if (!sessions || sessions.length === 0) {"""
content = content.replace(old_sess, new_sess)

old_ins = 'if (insertErr) console.error("Webhook insert message error:", insertErr);'
new_ins = """if (insertErr) {
    console.error("Webhook insert message error:", insertErr);
    fs.appendFileSync('webhook_debug.log', "Insert Err: " + JSON.stringify(insertErr) + "\\n");
} else {
    fs.appendFileSync('webhook_debug.log', "Insert OK!\\n");
}"""
content = content.replace(old_ins, new_ins)

with open('server.ts', 'w') as f:
    f.write(content)
