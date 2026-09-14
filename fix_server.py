with open('server.ts', 'r') as f:
    content = f.read()

content = content.replace("import fs from 'fs';", "const fs = require('fs');")

with open('server.ts', 'w') as f:
    f.write(content)
