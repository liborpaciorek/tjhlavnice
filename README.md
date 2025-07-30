# TJ Družba Hlavnice Website

A modern Django website for TJ Družba Hlavnice soccer club featuring news, matches, standings, team lineup, management, calendar, gallery, and more.

![TJ Družba Hlavnice Logo](media/club/logo.png)

## 🚀 Quick Start

1. **Clone and setup the project:**

   ```bash
   git clone <repository-url>
   cd tjhlavnice2
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**

   ```bash
   python manage.py createsuperuser
   ```

   Or use the pre-configured admin account:

   - Username: `admin`
   - Password: `admin123`

6. **Load sample data (optional):**

   ```bash
   python manage.py populate_data
   ```

7. **Start development server:**

   ```bash
   python manage.py runserver
   ```

8. **Visit the website:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## ✨ Features

### 🏠 Main Features

- **📰 News Management** - Add, edit, and manage club news with images
- **⚽ Match System** - Track fixtures, results, and upcoming matches
- **📊 League Standings** - Display current league table with club highlighting
- **👥 Team Lineup** - Player profiles with photos, positions, and statistics
- **🏛️ Management Team** - Club officials with contact information
- **📅 Event Calendar** - Schedule and track club events
- **🖼️ Photo Gallery** - Image gallery with lightbox functionality
- **📊 Analytics** - Page visit tracking and statistics

### 🎨 Design Features

- **📱 Fully Responsive** - Works perfectly on all devices
- **🎨 Modern UI** - Clean design with red and black club theme
- **🔧 Mobile Menu** - Collapsible navigation for mobile devices
- **⚡ Interactive Elements** - Hover effects and smooth transitions
- **♿ Accessibility** - Proper semantic HTML and ARIA labels

### 🛠️ Technical Features

- **🚀 Django 5.2.4** - Latest Django framework
- **🗄️ SQLite Database** - Lightweight database solution
- **🎨 TailwindCSS** - Modern CSS framework
- **🖼️ Image Processing** - Automatic image resizing with Pillow
- **📱 Vue.js Ready** - Frontend framework integration
- **🔧 Font Awesome** - Beautiful icon library

## 📋 Content Management

### Admin Panel Access

Visit `/admin/` to access the comprehensive admin interface where you can:

- **Club Information** - Edit basic club details and history
- **News Articles** - Create and manage news with rich content
- **Teams & Players** - Manage team roster with photos and statistics
- **Matches** - Add fixtures and record results
- **League Standings** - Update league table positions
- **Management Team** - Add club officials and their roles
- **Events** - Schedule club activities and matches
- **Gallery** - Upload and organize photos
- **Analytics** - View page visit statistics

### Default Admin Account

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@tjhlavnice.cz`

## 🏗️ Project Structure

```
tjhlavnice2/
├── football/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── admin.py             # Admin configuration
│   ├── urls.py              # URL routing
│   ├── middleware.py        # Custom middleware
│   └── management/          # Custom management commands
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   └── football/           # App-specific templates
├── static/                  # Static files
│   ├── css/                # Custom CSS
│   └── js/                 # JavaScript files
├── media/                   # User uploads
├── tjhlavnice/             # Project settings
└── manage.py               # Django management script
```

## 🗃️ Database Models

### Core Models

- **ClubInfo** - Club information and history
- **Team** - Team details with flag upload
- **Player** - Player profiles with positions and stats
- **Management** - Club management team
- **League** - Competition leagues
- **News** - News articles with images
- **Match** - Match fixtures and results
- **Standing** - League table positions
- **Event** - Calendar events
- **Gallery** - Photo gallery
- **PageVisit** - Analytics tracking
- **MainPage** - Homepage configuration

## 🎯 Key Features Detail

### 🏠 Homepage

- Latest news display (3 most recent)
- Upcoming match information
- Recent match results (2 latest)
- Current league position with surrounding teams
- Quick navigation links

### 📰 News System

- Rich content management
- Featured article highlighting
- Image upload and automatic resizing
- Author attribution
- Publication status control

### ⚽ Match Management

- Fixture scheduling
- Result recording
- League association
- Venue information
- Referee details
- Match notes

### 📊 League Standings

- Position tracking
- Points calculation
- Goal statistics
- Club team highlighting
- Multiple league support

### 👥 Team Management

- Player profiles with photos
- Position categorization (GK, DEF, MID, FWD)
- Jersey numbers
- Goal and card statistics
- Birth date tracking

### 📱 Responsive Design

- Mobile-first approach
- Collapsible navigation
- Touch-friendly interface
- Optimized images
- Fast loading times

## 🚀 Deployment

### Development

```bash
python manage.py runserver
```

### Production Setup

1. **Configure settings for production**
2. **Set up proper database (PostgreSQL recommended)**
3. **Configure static file serving**
4. **Set up media file handling**
5. **Use proper WSGI server (Gunicorn, uWSGI)**
6. **Configure reverse proxy (Nginx, Apache)**

### Environment Variables

Create a `.env` file for production:

```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## 🔧 Customization

### Colors

The website uses a custom color scheme:

- **Primary Red:** `#5f0909ff`
- **Dark Red:** `#991B1B`
- **Black:** `#111827`
- **Gray:** `#374151`

### Styling

- Modify `static/css/custom.css` for additional styling
- TailwindCSS classes are used throughout templates
- Custom CSS is loaded via CDN for rapid development

### Content

- All content is manageable through the Django admin
- Images are automatically resized for optimal performance
- SEO-friendly URLs and meta information

## 📈 Analytics

The website includes built-in analytics:

- **Page visit tracking** for all pages
- **IP address logging** (GDPR compliant)
- **User agent detection**
- **Admin dashboard** for viewing statistics

## 🆘 Support

### Getting Help

- Check the Django documentation for framework questions
- Review the admin interface for content management
- Contact the development team for technical issues

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Common Issues

- **Images not loading:** Check media file configuration
- **Admin access denied:** Verify superuser credentials
- **Styles not applying:** Clear browser cache
- **Database errors:** Run migrations

## 📝 License

This project is created for TJ Družba Hlavnice football club.

---

**TJ Družba Hlavnice** - Tradice od roku 1952 🏆

For technical support or questions, contact the club administrators through the admin panel.
