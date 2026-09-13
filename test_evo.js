import fetch from 'node-fetch';

async function test() {
  const url = "https://pool-evolution-api-018.cloud.pageup.dev.br/message/sendText/gestorpro";
  const apiKey = "ef42eadca2ba52dd70ba5a721c32affd";
  
  // just check instance status to not send a fake message
  const statusUrl = "https://pool-evolution-api-018.cloud.pageup.dev.br/instance/connectionState/gestorpro";
  try {
    const res = await fetch(statusUrl, {
      headers: {
        'apikey': apiKey
      }
    });
    console.log(res.status);
    const data = await res.json();
    console.log(data);
  } catch (e) {
    console.error(e);
  }
}
test();
