import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Lenis from '@studio-freight/lenis'
import './index.css'

gsap.registerPlugin(ScrollTrigger)

// ── Navigation ──────────────────────────────────────
function Nav() {
  return (
    <nav className="fixed top-4 left-4 right-4 z-40 mx-auto max-w-lg">
      <div className="flex items-center justify-between rounded-full border border-stone-200 bg-white/70 px-5 py-3 backdrop-blur-[20px]">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-coral">
            <div className="h-2 w-2 rounded-full bg-white" />
          </div>
          <span className="font-outfit text-sm font-medium text-dark">Thread</span>
        </div>
        <div className="flex items-center gap-4">
          <a href="#features" className="font-outfit text-sm font-medium text-muted hover:text-dark transition-colors">Features</a>
          <a href="#faq" className="font-outfit text-sm font-medium text-muted hover:text-dark transition-colors">FAQ</a>
          <a href="#waitlist" className="rounded-full bg-dark px-4 py-2 font-outfit text-sm font-medium text-white hover:scale-105 transition-transform">
            Join Waitlist
          </a>
        </div>
      </div>
    </nav>
  )
}

// ── Grain Overlay ───────────────────────────────────
function Grain() {
  return <div className="grain" />
}

// ── Blob ────────────────────────────────────────────
function Blob({ color, x, y, scale = 1 }: { color: string; x: string; y: string; scale?: number }) {
  return (
    <div
      className="absolute rounded-full opacity-60 animate-float"
      style={{
        background: color,
        width: `${300 * scale}px`,
        height: `${300 * scale}px`,
        left: x,
        top: y,
        filter: 'blur(80px)',
        animation: 'float 6s ease-in-out infinite',
        animationDelay: `${Math.random() * 3}s`,
      }}
    />
  )
}

// ── Hero ────────────────────────────────────────────
function Hero() {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!ref.current) return
    gsap.fromTo(ref.current.querySelectorAll('.reveal'), 
      { y: 30, opacity: 0 }, 
      { y: 0, opacity: 1, duration: 0.8, stagger: 0.15, ease: 'power2.out' }
    )
  }, [])
  return (
    <section ref={ref} className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-24 text-center">
      <Blob color="#FFE4E1" x="10%" y="10%" scale={1.2} />
      <Blob color="#E6E6FA" x="60%" y="50%" scale={1} />
      <div className="reveal relative z-10">
        <h1 className="font-outfit text-[clamp(48px,10vw,72px)] font-bold leading-[0.95] tracking-[-0.025em] text-dark">
          Your digital life,<br />
          <span className="font-reenie text-coral text-[clamp(56px,12vw,88px)]">woven</span> together
        </h1>
      </div>
      <p className="reveal relative z-10 mt-6 max-w-[500px] font-outfit text-lg text-muted">
        Thread watches your browser, terminal, and files — building a personal knowledge graph 
        so you never lose a thought again.
      </p>
      <div className="reveal relative z-10 mt-8 flex gap-3">
        <a href="#waitlist" className="rounded-full bg-coral px-8 py-3.5 font-outfit font-semibold text-dark shadow-[0_4px_20px_-2px_rgba(0,0,0,0.05)] hover:scale-105 transition-transform">
          Get Early Access
        </a>
        <a href="#features" className="rounded-full border border-stone-200 bg-white px-8 py-3.5 font-outfit font-semibold text-dark hover:scale-105 transition-transform">
          How it Works
        </a>
      </div>
    </section>
  )
}

// ── Horizontal Cards ────────────────────────────────
const CARDS = [
  { time: '10:23 AM', text: 'Browsed Next.js 15 docs — found new server component patterns' },
  { time: '11:05 AM', text: 'Ran deploy script — pushed to production with zero downtime' },
  { time: '2:14 PM', text: 'Fixed rate limiting middleware — edge case with IPv6 headers' },
  { time: '3:48 PM', text: 'Researched Supermemory Graph API — zero-config knowledge graphs' },
  { time: '5:30 PM', text: 'Edited config.py — switched DB from SQLite to Postgres' },
  { time: '7:12 PM', text: 'Pulled latest from main — 3 PRs merged, no conflicts' },
]

function HorizontalCards() {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState<number | null>(null)

  useEffect(() => {
    if (!scrollRef.current) return
    gsap.fromTo(scrollRef.current.querySelectorAll('.card'),
      { x: 60, opacity: 0 },
      {
        x: 0, opacity: 1, duration: 0.6, stagger: 0.08,
        scrollTrigger: { trigger: scrollRef.current, start: 'top 80%' }
      }
    )
  }, [])

  return (
    <section id="features" className="py-24 px-6">
      <h2 className="mb-2 font-outfit text-[32px] font-bold tracking-[-0.025em] text-dark text-center">
        Everything you touch, <span className="font-reenie text-coral text-[40px]">remembered</span>
      </h2>
      <p className="mb-10 text-center font-outfit text-muted">Scroll to see threads from your day</p>
      <div ref={scrollRef} className="flex gap-4 overflow-x-auto pb-4 -mx-6 px-6 snap-x snap-mandatory scrollbar-hide" style={{ scrollbarWidth: 'none' }}>
        {CARDS.map((card, i) => (
          <div
            key={i}
            className="card flex-shrink-0 w-[288px] h-[160px] bg-white rounded-[24px] p-6 flex flex-col justify-between snap-center cursor-pointer hover:shadow-lg transition-all duration-300"
            style={{ border: '1px solid #E7E5E4' }}
            onMouseEnter={() => setActive(i)}
            onMouseLeave={() => setActive(null)}
          >
            <span className="font-outfit text-sm text-stone-400">{card.time}</span>
            <span className={`font-outfit text-xl font-medium transition-colors duration-300 ${active === i ? 'text-coral' : 'text-stone-800'}`}>
              {card.text}
            </span>
          </div>
        ))}
      </div>
    </section>
  )
}

// ── Phone Mockups ────────────────────────────────────
function PhoneMockup({ bg, y, opacity, scale, pulse = false }: { bg: string; y: string; opacity: number; scale: number; pulse?: boolean }) {
  return (
    <div
      className="absolute left-1/2 rounded-[40px] border-4 border-stone-800 overflow-hidden shadow-lg"
      style={{
        width: `${300 * scale}px`,
        height: `${620 * scale}px`,
        background: bg,
        transform: `translateX(-50%) translateY(${y})`,
        opacity,
        zIndex: pulse ? 2 : 0,
      }}
    >
      <div className="flex flex-col items-center justify-center h-full px-6 text-center">
        <div className="text-stone-400 text-xs mb-4 font-outfit">THREAD</div>
        <div className="w-12 h-12 rounded-full bg-coral mb-4 flex items-center justify-center">
          <div className="w-3 h-3 rounded-full bg-white" />
        </div>
        <div className="text-dark font-outfit font-semibold text-lg mb-2">Today's Threads</div>
        <div className="text-muted font-outfit text-xs mb-6">12 memories woven</div>
        {pulse && (
          <button className="rounded-full bg-coral px-6 py-3 font-outfit text-sm font-semibold text-dark animate-pulse">
            Search memory
          </button>
        )}
      </div>
    </div>
  )
}

function AppPreview() {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!ref.current) return
    gsap.fromTo(ref.current, 
      { y: 40, opacity: 0 }, 
      { y: 0, opacity: 1, duration: 1, scrollTrigger: { trigger: ref.current, start: 'top 80%' } }
    )
  }, [])
  return (
    <section ref={ref} className="relative py-24 px-6 overflow-hidden">
      <h2 className="mb-2 font-outfit text-[32px] font-bold tracking-[-0.025em] text-dark text-center">
        One place, <span className="font-reenie text-coral text-[40px]">every tool</span>
      </h2>
      <p className="mb-10 text-center font-outfit text-muted">Browser, terminal, editor — all feeding one memory graph</p>
      <div className="relative h-[680px] mx-auto max-w-sm">
        <PhoneMockup bg="#EFEDF4" y="96px" opacity={0.8} scale={0.93} />
        <PhoneMockup bg="#E8EFE8" y="48px" opacity={1} scale={0.97} />
        <PhoneMockup bg="#FDFCF8" y="0" opacity={1} scale={1} pulse />
      </div>
    </section>
  )
}

// ── Testimonials ─────────────────────────────────────
const TESTIMONIALS = [
  { text: '"I stopped losing context between sessions. Thread remembers which API I was debugging last Tuesday."', author: 'Sarah Chen' },
  { text: '"Finally, my terminal history actually helps me. Thread connected a deploy error to a config change I made 3 days ago."', author: 'Marcus Rivera' },
]

function Testimonials() {
  return (
    <section className="py-24 px-6">
      <h2 className="mb-10 font-outfit text-[32px] font-bold tracking-[-0.025em] text-dark text-center">
        What early users <span className="font-reenie text-coral text-[40px]">say</span>
      </h2>
      <div className="grid md:grid-cols-2 gap-6 max-w-3xl mx-auto">
        {TESTIMONIALS.map((t, i) => (
          <div
            key={i}
            className="bg-white rounded-[24px] p-8 shadow-[0_4px_20px_-2px_rgba(0,0,0,0.05)] border border-stone-100"
            style={{ transform: `rotate(${i === 0 ? 1 : -1}deg)` }}
          >
            <p className="font-outfit text-stone-800 leading-relaxed mb-6">{t.text}</p>
            <div className="w-8 h-[2px] bg-stone-300 mb-2" />
            <span className="font-reenie text-2xl text-stone-500">{t.author}</span>
          </div>
        ))}
      </div>
    </section>
  )
}

// ── FAQ ──────────────────────────────────────────────
const FAQS = [
  { q: 'What does Thread watch?', a: 'Thread connects to your browser history, terminal commands, and recently edited files. Everything stays local — your data never leaves your machine until you explicitly sync it to Supermemory.' },
  { q: 'Do I need to run a server?', a: 'Thread runs as a lightweight background process. Start it once and it watches your activity continuously. The API is available at localhost:8000 for search and queries.' },
  { q: 'Is my data private?', a: 'Yes. By default, Thread runs entirely on your machine. When you connect Supermemory (cloud or local), only the extracted memories are synced — not raw browsing data or file contents.' },
  { q: 'Can I use it with AI coding agents?', a: 'Absolutely. Thread\'s API is compatible with any tool that can make HTTP requests. Pipe your Thread memories into Claude Code, Cursor, or Codex for persistent project context across sessions.' },
]

function FAQ() {
  const [open, setOpen] = useState<number | null>(null)
  return (
    <section id="faq" className="py-24 px-6 max-w-2xl mx-auto">
      <h2 className="mb-10 font-outfit text-[32px] font-bold tracking-[-0.025em] text-dark text-center">
        Questions? <span className="font-reenie text-coral text-[40px]">Answers.</span>
      </h2>
      <div className="space-y-3">
        {FAQS.map((faq, i) => (
          <div key={i} className="rounded-2xl bg-white border border-stone-100 overflow-hidden">
            <button
              onClick={() => setOpen(open === i ? null : i)}
              className="w-full flex items-center justify-between p-6 font-outfit font-medium text-left text-dark"
            >
              {faq.q}
              <span className={`text-2xl text-muted transition-transform duration-500 ${open === i ? 'rotate-45' : ''}`}>+</span>
            </button>
            <div
              className="transition-all duration-500 ease-in-out overflow-hidden"
              style={{ maxHeight: open === i ? '200px' : '0' }}
            >
              <p className="px-6 pb-6 font-outfit text-muted leading-relaxed">{faq.a}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

// ── Waitlist ─────────────────────────────────────────
function Waitlist() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (email) setSubmitted(true)
  }
  return (
    <section id="waitlist" className="relative py-32 px-6 overflow-hidden">
      <Blob color="#FFE4E1" x="20%" y="10%" scale={0.8} />
      <Blob color="#EFEDF4" x="60%" y="60%" scale={0.6} />
      <div className="relative z-10 max-w-lg mx-auto text-center">
        <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-dark mb-6">
          <div className="h-2.5 w-2.5 rounded-full bg-coral" />
        </div>
        <h2 className="font-outfit text-[40px] font-bold tracking-[-0.025em] text-dark mb-4">
          Never lose a thread
        </h2>
        <p className="font-outfit text-muted mb-8">
          Join the waitlist. First 100 users get free access.
        </p>
        {submitted ? (
          <p className="font-outfit text-coral font-semibold text-lg">You're on the list! 🧵</p>
        ) : (
          <form onSubmit={handleSubmit} className="flex gap-3 max-w-md mx-auto">
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="flex-1 rounded-full bg-stone-50 border border-stone-200 px-6 py-3.5 font-outfit text-dark placeholder:text-stone-400 focus:outline-none focus:border-coral"
              required
            />
            <button
              type="submit"
              className="rounded-full bg-dark px-8 py-3.5 font-outfit font-semibold text-white hover:scale-105 transition-transform"
            >
              Join
            </button>
          </form>
        )}
      </div>
    </section>
  )
}

// ── Footer ───────────────────────────────────────────
function Footer() {
  return (
    <footer className="py-12 px-6 text-center border-t border-stone-100">
      <div className="flex items-center justify-center gap-2 mb-3">
        <div className="flex h-6 w-6 items-center justify-center rounded-full bg-coral">
          <div className="h-1.5 w-1.5 rounded-full bg-white" />
        </div>
        <span className="font-outfit font-semibold text-dark">Thread</span>
      </div>
      <p className="font-outfit text-sm text-muted">Built for Supermemory Localhost:6767 · July 2026</p>
    </footer>
  )
}

// ── App ──────────────────────────────────────────────
export default function App() {
  useEffect(() => {
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t: number) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      smoothWheel: true,
    })
    function raf(time: number) { lenis.raf(time); requestAnimationFrame(raf) }
    requestAnimationFrame(raf)
    return () => lenis.destroy()
  }, [])

  return (
    <div className="relative">
      <Grain />
      <Nav />
      <main>
        <Hero />
        <HorizontalCards />
        <AppPreview />
        <Testimonials />
        <FAQ />
        <Waitlist />
      </main>
      <Footer />
    </div>
  )
}
