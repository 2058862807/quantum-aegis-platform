// Simple test to verify our API endpoints work
const http = require('http');

const server = http.createServer((req, res) => {
    console.log(`${req.method} ${req.url}`);
    
    // Set CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json');
    
    if (req.url === '/api/demo/metrics') {
        // Generate realistic dynamic metrics
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

        res.end(JSON.stringify(metrics));
        return;
    }
    
    if (req.url === '/api/demo/threats') {
        const threatTitles = [
            'Advanced Malware Detection',
            'Suspicious Email Campaign', 
            'Unusual Network Traffic',
            'Potential Data Exfiltration',
            'Unauthorized Access Attempt',
            'Crypto Mining Activity',
            'Phishing Domain Blocked'
        ];
        
        const sources = [
            'Email Gateway', 'Network Perimeter', 'Endpoint Detection', 
            'Web Filter', 'DNS Monitor', 'Behavioral Analysis'
        ];
        
        const threatTypes = ['malware', 'phishing', 'ddos', 'intrusion', 'botnet'];
        const statuses = ['BLOCKED', 'INVESTIGATING', 'MITIGATED', 'QUARANTINED'];
        
        const threats = [];
        const threatCount = 5 + Math.floor(Math.random() * 4);
        
        for (let i = 0; i < threatCount; i++) {
            threats.push({
                title: threatTitles[Math.floor(Math.random() * threatTitles.length)],
                source: sources[Math.floor(Math.random() * sources.length)], 
                type: threatTypes[Math.floor(Math.random() * threatTypes.length)],
                status: statuses[Math.floor(Math.random() * statuses.length)],
                timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString()
            });
        }

        res.end(JSON.stringify(threats));
        return;
    }
    
    // Serve the main HTML page
    if (req.url === '/' || req.url === '/index.html') {
        const fs = require('fs');
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
server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    console.log('API endpoints:');
    console.log('- GET /api/demo/metrics');
    console.log('- GET /api/demo/threats');
});