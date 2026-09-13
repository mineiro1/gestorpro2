import fetch from 'node-fetch';

async function test() {
  const url = "https://us.api-wa.me";
  try {
    const res = await fetch(url);
    console.log(res.status);
  } catch (e) {
    console.error(e);
  }
}
test();
