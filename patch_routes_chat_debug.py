import re

with open('src/pages/RoutesPage.tsx', 'r') as f:
    content = f.read()

handle_open_old = """  const handleOpenChat = async (client: any, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();"""

handle_open_new = """  const handleOpenChat = async (client: any, e?: React.MouseEvent) => {
    if (e) {
      e.stopPropagation();
      e.preventDefault();
    }
    console.log("Chat button clicked for client:", client?.id);"""

content = content.replace(handle_open_old, handle_open_new)

with open('src/pages/RoutesPage.tsx', 'w') as f:
    f.write(content)
