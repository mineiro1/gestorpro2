with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

modal_injection = """
      <ChatModal 
        isOpen={chatModalOpen} 
        onClose={() => setChatModalOpen(false)} 
        visit={activeChatVisit} 
        client={activeChatClient} 
        waSettings={(userProfile?.whatsappSettings as any)}
      />
"""

# Find the last occurrence of '  );'
idx = content.rfind('  );')
if idx != -1:
    # insert before the last '  );' but specifically before the last '    </div>'
    idx2 = content.rfind('    </div>', 0, idx)
    if idx2 != -1:
        content = content[:idx2] + modal_injection + content[idx2:]

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
