const http = require('http');
const https = require('https');

const data = JSON.stringify({
  "object": "wame",
  "entry": [
    {
      "id": "wame.eW91ci1pbnN0YW5jZS1pZA",
      "changes": [
        {
          "field": "messages",
          "value": {
            "messages": [
              {
                "from": "5567991907236",
                "type": "text",
                "text": {
                  "body": "Teste interno log PÚBLICO!"
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
  hostname: 'ais-pre-lafhr3cxydhbm5z265hztr-86812857430.us-east1.run.app',
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
  res.on('data', d => {
    process.stdout.write(d);
  });
});

req.on('error', error => {
  console.error(error);
});

req.write(data);
req.end();
