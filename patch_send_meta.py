import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    old_code = """    const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
    const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
    const url = `${baseUrl}${phoneId}/messages`;
    
    let response;
    try {
      response = await fetch(url, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${waSettings.metaToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          messaging_product: "whatsapp",
          recipient_type: "individual",
          to: number,
          type: "text",
          text: { 
            preview_url: false,
            body: text
          }
        })
      });"""
      
    new_code = """    const baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').replace(/\\/$/, '');
    const isWame = baseUrl.includes('api-wa.me') || baseUrl.includes('wame.api.br');
    
    let url, headers, body;
    
    if (isWame) {
       url = `${baseUrl}/${waSettings.metaToken}/message/text`;
       headers = { 'Content-Type': 'application/json' };
       body = JSON.stringify({ to: number, text: text });
    } else {
       const phoneId = waSettings.metaPhoneNumberId ? `/${waSettings.metaPhoneNumberId}` : '';
       url = `${baseUrl}${phoneId}/messages`;
       headers = {
          'Authorization': `Bearer ${waSettings.metaToken}`,
          'Content-Type': 'application/json'
       };
       body = JSON.stringify({
          messaging_product: "whatsapp",
          recipient_type: "individual",
          to: number,
          type: "text",
          text: { preview_url: false, body: text }
       });
    }
    
    let response;
    try {
      response = await fetch(url, { method: 'POST', headers, body });"""
      
    content = content.replace(old_code, new_code)
    with open(filename, 'w') as f:
        f.write(content)

update_file('src/pages/Billing.tsx')
update_file('src/pages/Messages.tsx')
