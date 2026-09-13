import re

with open('src/components/ChatModal.tsx', 'r') as f:
    content = f.read()

old_effect = """  useEffect(() => {
    if (isOpen && visit) {
      loadOrCreateSession();
    }
  }, [isOpen, visit]);"""

new_effect = """  useEffect(() => {
    if (isOpen && visit && visit.id) {
      loadOrCreateSession();
    } else if (isOpen && visit && !visit.id) {
      // Waiting for visitId to be resolved
      setLoading(true);
    }
  }, [isOpen, visit]);"""

content = content.replace(old_effect, new_effect)

with open('src/components/ChatModal.tsx', 'w') as f:
    f.write(content)
