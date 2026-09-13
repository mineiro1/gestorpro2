import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# Add handleOpenChat
handle_open_new = """  const handleOpenChat = async (client: any, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    
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
  };
"""

content = re.sub(r"(const handleOpenReport = \(client: any\) => \{)", handle_open_new + r"\n  \1", content, count=1)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
