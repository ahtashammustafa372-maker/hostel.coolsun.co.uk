# 🎨 Hostel ERP - Apple-Glass 2026 Theme Guide

## Core Philosophy: "Crystal & Void"
- **Light Mode:** Frosted glass on soft white/gray mesh.
- **Dark Mode:** Smoked glass on deep midnight blue/black with neon accents.

## 1. Glassmorphism Variables
- **Blur:** `backdrop-blur-2xl`
- **Border:** `border-white/20` (Thin, translucent)
- **Shadow:** `shadow-2xl`
- **Surface:** `bg-white/5` (Dark Mode), `bg-white/40` (Light Mode)

## 2. Mesh Gradients
- **Dark Mode Background:** `bg-void` with radial gradients:
  - Top-Left: `rgba(79,70,229,0.4)` (Indigo)
  - Center: `blue-600/30`
  - Bottom-Right: `purple-600/30`

## 3. Typography
- **Font:** Inter (`font-sans`)
- **Labels:** Uppercase, tracking-wider, text-xs, font-medium (`text-white/40`)

## 4. Components
### Sticky Glass Header
```jsx
<div className="sticky top-0 z-50 backdrop-blur-xl border-b border-white/10 bg-black/20">
  {/* Content */}
</div>
```

### Visual Room Card
```jsx
<div className="glass-card relative overflow-hidden rounded-2xl border border-white/20 bg-white/5 p-4 transition-all hover:bg-white/10">
  {/* Content */}
</div>
```
