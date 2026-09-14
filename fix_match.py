with open('server.ts', 'r') as f:
    content = f.read()

old_match = """      // Find matching client
      const matchedClient = clients.find(c => {
         const cp = (c.phone || '').replace(/\\D/g, '');
         const lp = (c.local_phone || '').replace(/\\D/g, '');
         return cp.includes(phone) || lp.includes(phone) || phone.includes(cp) || phone.includes(lp);
      });"""

new_match = """      // Find matching client
      const matchedClient = clients.find(c => {
         const cp = (c.phone || '').replace(/\\D/g, '');
         const lp = (c.local_phone || '').replace(/\\D/g, '');
         if (!cp && !lp) return false;
         
         let matchPhone = false;
         if (cp.length > 5) {
             matchPhone = cp.includes(phone) || phone.includes(cp);
         }
         let matchLocal = false;
         if (lp.length > 5) {
             matchLocal = lp.includes(phone) || phone.includes(lp);
         }
         return matchPhone || matchLocal;
      });"""

content = content.replace(old_match, new_match)
with open('server.ts', 'w') as f:
    f.write(content)
