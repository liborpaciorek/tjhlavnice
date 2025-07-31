DEFAULT PLAYER IMAGE SETUP
==========================

A default player image has been created and is now being used for all players without photos.

CURRENT STATUS:
✓ Template updated to use default player image
✓ Basic placeholder image created (default_player.png)

TO IMPROVE THE IMAGE:
Replace the current default_player.png with the soccer player image from your attachment:

1. Save the soccer player image (the one showing a player in red/white jersey) 
2. Rename it to: default_player.png
3. Place it in this directory: static/images/players/
4. The image should be square (recommended: 300x300 pixels) for best results

The template will automatically use this image for any player without an uploaded photo.

TECHNICAL DETAILS:
- Image path: {% static 'images/players/default_player.png' %}
- Used in: templates/football/team_lineup.html
- Applied to: All player positions (Goalkeepers, Defenders, Midfielders, Forwards)
- Styling: Circular crop, border matching position color
