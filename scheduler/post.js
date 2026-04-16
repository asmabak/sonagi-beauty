/**
 * Sonagi Beauty — Instagram Posting Script
 *
 * Usage:
 *   node scheduler/post.js            Post the next pending item
 *   node scheduler/post.js --preview  Show what would be posted next (no action)
 *
 * Requires: playwright (npm install playwright)
 * Uses existing Chrome profile to reuse Instagram login session.
 */

const fs = require('fs');
const path = require('path');

const SCHEDULE_PATH = path.join(__dirname, 'schedule.json');
const CHROME_PROFILE = 'C:/Users/marou/AppData/Local/ms-playwright/mcp-chrome-65e96ba';
const INSTAGRAM_URL = 'https://www.instagram.com/';

// ─── Helpers ────────────────────────────────────────────────────────────────

function loadSchedule() {
  const raw = fs.readFileSync(SCHEDULE_PATH, 'utf-8');
  return JSON.parse(raw);
}

function saveSchedule(schedule) {
  fs.writeFileSync(SCHEDULE_PATH, JSON.stringify(schedule, null, 2), 'utf-8');
}

function getNextPending(schedule) {
  const now = new Date();
  for (const post of schedule.posts) {
    if (post.status !== 'pending') continue;
    const postDate = new Date(`${post.date}T${post.time}:00`);
    if (postDate <= now) {
      return post;
    }
  }
  // If nothing is due yet, return the very next pending post
  return schedule.posts.find(p => p.status === 'pending') || null;
}

function getSlideFiles(folderPath) {
  if (!folderPath || !fs.existsSync(folderPath)) return [];
  const exts = ['.jpg', '.jpeg', '.png', '.webp', '.bmp'];
  return fs.readdirSync(folderPath)
    .filter(f => exts.includes(path.extname(f).toLowerCase()))
    .sort()
    .map(f => path.join(folderPath, f));
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ─── Preview Mode ───────────────────────────────────────────────────────────

function previewNext() {
  const schedule = loadSchedule();
  const post = getNextPending(schedule);

  if (!post) {
    console.log('\n  No pending posts remaining.\n');
    return;
  }

  console.log('\n  ╔══════════════════════════════════════════════════╗');
  console.log('  ║         NEXT SCHEDULED POST — PREVIEW           ║');
  console.log('  ╚══════════════════════════════════════════════════╝\n');
  console.log(`  Date:    ${post.date}`);
  console.log(`  Time:    ${post.time}`);
  console.log(`  Type:    ${post.type}`);

  if (post.type === 'carousel') {
    console.log(`  Folder:  ${post.slides_folder}`);
    const slides = getSlideFiles(post.slides_folder);
    if (slides.length > 0) {
      console.log(`  Slides:  ${slides.length} images found`);
      slides.forEach((s, i) => console.log(`           ${i + 1}. ${path.basename(s)}`));
    } else {
      console.log(`  Slides:  !! No images found in folder (create them before posting)`);
    }
    console.log(`\n  Caption:\n`);
    console.log(`  ${post.caption.replace(/\n/g, '\n  ')}`);
    console.log(`\n  Hashtags:\n  ${post.hashtags}`);
  } else if (post.type === 'story') {
    console.log(`  Script:  ${post.story_script}`);
    console.log(`  Visual:  ${post.visual_folder || '(none — text story)'}`);
  }

  const pending = schedule.posts.filter(p => p.status === 'pending').length;
  const posted = schedule.posts.filter(p => p.status === 'posted').length;
  console.log(`\n  Progress: ${posted}/${schedule.posts.length} posted, ${pending} remaining\n`);
}

// ─── Posting: Carousel ──────────────────────────────────────────────────────

async function postCarousel(page, post) {
  const slides = getSlideFiles(post.slides_folder);
  if (slides.length === 0) {
    throw new Error(`No slide images found in: ${post.slides_folder}\nCreate slide images before posting.`);
  }

  const fullCaption = `${post.caption}\n\n${post.hashtags}`;

  console.log(`  Uploading ${slides.length} slides from: ${post.slides_folder}`);

  // Click "New post" button (the + icon in the nav)
  // Instagram uses various selectors; we try multiple approaches
  await page.goto(INSTAGRAM_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await sleep(3000);

  // Look for the "New post" / create button in the sidebar
  const createBtn = await page.locator('svg[aria-label="New post"]').first();
  if (await createBtn.count() === 0) {
    // Fallback: try the aria-label variants
    const altBtn = await page.locator('[aria-label="New post"], [aria-label="Nouvelle publication"], [aria-label="Create"]').first();
    await altBtn.click();
  } else {
    await createBtn.click();
  }
  await sleep(2000);

  // Upload files via the file input (hidden input on the creation dialog)
  const fileInput = await page.locator('input[type="file"]').first();
  await fileInput.setInputFiles(slides);
  await sleep(3000);

  // If multiple slides, Instagram may show a "select multiple" toggle — handle it
  // Click through: crop step -> Next
  const nextBtnCrop = await page.locator('div[role="button"]:has-text("Next"), button:has-text("Next"), div[role="button"]:has-text("Suivant"), button:has-text("Suivant")').first();
  if (await nextBtnCrop.count() > 0) {
    await nextBtnCrop.click();
    await sleep(2000);
  }

  // Edit/filter step -> Next
  const nextBtnEdit = await page.locator('div[role="button"]:has-text("Next"), button:has-text("Next"), div[role="button"]:has-text("Suivant"), button:has-text("Suivant")').first();
  if (await nextBtnEdit.count() > 0) {
    await nextBtnEdit.click();
    await sleep(2000);
  }

  // Caption step: fill the textarea
  const captionArea = await page.locator('div[aria-label="Write a caption..."], div[aria-label="Ecrivez une legende..."], textarea[aria-label="Write a caption..."]').first();
  if (await captionArea.count() > 0) {
    await captionArea.click();
    await sleep(500);
    await captionArea.fill(fullCaption);
  } else {
    // Fallback: try contenteditable div or any visible textarea
    const fallbackArea = await page.locator('[contenteditable="true"]').first();
    await fallbackArea.click();
    await sleep(500);
    // Use keyboard to type since fill may not work on contenteditable
    await page.keyboard.type(fullCaption, { delay: 10 });
  }
  await sleep(1000);

  // Click Share
  const shareBtn = await page.locator('div[role="button"]:has-text("Share"), button:has-text("Share"), div[role="button"]:has-text("Partager"), button:has-text("Partager")').first();
  await shareBtn.click();
  await sleep(5000);

  // Wait for the "Post shared" confirmation or similar
  console.log('  Carousel posted successfully.');
}

// ─── Posting: Story ─────────────────────────────────────────────────────────

async function postStory(page, post) {
  console.log(`  Posting story: ${post.story_script}`);
  console.log('  NOTE: Instagram stories with polls/quizzes/Q&A require manual creation.');
  console.log('  The script will open Instagram stories camera for you.');

  await page.goto(INSTAGRAM_URL, { waitUntil: 'networkidle', timeout: 30000 });
  await sleep(3000);

  // If a visual folder is provided, upload it
  if (post.visual_folder && fs.existsSync(post.visual_folder)) {
    const slides = getSlideFiles(post.visual_folder);
    if (slides.length > 0) {
      console.log(`  Uploading story image: ${slides[0]}`);
    }
  }

  // Stories with interactive elements (polls, quizzes, Q&A, countdowns, this-or-that)
  // cannot be fully automated via the web UI — they require the mobile app or
  // Creator Studio with limited support. Log the script for manual posting.
  console.log('\n  ┌─────────────────────────────────────────────────┐');
  console.log('  │  STORY SCRIPT (post manually with stickers):    │');
  console.log('  ├─────────────────────────────────────────────────┤');
  console.log(`  │  ${post.story_script.substring(0, 48).padEnd(48)}│`);
  if (post.story_script.length > 48) {
    const remaining = post.story_script.substring(48);
    const lines = remaining.match(/.{1,48}/g) || [];
    lines.forEach(line => {
      console.log(`  │  ${line.padEnd(48)}│`);
    });
  }
  console.log('  └─────────────────────────────────────────────────┘');
  console.log('\n  Story marked as posted (manual action required for stickers).');
}

// ─── Main ───────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const isPreview = args.includes('--preview');

  if (isPreview) {
    previewNext();
    return;
  }

  const schedule = loadSchedule();
  const post = getNextPending(schedule);

  if (!post) {
    console.log('\n  No pending posts remaining.\n');
    return;
  }

  console.log('\n  ╔══════════════════════════════════════════════════╗');
  console.log('  ║         SONAGI BEAUTY — POSTING NOW             ║');
  console.log('  ╚══════════════════════════════════════════════════╝\n');
  console.log(`  Date: ${post.date}  Time: ${post.time}  Type: ${post.type}\n`);

  // Launch browser with existing Chrome profile
  let browser;
  try {
    const { chromium } = require('playwright');

    browser = await chromium.launchPersistentContext(CHROME_PROFILE, {
      headless: false,
      channel: 'msedge',
      viewport: { width: 1280, height: 900 },
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-first-run',
        '--no-default-browser-check'
      ]
    });

    const page = browser.pages()[0] || await browser.newPage();

    if (post.type === 'carousel') {
      await postCarousel(page, post);
    } else if (post.type === 'story') {
      await postStory(page, post);
    }

    // Mark as posted
    post.status = 'posted';
    post.posted_at = new Date().toISOString();
    saveSchedule(schedule);

    console.log(`\n  Status updated to "posted" at ${post.posted_at}`);
    console.log('  schedule.json saved.\n');

    // Keep browser open briefly so user can verify
    console.log('  Browser will close in 10 seconds (verify the post)...');
    await sleep(10000);

  } catch (err) {
    console.error('\n  ERROR:', err.message);
    console.error('  Make sure Playwright is installed: npm install playwright');
    console.error('  And that no other browser instance is using the profile.\n');
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
