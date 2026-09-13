import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# Add button near MapPin
btn_regex = r"(<MapPin size=\{20\} />\s*</button>)"
chat_btn = """<MapPin size={20} />
                          </button>
                          
                          {/* Botão Estou a caminho / Chat */}
                          <button
                            onClick={(e) => handleOpenChat(client, e)}
                            className="p-1 text-blue-600 hover:bg-blue-100 rounded-md transition-colors"
                            title="Avisar chegada / Chat"
                          >
                            <MessageCircle size={20} />
                          </button>"""

content = re.sub(btn_regex, chat_btn, content)

# I also need to change handleOpenChat to take `client` instead of `visit`, because visits don't exist yet!
# The user wants to start the chat from the client card.
handle_open_old = """  const handleOpenChat = (visit: any, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    const client = clients.find(c => c.id === visit.client_id);
    if (!client) return;
    setActiveChatVisit(visit);
    setActiveChatClient(client);
    setChatModalOpen(true);
  };"""

handle_open_new = """  const handleOpenChat = async (client: any, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    
    // We need a visit_id to associate with the chat session, even if not finalized.
    // Let's create an "iniciada" visit if one doesn't exist for today, just to hold the chat session.
    let visitId = null;
    const adminId = isAdmin ? userProfile.uid : userProfile.adminId;
    
    try {
      const { data: existingVisit } = await supabase.from('visits')
        .select('id')
        .eq('client_id', client.id)
        .eq('date', routeDate)
        .limit(1);
        
      if (existingVisit && existingVisit.length > 0) {
         visitId = existingVisit[0].id;
      } else {
         const { data: newVisit } = await supabase.from('visits').insert({
           admin_id: adminId,
           client_id: client.id,
           employee_id: selectedEmployee || userProfile.uid,
           date: routeDate,
           status: 'agendada'
         }).select('id').single();
         if (newVisit) visitId = newVisit.id;
      }
    } catch(err) {
      console.error(err);
    }

    setActiveChatVisit({ id: visitId });
    setActiveChatClient(client);
    setChatModalOpen(true);
  };"""

content = content.replace(handle_open_old, handle_open_new)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
