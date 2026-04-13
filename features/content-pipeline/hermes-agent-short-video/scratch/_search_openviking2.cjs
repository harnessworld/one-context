const http = require('http');
const PROXY_PORT = process.env.AUTH_GATEWAY_PORT || '19000';
const API_PATH = '/proxy/prosearch/search';

const payload = JSON.stringify({ keyword: 'OpenViking github repository 架构 文件系统', cnt: 8 });

const options = {
  hostname: '127.0.0.1', port: PROXY_PORT, path: API_PATH, method: 'POST',
  headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
};
const req = http.request(options, res => {
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const parsed = JSON.parse(data);
    if (parsed.success) console.log(parsed.message);
    else console.log('失败:', parsed.message);
  });
});
req.on('error', e => console.error('网络错误:', e.message));
req.write(payload);
req.end();
