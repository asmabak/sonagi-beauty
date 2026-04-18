/**
 * Sonagi Beauty — Schedule Review Script
 *
 * Usage:
 *   node scheduler/review.js          Show next 7 days of scheduled content
 *   node scheduler/review.js --all    Show all remaining pending posts
 *
 * Displays date, time, type, topic, and caption preview for each scheduled post.
 */

const fs = require('fs');
const path = require('path');

const SCHEDULE_PATH = path.join(__dirname, 'schedule.json');

function loadSchedule() {
  const raw = fs.readFileSync(SCHEDULE_PATH, 'utf-8');
  return JSON.parse(raw);
}

function truncate(str, len) {
  if (!str) return '(none)';
  const clean = str.replace(/\n/g, ' ');
  return clean.length > len ? clean.substring(0, len) + '...' : clean;
}

function getTopicFromFolder(folder) {
  if (!folder) return '-';
  const parts = folder.replace(/\\/g, '/').split('/');
  const last = parts[parts.length - 1];
  // Extract topic from folder name like "may01-7secondes"
  const match = last.match(/^may\d+-(.+)$/);
  return match ? match[1].replace(/-/g, ' ') : last;
}

function main() {
  const args = process.argv.slice(2);
  const showAll = args.includes('--all');

  const schedule = loadSchedule();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const sevenDaysLater = new Date(today);
  sevenDaysLater.setDate(sevenDaysLater.getDate() + 7);

  const pending = schedule.posts.filter(p => p.status === 'pending');
  const posted = schedule.posts.filter(p => p.status === 'posted');

  let filtered;
  if (showAll) {
    filtered = pending;
  } else {
    filtered = pending.filter(p => {
      const d = new Date(p.date);
      return d >= today && d < sevenDaysLater;
    });
    // If no posts in the next 7 days, show the next 14 pending posts
    if (filtered.length === 0) {
      filtered = pending.slice(0, 14);
    }
  }

  // Header
  console.log('');
  console.log('  ╔══════════════════════════════════════════════════════════════════════════════════╗');
  console.log('  ║                    SONAGI BEAUTY — SCHEDULE REVIEW                              ║');
  console.log('  ╚══════════════════════════════════════════════════════════════════════════════════╝');
  console.log('');
  console.log(`  Progress: ${posted.length} posted / ${pending.length} pending / ${schedule.posts.length} total`);
  console.log(`  Showing:  ${showAll ? 'ALL pending posts' : 'Next 7 days (or next 14 pending)'}`);
  console.log('');

  if (filtered.length === 0) {
    console.log('  No upcoming posts found.\n');
    return;
  }

  // Table header
  console.log('  ┌────────────┬───────┬───────────┬─────────────────────────┬────────────────────────────────────────────────────┐');
  console.log('  │ Date       │ Time  │ Type      │ Topic                   │ Caption / Script                                   │');
  console.log('  ├────────────┼───────┼───────────┼─────────────────────────┼────────────────────────────────────────────────────┤');

  let currentDate = '';
  for (const post of filtered) {
    const dateStr = post.date === currentDate ? '          ' : post.date;
    currentDate = post.date;

    const time = post.time;
    const type = post.type.padEnd(9);

    let topic, preview;
    if (post.type === 'carousel') {
      topic = truncate(getTopicFromFolder(post.slides_folder), 23).padEnd(23);
      preview = truncate(post.caption, 50).padEnd(50);
    } else {
      topic = '(story)'.padEnd(23);
      preview = truncate(post.story_script, 50).padEnd(50);
    }

    console.log(`  │ ${dateStr} │ ${time} │ ${type} │ ${topic} │ ${preview} │`);
  }

  console.log('  └────────────┴───────┴───────────┴─────────────────────────┴────────────────────────────────────────────────────┘');
  console.log('');
  console.log('  Commands:');
  console.log('    node scheduler/post.js --preview   Preview next post');
  console.log('    node scheduler/post.js             Post next pending item');
  console.log('    node scheduler/review.js --all     Show all remaining posts');
  console.log('');
}

main();
