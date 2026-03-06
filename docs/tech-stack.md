# Camp - Tech Stack Analysis

Phan tich va ly do lua chon cong nghe cho project Camp.

---

## Tong Quan Tech Stack

```
+-------------------+------------------------+---------------------------+
|     Layer         |     Technology         |     Purpose               |
+-------------------+------------------------+---------------------------+
| Frontend          | React + TypeScript     | SPA, component-based UI   |
| Styling           | Tailwind CSS           | Utility-first CSS         |
| State Management  | Zustand                | Lightweight global state  |
| Build Tool        | Vite                   | Fast dev server & build   |
| Real-time (Client)| Socket.IO Client       | WebSocket connection      |
| Voice (Client)    | simple-peer / WebRTC   | Peer-to-peer audio        |
+-------------------+------------------------+---------------------------+
| Backend           | Node.js + Express      | REST API server           |
| Real-time (Server)| Socket.IO              | WebSocket server          |
| Database          | MongoDB + Mongoose     | Document database         |
| Authentication    | JWT + bcrypt           | Token-based auth          |
| Media Storage     | Cloudinary             | Image/video/file hosting  |
| Validation        | Zod                    | Schema validation         |
+-------------------+------------------------+---------------------------+
| DevOps            | Git + GitHub           | Version control           |
| Package Manager   | npm / pnpm             | Dependency management     |
+-------------------+------------------------+---------------------------+
```

---

## Frontend

### React + TypeScript (Bat buoc)

**Ly do:**
- Yeu cau bat buoc cua project
- Component-based architecture phu hop voi chat UI (message list, sidebar, channels...)
- Ecosystem lon, nhieu thu vien ho tro
- TypeScript dam bao type safety, giam bug

**Version:** React 18+ (voi Concurrent Features)

**Key Libraries:**

| Library              | Version  | Muc dich                              |
|----------------------|----------|---------------------------------------|
| react                | ^18.x    | UI library                            |
| react-dom            | ^18.x    | DOM rendering                         |
| react-router-dom     | ^6.x     | Client-side routing                   |
| typescript           | ^5.x     | Type safety                           |

---

### Vite

**Ly do chon Vite thay vi CRA (Create React App):**
- Dev server khoi dong nhanh hon nhieu (ESM-based)
- Hot Module Replacement (HMR) nhanh
- Build nhanh hon (dung esbuild + Rollup)
- CRA da ngung phat trien, Vite la chuan moi
- Cau hinh don gian, de custom

---

### Tailwind CSS v4

**Ly do:**
- Utility-first approach - viet CSS nhanh, khong can tao file CSS rieng
- De tao dark theme (cau hinh colors truc tiep trong CSS voi `@theme`)
- Responsive utilities co san
- Kich thuoc bundle nho
- Phu hop voi component-based development

**Version:** Tailwind CSS v4+ (cau hinh trong CSS, khong dung tailwind.config.js)

**Setup (Vite):**
- Plugin: `@tailwindcss/vite` trong `vite.config.ts`
- Khong can `postcss.config.js` hay `tailwind.config.js`
- Moi cau hinh nam trong file CSS voi `@theme`

**Dark Theme Config (trong globals.css):**
```css
@import "tailwindcss";

@theme {
  --color-layer-0: #0c0c10;
  --color-layer-1: #121217;
  --color-layer-2: #1a1a21;
  --color-layer-3: #222229;
  --color-layer-4: #2a2a33;
  --color-layer-5: #33333d;
  --color-layer-6: #3d3d48;

  --color-accent-50: #EEF0FF;
  --color-accent-100: #D9DDFF;
  --color-accent-200: #B3BAFF;
  --color-accent-400: #818CF8;
  --color-accent-500: #6366F1;
  --color-accent-600: #4F46E5;
  --color-accent-700: #4338CA;
  --color-accent-900: #312E81;

  --color-online: #3BA55D;
  --color-idle: #FAA61A;
  --color-dnd: #ED4245;

  --color-success-400: #4ADE80;
  --color-success-500: #22C55E;
  --color-warning-400: #FBBF24;
  --color-warning-500: #F59E0B;
  --color-danger-400: #F87171;
  --color-danger-500: #EF4444;

  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

---

### Zustand (State Management)

**Ly do chon Zustand thay vi Redux/Context:**
- Don gian, it boilerplate
- Khong can Provider wrapper
- Performance tot (selective re-render)
- Nho gon, de hoc
- Phu hop cho du an cap sinh vien (khong qua phuc tap)
- Ho tro middleware (devtools, persist)

**So sanh:**

| Tieu chi        | Redux Toolkit | Zustand      | Context API  |
|-----------------|---------------|--------------|--------------|
| Boilerplate     | Nhieu         | It           | Trung binh   |
| Learning curve  | Cao           | Thap         | Thap         |
| Performance     | Tot           | Tot          | Kem (re-render) |
| DevTools        | Co            | Co           | Han che      |
| Phu hop         | Du an lon     | Du an nho-vua| State don gian |

**Stores Du Kien:**
```
stores/
  useAuthStore.ts        - User auth state, tokens
  useServerStore.ts      - Current server, servers list
  useChannelStore.ts     - Current channel, channels list
  useMessageStore.ts     - Messages per channel
  useMemberStore.ts      - Members, online status
  useVoiceStore.ts       - Voice channel state
  useUIStore.ts          - Sidebar toggle, modals, panels
  useSocketStore.ts      - Socket connection state
```

---

### Socket.IO Client

**Ly do:**
- Tuong thich voi Socket.IO server
- Auto-reconnect
- Event-based API de su dung
- Fallback tu WebSocket sang HTTP long-polling
- Room support (phia server)

---

### Cac Thu Vien Frontend Bo Sung

| Library                  | Muc dich                                    |
|--------------------------|---------------------------------------------|
| lucide-react             | Icon library (clean, consistent)            |
| react-hot-toast / sonner | Toast notifications                         |
| date-fns                 | Format ngay thang                           |
| emoji-mart               | Emoji picker component                      |
| react-dropzone           | Drag & drop file upload                     |
| react-virtuoso           | Virtual scrolling cho message list           |
| simple-peer              | WebRTC wrapper cho voice channel            |
| clsx / tailwind-merge    | Conditional CSS classes                     |
| zod                      | Client-side validation                      |
| axios                    | HTTP client (thay the fetch)                |

---

## Backend

### Node.js + Express (Bat buoc)

**Ly do:**
- Yeu cau bat buoc cua project
- JavaScript/TypeScript ca frontend va backend (full-stack)
- Non-blocking I/O phu hop cho realtime app
- Express: mature, stable, cong dong lon

**Version:** Node.js 20 LTS+, Express 4.x

---

### Socket.IO (Server)

**Ly do chon Socket.IO cho realtime:**
- Mature va stable, duoc su dung rong rai
- Auto-reconnection, heartbeat
- Room/namespace support (moi channel la 1 room)
- Fallback mechanisms (WebSocket -> HTTP long-polling)
- Middleware support (auth, validation)
- Acknowledgement callbacks
- De tich hop voi Express

**So sanh voi cac alternatives:**

| Tieu chi        | Socket.IO    | ws (raw WS)  | Pusher       |
|-----------------|--------------|---------------|--------------|
| Ease of use     | De           | Kho           | De           |
| Rooms/namespaces| Co           | Tu lam        | Co (channels)|
| Auto-reconnect  | Co           | Tu lam        | Co           |
| Fallback        | Co           | Khong         | Co           |
| Self-hosted     | Co           | Co            | Khong (SaaS) |
| Cost            | Mien phi     | Mien phi      | Tra phi       |

---

### MongoDB + Mongoose (Bat buoc)

**Ly do:**
- Yeu cau bat buoc cua project
- Document-based phu hop cho chat data (messages la documents)
- Schema linh hoat cho cac loai tin nhan khac nhau
- Mongoose cung cap schema validation, middleware, population
- MongoDB Atlas cung cap free tier de deploy

**Mongoose Models Du Kien:**
- User
- Server
- Channel
- Category
- Message
- Role
- DirectMessage
- AuditLog

**MongoDB Optimization:**
- Indexes cho cac query thuong dung (xem project-overview.md)
- Pagination su dung cursor-based (khong dung skip cho data lon)
- Text index cho message search
- TTL index cho temporary data (typing, sessions)

---

### JWT + bcrypt (Authentication)

**Ly do:**
- JWT: Stateless authentication, phu hop cho SPA + API
- bcrypt: Hash password an toan, chong brute-force (salt rounds)
- Khong can session store (tiet kiem server resources)

**Token Strategy:**
```
Access Token:
  - Expiry: 15 phut
  - Luu trong memory (Zustand store)
  - Gui qua Authorization header

Refresh Token:
  - Expiry: 7 ngay
  - Luu trong httpOnly cookie
  - Chi gui den /api/auth/refresh-token endpoint
  - Rotation: moi lan refresh tao token moi, vo hieu token cu
```

**Libraries:**
- `jsonwebtoken` - Tao va verify JWT
- `bcryptjs` - Hash va compare passwords
- `cookie-parser` - Parse cookies cho refresh token

---

### Cloudinary (Bat buoc)

**Ly do:**
- Yeu cau bat buoc cua project
- Cloud-based media storage
- Free tier du dung cho do an (25 credits/month)
- Image transformations (resize, crop, thumbnail)
- CDN delivery (nhanh)
- Ho tro nhieu dinh dang (image, video, raw files)

**Cach Su Dung:**

**Option A: Server-side Upload (De quan ly)**
```
Client -> Server (multipart/form-data) -> Cloudinary API -> Return URL
```
- Server kiem soat upload (validation, auth)
- Don gian hon, de bao mat

**Option B: Client-side Direct Upload (Nhanh hon)**
```
Client -> Cloudinary Direct Upload (signed) -> Return URL -> Gui URL den Server
```
- Nhanh hon (khong qua server)
- Can server tao signed upload params

**Khuyen nghi:** Option A cho do an sinh vien (don gian, de debug)

**Cloudinary Config:**
```
CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
```

**Gioi han Upload:**
- Images: 10MB max
- Videos: 50MB max
- Other files: 25MB max

---

### Zod (Validation)

**Ly do:**
- TypeScript-first schema validation
- Dung duoc ca client va server (shared schemas)
- Tich hop tot voi Express (middleware validation)
- Type inference tu schema (khong can viet types rieng)
- Nho gon, performance tot

**Vi du:**
```typescript
import { z } from 'zod';

const createServerSchema = z.object({
  name: z.string().min(1).max(100),
  icon: z.string().url().optional(),
});

const sendMessageSchema = z.object({
  content: z.string().min(1).max(2000),
  channelId: z.string(),
  replyTo: z.string().optional(),
  attachments: z.array(z.object({
    url: z.string().url(),
    type: z.enum(['image', 'video', 'file']),
    name: z.string(),
    size: z.number(),
  })).optional(),
});
```

---

### Cac Thu Vien Backend Bo Sung

| Library              | Muc dich                                    |
|----------------------|---------------------------------------------|
| cors                 | Cross-origin resource sharing               |
| helmet               | Security headers                            |
| morgan               | HTTP request logging                        |
| multer               | Multipart file upload handling              |
| cloudinary           | Cloudinary SDK                              |
| express-rate-limit   | Rate limiting API requests                  |
| dotenv               | Environment variables                       |
| winston / pino       | Structured logging                          |

---

## Voice Channel Technology

### WebRTC + simple-peer

**Ly do chon WebRTC:**
- Cong nghe chuan cho peer-to-peer audio/video
- Ho tro tren moi browser hien dai
- Do tre thap (P2P connection)
- Mien phi, khong can server trung gian cho media (P2P)

**Ly do chon simple-peer:**
- Wrapper don gian cho WebRTC API (native API rat phuc tap)
- De su dung voi Socket.IO (signaling)
- Phu hop cho do an sinh vien

**Architecture:**
```
Peer-to-Peer (cho nhom nho, < 8 nguoi):

User A <-------> User B
  ^                ^
  |                |
  v                v
User C <-------> User D

Signaling qua Socket.IO:
User A -> Socket.IO Server -> User B (exchange SDP/ICE candidates)
```

**Luu y:**
- P2P chi phu hop cho nhom nho (4-8 nguoi)
- Neu can nhom lon hon, can SFU (mediasoup) - ngoai scope MVP
- STUN server: dung Google STUN public servers
- TURN server: co the can neu users o sau NAT phuc tap (optional)

---

## Development Tools

### Package Manager: pnpm (Khuyen nghi)

**Ly do:**
- Nhanh hon npm
- Tiet kiem dung luong dia (symlink)
- Strict mode (tranh phantom dependencies)
- Workspace support cho monorepo

*Co the dung npm neu khong muon cai them tool*

### Monorepo Structure

```json
// Root package.json
{
  "name": "camp",
  "private": true,
  "workspaces": [
    "client",
    "server",
    "shared"
  ],
  "scripts": {
    "dev": "concurrently \"npm run dev:client\" \"npm run dev:server\"",
    "dev:client": "npm -w client run dev",
    "dev:server": "npm -w server run dev",
    "build": "npm -w shared run build && npm -w client run build && npm -w server run build"
  }
}
```

### Code Quality

| Tool        | Muc dich                    |
|-------------|------------------------------|
| ESLint      | Linting JavaScript/TypeScript |
| Prettier    | Code formatting              |
| TypeScript  | Type checking                |

### ESLint Config (Du kien):
```javascript
// Extends
'eslint:recommended'
'plugin:@typescript-eslint/recommended'
'plugin:react/recommended'
'plugin:react-hooks/recommended'
```

---

## Deployment (Tham khao)

### Frontend Hosting Options (Free):
- **Vercel** - De deploy React app, free tier tot
- **Netlify** - Tuong tu Vercel
- **Cloudflare Pages** - Nhanh, free

### Backend Hosting Options (Free/Cheap):
- **Render** - Free tier cho web service (co sleep sau 15p inactivity)
- **Railway** - $5 free credits/month
- **Fly.io** - Free tier
- **VPS** (DigitalOcean, Linode) - $5-6/month

### Database Hosting:
- **MongoDB Atlas** - Free tier (512MB storage, shared cluster)
- Du cho do an tot nghiep

### Luu Y Khi Deploy:
- Frontend va backend co the deploy rieng (CORS config)
- Hoac deploy chung (server serve static React build)
- WebSocket can persistent connection (khong phu hop serverless)
- Can HTTPS cho WebRTC
- Environment variables quan ly qua hosting platform

---

## Tom Tat Chon Lua

### Bat Buoc (Yeu Cau):
| Technology  | Role                    |
|-------------|-------------------------|
| React       | Frontend UI             |
| Node.js     | Backend runtime         |
| MongoDB     | Database                |
| Cloudinary  | Media storage           |

### Khuyen Nghi Bo Sung:
| Technology    | Role                    | Ly Do                           |
|---------------|-------------------------|---------------------------------|
| TypeScript    | Type safety             | Giam bug, DX tot hon            |
| Vite          | Build tool              | Nhanh, hien dai                 |
| Tailwind CSS  | Styling                 | Nhanh, de tao dark theme        |
| Socket.IO     | Realtime communication  | Mature, de dung, rooms support  |
| Zustand       | State management        | Don gian, nhe, hieu qua         |
| Zod           | Validation              | TypeScript-first, shared schemas|
| simple-peer   | WebRTC wrapper          | Don gian hoa voice channel      |
| Mongoose      | MongoDB ODM             | Schema, validation, middleware  |
| JWT + bcrypt  | Authentication          | Stateless auth, secure password |
| Lucide React  | Icons                   | Clean, consistent, nhe          |

---

**Last Updated:** 2026

**Status:** Tech Stack Finalized
