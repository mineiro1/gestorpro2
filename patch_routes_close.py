import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# Modify processReportSubmission to close chat session
close_logic = """
    // Fechamento Automático do Chat (Por Ação)
    try {
      await supabase.from('chat_sessions')
        .update({ status: 'closed', closed_at: new Date().toISOString() })
        .eq('client_id', selectedClientForReport.id)
        .eq('status', 'open');
    } catch(e) {}
"""

content = re.sub(r"(const checklistText = checkedItems\.length > 0 \? `\\n\\nTarefas realizadas:\\n- \$\{checkedItems\.join\('\\n- '\)\}` : '';)", close_logic + r"\n            \1", content, count=1)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
