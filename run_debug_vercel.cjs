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
                  "body": "Raio-X Vercel"
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
  path: '/api/webhook/wame?debug=1',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  }
};

const req = https.request(options, res => {
  let responseData = '';
  res.on('data', d => {
    responseData += d;
  });
  res.on('end', () => {
    console.log('--- RESPONSE LOGS ---');
    try {
       console.log(JSON.stringify(JSON.parse(responseData), null, 2));
    } catch(e) {
       console.log(responseData);
    }
  });
});

req.on('error', error => {
  console.error(error);
});

req.write(data);
req.end();
