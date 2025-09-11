"use client"

import type React from "react"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Send } from "lucide-react"
import AnimatedStars from "@/components/AnimatedStars"

interface Message {
  id: string
  text: string
  sender: "user" | "amma"
  timestamp: Date
}

export default function AmmaChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const [sessionId] = useState(() => `session_${Math.random().toString(36).substr(2, 9)}_${Date.now()}`)
  const [isConnected, setIsConnected] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const streamingMessageRef = useRef("")

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      try {
        // Use environment variable or detect Railway deployment
        const isRailway = window.location.hostname.includes('railway.app')
        const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 
                     (isRailway ? `wss://${window.location.hostname}:${parseInt(window.location.port || '3000') + 1}` : 'ws://localhost:8001')
        const ws = new WebSocket(`${wsUrl}/ws/${sessionId}`)
        wsRef.current = ws

        ws.onopen = () => {
          console.log('🌟 Connected to AMMA')
          setIsConnected(true)
          // Backend will automatically send greeting - no need to send "hey"
        }

        ws.onmessage = (event) => {
          const data = JSON.parse(event.data)
          
          if (data.type === 'response') {
            // Handle regular non-streaming response (fallback)
            const ammaResponse: Message = {
              id: Date.now().toString(),
              text: data.content,
              sender: "amma",
              timestamp: new Date(),
            }
            setMessages((prev) => [...prev, ammaResponse])
            setIsTyping(false)
            setIsStreaming(false)
          } else if (data.type === 'stream_start') {
            // Start streaming - clear current message and set streaming state
            streamingMessageRef.current = ""
            setCurrentStreamingMessage("")
            setIsStreaming(true)
            setIsTyping(false)
          } else if (data.type === 'stream_chunk') {
            // Add character to current streaming message
            streamingMessageRef.current += data.content
            setCurrentStreamingMessage(streamingMessageRef.current)
          } else if (data.type === 'stream_end') {
            // End streaming - add final message to messages array
            const finalMessage: Message = {
              id: Date.now().toString(),
              text: streamingMessageRef.current,
              sender: "amma",
              timestamp: new Date(),
            }
            setMessages((prev) => [...prev, finalMessage])
            streamingMessageRef.current = ""
            setCurrentStreamingMessage("")
            setIsStreaming(false)
          } else if (data.type === 'typing') {
            setIsTyping(true)
          } else if (data.type === 'error') {
            console.error('❌ AMMA Error:', data.content)
            const errorResponse: Message = {
              id: Date.now().toString(),
              text: "I'm sorry, dear one. Something went wrong. Please try again.",
              sender: "amma",
              timestamp: new Date(),
            }
            setMessages((prev) => [...prev, errorResponse])
            setIsTyping(false)
            setIsStreaming(false)
          }
        }

        ws.onclose = () => {
          console.log('🔌 Disconnected from AMMA - reconnecting...')
          setIsConnected(false)
          setIsStreaming(false)
          setIsTyping(false)
          // Attempt to reconnect after 3 seconds
          setTimeout(connectWebSocket, 3000)
        }

        ws.onerror = (error) => {
          console.error('❌ WebSocket error:', error)
          setIsConnected(false)
        }
      } catch (error) {
        console.error('Failed to connect WebSocket:', error)
        setIsConnected(false)
      }
    }

    connectWebSocket()

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [sessionId])

  // Remove hardcoded welcome message - AMMA will introduce herself via WebSocket

  const handleSendMessage = async () => {
    if (!inputValue.trim() || !isConnected) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const messageText = inputValue
    setInputValue("")
    setIsTyping(true)

    try {
      // Send message via WebSocket for streaming response
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          message: messageText
        }))
      } else {
        // Fallback to REST API if WebSocket is not available
        const isRailway = window.location.hostname.includes('railway.app')
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 
                      (isRailway ? `https://${window.location.hostname}:${parseInt(window.location.port || '3000') + 1}` : 'http://localhost:8001')
        const response = await fetch(`${apiUrl}/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: messageText,
            session_id: sessionId
          })
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        
        const ammaResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response,
          sender: "amma",
          timestamp: new Date(),
        }
        
        setMessages((prev) => [...prev, ammaResponse])
        setIsTyping(false)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: "I'm sorry, dear one. I'm having trouble connecting right now. Please try again in a moment.",
        sender: "amma",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorResponse])
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !isStreaming && !isTyping && isConnected && inputValue.trim()) {
      handleSendMessage()
    }
  }

  return (
    <div className="min-h-screen cosmic-background relative overflow-hidden">
      {/* Enhanced Cosmic Background Elements */}
      <AnimatedStars />

      {/* Main Chat Container */}
      <div className="relative z-10 flex flex-col h-screen">
        <header className="p-8 text-center">
          <div className="inline-block px-6 py-4 rounded-2xl bg-black/20 backdrop-blur-sm">
            <h1
              className="text-4xl md:text-5xl font-extralight text-white tracking-widest"
              style={{ textShadow: "0 2px 4px rgba(0,0,0,0.8)" }}
            >
              AMMA
            </h1>
            <p
              className="text-xs text-white/80 mt-2 font-light tracking-wide"
              style={{ textShadow: "0 1px 3px rgba(0,0,0,0.8)" }}
            >
              Your Motherly Storyteller
            </p>
            <div className="flex items-center justify-center mt-2 gap-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
              <span className="text-xs text-white/60">
                {isConnected ? 'Connected' : 'Connecting...'}
              </span>
            </div>
          </div>
        </header>

        {/* Chat Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-8 space-y-6 scrollbar-thin scrollbar-thumb-white/10">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex items-start gap-4 animate-fade-in ${
                message.sender === "user" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium ${
                  message.sender === "user" ? "bg-black/40 text-white" : "bg-black/50 text-white"
                }`}
                style={{ textShadow: "0 1px 2px rgba(0,0,0,0.8)" }}
              >
                {message.sender === "user" ? "Y" : "A"}
              </div>

              <div className="max-w-md lg:max-w-lg p-3 rounded-2xl bg-black/30 backdrop-blur-sm">
                <p
                  className="text-sm leading-relaxed font-light text-white"
                  style={{ textShadow: "0 1px 3px rgba(0,0,0,0.8)" }}
                >
                  {message.text}
                </p>
                <span className="text-xs text-white/80 mt-2 block" style={{ textShadow: "0 1px 2px rgba(0,0,0,0.8)" }}>
                  {message.timestamp.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                </span>
              </div>
            </div>
          ))}

          {/* Streaming Message */}
          {isStreaming && currentStreamingMessage && (
            <div className="flex items-start gap-4 animate-fade-in">
              <div
                className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium bg-black/50 text-white"
                style={{ textShadow: "0 1px 2px rgba(0,0,0,0.8)" }}
              >
                A
              </div>
              <div className="max-w-md lg:max-w-lg p-3 rounded-2xl bg-black/30 backdrop-blur-sm">
                <p
                  className="text-sm leading-relaxed font-light text-white"
                  style={{ textShadow: "0 1px 3px rgba(0,0,0,0.8)" }}
                >
                  {currentStreamingMessage}
                  <span className="animate-pulse">|</span>
                </p>
              </div>
            </div>
          )}

          {/* Typing Indicator */}
          {isTyping && (
            <div className="flex items-start gap-4 animate-fade-in">
              <div
                className="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium bg-black/50 text-white"
                style={{ textShadow: "0 1px 2px rgba(0,0,0,0.8)" }}
              >
                A
              </div>
              <div className="p-3 rounded-2xl bg-black/30 backdrop-blur-sm">
                <div className="flex space-x-1">
                  <div
                    className="w-1.5 h-1.5 bg-white/80 rounded-full animate-bounce"
                    style={{ animationDelay: "0ms" }}
                  />
                  <div
                    className="w-1.5 h-1.5 bg-white/80 rounded-full animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <div
                    className="w-1.5 h-1.5 bg-white/80 rounded-full animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="p-6">
          <div className="max-w-2xl mx-auto">
            <div className={`flex gap-3 p-4 rounded-full backdrop-blur-md border shadow-2xl transition-all duration-300 ${
              isStreaming || isTyping ? 
              'bg-black/10 border-white/5 opacity-75' : 
              'bg-black/20 border-white/10'
            }`}>
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder={isStreaming ? "AMMA is responding..." : "Share your thoughts with AMMA..."}
                disabled={isStreaming || isTyping || !isConnected}
                className="flex-1 bg-transparent border-none text-white/90 placeholder:text-white/40 focus:ring-0 focus:outline-none text-sm font-light disabled:opacity-50 disabled:cursor-not-allowed"
              />
              <Button
                onClick={handleSendMessage}
                disabled={!inputValue.trim() || !isConnected || isStreaming || isTyping}
                size="sm"
                className="bg-white/10 hover:bg-white/20 border-none text-white/80 backdrop-blur-sm disabled:opacity-30 rounded-full w-10 h-10 p-0"
                title={
                  isStreaming ? "AMMA is responding..." :
                  isTyping ? "AMMA is thinking..." :
                  !isConnected ? "Connecting to AMMA..." :
                  !inputValue.trim() ? "Type a message" :
                  "Send message"
                }
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
