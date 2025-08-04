const http = require('http');
const fs = require('fs');
const path = require('path');

// Mock Vercel request/response for local testing
function createMockVercelHandler(filePath) {
  return async (req, res) => {
    try {
      // Clear module cache to allow reloading
      delete require.cache[require.resolve(filePath)];
      
      const handler = require(filePath).default;
      
      const mockReq = {
        ...req,
        query: {},
        body: {}
      };
      
      const mockRes = {
        setHeader: (key, value) => res.setHeader(key, value),
        status: (code) => ({
          json: (data) => {
            res.statusCode = code;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(data));
          },
          end: () => {
            res.statusCode = code;
            res.end();
          }
        }),
        json: (data) => {
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify(data));
        }
      };
      
      await handler(mockReq, mockRes);
    } catch (error) {
      console.error('Handler error:', error);
      res.statusCode = 500;
      res.setHeader('Content-Type', 'application/json');
      res.end(JSON.stringify({ error: 'Internal server error', details: error.message }));
    }
  };
}

const server = http.createServer(async (req, res) => {
    console.log(`${req.method} ${req.url}`);
    
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle OPTIONS requests
    if (req.method === 'OPTIONS') {
        res.statusCode = 200;
        res.end();
        return;
    }
    
    // Route to TypeScript API endpoints
    if (req.url === '/api/demo/metrics') {
        const handler = createMockVercelHandler('./api/demo/metrics.js');
        await handler(req, res);
        return;
    }
    
    if (req.url === '/api/demo/threats') {
        const handler = createMockVercelHandler('./api/demo/threats.js');
        await handler(req, res);
        return;
    }
    
    // Serve the main HTML page
    if (req.url === '/' || req.url === '/index.html') {
        try {
            const data = fs.readFileSync('./index.html');
            res.setHeader('Content-Type', 'text/html');
            res.end(data);
        } catch (err) {
            res.statusCode = 404;
            res.end('File not found');
        }
        return;
    }
    
    res.statusCode = 404;
    res.end('Not found');
});

const PORT = 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 VirusTotal-powered Quantum Aegis server running at http://localhost:${PORT}/`);
    console.log('📡 Real-time threat intelligence endpoints:');
    console.log('- GET /api/demo/metrics - Live security metrics from VirusTotal');
    console.log('- GET /api/demo/threats - Real threat intelligence feed');
    console.log('🔗 VirusTotal API integration active!');
});