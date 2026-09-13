import re

with open('src/pages/ClientForm.tsx', 'r') as f:
    content = f.read()

# Using regex is safer for spacing
content = re.sub(r"phone: '',\s+address:", r"phone: '',\n    localPhone: '',\n    address:", content)
content = re.sub(r"phone: data\.phone \|\| '',\s+address:", r"phone: data.phone || '',\n              localPhone: data.local_phone || '',\n              address:", content)
content = re.sub(r"phone: formData\.phone,\s+address:", r"phone: formData.phone,\n      local_phone: formData.localPhone,\n      address:", content)

input_jsx = r"""            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contato no Local (Opcional - Caseiro/Portaria)
              </label>
              <input
                type="tel"
                value={formData.localPhone}
                onChange={e => setFormData({...formData, localPhone: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary outline-none"
              />
            </div>

            <div>"""
content = re.sub(r"            </div>\s+<div>", input_jsx, content, count=1)

with open('src/pages/ClientForm.tsx', 'w') as f:
    f.write(content)
