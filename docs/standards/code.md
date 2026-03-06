# Camp - Coding Standards & Project Rules

Coding standards cho project Camp - Realtime Chat Application.

---

## 1. Code Comments

### Rules:
- Comment ngan gon, trong tam, chi o noi can thiet
- Moi comment phai co muc dich ro rang
- Khong comment nhung gi code da the hien ro rang

### Standards:

#### TypeScript/JavaScript Comments:

**DO:**
```typescript
/**
 * Xac thuc WebSocket connection va attach user data vao socket
 */
export function authenticateSocket(socket: Socket, token: string): Promise<User> {
  // ...
}

// Kiem tra quyen truoc khi cho phep gui tin nhan vao channel
if (!hasPermission(user, channel, 'SEND_MESSAGES')) {
  throw new ForbiddenError();
}
```

**DON'T:**
```typescript
// TODO: fix this later
// This is for something
// Note: maybe we should change this

// BAD: Comment lap lai code
const message = await Message.findById(id); // Find message by ID
```

#### Function Comments:
- Chi dung JSDoc cho exported functions phuc tap hoac public APIs
- Khong can JSDoc cho functions don gian, ten da ro rang
- Mo ta ngan gon (1 cau)

#### Inline Comments:
- Chi comment "why" (tai sao), khong comment "what" (la gi)
- Chi comment logic phuc tap hoac business rules dac biet
- Khong comment tung dong code don gian

---

## 2. No Emojis in Code

### Rules:
- KHONG duoc them emoji vao bat ky file code nao
- File code nao co emoji can duoc loai bo ngay

### Scope:
- All `.ts`, `.tsx`, `.js`, `.jsx` files
- All `.json`, `.env` files
- Configuration files (`.config.js`, `.config.ts`)

---

## 3. No Emojis in Documentation

### Rules:
- KHONG them emoji vao documentation files
- File docs nao co emoji thi can duoc loai bo hoan toan

### Scope:
- All `.md` files (README, docs, etc.)
- All documentation comments in code

---

## 4. Language

### Rules:
- Tieng Anh la ngon ngu chinh cho tat ca noi dung
- Tat ca user-facing content (UI, error messages, notifications) phai bang tieng Anh
- Code elements (variables, functions, API endpoints) bang tieng Anh
- Code comments co the tieng Anh hoac tieng Viet (tuy ngu canh)

### Scope:

#### User-Facing Content (English):
- Error messages, success messages
- Toast notifications
- Form labels, button text
- Page titles, help text
- Validation messages
- System messages (chat system notifications)
- API error responses

#### Code Elements (English):
- Variable names: `camelCase`
- Function names: `camelCase`
- Class/Component names: `PascalCase`
- API endpoints: `kebab-case`
- Database fields: `camelCase` (MongoDB convention)
- Socket events: `camelCase` (e.g., `sendMessage`, `joinChannel`)

### Examples:

**DO:**
```typescript
toast.success('Message sent successfully');
toast.error('You do not have permission in this channel');
res.status(401).json({ error: 'Invalid email or password' });

socket.emit('sendMessage', { channelId, content });
socket.on('messageReceived', (message) => { ... });
```

**DON'T:**
```typescript
// DON'T: User messages bang tieng Viet
toast.error('Ban khong co quyen trong channel nay');

// DON'T: Socket events khong nhat quan
socket.emit('send-message', data);
socket.emit('SendMessage', data);
```

---

## 5. Code Formatting

### General:
- Use consistent indentation (2 spaces for TypeScript/JavaScript)
- Use single quotes for strings (unless escaping)
- Trailing commas in multi-line objects/arrays
- Semicolons required

### Naming Conventions:
- **Variables/Functions**: `camelCase`
- **Classes/Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `kebab-case` for components (e.g., `message-input.tsx`), `camelCase` for utilities
- **Folders**: `kebab-case` (e.g., `voice-channel/`, `message-list/`)
- **Socket Events**: `camelCase` (e.g., `joinServer`, `sendMessage`, `typingStart`)
- **MongoDB Collections**: `camelCase` plural (e.g., `messages`, `servers`, `channels`)

### File Naming Examples:
```
components/
  server-sidebar/
    server-sidebar.tsx
    server-sidebar.types.ts
  message-item/
    message-item.tsx
  voice-channel/
    voice-channel.tsx

hooks/
  useSocket.ts
  useVoiceChannel.ts

utils/
  formatDate.ts
  permissions.ts

models/
  Server.ts
  Message.ts
  User.ts
```

---

## 6. Error Handling

### Rules:
- Always handle errors explicitly
- Use try-catch for async operations
- Return appropriate HTTP status codes
- Log errors with context
- Handle WebSocket errors gracefully

### HTTP Error Example:
```typescript
try {
  const message = await Message.create({ content, channelId, authorId });
  return res.status(201).json({ data: message });
} catch (error) {
  logger.error('Failed to create message:', { error, channelId, authorId });
  return res.status(500).json({ error: 'Khong the gui tin nhan' });
}
```

### WebSocket Error Example:
```typescript
socket.on('sendMessage', async (data, callback) => {
  try {
    const message = await createMessage(data);
    socket.to(data.channelId).emit('messageReceived', message);
    callback({ success: true, data: message });
  } catch (error) {
    logger.error('Socket sendMessage error:', { error, data });
    callback({ success: false, error: 'Khong the gui tin nhan' });
  }
});
```

---

## 7. Type Safety

### Rules:
- Use TypeScript types strictly
- Avoid `any` type (use `unknown` if type is truly unknown)
- Define interfaces for all data models
- Define types for socket events
- Use type guards when needed

### Socket Event Types Example:
```typescript
interface ServerToClientEvents {
  messageReceived: (message: Message) => void;
  typingStart: (data: { userId: string; channelId: string }) => void;
  userStatusChanged: (data: { userId: string; status: UserStatus }) => void;
}

interface ClientToServerEvents {
  sendMessage: (data: SendMessagePayload, callback: AckCallback) => void;
  joinChannel: (channelId: string) => void;
  typingStart: (channelId: string) => void;
}
```

---

## 8. File Organization

### Rules:
- One component/class per file
- Group related files in folders
- Use index files for clean imports
- Keep files focused and small (< 300 lines when possible)
- Separate concerns: UI components, business logic, API calls, socket handlers

### Project Structure Pattern:
```
src/
  client/                    # Frontend (React)
    components/              # UI components
    pages/                   # Page components
    hooks/                   # Custom hooks
    stores/                  # State management
    services/                # API & socket services
    types/                   # TypeScript types
    utils/                   # Utility functions
    styles/                  # Global styles

  server/                    # Backend (Node.js)
    controllers/             # Request handlers
    models/                  # MongoDB models
    routes/                  # API routes
    middleware/              # Express middleware
    socket/                  # Socket.IO handlers
    services/                # Business logic
    utils/                   # Utility functions
    config/                  # Configuration

  shared/                    # Shared code (types, constants)
    types/
    constants/
```

---

## 9. Git Commit Messages

### Rules:
- Use clear, descriptive commit messages
- Start with type prefix
- Keep first line under 72 characters
- Add detailed description if needed

### Format:
```
<type>(<scope>): <description>

[optional body]
```

### Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `style`: UI/styling changes
- `docs`: Documentation
- `chore`: Build, config, dependencies
- `perf`: Performance improvement
- `test`: Tests

### Examples:
```
feat(chat): add real-time message delivery via WebSocket
fix(voice): resolve audio stream disconnection on channel switch
refactor(auth): extract JWT validation into middleware
style(sidebar): update server list dark theme colors
docs(api): add WebSocket event documentation
```

---

## 10. UI Logic & Layout

### Rules:
- Luon kiem tra logic UI, khong chi design ma con ve layout va text overflow
- Dam bao khong co text tran man hinh, lam hong layout
- Kiem tra responsive tren cac kich thuoc man hinh khac nhau
- Xu ly text dai bang truncate voi tooltip
- Chat UI phai hoat dong tot voi noi dung dai va ngan

### Chat-Specific UI Rules:

**Message List:**
- Virtual scrolling cho danh sach tin nhan dai
- Auto-scroll xuong khi co tin nhan moi (neu dang o cuoi)
- Hien thi "new messages" indicator khi khong o cuoi
- Load more khi scroll len (infinite scroll nguoc)

**Input Area:**
- Auto-resize textarea
- Gioi han chieu cao toi da
- Ho tro paste hinh anh
- Hien thi typing indicator

**Sidebar:**
- Collapsible categories
- Channel list scroll
- Active channel highlight
- Unread indicators

### Responsive:
- Desktop: Full layout (server list + channel sidebar + chat + member list)
- Tablet: Collapsible sidebar
- Mobile: Single panel with navigation

---

## 11. Real-time Code Patterns

### Socket Event Naming:
- Use verb-first pattern: `sendMessage`, `joinChannel`, `typingStart`
- Use past tense for server-to-client events: `messageReceived`, `memberJoined`
- Prefix related events: `voice:join`, `voice:leave`, `voice:mute`

### Socket Room Management:
- Join room khi vao server/channel
- Leave room khi roi server/channel
- Clean up khi disconnect
- Always validate permissions truoc khi join room

### Optimistic Updates:
- Hien thi tin nhan ngay khi gui (optimistic)
- Cap nhat trang thai khi server xac nhan
- Rollback neu bi loi
- Hien thi indicator cho tin nhan dang gui

---

## 12. Security Rules

### Authentication:
- JWT tokens cho API requests
- Socket authentication khi connect
- Token refresh mechanism
- Khong luu sensitive data tren client

### Authorization:
- Kiem tra permission o moi API endpoint
- Kiem tra permission o moi socket event
- Server-side validation cho moi input
- Rate limiting cho API va socket events

### Data Validation:
- Validate input ca client va server side
- Sanitize HTML trong tin nhan
- Gioi han file upload size
- Validate file types truoc khi upload

---

## Enforcement

- **Pre-commit checks**: Run linter and type checker
- **Code review**: All code must follow these standards
- **Automated checks**: CI/CD should validate standards

---

## Quick Reference Checklist

Truoc khi commit code, dam bao:
- [ ] No emojis in code files
- [ ] No emojis in documentation
- [ ] Comments are clear and purposeful
- [ ] User-facing content is in English
- [ ] Code follows naming conventions
- [ ] Error handling is proper (HTTP + WebSocket)
- [ ] TypeScript types are used correctly
- [ ] Socket events are typed and validated
- [ ] Permissions are checked server-side
- [ ] UI handles long content gracefully
- [ ] Chat scroll behavior works correctly
- [ ] Real-time features handle disconnect/reconnect
