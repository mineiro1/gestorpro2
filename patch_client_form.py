import re

with open('src/pages/ClientForm.tsx', 'r') as f:
    content = f.read()

# 1. Add local_phone to the formData state
state_match = r"(const\s+\[formData,\s+setFormData\]\s*=\s*useState<any>\(\{[\s\S]*?)(\}\);)"
content = re.sub(state_match, r"\1  local_phone: '',\n\2", content, count=1)

# 2. Add local_phone mapping in useEffect
effect_match = r"(setFormData\(\{[\s\S]*?)(payment_status:)"
content = re.sub(effect_match, r"\1local_phone: client.local_phone || '',\n      \2", content, count=1)

# 3. Add the input field in the JSX
input_jsx = """          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Contato no Local (Para Visitas - Opcional)
            </label>
            <input
              type="text"
              name="local_phone"
              value={formData.local_phone}
              onChange={handleChange}
              placeholder="Ex: Caseiro, Portaria"
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>"""

# Insert after phone field
phone_jsx_match = r"(<input[^>]*name=\"phone\"[^>]*>[\s\S]*?</div>)"
content = re.sub(phone_jsx_match, r"\1\n" + input_jsx, content, count=1)

with open('src/pages/ClientForm.tsx', 'w') as f:
    f.write(content)
