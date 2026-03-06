# Camp - Tien Do Phat Trien

Tong hop trang thai cac tinh nang da xong va viec tiep theo can lam.

---

## 1. Da Hoan Thanh

### Core
- Invite link `/invite/:code`, preview API
- Spoiler `||text||`, DM markdown, rate limit
- User profile popup (click avatar)
- @mentions, emoji picker, link preview
- Notifications, Inbox panel
- Add Friend (search by username), friend real-time
- Auth: refresh truoc getMe
- Responsive, accessibility
- Channel message cache (instant khi quay lai channel)
- Loading screens (app load, join invite)
- Server Profile: icon, banner (color/image)
- Invite page: full-screen, background, Join/Cancel
- Server templates (Gaming, Study, Community, Work, Default)
- Invisible status (hien offline nhung van dung app)
- Loading skeleton, optimistic updates, keyboard shortcuts

### Server Settings
- Overview: name, icon, banner, description
- Roles, Bans, Audit Log
- Invites: xem code, copy link, tao link moi

### User Settings
- My Account: username, display name, avatar, password
- Profile: activity status
- Notifications: desktop on/off, muted servers

### Scalability (danh sach lon)
- MemberList: search + virtualization (react-window) khi > 50
- getServerMembers: pagination (200), server-side search
- Add Members: server-side search
- MentionAutocomplete: limit 50 members, 15 roles

---

## 2. Tiep Theo Can Lam

### Uu tien cao
| Tinh nang | Mo ta |
|-----------|-------|
| Threads | Reply threads cho tung message |
| Phase 2b Settings | Privacy (Allow DMs, Friend requests), Notifications sound |

### Uu tien trung binh
| Tinh nang | Mo ta |
|-----------|-------|
| Slash commands | `/help`, `/giphy`... |
| Custom status | Emoji + text (vd: "Playing X") |
| Theme toggle | Light / Dark / System |
| User Settings | Bo sung trang cai dat day du |

### Uu tien thap / Optional
| Tinh nang | Mo ta |
|-----------|-------|
| Email change | Verify qua email |
| Server verification level | None / Low / Medium |
| Invite max uses | Gioi han nguoi join qua 1 link |
| DMSidebar virtualization | Khi 100+ DMs |
| InboxPanel virtualization | Khi 100+ notifications |

---

## 3. Tham Chieu

- `docs/guides/setup-guide.md` - Setup database, Cloudinary, env
- `docs/project-overview.md` - Kien truc, data model
- `docs/features.md` - Chi tiet 15 tinh nang + bo sung
- `docs/standards/code.md` - Quy tac code
- `docs/standards/design-system.md` - Design system
