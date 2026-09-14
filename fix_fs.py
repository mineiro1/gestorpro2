with open('server.ts', 'r') as f:
    content = f.read()

content = content.replace("import * as fs from 'fs';", "")
content = "import fs from 'fs';\n" + content

with open('server.ts', 'w') as f:
    f.write(content)
