import fetch from 'node-fetch';

async function test() {
  const url = "https://pool-evolution-api-018.cloud.pageup.dev.br/message/sendText/gestorpro";
  const apiKey = "ef42eadca2ba52dd70ba5a721c32affd";
  
  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'apikey': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        number: "5511999999999",
        text: "Teste",
        textMessage: { text: "Teste" },
        options: { delay: 1000, presence: "composing" }
      })
    });
    console.log(res.status);
    const data = await res.json();
    console.log(data);
  } catch (e) {
    console.error(e);
  }
}
test();
