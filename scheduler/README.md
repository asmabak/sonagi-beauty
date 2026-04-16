# Sonagi Beauty — Instagram Posting Scheduler

Automated posting system for Sonagi Beauty's Instagram account. May 2026 content calendar with 62 entries (31 days x 2 posts/day).

## Setup

```bash
cd C:\Users\marou\sonagi-beauty
npm install playwright
```

The script uses the existing Chrome/Edge browser profile at:
```
C:\Users\marou\AppData\Local\ms-playwright\mcp-chrome-65e96ba
```

Make sure you are logged into Instagram in that browser profile before running the posting script.

## Commands

### Review upcoming posts

```bash
node scheduler/review.js
```

Shows the next 7 days of scheduled content in a table: date, time, type, topic, and caption preview (first 50 chars).

```bash
node scheduler/review.js --all
```

Shows ALL remaining pending posts.

### Preview next post

```bash
node scheduler/post.js --preview
```

Shows full details of the next pending post without taking any action. Displays:
- Date, time, and type
- Slide images found in the folder (for carousels)
- Full caption and hashtags
- Story script (for stories)
- Overall progress count

### Post the next item

```bash
node scheduler/post.js
```

Opens a browser, logs into Instagram using the saved session, and posts the next pending item:
- **Carousel posts**: uploads all slide images from the folder, fills the caption + hashtags, and clicks Share
- **Story posts**: displays the story script for manual posting (stories with interactive stickers like polls/quizzes/Q&A cannot be fully automated via web)

After posting, updates `schedule.json` with `"status": "posted"` and a `"posted_at"` timestamp.

## Schedule Structure

`schedule.json` contains 62 entries:
- **Morning (12:00)**: Carousel posts — educational K-beauty content
- **Afternoon (18:00)**: Story posts — polls, quizzes, Q&A, this-or-that, countdowns

Each carousel entry points to a `slides_folder` where the slide images should be placed before posting. Create the images and save them in the correct folder before running the post script.

### Folder structure for slides

```
C:/Users/marou/images/2026-04-16/may-content/
  week1/
    may01-7secondes/     (slide1.png, slide2.png, ...)
    may02-3serums/
    ...
  week2/
    may08-centella/
    ...
  week3/
    may15-routine-7etapes/
    ...
  week4/
    may22-10erreurs/
    ...
  week5/
    may29-bilan-mois/
    ...
```

## Skip or Reschedule a Post

To **skip** a post, edit `schedule.json` and change its status:
```json
{
  "status": "skipped"
}
```

To **reschedule** a post, change the `date` and/or `time` fields:
```json
{
  "date": "2026-05-15",
  "time": "14:00"
}
```

The posting script always picks the next `"pending"` entry whose date/time has passed (or the earliest pending if none are due yet).

## Automated Daily Runs with Windows Task Scheduler

To automate posting, set up two tasks in Windows Task Scheduler:

### Morning post (carousel at 12:00)

1. Open **Task Scheduler** (search "Task Scheduler" in Start)
2. Click **Create Basic Task**
3. Name: `Sonagi Morning Post`
4. Trigger: **Daily**, start date 2026-05-01, time **12:00**
5. Action: **Start a program**
   - Program: `node`
   - Arguments: `C:\Users\marou\sonagi-beauty\scheduler\post.js`
   - Start in: `C:\Users\marou\sonagi-beauty`
6. Finish

### Afternoon post (story at 18:00)

1. Create another Basic Task
2. Name: `Sonagi Afternoon Post`
3. Trigger: **Daily**, start date 2026-05-01, time **18:00**
4. Action: **Start a program**
   - Program: `node`
   - Arguments: `C:\Users\marou\sonagi-beauty\scheduler\post.js`
   - Start in: `C:\Users\marou\sonagi-beauty`
5. Finish

### Important notes for Task Scheduler

- The computer must be **on and unlocked** for Playwright to open a visible browser
- If using a laptop, disable sleep/hibernate during posting times
- Under task Properties > Conditions, uncheck "Start only if computer is on AC power"
- Under Settings, check "Run task as soon as possible after a scheduled start is missed"
- Story posts will open the browser but require manual sticker placement (polls, quizzes, etc.)

### Alternative: PowerShell one-liner to create tasks

```powershell
# Morning post at 12:00
schtasks /create /tn "Sonagi Morning Post" /tr "node C:\Users\marou\sonagi-beauty\scheduler\post.js" /sc daily /st 12:00 /sd 2026/05/01

# Afternoon post at 18:00
schtasks /create /tn "Sonagi Afternoon Post" /tr "node C:\Users\marou\sonagi-beauty\scheduler\post.js" /sc daily /st 18:00 /sd 2026/05/01
```

## Troubleshooting

- **"No slide images found"**: Create the carousel slide images in the folder listed in `slides_folder` before posting
- **Browser won't open**: Make sure no other browser is using the Chrome profile. Close all Edge/Chrome instances first
- **Instagram session expired**: Open Edge manually, go to instagram.com, log in, then try again
- **Playwright not found**: Run `npm install playwright` in the project directory
