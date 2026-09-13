const url = 'https://www.rspiscinas.app.br/api/webhook/evolution';

const mockEvolutionPayload = {
  data: {
    key: {
      remoteJid: '5511999999999@s.whatsapp.net',
      fromMe: false,
      id: 'mock_message_id_123'
    },
    message: {
      conversation: 'Teste manual disparado do servidor para verificar se o Webhook da Vercel está vivo!'
    }
  }
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(mockEvolutionPayload)
})
.then(res => {
   console.log('Status HTTP:', res.status);
   return res.text();
})
.then(text => console.log('Resposta do Webhook:', text))
.catch(err => console.error('Erro ao chamar Webhook:', err));
