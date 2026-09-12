import re

with open('src/contexts/AuthContext.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { useAutoRefresh } from '../hooks/useAutoRefresh';", "import { useRealtimeUpdates } from '../hooks/useRealtimeUpdates';")

old_refresh = """  useAutoRefresh(() => {
    if (currentUser) {
      handleUserChange(currentUser);
    }
  }, 60000); // 1 minute refresh for auth context"""

new_refresh = """  const refreshTrigger = useRealtimeUpdates(['users'], 'id', currentUser?.id);
  useEffect(() => {
    if (currentUser && refreshTrigger > 0) {
      handleUserChange(currentUser);
    }
  }, [refreshTrigger]);"""

content = content.replace(old_refresh, new_refresh)

with open('src/contexts/AuthContext.tsx', 'w') as f:
    f.write(content)
