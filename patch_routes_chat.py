import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# Make sure imports are there
if "import { ChatModal } from '../components/ChatModal'" not in content:
    content = re.sub(r"(import React.*?;\n)", r"\1import { ChatModal } from '../components/ChatModal';\nimport { MessageCircle } from 'lucide-react';\n", content, count=1)

# Add states
if "const [chatModalOpen, setChatModalOpen] = useState(false);" not in content:
    state_injection = """
  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [activeChatVisit, setActiveChatVisit] = useState<any>(null);
  const [activeChatClient, setActiveChatClient] = useState<any>(null);
"""
    content = re.sub(r"(const \[visits, setVisits\] = useState<any\[\]>\(\[\]\);)", r"\1" + state_injection, content, count=1)

# Add handleOpenChat
if "const handleOpenChat" not in content:
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

# Modify handleFinishVisit
if "Fechamento Automático do Chat" not in content:
    finish_visit_logic = """
    // Fechamento Automático do Chat (Por Ação)
    try {
      await supabase.from('chat_sessions').update({ status: 'closed', closed_at: new Date().toISOString() }).eq('visit_id', visitId).eq('status', 'open');
    } catch(e) {}
"""
    content = re.sub(r"(setVisits\(visits\.map\(v => v\.id === visitId \? \{ \.\.\.v, status: 'finalizada' \} : v\)\);)", r"\1" + finish_visit_logic, content, count=1)

# Add button to the UI
if "Botão Estou a caminho / Chat" not in content:
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
    content = re.sub(r"(<button\s*onClick=\{\(e\) => \{\s*e\.stopPropagation\(\);\s*openWhatsApp[\s\S]*?</button>)", r"\1" + chat_btn, content)

# Add ChatModal at the end
if "<ChatModal" not in content:
    modal_injection = """
      <ChatModal 
        isOpen={chatModalOpen} 
        onClose={() => setChatModalOpen(false)} 
        visit={activeChatVisit} 
        client={activeChatClient} 
        waSettings={(userProfile?.whatsappSettings as any)}
      />
"""
    content = re.sub(r"(</Layout>)", modal_injection + r"\1", content)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
