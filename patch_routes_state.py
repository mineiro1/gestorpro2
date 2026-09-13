import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

state_injection = """  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [activeChatVisit, setActiveChatVisit] = useState<any>(null);
  const [activeChatClient, setActiveChatClient] = useState<any>(null);
"""
content = re.sub(r"(const \[generated, setGenerated\] = useState\(false\);)", r"\1\n" + state_injection, content, count=1)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
