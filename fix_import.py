with open('server.ts', 'r') as f:
    content = f.read()
content = content.replace("const fs = require('fs');", "import * as fs from 'fs';")
with open('server.ts', 'w') as f:
    f.write(content)
