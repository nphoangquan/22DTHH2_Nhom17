# Camp - Design System

Dark Theme UI Design Guidelines cho Camp - Realtime Chat Application.
Lay cam hung tu Discord, toi uu cho giao dien chat voi dark color scheme lam chu dao.

---

## Design Philosophy

### Core Principles

**1. Dark-First Design**
- Giao dien toi la mac dinh va duy nhat
- Giam moi mat khi su dung thoi gian dai
- Tao cam giac tap trung vao noi dung chat
- Phan biet cac layers bang do sang, khong bang mau sac

**2. Functional Clarity**
- Moi element phai co muc dich ro rang
- Giao dien phuc vu giao tiep, khong phuc vu trang tri
- Hierarchy thong tin ro rang: server > channel > messages
- Navigation truc quan, khong can hoc

**3. Real-time Responsive**
- UI phan hoi nhanh voi moi thay doi
- Trang thai online/offline ro rang
- Typing indicators, unread badges cap nhat tuc thi
- Transitions muot ma nhung khong gay phan tan

**4. Density Balance**
- Du compact de hien thi nhieu thong tin
- Du thoang de khong bi roi mat
- Chat messages can khoang cach hop ly
- Sidebar compact nhung van de doc

---

## Color Palette

### Background Layers (Dark to Light)

Hệ thống layer: mỗi layer cao hơn sẽ sáng hơn một chút, tạo cảm giác "nổi" lên.

```
Layer 0 - Base:       #0c0c10   Server navigation bar (darkest)
Layer 1 - Primary:    #121217   Channel sidebar, member list
Layer 2 - Secondary:  #1a1a21   Main chat area
Layer 3 - Tertiary:   #222229   Input fields, cards, elevated elements
Layer 4 - Hover:      #2a2a33   Hover states, dropdowns
Layer 5 - Active:     #33333d   Active states, selected items
Layer 6 - Highlight:  #3d3d48   Strong highlight, focus rings
```

### Text Colors

```
text-primary:    #FFFFFF    Headings, ten server, ten user
text-secondary:  #B5BAC1    Body text, noi dung tin nhan
text-muted:      #80848E    Timestamps, secondary info
text-subtle:     #5C5F66    Placeholders, disabled text
text-link:       #6C8CFF    Links trong tin nhan
```

### Accent Color (Brand)

Mau chu dao cua Camp - Indigo Blue, noi bat tren nen toi.

```
accent-50:    #EEF0FF    Subtle backgrounds
accent-100:   #D9DDFF    Badges, notifications bg
accent-200:   #B3BAFF    Light accent elements
accent-400:   #818CF8    Hover states
accent-500:   #6366F1    Primary brand color - buttons, links, active states
accent-600:   #4F46E5    Pressed/active states
accent-700:   #4338CA    Deep accent
accent-900:   #312E81    Darkest accent
```

**Usage:**
- `accent-500` (#6366F1): Primary buttons, active navigation, links
- `accent-400` (#818CF8): Hover states
- `accent-600` (#4F46E5): Pressed states
- `accent-100` (#D9DDFF): Notification badges, subtle indicators

### Semantic Colors

**Online Status (Green)**
```
online:       #3BA55D    Online indicator dot
online-bg:    #3BA55D20  Subtle background
```

**Idle Status (Amber)**
```
idle:         #FAA61A    Idle indicator
idle-bg:      #FAA61A20  Subtle background
```

**Do Not Disturb (Red)**
```
dnd:          #ED4245    DND indicator
dnd-bg:       #ED424520  Subtle background
```

**Offline (Gray)**
```
offline:      #80848E    Offline indicator
```

**Success**
```
success-400:  #4ADE80    Success text on dark
success-500:  #22C55E    Success indicators
success-bg:   #22C55E15  Success subtle background
```

**Warning**
```
warning-400:  #FBBF24    Warning text on dark
warning-500:  #F59E0B    Warning indicators
warning-bg:   #F59E0B15  Warning subtle background
```

**Danger/Error**
```
danger-400:   #F87171    Error text on dark
danger-500:   #EF4444    Error indicators, destructive actions
danger-bg:    #EF444415  Error subtle background
```

### Color Usage Rules

**DO:**
- Su dung background layers de tao chieu sau
- Su dung accent-500 cho cac hanh dong chinh (sparingly)
- Su dung semantic colors chi khi can thiet
- Dam bao contrast ratio toi thieu 4.5:1 cho text
- Su dung opacity thay vi mau moi cho hover states

**DON'T:**
- Khong su dung mau sang lam background
- Khong su dung nhieu mau accent cung luc
- Khong su dung pure black (#000000) lam background chinh
- Khong su dung text-subtle cho noi dung quan trong

---

## Typography

### Font Family

**Primary Font:** Inter
- Clean, modern, doc tot tren nen toi
- Ho tro tieng Viet tot

**Monospace Font:** JetBrains Mono / Fira Code
- Dung cho code blocks trong chat
- Dung cho message timestamps (optional)

**Usage:**
```css
--font-primary: 'Inter', system-ui, -apple-system, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### Font Sizes

**Hierarchy:**
```
text-2xl:  1.5rem / 24px    Server name, page titles
text-xl:   1.25rem / 20px   Section headings, modal titles
text-lg:   1.125rem / 18px  Channel group headers
text-base: 1rem / 16px      Message content, body text (default)
text-sm:   0.875rem / 14px  Channel names, usernames, labels
text-xs:   0.75rem / 12px   Timestamps, badges, captions
text-2xs:  0.625rem / 10px  Micro labels (online count)
```

### Font Weights

```
font-bold:     700   Server name, headings
font-semibold: 600   Channel names (active), usernames
font-medium:   500   Channel names, labels, buttons
font-normal:   400   Message content (default)
font-light:    300   Timestamps, secondary info
```

### Typography on Dark Background

**DO:**
- Su dung `text-secondary` (#B5BAC1) cho body text, khong dung pure white
- Su dung `text-primary` (#FFFFFF) chi cho headings va emphasized text
- Dam bao line-height thoai mai (1.5 - 1.6) cho message content
- Su dung letter-spacing nhe cho text-xs (0.02em)

**DON'T:**
- Khong dung pure white (#FFFFFF) cho body text (choi mat)
- Khong dung font-weight qua nhe (<300) tren nen toi
- Khong dung text nho hon 11px

---

## Layout Structure

### Main Application Layout

```
+-------+------------+------------------+----------+
|       |            |                  |          |
|Server | Channel    |   Main Chat      | Member   |
| List  | Sidebar    |   Area           | List     |
|       |            |                  |          |
| 72px  |   240px    |   flexible       |  240px   |
|       |            |                  |          |
| L0    |    L1      |     L2           |   L1     |
+-------+------------+------------------+----------+
```

**Server List (Left Bar):**
- Width: 72px (fixed)
- Background: Layer 0 (#0c0c10)
- Server icons: 48px circles
- Scrollable vertically

**Channel Sidebar:**
- Width: 240px (fixed, collapsible on mobile)
- Background: Layer 1 (#121217)
- Server name header + channel list + user panel

**Main Chat Area:**
- Width: Flexible (fill remaining space)
- Background: Layer 2 (#1a1a21)
- Header + message list + input

**Member List (Right Panel):**
- Width: 240px (toggleable)
- Background: Layer 1 (#121217)
- Online/offline member groups

### Chat Area Layout

```
+------------------------------------------+
| Channel Header (h-12, Layer 3)           |
| #channel-name | topic | actions          |
+------------------------------------------+
|                                          |
| Message List (scrollable, Layer 2)       |
| - Message groups by user                 |
| - Date separators                        |
| - Unread indicator                       |
|                                          |
+------------------------------------------+
| Typing Indicator (Layer 2)               |
+------------------------------------------+
| Message Input (Layer 3)                  |
| [+] Type a message...          [emoji]   |
+------------------------------------------+
```

---

## Spacing

### Spacing Scale

```
space-0.5: 2px    Micro spacing (icon gap)
space-1:   4px    Tight (inline elements)
space-2:   8px    Small (button padding, icon + text)
space-3:   12px   Medium-small (list item padding)
space-4:   16px   Standard (card padding, section gap)
space-5:   20px   Medium (channel sidebar padding)
space-6:   24px   Comfortable (message group gap)
space-8:   32px   Large (section spacing)
```

### Component-Specific Spacing

**Message Item:**
- Padding: 2px 16px (compact)
- Group gap (same author): 2px
- Group gap (different author): 16px
- Avatar size: 40px
- Avatar margin-right: 16px

**Channel List Item:**
- Padding: 6px 8px
- Border-radius: 4px
- Gap between icon and name: 8px

**Server Icon:**
- Size: 48px
- Gap between servers: 8px
- Border-radius: 16px (hover: 12px, animated)

---

## Components

### Server Icon

```
Default:     bg-layer-3, rounded-[24px], 48x48px
Hover:       bg-accent-500, rounded-[16px], transition 150ms
Active:      bg-accent-500, rounded-[16px]
Indicator:   Left bar 4px, rounded, accent-500
Unread:      Left bar 4px, rounded, text-primary
```

### Channel Item

```
Default:     text-muted, hover:text-secondary, hover:bg-layer-4
Active:      text-primary, bg-layer-5
Unread:      text-primary, font-semibold
Muted:       text-subtle, opacity-50
```

**Channel Types:**
- Text channel: Hash icon (#)
- Voice channel: Speaker icon
- Category: Collapsible header, uppercase text-xs

### Message Item

**Standard Message:**
```
+--+-------------------------------------------+
|  | Username          timestamp                |
|AV| Message content here                       |
|  | [reactions] [action buttons on hover]      |
+--+-------------------------------------------+
```

- Avatar: 40px circle, rounded-full
- Username: text-sm font-semibold, mau role cua user
- Timestamp: text-xs text-muted, hien khi hover (compact mode)
- Content: text-base text-secondary
- Hover: bg-layer-4 (subtle)

**Compact Message (same author, < 5 min gap):**
```
|  | Message content here              time     |
```
- Khong hien avatar va username
- Timestamp hien khi hover

**System Message:**
```
|     [icon] User joined the server             |
```
- Centered, text-muted, text-sm

### Message Input

```
Background:  Layer 3 (#222229)
Border:      1px solid Layer 5 (#33333d)
Focus:       border-accent-500
Placeholder: text-subtle
Text:        text-secondary
Padding:     12px 16px
Border-radius: 8px
```

**Buttons:**
- Attach file: left side
- Emoji picker: right side
- Send button: accent-500 (optional, Enter to send)

### Buttons

**Primary Button:**
```
bg: accent-500
text: white
hover: accent-400
active: accent-600
disabled: accent-500/50
border-radius: 4px
padding: 8px 16px
font-weight: 500
```

**Secondary Button:**
```
bg: Layer 4
text: text-secondary
hover: Layer 5
active: Layer 6
border-radius: 4px
```

**Danger Button:**
```
bg: danger-500
text: white
hover: danger-400
active: danger-600
```

**Ghost Button:**
```
bg: transparent
text: text-muted
hover: bg-layer-4, text-secondary
```

### Modal / Dialog

```
Overlay:     bg-black/60
Background:  Layer 1 (#121217)
Border:      none
Shadow:      0 8px 32px rgba(0,0,0,0.5)
Radius:      8px
Padding:     16px
Max-width:   440px (small), 600px (medium), 800px (large)
```

**Modal Header:**
- text-xl font-semibold text-primary
- Padding-bottom: 16px

**Modal Footer:**
- Background: Layer 0
- Padding: 16px
- Buttons aligned right

### Tooltips

```
Background:  #111214
Text:        text-secondary
Padding:     8px 12px
Radius:      4px
Font-size:   text-sm
Shadow:      0 4px 12px rgba(0,0,0,0.3)
```

### Badges

**Notification Badge:**
```
bg: danger-500
text: white
font-size: text-xs (12px)
min-width: 16px
height: 16px
border-radius: full
padding: 0 4px
```

**Role Badge:**
```
bg: role-color/20
text: role-color
border: 1px solid role-color/40
font-size: text-xs
padding: 2px 6px
border-radius: full
```

**Status Badge (Online/Idle/DND/Offline):**
```
size: 10px (small), 14px (medium)
border: 3px solid parent-bg (cut-out effect)
border-radius: full
```

### Scrollbar (Custom)

```css
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #1a1a21;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #222229;
}
```

---

## Shadows & Borders

### Shadows (on Dark)

Tren nen toi, shadow phai dam hon so voi light theme.

```
shadow-sm:     0 1px 2px rgba(0, 0, 0, 0.3)
shadow-md:     0 4px 12px rgba(0, 0, 0, 0.4)
shadow-lg:     0 8px 24px rgba(0, 0, 0, 0.5)
shadow-xl:     0 12px 48px rgba(0, 0, 0, 0.6)
shadow-popup:  0 8px 32px rgba(0, 0, 0, 0.5)
```

- Su dung `shadow-md` cho dropdowns, tooltips
- Su dung `shadow-lg` cho modals
- Su dung `shadow-popup` cho context menus

### Borders

```
border-subtle:  1px solid rgba(255, 255, 255, 0.06)
border-default: 1px solid rgba(255, 255, 255, 0.10)
border-strong:  1px solid rgba(255, 255, 255, 0.16)
border-accent:  1px solid accent-500/40
```

**Usage:**
- `border-subtle`: Dividers giua messages, thin separators
- `border-default`: Channel header bottom border, input borders
- `border-strong`: Focus states, emphasized sections
- `border-accent`: Active input focus

---

## Icons

### Icon Library: Lucide React

- Clean, consistent stroke icons
- Phu hop voi dark theme

### Icon Sizes

```
w-4 h-4:  16px   Button icons, badges, channel type
w-5 h-5:  20px   Navigation icons, action buttons
w-6 h-6:  24px   Header icons, feature icons
w-8 h-8:  32px   Empty states
w-10 h-10: 40px  Large empty states
```

### Icon Colors

```
Default:    text-muted (#80848E)
Hover:      text-secondary (#B5BAC1)
Active:     text-primary (#FFFFFF)
Accent:     accent-500 (#6366F1)
Danger:     danger-400 (#F87171)
Disabled:   text-subtle (#5C5F66)
```

---

## Interaction States

### Hover

- Message: bg-layer-4 (very subtle)
- Channel item: bg-layer-4
- Button: specified per variant
- Server icon: rounded-[16px] from rounded-[24px]

### Focus

- Input: border-accent-500, ring-2 ring-accent-500/20
- Button: ring-2 ring-accent-500/30 ring-offset-2 ring-offset-layer-2

### Active/Selected

- Channel: bg-layer-5, text-primary
- Server: bg-accent-500, rounded-[16px], left indicator
- Message (selected): bg-accent-500/10

### Transitions

```
Default:    transition-all duration-150 ease-out
Color:      transition-colors duration-100
Transform:  transition-transform duration-200
Opacity:    transition-opacity duration-150
Server icon: transition-all duration-200 (border-radius + color)
```

---

## Chat-Specific Patterns

### Message Group

Messages tu cung 1 user trong vong 5 phut duoc nhom lai:

```
[Avatar] Username    Today at 10:30 AM
         First message content
         Second message content (no avatar/name)
         Third message content

[Avatar] Different User    Today at 10:35 AM
         Their message
```

### Date Separator

```
--------------------- January 1, 2026 ---------------------
```

- Text: text-xs text-muted
- Line: border-subtle
- Background: Layer 2 (match chat bg)

### Unread Indicator

```
------------- NEW MESSAGES -------------------
```
- Text: danger-500
- Line: danger-500
- Appears above first unread message

### Typing Indicator

```
UserA is typing...
UserA, UserB are typing...
Several people are typing...
```
- Position: Below message list, above input
- Text: text-muted text-xs
- Animated dots

### Mention Highlight

```
Background:  accent-500/10
Border-left: 2px solid accent-500
```

### Emoji Reaction

```
Default:     bg-layer-3, border-subtle, rounded-md
Reacted:     bg-accent-500/15, border-accent-500/40
Count:       text-xs text-secondary
Hover:       bg-layer-4
Padding:     4px 8px
```

---

## Responsive Design

### Breakpoints

```
sm:   640px
md:   768px
lg:   1024px
xl:   1280px
2xl:  1536px
```

### Layout Behavior

**Desktop (>= 1024px):**
- Full layout: Server list + Channel sidebar + Chat + Member list
- Member list toggleable

**Tablet (768px - 1023px):**
- Server list + Chat area
- Channel sidebar overlay (slide in)
- Member list hidden, accessible via toggle

**Mobile (< 768px):**
- Single panel view
- Bottom navigation hoac hamburger menu
- Swipe gestures for navigation
- Full-screen chat view

### Touch Targets

- Minimum touch target: 44x44px
- Channel items: min-height 32px (desktop), 44px (mobile)
- Buttons: min-height 36px (desktop), 44px (mobile)

---

## Accessibility on Dark Theme

### Contrast Ratios (WCAG AA)

- text-primary (#FFF) on Layer 2 (#1a1a21): 14.3:1
- text-secondary (#B5BAC1) on Layer 2 (#1a1a21): 8.5:1
- text-muted (#80848E) on Layer 2 (#1a1a21): 4.5:1
- accent-500 (#6366F1) on Layer 2 (#1a1a21): 4.8:1

### Focus Indicators

- Tat ca interactive elements phai co visible focus ring
- Focus ring: 2px accent-500 voi offset
- Keyboard navigation support cho tat ca features

### Screen Readers

- Proper semantic HTML
- ARIA labels cho icon-only buttons
- Live regions cho new messages
- Role announcements cho status changes

---

## Animation Guidelines

### Allowed Animations

- Server icon border-radius transition (150-200ms)
- Sidebar slide in/out (200ms ease-out)
- Modal fade in (150ms)
- Tooltip appear (100ms)
- Message send (fade in, 100ms)
- Typing indicator dots (looping)

### Performance Rules

- Su dung `transform` va `opacity` cho animations (GPU-accelerated)
- Tranh animate `width`, `height`, `top`, `left`
- Su dung `will-change` cho elements animate thuong xuyen
- Tat animation khi `prefers-reduced-motion`

---

## Do's and Don'ts Summary

### DO

- Su dung he thong layer de tao chieu sau
- Giu mau accent sparingly (chi cho actions chinh)
- Dam bao contrast tot cho text tren dark bg
- Test UI trong dieu kien anh sang khac nhau
- Su dung subtle hover effects
- Giu chat messages de doc
- Toi uu performance cho danh sach tin nhan dai

### DON'T

- Khong dung pure black (#000) lam background
- Khong dung qua nhieu mau khac nhau
- Khong dung shadow qua dam (se bi "dirty" look)
- Khong dung bright colors lam background
- Khong dung text-primary (white) cho moi thu
- Khong dung animation qua nhieu
- Khong lam sidebar qua rong (> 300px)

---

## Component Checklist

Khi tao component moi, dam bao:
- [ ] Su dung dung background layer theo vi tri
- [ ] Text colors theo hierarchy (primary > secondary > muted > subtle)
- [ ] Hover va focus states ro rang
- [ ] Accessible (focus ring, ARIA labels)
- [ ] Responsive behavior defined
- [ ] Transitions smooth (150-200ms)
- [ ] Consistent voi cac component khac
- [ ] Khong lam giam performance chat

---

**Last Updated:** 2026

**Status:** Active Design System - Camp v1.0
