const https = require('https');

const data = JSON.stringify({
  "object": "wame",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messages": [
              {
                "from": "5567991907236",
                "type": "text",
                "text": {
                  "body": "Teste 1000 - Vercel Serverless"
                }
              }
            ]
          }
        }
      ]
    }
  ]
});

const options = {
  hostname: 'www.rspiscinas.app.br',
  port: 443,
  path: '/api/webhook/wame',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, res => {
  console.log(`statusCode: ${res.statusCode}`);
  let responseData = '';
  res.on('data', d => {
    responseData += d;
  });
  res.on('end', () => {
    console.log('Response body:', responseData);
  });
});

req.on('error', error => {
  console.error(error);
});

req.write(data);
req.end();
