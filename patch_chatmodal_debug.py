import re

with open('src/components/ChatModal.tsx', 'r') as f:
    content = f.read()

debug_log = """
        const { data: newSession, error: createError } = await supabase
          .from('chat_sessions')
          .insert({
            visit_id: visit.id,
            admin_id: adminId,
            client_id: client.id,
            employee_id: userProfile?.id,
            status: 'open'
          }).select().single();
          
        console.log("CREATE SESSION RESULT:", newSession, "ERROR:", createError, "PARAMS:", { visit_id: visit.id, admin_id: adminId, client_id: client.id, employee_id: userProfile?.id });
"""

content = re.sub(r"(const \{ data: newSession, error: createError \} = await supabase[\s\S]*?\}\)\.select\(\)\.single\(\);)", debug_log, content, count=1)

with open('src/components/ChatModal.tsx', 'w') as f:
    f.write(content)
