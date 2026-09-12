import re

with open('src/pages/Clients.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { useAutoRefresh } from '../hooks/useAutoRefresh';", "import { useRealtimeUpdates } from '../hooks/useRealtimeUpdates';")

old_code = """  const [refreshTrigger, setRefreshTrigger] = useState(0);
  useAutoRefresh(() => setRefreshTrigger(t => t + 1), 30000); // 30s refresh"""

new_code = """  const adminId = userProfile?.role === 'admin' ? userProfile.uid : userProfile?.adminId;
  const refreshTrigger = useRealtimeUpdates(['clients'], 'admin_id', adminId);"""

content = content.replace(old_code, new_code)

# Remove the old manual channel subscriptions since useRealtimeUpdates handles it now.
old_effect = """  useEffect(() => {
    if (!userProfile?.uid) return;
    const adminId = isAdmin ? userProfile.uid : userProfile.adminId;

    const clientChannel = supabase.channel('clients-realtime-clients')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'clients', filter: `admin_id=eq.${adminId}` }, () => {
        setRefreshTrigger(t => t + 1);
      })
      .subscribe();

    const paymentChannel = supabase.channel('clients-realtime-payments')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'payments', filter: `admin_id=eq.${adminId}` }, () => {
        setRefreshTrigger(t => t + 1);
      })
      .subscribe();

    return () => {
      supabase.removeChannel(clientChannel);
      supabase.removeChannel(paymentChannel);
    };
  }, [userProfile, isAdmin, isManager, loadLimit, searchTerm, refreshTrigger]);"""

# Wait, if I look closely, the previous fetchClients useEffect doesn't have this channel creation, maybe it's a separate useEffect? Let's check Clients.tsx.

with open('src/pages/Clients.tsx', 'w') as f:
    f.write(content)
