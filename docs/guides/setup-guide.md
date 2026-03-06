# Camp - Setup Guide

Huong dan setup project cho nguoi moi tiep tuc phat trien. Doc nay gom: yeu cau he thong, database, Cloudinary, env vars, va cac thu vien chinh.

---

## 1. Yeu cau he thong

| Thu | Phien ban |
|-----|-----------|
| Node.js | 20+ |
| npm | 9+ (di kem Node) |
| MongoDB | 6+ (local) hoac MongoDB Atlas |
| Git | Bat ky |

---

## 2. Cau truc project

```
campp/
  client/          # React frontend (Vite)
  server/          # Express backend (Node.js)
  docs/            # Documentation
```

- **Client**: React + TypeScript + Vite, chay port 5173
- **Server**: Express + Socket.IO, chay port 5000
- Client proxy `/api` va socket den server khi dev

---

## 3. Database (MongoDB)

### Option A: MongoDB Local

1. Cai dat MongoDB: https://www.mongodb.com/try/download/community
2. Chay MongoDB service (trên Windows: MongoDB Compass hoac service; Mac: `brew services start mongodb-community`)
3. Ket noi: `mongodb://localhost:27017/camp`

### Option B: MongoDB Atlas (Cloud)

1. Tao tai khoan: https://www.mongodb.com/cloud/atlas
2. Tao cluster (Free tier M0)
3. Database Access > Add User: tao user + password
4. Network Access > Add IP: `0.0.0.0` (cho phep moi IP) hoac IP cua ban
5. Connect > Drivers > Copy connection string
6. Thay `<password>` bang password user vua tao
7. Format: `mongodb+srv://<user>:<password>@cluster0.xxxxx.mongodb.net/camp?retryWrites=true&w=majority`

### Collections tu dong tao

Mongoose tao collection khi co document dau tien. Khong can tao truoc. Cac collection chinh: `users`, `servers`, `channels`, `messages`, `conversations`, `directmessages`, ...

---

## 4. Cloudinary (Media upload)

Dung cho avatar, banner, file attach trong tin nhan.

### Buoc 1: Tao tai khoan

1. Dang ky: https://cloudinary.com
2. Free tier du cho development

### Buoc 2: Lay credentials

1. Dashboard > Settings (hoac Account Details)
2. Copy: **Cloud name**, **API Key**, **API Secret**

### Buoc 3: Gan vao .env

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Neu khong cau hinh Cloudinary

- Server van chay binh thuong
- Console se co: `Cloudinary is not configured. File uploads will be disabled.`
- Upload avatar, banner, file attach se loi

---

## 5. Environment Variables

### Server (`server/.env`)

Copy tu `server/.env.example`:

```bash
cd server
cp .env.example .env
```

| Bien | Bat buoc | Mo ta |
|-----|----------|-------|
| MONGODB_URI | Co | Connection string MongoDB |
| JWT_ACCESS_SECRET | Co | Secret cho access token (string bat ky, dai) |
| JWT_REFRESH_SECRET | Co | Secret cho refresh token (string bat ky, dai) |
| JWT_ACCESS_EXPIRES_IN | Khong | Mac dinh `15m` |
| JWT_REFRESH_EXPIRES_IN | Khong | Mac dinh `7d` |
| PORT | Khong | Mac dinh `5000` |
| CLIENT_URL | Khong | CORS origin, mac dinh `http://localhost:5173` |
| CLOUDINARY_CLOUD_NAME | Khong | Neu co thi enable upload |
| CLOUDINARY_API_KEY | Khong | |
| CLOUDINARY_API_SECRET | Khong | |

**Vi du .env day du:**

```env
NODE_ENV=development
PORT=5000

MONGODB_URI=mongodb://localhost:27017/camp

JWT_ACCESS_SECRET=my_super_secret_access_key_change_in_production
JWT_REFRESH_SECRET=my_super_secret_refresh_key_change_in_production
JWT_ACCESS_EXPIRES_IN=15m
JWT_REFRESH_EXPIRES_IN=7d

CLIENT_URL=http://localhost:5173

CLOUDINARY_CLOUD_NAME=my_cloud
CLOUDINARY_API_KEY=123456789
CLOUDINARY_API_SECRET=abcdefgh
```

### Client (`client/.env`)

Copy tu `client/.env.example`:

```bash
cd client
cp .env.example .env
```

| Bien | Bat buoc | Mo ta |
|-----|----------|-------|
| VITE_API_URL | Khong | Base URL cho API. Dev: `/api` (dung proxy). Prod: `https://your-api.com/api` |
| VITE_SOCKET_URL | Khong | Socket.IO URL. Dev: `http://localhost:5000`. Prod: `https://your-api.com` |

**Dev mode** (client + server cung localhost): co the de mac dinh hoac:

```env
VITE_API_URL=/api
VITE_SOCKET_URL=http://localhost:5000
```

**Production**: dat URL that cua server.

---

## 6. Cai dat va chay

### Lan dau setup

```bash
# Server
cd server
npm install
cp .env.example .env
# Chinh sua .env (MONGODB_URI, JWT secrets, Cloudinary neu co)

# Client
cd client
npm install
cp .env.example .env
# Neu can, chinh VITE_API_URL, VITE_SOCKET_URL
```

### Chay development

**Terminal 1 - Server:**
```bash
cd server
npm run dev
```

**Terminal 2 - Client:**
```bash
cd client
npm run dev
```

- Client: http://localhost:5173
- Server API: http://localhost:5000/api

### Build production

```bash
# Server
cd server
npm run build
npm start

# Client
cd client
npm run build
# File output trong client/dist, deploy len static host
```

---

## 7. Thu vien chinh

### Server

| Thu vien | Muc dich |
|----------|----------|
| express | Web framework |
| mongoose | MongoDB ODM |
| socket.io | Realtime (chat, typing, presence) |
| jsonwebtoken | JWT auth |
| bcryptjs | Hash password |
| cloudinary | Upload avatar, banner, file |
| multer | Parse multipart/form-data |
| zod | Validate env, input |
| cookie-parser | Doc JWT tu cookie |
| cors | CORS |
| helmet | Security headers |
| express-rate-limit | Rate limiting |
| morgan | HTTP logging |

### Client

| Thu vien | Muc dich |
|----------|----------|
| react, react-dom | UI |
| react-router-dom | Routing |
| zustand | State management |
| axios | HTTP client |
| socket.io-client | Realtime |
| lucide-react | Icons |
| tailwindcss | Styling |
| date-fns | Format date |
| emoji-picker-react | Emoji picker |
| react-window | Virtual list (MemberList) |
| sonner | Toast notifications |

---

## 8. Xu ly loi thuong gap

### Server khong ket noi MongoDB

- Kiem tra MongoDB dang chay (local) hoac connection string dung (Atlas)
- Atlas: kiem tra IP da add vao Network Access
- Kiem tra MONGODB_URI trong .env

### Client loi CORS

- Kiem tra CLIENT_URL trong server .env trung voi URL client (vd `http://localhost:5173`)
- Kiem tra server da restart sau khi doi .env

### Upload file loi

- Kiem tra Cloudinary da cau hinh day du trong server .env
- Kiem tra Cloud name, API Key, API Secret dung

### Socket khong ket noi

- Kiem tra server dang chay
- Kiem tra VITE_SOCKET_URL tro dung server
- Kiem tra da login (socket can token)

### JWT / Auth loi

- Kiem tra JWT_ACCESS_SECRET va JWT_REFRESH_SECRET da set (khong de rong)
- Production: dung secret manh, khac nhau giua access va refresh

---

## 9. Tai lieu lien quan

- `docs/progress.md` - Tien do phat trien, viec tiep theo
- `docs/project-overview.md` - Kien truc, data model
- `docs/features.md` - Chi tiet tinh nang
- `docs/standards/code.md` - Quy tac code
- `docs/standards/design-system.md` - Design system
