'use client'

import { useEffect, useState } from 'react'

interface Star {
  id: number
  left: number
  top: number
  delay: number
  size: 'small' | 'medium' | 'large'
}

export default function AnimatedStars() {
  const [stars, setStars] = useState<Star[]>([])

  useEffect(() => {
    // Generate stars only on client side to avoid hydration mismatch
    const generatedStars: Star[] = Array.from({ length: 40 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      delay: Math.random() * 3,
      size: i % 3 === 0 ? 'small' : i % 3 === 1 ? 'medium' : 'large'
    }))
    
    setStars(generatedStars)
  }, [])

  if (stars.length === 0) {
    // Return null during SSR to avoid hydration mismatch
    return null
  }

  return (
    <div className="absolute inset-0 overflow-hidden">
      {stars.map((star) => (
        <div
          key={star.id}
          className={`absolute bg-white rounded-full ${
            star.size === 'small'
              ? "star-twinkle-1 w-0.5 h-0.5"
              : star.size === 'medium'
                ? "star-twinkle-2 w-0.5 h-0.5"
                : "star-twinkle-3 w-1 h-1"
          }`}
          style={{
            left: `${star.left}%`,
            top: `${star.top}%`,
            animationDelay: `${star.delay}s`,
          }}
        />
      ))}

      {/* Animated Shooting Stars */}
      <div className="shooting-star shooting-star-1"></div>
      <div className="shooting-star shooting-star-2"></div>

      {/* Mountain Silhouette */}
      <div className="mountain-silhouette"></div>
    </div>
  )
}
