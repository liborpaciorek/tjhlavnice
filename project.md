# TJ Družba Hlavnice Website

A modern Django website for TJ Družba Hlavnice soccer club featuring news, matches, standings, team lineup, management, calendar, gallery, and more.

## Features

- 📰 News management with images
- ⚽ Match results and upcoming fixtures
- 📊 League standings with highlighting for club teams
- 👥 Team lineup with player details
- 🏛️ Management team information
- 📅 Event calendar
- 🖼️ Photo gallery with lightbox
- 📱 Fully responsive design with mobile-friendly navigation
- 🎨 Modern design using TailwindCSS and BasecoatUI
- 📊 Page visit tracking and analytics
- 🛡️ Admin panel for content management

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite3
- **Frontend**: TailwindCSS, BasecoatUI, VUE.js
- **Icons**: Font Awesome
- **Images**: Pillow for image handling

## Setup Instructions
- Login with: `admin` / `admin123` (if using sample superuser)
- Everything including Admin must be in Czech language.

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Key Models

- **ClubInfo**: Club information and history
- **News**: News articles with images, add posibility to share news over link or Facebook
- **Team**: Team information
- **Player**: Player details with positions
- **Management**: Club management team
- **Match**: Match fixtures and results
- **Standing**: League standings
- **Event**: Calendar events
- **Gallery**: Photo gallery, add posibility to share pictures all albums over link or Facebook
- **PageVisit**: Analytics tracking
- **MainPage**: Contains latest news samples, one upcoming and two past matches with results, standing postion of TJ Hlavnice with 2 above and two below teams in standings.

## Admin Panel Features

The admin panel provides comprehensive content management:

- Club information editing
- News article creation and management
- Leagues
- Teams, posibility to upload team flag
- Team and player management, posibility to upload players and management photos.
- Match result tracking
- Standing tables management, with highlite of TJ Hlavnice.
- Event calendar
- Photo gallery management
- Page visit analytics

## Design Features

- **Responsive Design**: Works on all devices
- **Modern UI**: Clean, professional design with red and black theme
- **Mobile Menu**: Collapsible navigation for mobile devices
- **Interactive Elements**: Hover effects, smooth transitions
- **Accessibility**: Proper semantic HTML and ARIA labels

## Customization

### Colors

The website uses a custom color scheme defined in TailwindCSS configuration:

- Primary Red: #5f0909ff
- Dark Red: #991B1B
- Black: #111827
- Gray: #374151

### Content Management

All content can be managed through the Django admin panel:

1. Log in to `/admin/`
2. Use the intuitive interface to add/edit content
3. Changes appear immediately on the website

## Support

For support or questions about the website, contact the club administrators through the admin panel.

---

**TJ Družba Hlavnice** - Tradice od roku 1952
