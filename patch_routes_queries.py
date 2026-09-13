import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

# Change .select('client_id') to .select('client_id, status') in the 3 queries
content = content.replace(".select('client_id')", ".select('client_id, status')")

# Change the forEach loop to filter out 'agendada'
loop_old = """      if (visitsSnap) {
        visitsSnap.forEach(data => {
            completedIds.add(data.client_id);
        });
      }"""

loop_new = """      if (visitsSnap) {
        visitsSnap.forEach(data => {
            if (data.status !== 'agendada') {
               completedIds.add(data.client_id);
            }
        });
      }"""
content = content.replace(loop_old, loop_new)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
