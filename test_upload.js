const https = require('https');

const data = Buffer.alloc(10 * 1024 * 1024, 'a');
const startTime = Date.now();

const req = https.request('https://speed.cloudflare.com/__up', {
    method: 'POST',
    headers: { 'Content-Length': data.length }
}, (res) => {
    console.log(`Status: ${res.statusCode}`);
    console.log(`Time: ${(Date.now() - startTime)} ms`);
});

req.write(data);
req.end();
