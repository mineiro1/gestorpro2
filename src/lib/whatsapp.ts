export const openWhatsApp = (phone: string, message: string = '') => {
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const cleanPhone = phone.replace(/\D/g, '');
  const encodedMessage = encodeURIComponent(message);
  
  if (isMobile) {
    const schemeUrl = `whatsapp://send?phone=${cleanPhone}&text=${encodedMessage}`;
    window.location.href = schemeUrl;
    setTimeout(() => {
    }, 300);
  } else {
    const webUrl = `https://wa.me/${cleanPhone}?text=${encodedMessage}`;
    window.open(webUrl, '_blank');
  }
};

export const sendEvolutionMessage = async (phone: string, text: string, waSettings: any) => {
  if (!waSettings.evolutionApiUrl || !waSettings.evolutionApiKey || !waSettings.evolutionInstanceName) {
    throw new Error("Credenciais da Evolution API incompletas nas configurações.");
  }
  
  const cleanPhone = phone.replace(/\D/g, '');
  const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
  
  let baseUrl = waSettings.evolutionApiUrl.trim().replace(/\/$/, '');
  if (baseUrl && !baseUrl.startsWith('http')) {
    baseUrl = 'https://' + baseUrl;
  }
  const url = `${baseUrl}/message/sendText/${waSettings.evolutionInstanceName}`;
  
  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'apikey': waSettings.evolutionApiKey
      },
      body: JSON.stringify({
        number: number,
        text: text,
        textMessage: {
          text: text
        },
        options: {
          delay: 1000,
          presence: "composing"
        }
      })
    });
  } catch (e: any) {
    if (e.message === 'Failed to fetch') {
      throw new Error(`Falha de conexão. Verifique se o seu servidor Evolution API (${baseUrl}) possui o CORS habilitado. O navegador bloqueou a requisição (Failed to fetch).`);
    }
    throw e;
  }
  
  if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = JSON.stringify(errData);
    } catch(e) {}
    throw new Error(`Erro na Evolution API (${response.status}): ${errDesc}`);
  }
  return await response.json();
};

export const sendMetaMessage = async (phone: string, text: string, waSettings: any) => {
  console.log("SEND META MESSAGE CALLED");
  console.log("Phone:", phone);
  console.log("Base URL raw:", waSettings.metaServerUrl);
  console.log("Token:", waSettings.metaToken);
  if (!waSettings.metaToken) {
    throw new Error("O Token/Key da API Oficial (Meta) é obrigatório.");
  }
  
  const cleanPhone = phone.replace(/\D/g, '');
  const number = cleanPhone.startsWith('55') ? cleanPhone : `55${cleanPhone}`;
  
  let baseUrl = (waSettings.metaServerUrl || 'https://graph.facebook.com/v19.0').trim().replace(/\/$/, '');
  if (baseUrl && !baseUrl.startsWith('http')) {
    baseUrl = 'https://' + baseUrl;
  }
  const isWame = baseUrl && !baseUrl.includes('graph.facebook.com');
  
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
    response = await fetch(url, { method: 'POST', headers, body });
  } catch (e: any) {
    if (e.message === 'Failed to fetch') {
      throw new Error('Falha de conexão com a API da Meta. (Failed to fetch)');
    }
    throw e;
  }
  
  if (!response.ok) {
    let errDesc = 'Desconhecido';
    try {
      const errData = await response.json();
      errDesc = errData.message || errData.error?.message || JSON.stringify(errData);
    } catch(e) {}
    
    if (response.status === 409 || errDesc.includes('24h') || errDesc.includes('Janela')) {
        throw new Error("Janela de 24h fechada. A Meta (WhatsApp) bloqueou esta mensagem. Para iniciar a conversa, o cliente deve te enviar uma mensagem primeiro ou você deve usar Templates aprovados.");
    }
    
    throw new Error(`Erro na API WAME/Meta (${response.status}): ${errDesc}`);
  }
  return await response.json();
};
