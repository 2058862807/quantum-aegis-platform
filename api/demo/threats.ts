import type { VercelRequest, VercelResponse } from '@vercel/node'

export default function handler(req: VercelRequest, res: VercelResponse) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  if (req.method === 'OPTIONS') {
    res.status(200).end()
    return
  }

  try {
    // Pool of realistic cybersecurity threats
    const threatTypes = [
      'malware', 'phishing', 'ransomware', 'ddos', 'intrusion', 'botnet', 
      'credential_theft', 'data_exfiltration', 'zero_day', 'sql_injection'
    ]
    
    const sources = [
      'Email Gateway', 'Network Perimeter', 'Endpoint Detection', 'Web Filter',
      'DNS Monitor', 'Behavioral Analysis', 'Threat Intelligence', 'File Scanner',
      'Network Traffic', 'User Activity', 'Cloud Security', 'Mobile Security'
    ]
    
    const threatTitles = [
      'Advanced Malware Detection',
      'Suspicious Email Campaign',
      'Unusual Network Traffic',
      'Potential Data Exfiltration',
      'Unauthorized Access Attempt',
      'Crypto Mining Activity',
      'Phishing Domain Blocked',
      'Lateral Movement Detected',
      'Credential Stuffing Attack',
      'Zero-Day Exploit Attempt',
      'Backdoor Communication',
      'Suspicious File Execution',
      'Anomalous User Behavior',
      'Command & Control Traffic',
      'Privilege Escalation Attempt'
    ]
    
    const statuses = ['BLOCKED', 'INVESTIGATING', 'MITIGATED', 'QUARANTINED']
    
    // Generate 5-8 dynamic threats
    const threatCount = 5 + Math.floor(Math.random() * 4)
    const threats = []
    
    for (let i = 0; i < threatCount; i++) {
      const threat = {
        id: `threat_${Date.now()}_${i}`,
        title: threatTitles[Math.floor(Math.random() * threatTitles.length)],
        source: sources[Math.floor(Math.random() * sources.length)],
        type: threatTypes[Math.floor(Math.random() * threatTypes.length)],
        status: statuses[Math.floor(Math.random() * statuses.length)],
        timestamp: new Date(Date.now() - Math.random() * 3600000).toISOString(), // Within last hour
        severity: Math.random() > 0.7 ? 'HIGH' : Math.random() > 0.4 ? 'MEDIUM' : 'LOW',
        confidence: Math.floor(85 + Math.random() * 15) // 85-100% confidence
      }
      threats.push(threat)
    }
    
    // Sort by timestamp (newest first)
    threats.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())

    res.status(200).json(threats)
  } catch (error) {
    console.error('Error generating threats:', error)
    res.status(500).json({ error: 'Failed to generate threats' })
  }
}