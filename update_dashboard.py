import re

with open('src/pages/Dashboard.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { useAutoRefresh } from '../hooks/useAutoRefresh';", "import { useRealtimeUpdates } from '../hooks/useRealtimeUpdates';")

old_code = """  const [refreshTrigger, setRefreshTrigger] = useState(0);
  useAutoRefresh(() => setRefreshTrigger(t => t + 1), 30000); // 30s refresh"""

new_code = """  const adminId = userProfile?.role === 'admin' ? userProfile.uid : userProfile?.adminId;
  const refreshTrigger = useRealtimeUpdates(['clients', 'visits', 'oneoffjobs', 'payments'], 'admin_id', adminId);"""

content = content.replace(old_code, new_code)

with open('src/pages/Dashboard.tsx', 'w') as f:
    f.write(content)
