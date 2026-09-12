import re

with open('src/pages/Agenda.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { useAutoRefresh } from '../hooks/useAutoRefresh';", "import { useRealtimeUpdates } from '../hooks/useRealtimeUpdates';")

old_code = """  const [refreshTrigger, setRefreshTrigger] = useState(0);
  useAutoRefresh(() => setRefreshTrigger(t => t + 1), 30000);"""

new_code = """  const adminId = userProfile?.role === 'admin' ? userProfile.uid : userProfile?.adminId;
  const refreshTrigger = useRealtimeUpdates(['agenda_contacts'], 'admin_id', adminId);"""

content = content.replace(old_code, new_code)

# Check if useState is no longer needed for refreshTrigger (it's returned by the hook now).
with open('src/pages/Agenda.tsx', 'w') as f:
    f.write(content)
