# Camp - Feature Analysis & MVP Specification

Phan tich chi tiet cac tinh nang cua Camp, bao gom 15 tinh nang chinh theo yeu cau
va cac tinh nang bo sung de hoan thien MVP.

---

## Tong Quan Tinh Nang

### 15 Tinh Nang Chinh (Yeu Cau)

| #  | Tinh Nang            | Do Phuc Tap | Uu Tien |
|----|----------------------|-------------|---------|
| 1  | Server Management    | Trung binh  | Cao     |
| 2  | Category             | Thap        | Cao     |
| 3  | Text Channel         | Trung binh  | Cao     |
| 4  | Voice Channel        | Cao         | Cao     |
| 5  | Realtime Messaging   | Cao         | Cao     |
| 6  | Reply Message        | Thap        | Trung binh |
| 7  | Edit & Delete Message| Thap        | Trung binh |
| 8  | Emoji & Media        | Trung binh  | Trung binh |
| 9  | Pin Message          | Thap        | Thap    |
| 10 | Role & Permission    | Cao         | Cao     |
| 11 | Channel Permission   | Cao         | Trung binh |
| 12 | Moderation           | Trung binh  | Trung binh |
| 13 | Message Search       | Trung binh  | Trung binh |
| 14 | Authentication       | Trung binh  | Cao     |
| 15 | Friend List & DM     | Trung binh  | Trung binh |

### Tinh Nang Bo Sung (Hoan Thien MVP)

| #  | Tinh Nang              | Do Phuc Tap | Uu Tien    |
|----|------------------------|-------------|------------|
| S1 | User Profile & Status  | Thap        | Cao        |
| S2 | Online/Offline Status  | Trung binh  | Cao        |
| S3 | Typing Indicator       | Thap        | Trung binh |
| S4 | Unread Indicators      | Trung binh  | Cao        |
| S5 | Server Invite System   | Thap        | Cao        |
| S6 | Notification System    | Trung binh  | Trung binh |
| S7 | User Settings          | Thap        | Thap       |

---

## Chi Tiet Tung Tinh Nang

---

### 1. Server (Group) Management

**Mo ta:** Tao va quan ly cac server (group) - don vi to chuc chinh cua ung dung, tuong tu Discord server.

**Chuc nang chi tiet:**
- Tao server moi (ten, icon, mo ta)
- Chinh sua thong tin server (ten, icon, mo ta)
- Xoa server (chi owner)
- Xem danh sach thanh vien
- Transfer ownership
- Server settings page

**User Stories:**
- Nguoi dung co the tao server moi voi ten va icon
- Owner co the chinh sua thong tin server
- Owner co the xoa server
- Thanh vien co the xem danh sach thanh vien cua server

**API Endpoints:**
```
POST   /api/servers              - Tao server
GET    /api/servers/:id          - Lay thong tin server
PATCH  /api/servers/:id          - Cap nhat server
DELETE /api/servers/:id          - Xoa server
GET    /api/servers/:id/members  - Danh sach thanh vien
```

**Data Model:** Xem `Servers` collection trong project-overview.md

---

### 2. Category

**Mo ta:** Nhom cac channel lai theo chu de/muc dich de to chuc server gon gang hon.

**Chuc nang chi tiet:**
- Tao category moi
- Doi ten category
- Xoa category (cac channel ben trong se chuyen ve uncategorized)
- Sap xep thu tu category (drag & drop hoac move up/down)
- Collapse/expand category
- Quan ly channel trong category

**User Stories:**
- Admin co the tao category de nhom cac channel
- Admin co the doi ten va xoa category
- Nguoi dung co the collapse/expand category de gon giao dien
- Admin co the sap xep lai thu tu category

**API Endpoints:**
```
POST   /api/servers/:serverId/categories     - Tao category
PATCH  /api/categories/:id                   - Cap nhat category
DELETE /api/categories/:id                   - Xoa category
PATCH  /api/servers/:serverId/categories/reorder - Sap xep lai
```

---

### 3. Text Channel

**Mo ta:** Kenh giao tiep bang van ban realtime, noi thanh vien gui va nhan tin nhan.

**Chuc nang chi tiet:**
- Tao text channel (ten, topic, category)
- Chinh sua channel (ten, topic)
- Xoa channel
- Hien thi danh sach tin nhan (pagination, scroll nguoc)
- Channel topic hien thi o header
- Sap xep channel trong category

**User Stories:**
- Admin co the tao text channel trong category
- Nguoi dung co the gui va nhan tin nhan trong channel
- Nguoi dung co the xem lich su tin nhan khi scroll len
- Admin co the thay doi ten va topic cua channel

**API Endpoints:**
```
POST   /api/servers/:serverId/channels     - Tao channel
GET    /api/servers/:serverId/channels     - Danh sach channels
PATCH  /api/channels/:id                   - Cap nhat channel
DELETE /api/channels/:id                   - Xoa channel
GET    /api/channels/:id/messages          - Lay tin nhan (paginated)
```

**UI Components:**
- ChannelHeader (ten, topic, actions)
- MessageList (virtual scroll, infinite load)
- MessageInput (textarea, file attach, emoji)

---

### 4. Voice Channel

**Mo ta:** Kenh giao tiep bang am thanh realtime. Nguoi dung co the tham gia va roi phong tuc thi ma khong can "goi dien".

**Chuc nang chi tiet:**
- Tao voice channel
- Tham gia voice channel (click vao la join)
- Roi voice channel
- Hien thi danh sach nguoi dang trong voice
- Mute/unmute microphone
- Deafen/undeafen (tat am thanh nhan)
- Hien thi trang thai mute/deafen cua moi nguoi
- Tu dong disconnect khi dong tab/mat ket noi

**User Stories:**
- Nguoi dung click vao voice channel de tham gia
- Nguoi dung co the mute/unmute mic cua minh
- Nguoi dung co the deafen de khong nghe nguoi khac
- Nguoi dung thay ai dang trong voice channel
- Nguoi dung thay ai dang mute/deafen

**Technical Notes:**
- Su dung WebRTC (via simple-peer hoac mediasoup)
- Signaling qua Socket.IO
- Peer-to-peer cho nhom nho (< 8 nguoi)
- SFU (Selective Forwarding Unit) neu can scale

**Socket Events:**
```
Client: voiceJoin(channelId)
Client: voiceLeave(channelId)
Client: voiceToggleMute(channelId)
Client: voiceToggleDeafen(channelId)
Server: voiceStateUpdate({ channelId, userId, muted, deafened, joined })
Server: voiceSignal({ from, to, signal })  // WebRTC signaling
```

**UI Components:**
- VoiceChannel (danh sach nguoi trong voice)
- VoiceControls (mute, deafen, disconnect buttons)
- VoiceStatusBar (hien thi khi dang trong voice call)

---

### 5. Realtime Messaging

**Mo ta:** He thong gui nhan tin nhan voi do tre thap, su dung co che push hai chieu qua WebSocket.

**Chuc nang chi tiet:**
- Gui tin nhan realtime (nhan ngay lap tuc)
- Nhan tin nhan tu nguoi khac realtime
- Optimistic update (hien thi ngay khi gui, confirm sau)
- Message delivery status (sending, sent, failed)
- Auto-reconnect khi mat ket noi
- Message queue khi offline (gui lai khi reconnect)
- Nhom tin nhan theo nguoi gui va thoi gian

**User Stories:**
- Nguoi dung gui tin nhan va thay no hien thi ngay lap tuc
- Nguoi dung khac trong channel nhan tin nhan ngay khi duoc gui
- Khi mat ket noi, he thong tu dong ket noi lai
- Tin nhan chua gui duoc se hien thi trang thai "dang gui"

**Technical Notes:**
- Socket.IO voi room-based broadcasting
- Moi channel la 1 room
- Tin nhan luu vao MongoDB truoc khi broadcast
- Client su dung optimistic update pattern
- Pagination: Cursor-based (dua tren message _id va createdAt)

**Socket Events:**
```
Client: sendMessage({ channelId, content, attachments, replyTo })
Server: messageReceived(message)
```

**Performance:**
- Virtual scrolling cho message list (chi render messages visible)
- Batch message loading (50 messages/page)
- Debounce scroll events
- Lazy load images/media

---

### 6. Reply Message

**Mo ta:** Tra loi truc tiep 1 tin nhan cu, giu mach hoi thoai trong channel dong nguoi.

**Chuc nang chi tiet:**
- Click "Reply" tren 1 tin nhan
- Hien thi preview tin nhan dang reply o tren input
- Tin nhan reply hien thi reference den tin nhan goc
- Click vao reference de scroll den tin nhan goc
- Huy reply (click X tren preview)

**User Stories:**
- Nguoi dung click reply tren tin nhan bat ky
- Input hien thi preview ngan cua tin nhan dang reply
- Khi gui, tin nhan moi co reference link den tin nhan goc
- Nguoi khac click vao reference se scroll den tin nhan goc

**UI:**
```
+---------------------------------------------+
| Replying to Username                    [X]  |  <- Reply preview
| Original message preview (truncated)...      |
+---------------------------------------------+
| [+] Type a message...              [emoji]   |  <- Input
+---------------------------------------------+
```

**Trong message list:**
```
  |---> Reply to: Username - "original message..."    <- Click de scroll
  [AV] Username    10:30 AM
       Reply content here
```

---

### 7. Edit & Delete Message

**Mo ta:** Cho phep nguoi gui chinh sua hoac xoa tin nhan cua minh. Nguoi co quyen MANAGE_MESSAGES co the xoa tin nhan cua nguoi khac.

**Chuc nang chi tiet:**

**Edit:**
- Chi nguoi gui moi co the edit tin nhan cua minh
- Hien thi "(da chinh sua)" label ben canh timestamp
- Luu lich su chinh sua (co the xem cac phien ban cu)
- Enter de save, Escape de cancel
- Edit mode: inline editing trong message

**Delete:**
- Nguoi gui co the xoa tin nhan cua minh
- Nguoi co MANAGE_MESSAGES co the xoa tin nhan cua nguoi khac
- Hien thi confirmation dialog truoc khi xoa
- Soft delete: tin nhan hien thi "Tin nhan da bi xoa"
- Delete for everyone (khong co delete for me)

**User Stories:**
- Nguoi dung click edit, sua noi dung va nhan Enter de luu
- Nguoi dung click delete, xac nhan, tin nhan bi xoa
- Tin nhan da sua hien thi "(da chinh sua)"
- Moderator co the xoa tin nhan cua nguoi khac

**Socket Events:**
```
Client: editMessage({ messageId, content })
Client: deleteMessage(messageId)
Server: messageUpdated(message)
Server: messageDeleted({ messageId, channelId })
```

---

### 8. Emoji & Media

**Mo ta:** Phan hoi nhanh bang emoji reactions va gui cac file media (hinh anh, video, file).

**Chuc nang chi tiet:**

**Emoji Reactions:**
- Them reaction vao tin nhan (click emoji picker)
- Bo reaction (click lai emoji da react)
- Hien thi so luong react va danh sach nguoi react
- Quick reactions (emoji thuong dung)
- Emoji picker voi search

**Media Upload:**
- Upload hinh anh (jpg, png, gif, webp)
- Upload video (mp4, webm) - gioi han dung luong
- Upload file (pdf, doc, zip...) - gioi han dung luong
- Preview hinh anh/video trong chat
- Download file
- Drag & drop upload
- Paste image tu clipboard
- Progress bar khi upload

**User Stories:**
- Nguoi dung click emoji tren tin nhan de react
- Nguoi dung co the upload file bang nut attach hoac drag & drop
- Hinh anh hien thi preview trong chat
- Nguoi dung co the download file da gui

**Technical Notes:**
- Media luu tru tren Cloudinary
- Upload truc tiep tu client den Cloudinary (signed upload)
- Hoac upload qua server (server-side upload)
- Gioi han file size: 10MB cho hinh anh, 50MB cho video, 25MB cho file khac
- Cloudinary transformations cho thumbnail

**API:**
```
POST /api/upload           - Upload file len Cloudinary
DELETE /api/upload/:id     - Xoa file tren Cloudinary
```

**Socket Events (Reactions):**
```
Client: addReaction({ messageId, emoji })
Client: removeReaction({ messageId, emoji })
Server: reactionAdded({ messageId, emoji, userId })
Server: reactionRemoved({ messageId, emoji, userId })
```

---

### 9. Pin Message

**Mo ta:** Ghim tin nhan quan trong trong channel de de truy cap, phuc vu thong bao va tai lieu chung.

**Chuc nang chi tiet:**
- Pin tin nhan (can quyen PIN_MESSAGES)
- Unpin tin nhan
- Xem danh sach tin nhan da pin (panel hoac modal)
- Click vao pinned message de scroll den vi tri
- Hien thi system message khi pin/unpin
- Gioi han so luong pin (50 pins/channel)

**User Stories:**
- Nguoi co quyen co the pin tin nhan quan trong
- Moi nguoi co the xem danh sach pinned messages
- Click vao pinned message se scroll den vi tri trong chat
- Khi pin/unpin, he thong hien thi thong bao trong channel

**API:**
```
POST   /api/messages/:id/pin    - Pin message
DELETE /api/messages/:id/pin    - Unpin message
GET    /api/channels/:id/pins   - Danh sach pinned messages
```

---

### 10. Role & Permission

**Mo ta:** He thong phan quyen nguoi dung theo vai tro (role), kiem soat truy cap va hanh dong trong server.

**Chuc nang chi tiet:**
- Tao role moi (ten, mau sac, permissions)
- Chinh sua role (ten, mau, permissions)
- Xoa role
- Sap xep thu tu role (hierarchy)
- Gan role cho thanh vien
- Go role khoi thanh vien
- @everyone role (default, khong the xoa)
- Role color hien thi tren username

**Permission Categories:**
```
General:
  - Administrator (full quyen)
  - Manage Server
  - Manage Channels
  - Manage Roles

Membership:
  - Kick Members
  - Ban Members
  - Create Invite

Text:
  - Send Messages
  - Manage Messages (xoa tin nhan nguoi khac)
  - Attach Files
  - Add Reactions
  - Mention Everyone
  - Pin Messages
  - Read Message History

Voice:
  - Connect
  - Speak
  - Mute Members
  - Deafen Members

Channel:
  - View Channel
```

**User Stories:**
- Admin co the tao role voi ten, mau va permissions cu the
- Admin co the gan nhieu role cho 1 thanh vien
- Username hien thi mau cua role cao nhat
- Nguoi dung chi co the thuc hien hanh dong ma role cho phep

**UI Components:**
- RoleSettings (tao, sua, xoa roles)
- PermissionEditor (toggle tung permission)
- MemberRoleManager (gan/go role cho member)
- RoleBadge (hien thi role cua user)

---

### 11. Channel Permission & User Status

**Mo ta:** Tuy chinh quyen truy cap theo tung channel cu the va hien thi trang thai nguoi dung.

**Chuc nang chi tiet:**

**Channel Permission Overrides:**
- Override permission cua role cho 1 channel cu the
- Override permission cho 1 member cu the
- 3 trang thai: Allow / Deny / Inherit (tu role)
- Private channel (chi nguoi co quyen moi thay)

**Online/Offline Status:**
- Hien thi trang thai: Online, Idle, Do Not Disturb, Offline
- Cap nhat realtime theo ket noi WebSocket
- Tu dong chuyen sang Idle sau thoi gian khong hoat dong
- Indicator dot tren avatar

**Activity Status:**
- Nguoi dung co the dat custom status text
- Hien thi duoi ten nguoi dung trong member list

**User Stories:**
- Admin co the an channel khoi 1 so role/member
- Admin co the tat quyen gui tin nhan cua 1 role trong 1 channel
- Nguoi dung thay ai dang online/offline trong member list
- Nguoi dung co the dat trang thai DND de khong bi lam phien

**Socket Events:**
```
Client: updateStatus(status)
Server: userStatusChanged({ userId, status, activityStatus })
```

---

### 12. Moderation

**Mo ta:** Cong cu quan tri server: mute, kick, ban, timeout va he thong log hanh dong.

**Chuc nang chi tiet:**

**Moderation Actions:**
- **Mute:** Chan nguoi dung gui tin nhan (tam thoi)
- **Kick:** Dua nguoi dung ra khoi server (co the join lai)
- **Ban:** Cam nguoi dung vinh vien (khong the join lai)
- **Timeout:** Cam hoat dong trong thoi gian nhat dinh (1 phut - 1 tuan)
- **Unban:** Go ban cho nguoi dung

**Audit Log:**
- Ghi lai moi hanh dong moderation
- Thong tin: Ai, lam gi, voi ai, khi nao, ly do
- Loc theo loai hanh dong, nguoi thuc hien
- Chi nguoi co quyen moi xem audit log

**User Stories:**
- Moderator co the kick thanh vien vi pham
- Moderator co the ban thanh vien voi ly do
- Moderator co the timeout nguoi dung trong 1 khoang thoi gian
- Admin co the xem audit log de theo doi hanh dong moderation

**API:**
```
POST /api/servers/:id/members/:userId/kick
POST /api/servers/:id/members/:userId/ban
POST /api/servers/:id/members/:userId/mute
POST /api/servers/:id/members/:userId/timeout
DELETE /api/servers/:id/bans/:userId              - Unban
GET  /api/servers/:id/bans                        - Danh sach banned
GET  /api/servers/:id/audit-logs                  - Audit logs
```

---

### 13. Message Search

**Mo ta:** Tim kiem tin nhan trong server theo tu khoa, nguoi gui, channel.

**Chuc nang chi tiet:**
- Tim kiem theo noi dung tin nhan (full-text search)
- Loc theo nguoi gui
- Loc theo channel
- Loc theo khoang thoi gian
- Hien thi ket qua voi context (tin nhan truoc/sau)
- Click vao ket qua de nhay den vi tri tin nhan
- Pagination cho ket qua tim kiem
- Ket hop nhieu bo loc

**User Stories:**
- Nguoi dung co the tim tin nhan bang tu khoa
- Nguoi dung co the loc ket qua theo nguoi gui hoac channel
- Click vao ket qua se scroll den tin nhan do trong channel
- Tim kiem hoat dong tren toan bo server

**Technical Notes:**
- MongoDB text index tren truong `content`
- Co the ket hop voi regex cho tim kiem linh hoat
- Pagination: limit + skip hoac cursor-based
- Debounce search input (300ms)

**API:**
```
GET /api/servers/:serverId/messages/search
  Query params:
    - q: string (tu khoa)
    - authorId: string (loc theo nguoi gui)
    - channelId: string (loc theo channel)
    - before: date (truoc ngay)
    - after: date (sau ngay)
    - limit: number (default 25)
    - offset: number
```

**UI Components:**
- SearchModal / SearchPanel
- SearchFilters (author, channel, date)
- SearchResults (danh sach ket qua)
- SearchResultItem (preview tin nhan + context)

---

### 14. Authentication

**Mo ta:** He thong dang ky, dang nhap, xac thuc nguoi dung.

**Chuc nang chi tiet:**

**Dang Ky:**
- Dang ky bang email + password
- Validation: email format, password strength (min 8 ky tu)
- Username unique check
- Avatar mac dinh (generated hoac default image)

**Dang Nhap:**
- Dang nhap bang email + password
- JWT token (access token + refresh token)
- Remember me (refresh token luu trong httpOnly cookie)
- Auto-login khi con token hop le

**Bao Mat:**
- Password hash (bcrypt)
- JWT access token (expiry: 15 phut)
- JWT refresh token (expiry: 7 ngay)
- Token rotation khi refresh
- Logout: Invalidate refresh token

**User Stories:**
- Nguoi dung co the dang ky tai khoan voi email va password
- Nguoi dung co the dang nhap va duoc redirect vao app
- Session duoc duy tri qua refresh token
- Nguoi dung co the dang xuat

**API:**
```
POST /api/auth/register       - Dang ky
POST /api/auth/login          - Dang nhap
POST /api/auth/logout         - Dang xuat
POST /api/auth/refresh-token  - Lam moi token
GET  /api/auth/me             - Lay thong tin user hien tai
```

**UI Pages:**
- LoginPage
- RegisterPage
- Protected route wrapper

---

### 15. Friend List & Direct Messages

**Mo ta:** He thong ket ban va nhan tin rieng giua ban be.

**Chuc nang chi tiet:**

**Friend System:**
- Gui loi moi ket ban (theo username)
- Chap nhan / tu choi loi moi
- Huy loi moi da gui
- Xoa ban (unfriend)
- Block nguoi dung
- Danh sach ban be (online/all)
- Danh sach loi moi (pending)

**Direct Messages (DM):**
- Nhan tin 1-1 giua 2 nguoi dung (la ban be)
- DM history luu tru
- Realtime messaging (nhu text channel)
- Hien thi trong DM list o sidebar
- Typing indicator trong DM

**User Stories:**
- Nguoi dung co the tim va gui loi moi ket ban
- Nguoi dung co the chap nhan hoac tu choi loi moi
- Ban be co the nhan tin rieng voi nhau
- DM hien thi trong khu vuc rieng tren sidebar

**API:**
```
POST   /api/friends/request          - Gui loi moi
PATCH  /api/friends/accept/:id       - Chap nhan
DELETE /api/friends/reject/:id       - Tu choi
DELETE /api/friends/:friendId        - Xoa ban
POST   /api/friends/block/:userId    - Block
GET    /api/friends                  - Danh sach ban be
GET    /api/friends/pending          - Loi moi dang cho

GET    /api/dm                       - Danh sach DM conversations
POST   /api/dm/:userId              - Tao/mo DM voi 1 user
GET    /api/dm/:conversationId/messages - Lay tin nhan DM
```

---

## Tinh Nang Bo Sung (Supplementary)

### S1. User Profile & Settings

**Mo ta:** Trang ca nhan va cai dat nguoi dung.

**Chuc nang:**
- Xem/chinh sua display name
- Doi avatar (upload Cloudinary)
- Dat bio/about me
- Thay doi password
- Xem profile nguoi khac (modal/popup)
- Server-specific nickname

**UI:**
- UserProfileModal (xem profile nguoi khac)
- UserSettingsPage (chinh sua profile cua minh)
- UserPanel (goc duoi sidebar - avatar, ten, status)

---

### S2. Online/Offline Status (Da bao gom trong Feature #11)

Phan nay duoc tich hop vao Feature #11. Chi tiet:
- WebSocket connection = Online
- Idle detection (5 phut khong tuong tac) = Idle
- Manual set DND
- Disconnect = Offline
- Realtime broadcast trang thai den tat ca server cua user

---

### S3. Typing Indicator

**Mo ta:** Hien thi khi nguoi khac dang go tin nhan.

**Chuc nang:**
- Phat hien nguoi dung dang go (debounce)
- Hien thi "[Username] dang go..." duoi message list
- Nhieu nguoi go: "[A], [B] dang go..."
- 3+ nguoi: "Nhieu nguoi dang go..."
- Tu dong an sau 5 giay khong go

**Socket Events:**
```
Client: typingStart(channelId)
Server: typingStart({ channelId, userId, username })
```

---

### S4. Unread Indicators

**Mo ta:** Hien thi so tin nhan chua doc cho moi channel va server.

**Chuc nang:**
- Dem so tin nhan chua doc per channel
- Bold ten channel khi co tin nhan chua doc
- Badge so tren server icon
- Mark as read khi mo channel
- Mention badge (@ you) noi bat hon unread thuong

**Technical Notes:**
- Luu `lastReadMessageId` per user per channel
- So sanh voi message moi nhat de tinh unread count
- Cap nhat realtime qua socket

---

### S5. Server Invite System

**Mo ta:** Tao va quan ly link moi tham gia server.

**Chuc nang:**
- Tao invite link (unique code)
- Invite link co thoi han (1h, 6h, 12h, 24h, 7 ngay, vinh vien)
- Gioi han so lan su dung (1, 5, 10, 25, 50, 100, khong gioi han)
- Xem danh sach invite da tao
- Thu hoi (revoke) invite
- Trang join server khi click invite link

**API:**
```
POST   /api/servers/:id/invites      - Tao invite
GET    /api/servers/:id/invites      - Danh sach invites
DELETE /api/invites/:code            - Thu hoi invite
POST   /api/invites/:code/join       - Join server bang invite
GET    /api/invites/:code            - Thong tin invite (public)
```

---

### S6. Notification System

**Mo ta:** He thong thong bao cho nguoi dung ve cac su kien quan trong.

**Chuc nang:**
- Thong bao khi bi mention (@username)
- Thong bao khi co DM moi
- Thong bao khi co loi moi ket ban
- Browser notification (neu cho phep)
- Notification sound
- Notification settings per server/channel (all/mentions/none)

---

### S7. User Settings

**Mo ta:** Cai dat ung dung cua nguoi dung.

**Chuc nang:**
- Profile settings (display name, avatar, bio)
- Account settings (email, password)
- Notification settings
- Appearance settings (future: font size)
- Privacy settings (ai co the gui loi moi ket ban)

---

## MVP Scope Summary

### Must Have (v1.0):
- Authentication (register, login, JWT)
- Server CRUD + invite system
- Category va Channel management
- Realtime text messaging
- Reply, Edit, Delete messages
- Emoji reactions + Media upload
- Pin messages
- Role & Permission system
- Channel permission overrides
- Online/Offline status
- Moderation tools (kick, ban, mute, timeout)
- Message search
- Friend list & Direct messages
- User profile
- Typing indicator
- Unread indicators

### Nice to Have (v1.1+):
- Voice channels (WebRTC)
- Audit logs
- Server invite management (advanced)
- Browser notifications
- User settings page
- Activity status
- Message edit history viewer

---

**Last Updated:** 2026

Xem [progress.md](./progress.md) de biet trang thai hien tai va viec tiep theo.
