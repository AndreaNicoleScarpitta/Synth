import { useEffect, useRef } from 'react'

export function MatrixBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const resizeCanvas = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    resizeCanvas()
    window.addEventListener('resize', resizeCanvas)

    // Matrix characters
    const characters = '01ATCGACGTACGTACG'
    const fontSize = 14
    const columns = Math.floor(canvas.width / fontSize)
    
    // Array to store y position of each column
    const drops: number[] = new Array(columns).fill(1)

    const draw = () => {
      // Black background with slight transparency for trailing effect
      ctx.fillStyle = 'rgba(0, 0, 0, 0.05)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Gold text
      ctx.fillStyle = '#fbbf24'
      ctx.font = `${fontSize}px monospace`

      // Draw characters
      for (let i = 0; i < drops.length; i++) {
        const text = characters[Math.floor(Math.random() * characters.length)]
        const x = i * fontSize
        const y = drops[i] * fontSize

        // Add some randomness to the gold color intensity
        const opacity = Math.random() * 0.5 + 0.5
        ctx.fillStyle = `rgba(251, 191, 36, ${opacity})`
        ctx.fillText(text, x, y)

        // Reset drop to top randomly
        if (y > canvas.height && Math.random() > 0.975) {
          drops[i] = 0
        }

        drops[i]++
      }
    }

    const interval = setInterval(draw, 50)

    return () => {
      clearInterval(interval)
      window.removeEventListener('resize', resizeCanvas)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 -z-10 opacity-20"
      style={{ pointerEvents: 'none' }}
    />
  )
}