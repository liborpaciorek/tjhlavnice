# Czech Admin Translation Implementation

## Přehled změn / Overview of Changes

Implementace české lokalizace Django admin rozhraní pro webové stránky TJ Družba Hlavnice.
Implementation of Czech localization for Django admin interface for TJ Družba Hlavnice website.

## Změny v konfiguracii / Configuration Changes

### Settings.py
- **LANGUAGE_CODE**: Změněno z 'en-us' na 'cs' / Changed from 'en-us' to 'cs'
- **TIME_ZONE**: Změněno z 'UTC' na 'Europe/Prague' / Changed from 'UTC' to 'Europe/Prague'
- **LOCALE_PATHS**: Přidána podpora pro české překlady / Added support for Czech translations

## Modely / Models

Všechny modely byly aktualizovány s českými popisky polí a názvy:

### ClubInfo - Informace o klubu
- `name` → "Název klubu"
- `founded_year` → "Rok založení"
- `history` → "Historie klubu"
- `logo` → "Logo"
- `address` → "Adresa"
- `contact_email` → "Kontaktní email"
- `contact_phone` → "Kontaktní telefon"

### League - Soutěž
- `name` → "Název soutěže"
- `season` → "Sezóna"
- `description` → "Popis"

### Team - Tým
- `name` → "Název týmu"
- `flag` → "Vlajka/Logo"
- `founded` → "Rok založení"
- `city` → "Město"
- `league` → "Soutěž"
- `is_club_team` → "Náš tým"

### Player - Hráč
Pozice hráčů přeloženy:
- 'GK' → 'Brankář' (Goalkeeper)
- 'DEF' → 'Obránce' (Defender)
- 'MID' → 'Záložník' (Midfielder)
- 'FWD' → 'Útočník' (Forward)

Pole:
- `team` → "Tým"
- `jersey_number` → "Číslo dresu"
- `first_name` → "Křestní jméno"
- `last_name` → "Příjmení"
- `position` → "Pozice"
- `birth_date` → "Datum narození"
- `photo` → "Fotografie"
- `goals` → "Góly"
- `yellow_cards` → "Žluté karty"
- `red_cards` → "Červené karty"

### Management - Vedení klubu
Role přeloženy:
- 'PRESIDENT' → 'Předseda'
- 'COACH' → 'Trenér'
- 'ASSISTANT' → 'Asistent trenéra'
- 'TREASURER' → 'Pokladník'
- 'SECRETARY' → 'Sekretář'
- 'MANAGER' → 'Manažer'
- 'OTHER' → 'Ostatní'

### News - Aktuality
- `title` → "Nadpis"
- `content` → "Obsah"
- `image` → "Obrázek"
- `created_at` → "Vytvořeno"
- `updated_at` → "Upraveno"
- `author` → "Autor"
- `is_featured` → "Doporučený článek"
- `published` → "Publikováno"

### Match - Zápas
- `home_team` → "Domácí tým"
- `away_team` → "Hostující tým"
- `date` → "Datum a čas"
- `league` → "Soutěž"
- `home_score` → "Skóre domácích"
- `away_score` → "Skóre hostů"
- `location` → "Místo konání"
- `referee` → "Rozhodčí"
- `notes` → "Poznámky"

### Standing - Tabulka
- `team` → "Tým"
- `league` → "Soutěž"
- `position` → "Pozice"
- `played` → "Odehráno"
- `won` → "Výhry"
- `drawn` → "Remízy"
- `lost` → "Prohry"
- `goals_for` → "Góly vstřelené"
- `goals_against` → "Góly obdržené"
- `points` → "Body"

### Event - Událost
- `title` → "Název události"
- `description` → "Popis"
- `date` → "Datum a čas"
- `location` → "Místo konání"
- `is_match` → "Je to zápas"
- `match` → "Zápas"

### Gallery - Galerie
- `title` → "Název"
- `description` → "Popis"
- `image` → "Obrázek"
- `uploaded_at` → "Nahráno"
- `event` → "Událost"

### PageVisit - Návštěva stránky
- `page_name` → "Název stránky"
- `ip_address` → "IP adresa"
- `user_agent` → "User Agent"
- `timestamp` → "Čas návštěvy"

### MainPage - Konfigurace hlavní stránky
- `featured_news` → "Doporučené aktuality"

## Admin rozhraní / Admin Interface

### Aktualizované zobrazení
- Všechny `short_description` atributy přeloženy do češtiny
- Zprávy v admin rozhraní ("Bez fotografie", "Bez obrázku", atd.)
- Názvy sekcí a modelů v českém jazyce

## Rich Text Editor

- **CKEditor automaticky načítá české překlady** když je `LANGUAGE_CODE = 'cs'`
- Toolbar a nabídky se zobrazují v češtině
- Zachována funkčnost bohatého formátování textu

## Technické detaily

### Migrations
- Žádné databázové migrace nejsou potřeba
- Změny se týkají pouze zobrazení (verbose_name, help_text)

### Kompatibilita
- Zachována zpětná kompatibilita s existujícími daty
- Administrátorské rozhraní kompletně v češtině
- Frontend zůstává beze změny

## Testování

### Co bylo otestováno:
✅ Django admin se zobrazuje v češtině
✅ CKEditor používá české překlady
✅ Všechny modely mají české názvy
✅ Formuláře zobrazují česká pole
✅ Filtry a vyhledávání funguje správně

### Příklad použití:
1. Přihlaste se do admin rozhraní na `/admin/`
2. Všechny sekce jsou nyní v češtině:
   - "Aktuality" místo "News"
   - "Týmy" místo "Teams"
   - "Hráči" místo "Players"
   - Atd.

## Výsledek

Kompletní česká lokalizace admin rozhraní Django aplikace pro TJ Družba Hlavnice, včetně:
- České názvy všech modelů a polí
- České překlady v rich text editoru
- České zobrazení dat a filtrů
- Zachování všech funkcionalit

Administrátoři nyní mohou pracovat s intuitivním českým rozhraním při správě obsahu webu.
