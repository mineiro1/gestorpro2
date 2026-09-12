import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# 1. Imports
imports = """import { ChatModal } from '../components/ChatModal';
import { MessageCircle } from 'lucide-react';"""
content = re.sub(r"(import React.*?;\n)", r"\1" + imports + "\n", content, count=1)

# 2. Add state
state_match = r"(const \[visits, setVisits\] = useState<any\[\]>\(\[\]\);)"
state_injection = """
  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [activeChatVisit, setActiveChatVisit] = useState<any>(null);
  const [activeChatClient, setActiveChatClient] = useState<any>(null);
"""
content = re.sub(state_match, r"\1" + state_injection, content, count=1)

# 3. Add handleOpenChat function
handle_open = """
  const handleOpenChat = (visit: any, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    const client = clients.find(c => c.id === visit.client_id);
    if (!client) return;
    setActiveChatVisit(visit);
    setActiveChatClient(client);
    setChatModalOpen(true);
  };
"""

content = re.sub(r"(const handleFinishVisit = async \(visitId: string\) => \{)", handle_open + r"\n  \1", content, count=1)

# 4. In handleFinishVisit, automatically close the chat session
finish_visit_logic = """
    // Fechamento Automático do Chat (Por Ação)
    try {
      await supabase.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('visit_id', visitId).eq('status', 'open');
    } catch(e) {}
"""
content = re.sub(r"(setVisits\(visits\.map\(v => v\.id === visitId \? \{ \.\.\.v, status: 'finalizada' \} : v\)\);)", r"\1" + finish_visit_logic, content, count=1)

# 5. Add button to the UI. Find where buttons are rendered.
# Looking for `<button onClick={(e) => { e.stopPropagation(); openWhatsApp(`
btn_regex = r"(<button\s*onClick=\{\(e\) => \{\s*e\.stopPropagation\(\);\s*openWhatsApp[\s\S]*?</button>)"

chat_btn = """
                          {/* Botão Estou a caminho / Chat */}
                          <button
                            onClick={(e) => handleOpenChat(visit, e)}
                            className="p-2 bg-blue-100 text-blue-600 rounded-full hover:bg-blue-200 transition-colors"
                            title="Avisar chegada / Chat"
                          >
                            <MessageCircle size={18} />
                          </button>
"""

content = re.sub(btn_regex, r"\1" + chat_btn, content)

# 6. Add ChatModal at the end
modal_regex = r"(</Layout>)"
modal_injection = """
      <ChatModal 
        isOpen={chatModalOpen} 
        onClose={() => setChatModalOpen(false)} 
        visit={activeChatVisit} 
        client={activeChatClient} 
        waSettings={userProfile?.whatsappSettings}
      />
"""
content = re.sub(modal_regex, modal_injection + r"\1", content)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
