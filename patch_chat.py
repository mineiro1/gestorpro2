with open('src/components/ChatModal.tsx', 'r') as f:
    content = f.read()

old_block = """        if (currentSession.status === 'open') {
          const createdTime = new Date(currentSession.created_at).getTime();
          const now = new Date().getTime();
          if (now - createdTime > 30 * 60 * 1000) {
             await supabase.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', currentSession.id);
             currentSession.status = 'closed';
          }
        }"""

new_block = """        // if (currentSession.status === 'open') {
        //   const createdTime = new Date(currentSession.created_at).getTime();
        //   const now = new Date().getTime();
        //   if (now - createdTime > 30 * 60 * 1000) {
        //      await supabase.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('id', currentSession.id);
        //      currentSession.status = 'closed';
        //   }
        // }"""

content = content.replace(old_block, new_block)

with open('src/components/ChatModal.tsx', 'w') as f:
    f.write(content)
