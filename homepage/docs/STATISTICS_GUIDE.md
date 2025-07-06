# Statistics Tracker Documentation

## Overview
The homepage now includes a comprehensive statistics tracking system that monitors visitor activity and content statistics in both English and Japanese.

## Features

### 📊 Visitor Statistics
- **Daily Visitors**: Number of unique visitors today (本日の訪問者)
- **Total Visitors**: Cumulative count of all visitors (総訪問者数)
- **Weekly Visitors**: Visitors in the last 7 days (週間訪問者数)

### 📚 Content Statistics
- **Total Posts**: Combined count of all content (総投稿数)
- **Journal Entries**: Number of journal posts (日記エントリー)
- **Garden Notes**: Number of notes in the garden (ガーデンノート)
- **References**: Number of reference materials (参考文献)

## How It Works

### Visitor Tracking
- Each unique session is tracked per day
- Uses Django session framework for identification
- IP address and user agent are stored for analytics
- Daily visitor counts are automatically maintained

### Data Models
- `VisitorTracking`: Stores daily visitor counts
- `VisitorSession`: Tracks individual visitor sessions

### Privacy & Performance
- Only session keys and IP addresses are stored
- No personal information is collected
- Old visitor data can be cleaned up using management commands

## Management Commands

### Cleanup Old Data
```bash
python manage.py cleanup_visitor_data --days 90
```

Options:
- `--days`: Number of days to keep (default: 90)
- `--dry-run`: Show what would be deleted without deleting

## Admin Interface
- View daily visitor statistics in Django admin
- Monitor individual visitor sessions
- Track content growth over time

## Styling
The statistics section features:
- Responsive card-based layout
- Smooth hover animations
- Bilingual display (English/Japanese)
- Ninja/samurai themed design
- Mobile-friendly responsive design

## Technical Details
- Automatic visitor tracking on homepage load
- Real-time content counting
- Efficient database queries with aggregation
- Caching-friendly architecture
