with open('src/lib/whatsapp.ts', 'r') as f:
    content = f.read()

new_fn = """export const normalizePhoneNumber = (phone: string): string => {
  if (!phone) return '';
  
  // 1. Remove all non-numeric characters
  let cleanPhone = phone.replace(/\D/g, '');
  if (!cleanPhone) return '';

  // 2. If number is local without DDI (10 or 11 digits), prepend 55 (Brazil)
  if (cleanPhone.length === 10 || cleanPhone.length === 11) {
    cleanPhone = `55${cleanPhone}`;
  }
  
  // 3. Handle Brazilian numbers (start with 55)
  if (cleanPhone.startsWith('55')) {
    // If it has 12 digits (55 + 2 DDD + 8 digit number)
    if (cleanPhone.length === 12) {
      const ddd = cleanPhone.substring(2, 4);
      const number = cleanPhone.substring(4);
      // Only add 9 if it looks like a mobile (starts with 6, 7, 8, 9)
      if (['6', '7', '8', '9'].includes(number[0])) {
         return `55${ddd}9${number}`;
      }
    }
  }

  return cleanPhone;
};
"""

with open('src/lib/whatsapp.ts', 'w') as f:
    f.write(new_fn + "\n" + content)
