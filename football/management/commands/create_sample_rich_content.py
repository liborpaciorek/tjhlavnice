from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from football.models import News, ClubInfo, Management

class Command(BaseCommand):
    help = 'Create sample rich text content for testing'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@tjhlavnice.cz',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('adminpass123')
            admin_user.save()
        
        # Create sample news with rich text content
        sample_news_content = """
        <h2>Vítejte v novém systému správy obsahu!</h2>
        
        <p>Jsme rádi, že můžeme představit <strong>nový systém</strong> pro správu obsahu našeho webu. 
        Díky tomuto systému můžeme nyní vytvářet mnohem <em>kvalitnější a vizuálně atraktivnější</em> články.</p>
        
        <h3>Co je nového?</h3>
        <ul>
            <li>Rich text editor pro snadné formátování textu</li>
            <li>Možnost vkládání obrázků přímo do článků</li>
            <li>Podpora pro tabulky a seznamy</li>
            <li>Lepší organizace obsahu</li>
        </ul>
        
        <h3>Výhody pro návštěvníky</h3>
        <ol>
            <li>Přehlednější články s lepším formátováním</li>
            <li>Rychlejší načítání stránek</li>
            <li>Responzivní design pro všechna zařízení</li>
        </ol>
        
        <blockquote>
            <p>"Tento nový systém nám umožní lépe informovat naše fanoušky o dění v klubu 
            a poskytovat jim kvalitní obsah." - Vedení TJ Družba Hlavnice</p>
        </blockquote>
        
        <p>Těšíme se na vaše <a href="mailto:info@tjhlavnice.cz">zpětnou vazbu</a> 
        k novému designu a funkcionalitě webu!</p>
        """
        
        News.objects.get_or_create(
            title="Nový systém správy obsahu",
            defaults={
                'content': sample_news_content,
                'author': admin_user,
                'is_featured': True,
                'published': True
            }
        )

        # Update club info with rich text
        sample_club_history = """
        <h2>Historie klubu TJ Družba Hlavnice</h2>
        
        <p>TJ Družba Hlavnice byla založena v roce <strong>1952</strong> jako součást tehdejší 
        společenské organizace. Od samého počátku se klub zaměřoval na rozvoj fotbalu 
        v regionu a výchovu mladých talentů.</p>
        
        <h3>Významné milníky</h3>
        <ul>
            <li><strong>1952</strong> - Založení klubu</li>
            <li><strong>1960-1970</strong> - Výstavba prvního hřiště</li>
            <li><strong>1980-1990</strong> - Zlatá éra klubu, postup do vyšších soutěží</li>
            <li><strong>2000</strong> - Rekonstrukce zázemí klubu</li>
            <li><strong>2010</strong> - Modernizace hřiště a osvětlení</li>
            <li><strong>2020</strong> - Spuštění nového webu klubu</li>
        </ul>
        
        <h3>Naše hodnoty</h3>
        <p>Klub se řídí tradičními hodnotami <em>fair play</em>, <em>týmového ducha</em> 
        a <em>oddanosti fotbalu</em>. Snažíme se vytvářet prostředí, kde se každý hráč 
        může rozvinout podle svých schopností.</p>
        
        <blockquote>
            <p>"Fotbal není jen hra, je to způsob života. V našem klubu se učíme 
            nejen fotbalovým dovednostem, ale také životním hodnotám."</p>
        </blockquote>
        
        <p>Dnes má klub více než <strong>100 registrovaných hráčů</strong> ve všech 
        věkových kategoriích a pokračuje v tradici kvalitního fotbalu v regionu.</p>
        """
        
        club_info, created = ClubInfo.objects.get_or_create(
            defaults={
                'name': 'TJ Družba Hlavnice',
                'founded_year': 1952,
                'history': sample_club_history,
                'address': 'Sportovní areál\nHlavnice 123\n123 45 Hlavnice',
                'contact_email': 'info@tjhlavnice.cz',
                'contact_phone': '+420 123 456 789'
            }
        )
        
        if not created and not club_info.history:
            club_info.history = sample_club_history
            club_info.save()

        # Create sample management member with rich bio
        sample_bio = """
        <p><strong>Jan Novák</strong> vede náš klub již více než <em>10 let</em>. 
        Pod jeho vedením klub dosáhl významných úspěchů.</p>
        
        <h4>Kariéra</h4>
        <ul>
            <li>Bývalý profesionální fotbalista</li>
            <li>UEFA B licence</li>
            <li>15 let trenérské praxe</li>
        </ul>
        
        <p>Jan je známý svým <strong>pozitivním přístupem</strong> a schopností 
        motivovat mladé hráče k podávání nejlepších výkonů.</p>
        """
        
        Management.objects.get_or_create(
            first_name="Jan",
            last_name="Novák",
            defaults={
                'role': 'COACH',
                'bio': sample_bio,
                'email': 'jan.novak@tjhlavnice.cz',
                'phone': '+420 987 654 321',
                'order': 1
            }
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample rich text content!')
        )
