# Camp - Project Overview

## Gioi Thieu

**Camp** la mot ung dung chat realtime lay cam hung tu Discord, duoc xay dung nhu do an tot nghiep dai hoc. Ung dung cho phep nguoi dung tao server, tham gia cac kenh text va voice, giao tiep realtime, va quan ly cong dong voi he thong phan quyen linh hoat.

---

## Pham Vi Du An

### Muc Tieu

- Xay dung ung dung web chat realtime day du tinh nang
- Ho tro giao tiep bang van ban va am thanh (voice)
- He thong quan ly server/group voi role va permission
- Giao dien dark theme hien dai, truc quan
- Do an cap do sinh vien dai hoc, tap trung vao cac tinh nang core

### Doi Tuong Su Dung

- Sinh vien, nhom hoc tap, cong dong nho
- Nguoi dung muon tao server rieng de giao tiep
- Nhom lam viec can cong cu chat realtime

### Khong Bao Gom (Out of Scope)

- Streaming video/share screen phuc tap
- Bot system va API cho third-party
- Marketplace / Nitro / monetization
- Mobile native app (chi web responsive)
- End-to-end encryption

---

## Kien Truc Tong Quan

### Architecture Pattern: Client-Server voi WebSocket

```
+------------------+         +------------------+         +------------------+
|                  |  HTTP   |                  |         |                  |
|  React Client   | <-----> |  Node.js Server  | <-----> |    MongoDB       |
|  (SPA)          |         |  (Express)       |         |    Database      |
|                  | Socket  |                  |         |                  |
|                  | <-----> |  Socket.IO       |         +------------------+
+------------------+   WS   +------------------+
                                    |
                                    |  HTTP
                                    v
                             +------------------+
                             |   Cloudinary     |
                             |   (Media Store)  |
                             +------------------+
```

### Data Flow

**1. REST API Flow (CRUD operations):**
```
Client -> HTTP Request -> Express Router -> Controller -> Service -> MongoDB
Client <- HTTP Response <- Controller <- Service <- MongoDB
```

**2. Realtime Flow (Chat, Status, Notifications):**
```
Client A -> Socket.IO emit -> Server Handler -> Validate -> Save to DB
                                             -> Broadcast to Room -> Client B, C, D...
```

**3. Media Upload Flow:**
```
Client -> File Select -> Upload to Cloudinary (direct hoac via server)
       -> Nhan URL -> Gui message voi media URL -> Save to DB
```

### Folder Structure (Du kien)

```
campp/
  docs/                      # Documentation
    standards/               # Coding & design standards
    project-overview.md      # File nay
    features.md              # Feature analysis
    tech-stack.md            # Tech stack analysis

  client/                    # Frontend - React Application
    public/                  # Static assets
    src/
      assets/                # Images, fonts
      components/            # Reusable UI components
        ui/                  # Base UI components (Button, Input, Modal...)
        layout/              # Layout components (Sidebar, Header...)
        chat/                # Chat-related components
        server/              # Server-related components
        channel/             # Channel-related components
        voice/               # Voice-related components
        user/                # User-related components
      pages/                 # Page-level components
      hooks/                 # Custom React hooks
      stores/                # State management (Zustand)
      services/              # API calls & socket services
        api/                 # REST API service
        socket/              # Socket.IO service
      types/                 # TypeScript type definitions
      utils/                 # Utility functions
      styles/                # Global CSS / Tailwind config
      App.tsx
      main.tsx
    package.json
    tsconfig.json
    vite.config.ts
    tailwind.config.js

  server/                    # Backend - Node.js Application
    src/
      config/                # Environment, database config
      controllers/           # Route handlers
      middleware/            # Auth, permission, validation middleware
      models/                # Mongoose models
      routes/                # Express route definitions
      services/              # Business logic layer
      socket/                # Socket.IO event handlers
        handlers/            # Handler per feature (chat, voice, status...)
        middleware/          # Socket authentication
      utils/                 # Utility functions
      validators/            # Input validation schemas
      app.ts                 # Express app setup
      server.ts              # Server entry point
    package.json
    tsconfig.json
    .env

  .gitignore
  README.md
```

**Luu y:** `client/` va `server/` la 2 project doc lap, moi project co `package.json` rieng. Chay bang 2 terminal rieng biet:
```
# Terminal 1
cd server && npm run dev

# Terminal 2
cd client && npm run dev
```

---

## Database Design (MongoDB)

### Collections Chinh

**Users**
```
{
  _id: ObjectId,
  username: String (unique),
  email: String (unique),
  passwordHash: String,
  displayName: String,
  avatar: String (Cloudinary URL),
  status: 'online' | 'idle' | 'dnd' | 'offline',
  activityStatus: String,
  friends: [ObjectId],
  friendRequests: {
    incoming: [ObjectId],
    outgoing: [ObjectId]
  },
  servers: [ObjectId],
  createdAt: Date,
  updatedAt: Date
}
```

**Servers**
```
{
  _id: ObjectId,
  name: String,
  icon: String (Cloudinary URL),
  ownerId: ObjectId (ref: Users),
  members: [{
    userId: ObjectId,
    roles: [ObjectId],
    joinedAt: Date,
    nickname: String
  }],
  categories: [ObjectId],
  channels: [ObjectId],
  roles: [ObjectId],
  inviteCode: String (unique),
  createdAt: Date,
  updatedAt: Date
}
```

**Channels**
```
{
  _id: ObjectId,
  name: String,
  type: 'text' | 'voice',
  serverId: ObjectId (ref: Servers),
  categoryId: ObjectId (ref: Categories),
  topic: String,
  position: Number,
  permissionOverrides: [{
    targetType: 'role' | 'member',
    targetId: ObjectId,
    allow: Number (bitfield),
    deny: Number (bitfield)
  }],
  createdAt: Date,
  updatedAt: Date
}
```

**Categories**
```
{
  _id: ObjectId,
  name: String,
  serverId: ObjectId (ref: Servers),
  position: Number,
  channels: [ObjectId],
  createdAt: Date
}
```

**Messages**
```
{
  _id: ObjectId,
  content: String,
  authorId: ObjectId (ref: Users),
  channelId: ObjectId (ref: Channels),
  serverId: ObjectId (ref: Servers),
  type: 'default' | 'reply' | 'system' | 'pin',
  replyTo: ObjectId (ref: Messages),
  attachments: [{
    url: String (Cloudinary URL),
    type: 'image' | 'video' | 'file',
    name: String,
    size: Number
  }],
  reactions: [{
    emoji: String,
    users: [ObjectId]
  }],
  mentions: [ObjectId],
  pinned: Boolean,
  editedAt: Date,
  editHistory: [{
    content: String,
    editedAt: Date
  }],
  deleted: Boolean,
  createdAt: Date,
  updatedAt: Date
}
```

**Roles**
```
{
  _id: ObjectId,
  name: String,
  serverId: ObjectId (ref: Servers),
  color: String (hex),
  permissions: Number (bitfield),
  position: Number,
  isDefault: Boolean,
  createdAt: Date
}
```

**DirectMessages**
```
{
  _id: ObjectId,
  participants: [ObjectId] (ref: Users, max 2),
  lastMessage: ObjectId (ref: Messages),
  createdAt: Date,
  updatedAt: Date
}
```

**AuditLogs**
```
{
  _id: ObjectId,
  serverId: ObjectId,
  executorId: ObjectId (ref: Users),
  targetId: ObjectId,
  targetType: 'member' | 'channel' | 'role' | 'server',
  action: String ('MEMBER_KICK' | 'MEMBER_BAN' | 'CHANNEL_CREATE' | ...),
  changes: Object,
  reason: String,
  createdAt: Date
}
```

### Indexes Quan Trong

```javascript
// Messages - truy van nhanh theo channel va thoi gian
messages: { channelId: 1, createdAt: -1 }
messages: { serverId: 1, content: 'text' }  // Full-text search
messages: { channelId: 1, pinned: 1 }

// Users
users: { email: 1 }  // unique
users: { username: 1 }  // unique

// Servers
servers: { inviteCode: 1 }  // unique
servers: { 'members.userId': 1 }
```

---

## API Design

### REST API Endpoints (Chinh)

**Authentication:**
```
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/refresh-token
GET    /api/auth/me
```

**Users:**
```
GET    /api/users/:userId
PATCH  /api/users/:userId
GET    /api/users/:userId/servers
POST   /api/users/friends/request
PATCH  /api/users/friends/accept/:requestId
DELETE /api/users/friends/:friendId
```

**Servers:**
```
POST   /api/servers
GET    /api/servers/:serverId
PATCH  /api/servers/:serverId
DELETE /api/servers/:serverId
POST   /api/servers/:serverId/join
POST   /api/servers/:serverId/leave
GET    /api/servers/:serverId/members
POST   /api/servers/join/:inviteCode
```

**Channels:**
```
POST   /api/servers/:serverId/channels
GET    /api/servers/:serverId/channels
PATCH  /api/channels/:channelId
DELETE /api/channels/:channelId
```

**Categories:**
```
POST   /api/servers/:serverId/categories
PATCH  /api/categories/:categoryId
DELETE /api/categories/:categoryId
```

**Messages:**
```
GET    /api/channels/:channelId/messages
POST   /api/channels/:channelId/messages
PATCH  /api/messages/:messageId
DELETE /api/messages/:messageId
POST   /api/messages/:messageId/pin
DELETE /api/messages/:messageId/pin
POST   /api/messages/:messageId/reactions
GET    /api/servers/:serverId/messages/search
```

**Roles:**
```
POST   /api/servers/:serverId/roles
PATCH  /api/roles/:roleId
DELETE /api/roles/:roleId
PATCH  /api/servers/:serverId/members/:userId/roles
```

**Moderation:**
```
POST   /api/servers/:serverId/members/:userId/kick
POST   /api/servers/:serverId/members/:userId/ban
POST   /api/servers/:serverId/members/:userId/mute
POST   /api/servers/:serverId/members/:userId/timeout
GET    /api/servers/:serverId/audit-logs
```

**Media:**
```
POST   /api/upload
DELETE /api/upload/:publicId
```

### Socket.IO Events

**Client -> Server:**
```
joinServer(serverId)
leaveServer(serverId)
joinChannel(channelId)
leaveChannel(channelId)
sendMessage({ channelId, content, attachments, replyTo })
editMessage({ messageId, content })
deleteMessage(messageId)
addReaction({ messageId, emoji })
removeReaction({ messageId, emoji })
typingStart(channelId)
typingStop(channelId)
voiceJoin(channelId)
voiceLeave(channelId)
voiceToggleMute(channelId)
voiceToggleDeafen(channelId)
updateStatus(status)
```

**Server -> Client:**
```
messageReceived(message)
messageUpdated(message)
messageDeleted({ messageId, channelId })
reactionAdded({ messageId, emoji, userId })
reactionRemoved({ messageId, emoji, userId })
typingStart({ channelId, userId, username })
typingStop({ channelId, userId })
memberJoined({ serverId, member })
memberLeft({ serverId, userId })
memberUpdated({ serverId, member })
channelCreated(channel)
channelUpdated(channel)
channelDeleted(channelId)
voiceStateUpdate({ channelId, userId, muted, deafened })
userStatusChanged({ userId, status })
messagePinned({ channelId, messageId })
messageUnpinned({ channelId, messageId })
```

---

## Permission System

### Permission Bitfield

Su dung bitfield de quan ly permissions, tuong tu Discord.

```typescript
enum Permission {
  // General
  ADMINISTRATOR        = 1 << 0,   // 1
  MANAGE_SERVER        = 1 << 1,   // 2
  MANAGE_CHANNELS      = 1 << 2,   // 4
  MANAGE_ROLES         = 1 << 3,   // 8

  // Membership
  KICK_MEMBERS         = 1 << 4,   // 16
  BAN_MEMBERS          = 1 << 5,   // 32
  CREATE_INVITE        = 1 << 6,   // 64

  // Text Channel
  SEND_MESSAGES        = 1 << 7,   // 128
  MANAGE_MESSAGES      = 1 << 8,   // 256
  ATTACH_FILES         = 1 << 9,   // 512
  ADD_REACTIONS        = 1 << 10,  // 1024
  MENTION_EVERYONE     = 1 << 11,  // 2048
  PIN_MESSAGES         = 1 << 12,  // 4096
  READ_MESSAGE_HISTORY = 1 << 13,  // 8192

  // Voice Channel
  CONNECT              = 1 << 14,  // 16384
  SPEAK                = 1 << 15,  // 32768
  MUTE_MEMBERS         = 1 << 16,  // 65536
  DEAFEN_MEMBERS       = 1 << 17,  // 131072

  // Channel
  VIEW_CHANNEL         = 1 << 18,  // 262144
}
```

### Permission Resolution Order

```
1. Server Owner -> Co tat ca quyen
2. ADMINISTRATOR permission -> Co tat ca quyen
3. Role permissions (merged, bitwise OR)
4. Channel permission overrides (allow/deny)
   - Role overrides
   - Member-specific overrides (cao nhat)
```

---

## Development Phases

### Phase 1: Foundation
- Setup project structure (monorepo)
- Setup development environment
- Authentication (register, login, JWT)
- Database models va connections
- Basic UI layout (dark theme skeleton)

### Phase 2: Core Chat
- Server CRUD
- Channel CRUD (text channels)
- Category management
- Real-time messaging (Socket.IO)
- Message history va pagination
- Basic message input

### Phase 3: Enhanced Messaging
- Reply messages
- Edit va delete messages
- Emoji reactions
- Media upload (Cloudinary)
- Pin messages
- Message search
- Typing indicators

### Phase 4: Permission & Moderation
- Role system
- Permission bitfield
- Channel permission overrides
- Moderation tools (kick, ban, mute, timeout)
- Audit logs
- Online/offline status

### Phase 5: Voice & Social
- Voice channels (WebRTC)
- Join/leave voice rooms
- Mute/deafen controls
- Friend system
- Direct messages
- User profiles

### Phase 6: Polish & Deploy
- UI polish va responsive
- Performance optimization
- Error handling improvements
- Testing
- Deployment
- Documentation

---

## Conventions

- Xem chi tiet tai [Coding Standards](./standards/code.md)
- Xem chi tiet tai [Design System](./standards/design-system.md)
- Xem chi tiet tai [Features](./features.md)
- Xem tien do tai [progress.md](./progress.md)
- Xem setup tai [guides/setup-guide.md](./guides/setup-guide.md)

---

**Last Updated:** 2026
