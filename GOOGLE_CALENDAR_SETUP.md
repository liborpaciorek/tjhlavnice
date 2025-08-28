# Google Calendar Integration - Setup Guide

## Overview
The TJ Družba Hlavnice website now includes Google Calendar integration that allows displaying club events directly from a Google Calendar. This feature provides:

- Display of upcoming and past events
- Event details (title, description, location, time)
- Responsive design matching the existing website style
- Admin panel configuration
- Direct links to Google Calendar

## Prerequisites

1. **Google Account**: You need a Google account to create and manage calendars
2. **Google Cloud Project**: Required for API access
3. **Google Calendar API Key**: For accessing calendar data

## Setup Instructions

### Step 1: Create a Google Calendar

1. Go to [Google Calendar](https://calendar.google.com)
2. Sign in with your Google account
3. Create a new calendar or use an existing one
4. Make the calendar public:
   - Go to calendar settings
   - Under "Access permissions", check "Make available to public"
   - Set "See all event details" to allow full access

### Step 2: Get the Calendar ID

1. In Google Calendar, go to your calendar settings
2. Scroll down to "Calendar ID" section
3. Copy the Calendar ID (looks like: `abcd1234@group.calendar.google.com`)

### Step 3: Create Google Cloud Project and API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing one
3. Enable the Calendar API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"
4. Create an API Key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key
   - (Optional) Restrict the key to Calendar API for security

### Step 4: Configure in Django Admin

1. Start your Django server: `python manage.py runserver`
2. Go to Django admin: `http://localhost:8000/admin/`
3. Navigate to "Google Calendar Settings"
4. Fill in the configuration:
   - **Název kalendáře**: Display name for the calendar
   - **ID Google kalendáře**: Paste the Calendar ID from Step 2
   - **Google API klíč**: Paste the API key from Step 3
   - **Aktivní**: Check this box to enable the calendar
   - **Maximum událostí**: Number of events to display (default: 50)
   - **Zobrazit minulé události**: Show past events
   - **Dny zpět**: How many days back to show past events

5. Save the settings

### Step 5: Test the Integration

1. Go to `http://localhost:8000/kalendar/`
2. You should see your calendar events displayed
3. If there are issues, check the error messages displayed on the page

## Features

### Calendar Display
- **Event Order**: Shows 6 upcoming events (nearest first) followed by 6 past events (most recent first)
- Each event shows:
  - Date and time
  - Event title
  - Description (if available)
  - Location (if available)
  - Link to Google Calendar

### Event Status Indicators
- **DNES**: Today's events (green badge)  
- **Nadcházející**: Future events (blue badge)
- **Proběhlo**: Past events (gray badge)

### Event Sections
- **Nadcházející události**: Up to 6 upcoming events, sorted by date (nearest first)
- **Nedávné události**: Up to 6 past events, sorted by date (most recent first)

### Admin Configuration Options
- **is_active**: Enable/disable calendar display
- **max_events**: Currently displays 6 upcoming + 6 past events (total 12)
- **show_past_events**: Include past events section
- **past_events_days**: How many days back to search for past events

## Navigation Integration

The calendar is accessible through:
- **Desktop menu**: "KALENDÁŘ" link
- **Mobile menu**: "KALENDÁŘ" link
- **Direct URL**: `/kalendar/`

## Technical Details

### Files Added/Modified

#### Models (`football/models.py`)
- Added `GoogleCalendarSettings` model for configuration

#### Views (`football/views.py`)
- Added `google_calendar_view` function
- Added `fetch_google_calendar_events` helper function

#### URLs (`football/urls.py`)
- Added `/kalendar/` route

#### Templates
- `templates/football/google_calendar.html`: Calendar display page
- Updated navigation in `templates/base.html`

#### Admin (`football/admin.py`)
- Added `GoogleCalendarSettingsAdmin` for configuration

#### Dependencies
- Added `requests` library to `requirements.txt`

### Management Command
Run `python manage.py setup_google_calendar` to create initial settings.

## Troubleshooting

### Common Issues

1. **"API Error 403: Přístup odmítnut" (Most Common)**
   
   **Possible Causes:**
   - Calendar is not public
   - API Key doesn't have Calendar API enabled
   - Invalid API Key
   - API Key has IP restrictions
   - Daily quota exceeded
   
   **Solutions:**
   
   **a) Make Calendar Public:**
   - Go to Google Calendar
   - Click on your calendar settings (gear icon next to calendar name)
   - Under "Access permissions for events":
     - ✅ Check "Make available to public"
     - ✅ Set to "See all event details"
   - Click "Save"
   
   **b) Enable Calendar API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Select your project
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Make sure it shows "ENABLED" (if not, click Enable)
   
   **c) Check API Key:**
   - Go to "APIs & Services" > "Credentials"
   - Click on your API Key
   - Under "API restrictions":
     - Either select "Don't restrict key" (less secure)
     - Or select "Restrict key" and add "Google Calendar API"
   - Under "Application restrictions":
     - For production: Add your server IP address
     - For testing: Select "None" temporarily
   
   **d) Test API Key manually:**
   ```
   https://www.googleapis.com/calendar/v3/calendars/YOUR_CALENDAR_ID/events?key=YOUR_API_KEY&maxResults=1
   ```
   Replace YOUR_CALENDAR_ID and YOUR_API_KEY with actual values and test in browser.

2. **"Kalendář není správně nakonfigurován"**
   - Check that both Calendar ID and API Key are filled in admin
   - Verify the calendar is public

3. **"API Error: 404"**
   - Invalid Calendar ID format
   - Calendar doesn't exist
   - Double-check Calendar ID in Google Calendar settings

4. **"API Error: 400"**
   - Invalid Calendar ID format
   - Calendar doesn't exist

5. **"Connection Error"**
   - No internet connection
   - Google API is temporarily unavailable

6. **"Error: can't compare offset-naive and offset-aware datetimes"**
   - Fixed in the latest version with proper timezone handling
   - All datetime comparisons are now timezone-aware

### Debugging Tools

**Use the test command:**
```bash
python manage.py test_google_calendar
```
This will diagnose your configuration and provide specific error details.

### Testing API Access
You can test your setup by visiting this URL in browser:
```
https://www.googleapis.com/calendar/v3/calendars/YOUR_CALENDAR_ID/events?key=YOUR_API_KEY&maxResults=5
```
Replace `YOUR_CALENDAR_ID` and `YOUR_API_KEY` with your values.

**Expected responses:**
- ✅ **200**: JSON with calendar events (success)
- ❌ **403**: Permission denied (see solutions above)
- ❌ **404**: Calendar not found (check Calendar ID)
- ❌ **400**: Bad request (invalid Calendar ID format)

## Security Considerations

1. **API Key Security**:
   - Restrict API key to Calendar API only
   - Consider IP restrictions in production
   - Store API key securely (use environment variables in production)

2. **Calendar Privacy**:
   - Only make calendar public if you want events to be publicly visible
   - Be careful about sensitive event information

## Future Enhancements

Possible improvements:
- OAuth integration for private calendars
- Multiple calendar support
- Event filtering by categories
- Calendar event creation from admin panel
- Email notifications for events
