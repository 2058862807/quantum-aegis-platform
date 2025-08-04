const http = require('http');
const path = require('path');
const fs = require('fs');

// Import our API handlers
const metricsHandler = require('./api/demo/metrics.ts');
const threatsHandler = require('./api/demo/threats.ts');

const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);
    
    if (req.url === '/api/demo/metrics') {
        // Call our metrics handler
        const mockReq = { method: req.method, query: {} };
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
        
        try {
            // Test the metrics endpoint directly
            const now = Date.now();
            const hourOfDay = new Date().getHours();
            
            const baseThreats = 2500 + (hourOfDay * 50);
            const threatsVariation = Math.sin(now / 60000) * 200;
            const threatsBlocked = Math.floor(baseThreats + threatsVariation + Math.random() * 100);
            
            const baseMTTD = 1.1 + (Math.random() * 0.4);
            const mttd = Math.round(baseMTTD * 10) / 10;
            
            const baseConfidence = 97.2 + (Math.random() * 1.2);
            const aiConfidence = Math.round(baseConfidence * 10) / 10;
            
            const baseKeys = 45 + Math.sin(now / 30000) * 5;
            const quantumKeys = Math.floor(baseKeys + Math.random() * 3);

            const metrics = {
                threatsBlocked,
                mttd,
                aiConfidence,
                quantumKeys,
                timestamp: now
            };

            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.end(JSON.stringify(metrics));
        } catch (error) {
            res.statusCode = 500;
            res.end(JSON.stringify({ error: 'Failed to generate metrics' }));
        }
        return;
    }
    
    if (req.url === '/api/demo/threats') {
        try {
            const threatTitles = [
                'Advanced Malware Detection',
                'Suspicious Email Campaign', 
                'Unusual Network Traffic',
                'Potential Data Exfiltration',
                'Unauthorized Access Attempt'
            ];
            
            const sources = ['Email Gateway', 'Network Perimeter', 'Endpoint Detection', 'Web Filter'];
            const threatTypes = ['malware', 'phishing', 'ddos', 'intrusion'];
            const statuses = ['BLOCKED', 'INVESTIGATING', 'MITIGATED'];
            
            const threats = [];
            for (let i = 0; i < 5; i++) {
                threats.push({
                    title: threatTitles[Math.floor(Math.random() * threatTitles.length)],
                    source: sources[Math.floor(Math.random() * sources.length)], 
                    type: threatTypes[Math.floor(Math.random() * threatTypes.length)],
                    status: statuses[Math.floor(Math.random() * statuses.length)]
                });
            }

            res.setHeader('Content-Type', 'application/json');
            res.setHeader('Access-Control-Allow-Origin', '*');
            res.end(JSON.stringify(threats));
        } catch (error) {
            res.statusCode = 500;
            res.end(JSON.stringify({ error: 'Failed to generate threats' }));
        }
        return;
    }
    
    // Serve static files
    if (req.url === '/' || req.url === '/index.html') {
        fs.readFile('./index.html', (err, data) => {
            if (err) {
                res.statusCode = 404;
                res.end('File not found');
                return;
            }
            res.setHeader('Content-Type', 'text/html');
            res.end(data);
        });
        return;
    }
    
    res.statusCode = 404;
    res.end('Not found');
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});