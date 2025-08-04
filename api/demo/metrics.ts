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
    // Generate realistic dynamic metrics with some variation
    const now = Date.now()
    const hourOfDay = new Date().getHours()
    
    // Base metrics with realistic cybersecurity numbers
    const baseThreats = 2500 + (hourOfDay * 50) // More threats during business hours
    const threatsVariation = Math.sin(now / 60000) * 200 // ±200 variation every minute
    const threatsBlocked = Math.floor(baseThreats + threatsVariation + Math.random() * 100)
    
    // Mean Time to Detect (lower is better)
    const baseMTTD = 1.1 + (Math.random() * 0.4) // 1.1-1.5 seconds base
    const mttd = Math.round(baseMTTD * 10) / 10 // Round to 1 decimal
    
    // AI Confidence (should be high and stable)
    const baseConfidence = 97.2 + (Math.random() * 1.2) // 97.2-98.4%
    const aiConfidence = Math.round(baseConfidence * 10) / 10
    
    // Quantum Keys (cycling between 40-55)
    const baseKeys = 45 + Math.sin(now / 30000) * 5 // Slow oscillation
    const quantumKeys = Math.floor(baseKeys + Math.random() * 3)

    const metrics = {
      threatsBlocked,
      mttd,
      aiConfidence,
      quantumKeys,
      timestamp: now,
      trends: {
        threatsChange: '+12%',
        mttdChange: '-0.3s',
        confidenceChange: '+2.1%',
        keysStatus: 'rotating'
      }
    }

    res.status(200).json(metrics)
  } catch (error) {
    console.error('Error generating metrics:', error)
    res.status(500).json({ error: 'Failed to generate metrics' })
  }
}