with open('server.ts', 'r') as f:
    content = f.read()

import re

# Block 1 in Wame Webhook
content = re.sub(
r"""      const createdTime = new Date\(activeSession\.created_at\)\.getTime\(\);\n      const now = new Date\(\)\.getTime\(\);\n      \n      if \(now - createdTime > 30 \* 60 \* 1000\) \{\n         await supabaseAdmin\.from\('chat_sessions'\)\.update\(\{ status: 'closed', closed_at: new Date\(\)\.toISOString\(\) \}\)\.eq\('id', activeSession\.id\);\n         return res\.status\(200\)\.send\("EVENT_RECEIVED"\);\n      \}""",
r"""      // Time lock removed for testing
      // const createdTime = new Date(activeSession.created_at).getTime();
      // const now = new Date().getTime();
      // if (now - createdTime > 30 * 60 * 1000) {
      //    await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
      //    return res.status(200).send("EVENT_RECEIVED");
      // }""",
content)

# Block 2 in Evolution Webhook
content = re.sub(
r"""      const createdTime = new Date\(activeSession\.created_at\)\.getTime\(\);\n      const now = new Date\(\)\.getTime\(\);\n      if \(now - createdTime > 30 \* 60 \* 1000\) \{\n         // Auto close it\n         await supabaseAdmin\.from\('chat_sessions'\)\.update\(\{ status: 'closed', closed_at: new Date\(\)\.toISOString\(\) \}\)\.eq\('id', activeSession\.id\);\n         return res\.status\(200\)\.send\("OK"\);\n      \}""",
r"""      // Time lock removed for testing
      // const createdTime = new Date(activeSession.created_at).getTime();
      // const now = new Date().getTime();
      // if (now - createdTime > 30 * 60 * 1000) {
      //    await supabaseAdmin.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', activeSession.id);
      //    return res.status(200).send("OK");
      // }""",
content)

with open('server.ts', 'w') as f:
    f.write(content)
