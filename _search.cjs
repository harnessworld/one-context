const http = require('http');
const PROXY_PORT = process.env.AUTH_GATEWAY_PORT || '19000';
const keyword = process.argv[2] || '大麦抢票 成功率';
const body = JSON.stringify({ keyword });
const req = http.request(
  { host: '127.0.0.1', port: Number(PROXY_PORT), path: '/proxy/prosearch/search', method: 'POST', timeout: 15000,
    headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } },
  (res) => { let data = ''; res.setEncoding('utf8'); res.on('data', c => data += c); res.on('end', () => console.log(data)); }
);
req.on('timeout', () => { req.destroy(); console.log('{"success":false,"message":"timeout"}'); });
req.on('error', e => console.log('{"success":false,"message":"' + e.message + '"}'));
req.write(body); req.end();
