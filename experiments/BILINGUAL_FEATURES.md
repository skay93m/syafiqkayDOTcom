# Experiments App - Bilingual Features

## Overview
The experiments app templates have been updated to include bilingual support, displaying both English and Japanese text with ruby annotations, following the same pattern as other apps in the project.

## Bilingual Elements

### Dashboard Template (`dashboard.html`)
- **Header**: Lab title with Japanese ruby annotations
- **Statistics Cards**: All stat cards include Japanese labels
- **Experiment Status**: Status badges with Japanese translations
- **Experiment Metadata**: Creation/update dates in Japanese format
- **Hypothesis Preview**: Bilingual hypothesis labels
- **Resource Count**: Japanese resource count display
- **Action Buttons**: Bilingual action buttons for better UX
- **Pagination**: Japanese pagination info

### Detail Template (`experiment_detail.html`)
- **Breadcrumb Navigation**: Bilingual breadcrumbs
- **Status Information**: Status badges with Japanese translations
- **Meta Information**: Dates displayed in Japanese format
- **Section Headers**: All sections (Hypothesis, Methodology, Results, etc.) with Japanese translations
- **Progress Tracking**: Bilingual progress steps
- **Action Buttons**: Bilingual navigation and edit buttons

## Japanese Translations Used

### Status Translations
- **Conceptualizing** → 構想中 (こうそうちゅう)
- **Designing** → 設計中 (せっけいちゅう)
- **Testing** → 実験中 (じっけんちゅう)
- **Analyzing** → 分析中 (ぶんせきちゅう)
- **Completed** → 完了 (かんりょう)
- **Abandoned** → 中止 (ちゅうし)

### Section Translations
- **Hypothesis** → 仮説 (かせつ)
- **Methodology** → 方法論 (ほうほうろん)
- **Results** → 結果 (けっか)
- **Conclusions** → 結論 (けつろん)
- **Resources** → 資料 (しりょう)
- **Progress** → 進捗 (しんちょく)
- **Actions** → アクション (Action)

### Interface Elements
- **Total Experiments** → 全実験 (ぜんじっけん)
- **Published Experiments** → 公開実験 (こうかいじっけん)
- **Pages** → ページ (Page)
- **Current Experiments** → 現在の実験 (げんざいのじっけん)
- **Created** → 作成 (さくせい)
- **Updated** → 更新 (こうしん)
- **Tags** → タグ (Tag)
- **Quick Actions** → クイックアクション (Quick Action)

## CSS Styling
- **Japanese text** uses `jp-text japanese-text` classes
- **Smaller font size** for Japanese text for better readability
- **Consistent color scheme** with existing app styling
- **Ruby annotations** for proper pronunciation guidance

## Date Formatting
- **English**: "M d, Y" format (e.g., "Jul 8, 2025")
- **Japanese**: "Y年m月d日" format (e.g., "2025年7月8日")

## Implementation Notes
- All bilingual elements follow the same pattern as other apps
- Japanese text is properly styled with appropriate CSS classes
- Ruby annotations provide pronunciation guidance
- Responsive design maintains readability on all devices
- No data translation required - only interface elements are bilingual

## Future Enhancements
- Consider adding language toggle functionality
- Add more detailed Japanese explanations for complex scientific terms
- Implement Japanese text search capabilities
- Add Japanese-specific date/time formatting preferences
