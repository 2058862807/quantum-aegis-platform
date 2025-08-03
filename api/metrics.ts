typescriptimport type { VercelRequest, VercelResponse } from '@vercel/node'

export default function handler(req: VercelRequest, res: VercelResponse) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')

  if (req.method === 'OPTIONS') {
    return res.status(200).end()
  }

  // Generate realistic but dynamic metrics
  const baseTime = Date.now()
  const dayOffset = Math.floor(baseTime / (1000 * 60 * 60 * 24))
  
  // Use deterministic randomness based on current day
  const seed = dayOffset % 1000
  const random = (seed * 9301 + 49297) % 233280
  
  const threatsBlocked = 298000 + (random % 5000)
  const mttd = (1.0 + (random % 100) / 1000).toFixed(1)
  const aiConfidence = (97.0 + (random % 300) / 100).toFixed(1)
  const quantumKeys = 45 + (random % 8)

  const metrics = {
    threatsBlocked,
    mttd: parseFloat(mttd),
    aiConfidence: parseFloat(aiConfidence),
    quantumKeys,
    timestamp: new Date().toISOString()
  }

  return res.json(metrics)
}
