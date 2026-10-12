# -*- coding: utf-8 -*-
"""Czech versions of the privacy and cookie policies (translations of tools/legal_pages.py).

Same facts as the English notices; additions for Czech readers are marked [CS] in comments. This is a
translation of a legal notice: it needs review by a lawyer / data-protection adviser before it is promoted.
"""

from html import escape

import site_config as cfg

UPDATED = "8. 10. 2026"
UPDATED_ISO = "2026-10-08"
PRIVACY_PATH = "/cs/zasady-ochrany-osobnich-udaju/"
COOKIES_PATH = "/cs/zasady-cookies/"

IDENTITY = f'''<p><strong>{escape(cfg.ORG_COMPANY_NAME)}</strong> provozuje registrovanou cestovní agenturu <strong>{escape(cfg.ORG_AGENCY_NAME)}</strong> (číslo agentury TÜRSAB {cfg.ORG_TURSAB_NUMBER}), prostřednictvím které se vyřizují web DMC Turkey Partner a poptávky.</p>
<p>Adresa: Güzeloba, 2268 Sok No:33, 07230 Muratpaşa/Antalya, Türkiye.<br>E-mail: <a href="mailto:{cfg.ORG_EMAIL}">{cfg.ORG_EMAIL}</a><br>Telefon: <a href="tel:{cfg.ORG_PHONE}">{cfg.ORG_PHONE_DISPLAY}</a>.</p>
<p>Názvy agentury a společnosti jsou uvedeny společně ve <a href="{cfg.ORG_AGENCY_RECORD_URL}" target="_blank" rel="noopener">zveřejněném záznamu agentur TÜRSAB</a> (strana 19). Tento zveřejněný seznam slouží jako odkaz na identitu, nikoli jako aktuální ověření platnosti osvědčení.</p>'''

PRIVACY = f'''<div class="legal-summary"><p><strong>Vaše poptávka zůstává poptávkou.</strong> Vaše údaje používáme k posouzení zadání, ke kontaktování Vás a k přípravě nabídky. Odesláním poptávky se nezapojujete do marketingu. Volitelná služba Google Analytics se spustí pouze tehdy, pokud ji povolíte.</p></div>
<h2>1. Kdo odpovídá za Vaše údaje?</h2>
{IDENTITY}
<p>Pro provoz webu a vyřizování poptávek popsané zde je správcem osobních údajů výše uvedená společnost. S dotazy k ochraně soukromí a s žádostmi o uplatnění práv se obracejte na výše uvedený e-mail nebo poštovní adresu.</p>
<h2>2. Jaké údaje shromažďujeme?</h2>
<ul><li><strong>Údaje, které odešlete:</strong> jméno, společnost, pracovní e-mail, destinace, přibližná velikost skupiny, termíny cesty či akce, typ projektu a popis, který se rozhodnete uvést. Pokud ve formuláři uvedete telefonní číslo, zpracujeme i to. Poptávka z kalkulačky může obsahovat také Vámi zvolené předpoklady programu a odhadovaný rozpočet.</li>
<li><strong>Kontext poptávky:</strong> stránka nebo služba, ze které jste nabídku poptávali, stránka odeslání a čas odeslání. U poptávky z české stránky uchováváme také jazykovou verzi a krátké referenční číslo, abychom mohli spojit konverzaci na WhatsApp s Vaší poptávkou. Volitelná kampaňová atribuce se ukládá ve Vašem prohlížeči pouze po udělení souhlasu s analytikou.</li>
<li><strong>Technické informace:</strong> poskytovatelé hostingu a e-mailu mohou zpracovávat síťové adresy, informace o prohlížeči či zařízení, záznamy o doručení a bezpečnostní logy nutné k provozu webu, prevenci zneužití a doručení Vaší poptávky. Z IP adresy odvozujeme přibližnou zemi pouze pro statistické účely a nepoužíváme ji k rozhodování, kam bude Vaše poptávka směrována.</li>
<li><strong>Volitelné informace o používání:</strong> po udělení souhlasu s analytikou přijímá Google Analytics informace o zobrazených stránkách, používaných funkcích, interakcích s poptávkou a vlastnostech prohlížeče či zařízení. Jméno, e-mail ani Váš popis do polí analytických událostí neodesíláme.</li></ul>
<p>Úvodní formulář nepožaduje kopie pasů, údaje o platebních kartách, zdravotní údaje ani seznamy cestujících. Neuvádějte je prosím ani do volného textu popisu. Bude-li další plánování vyžadovat údaje o účastnících, vysvětlíme účel a vhodný způsob jejich samostatného poskytnutí.</p>
<h2>3. Proč údaje zpracováváme a na jakém základě?</h2>
<ul><li><strong>Vyřízení poptávky a příprava nabídky:</strong> abychom porozuměli Vašim požadavkům a mohli s Vámi komunikovat. Základem je – tam, kde se použije – provedení opatření přijatých na Vaši žádost před uzavřením smlouvy nebo plnění smlouvy; u zástupců firem může být základem oprávněný zájem odpovědět na poptávku společnosti, vyvážený s právy dotčené osoby.</li>
<li><strong>Provoz webu, bezpečnost a doručení:</strong> abychom web udrželi dostupný, rozpoznali zneužití a doručovali zprávy. Základem je oprávněný zájem na provozu a ochraně služby, v souladu s příslušnými právními podmínkami.</li>
<li><strong>Evidence a právní záležitosti:</strong> ke splnění příslušných právních povinností nebo k určení, výkonu či obhajobě právních nároků.</li>
<li><strong>Volitelná analytika:</strong> Váš souhlas. Můžete jej odmítnout nebo odvolat, aniž byste ztratili přístup k webu či formuláři poptávky.</li></ul>
<p>Odeslání poptávky nepovažujeme za souhlas se zasíláním nesouvisejících reklamních e-mailů. Případný marketing vyžadující souhlas musí být řešen odděleně od Vaší poptávky. Použitelný turecký právní rámec zahrnuje zákon č. 6698 (KVKK); podle okolností se mohou použít i další předpisy o ochraně osobních údajů, včetně nařízení (EU) 2016/679 (GDPR), v rozsahu, v jakém se na zpracování vztahuje.</p>
<h2>4. Kdo údaje přijímá?</h2>
<p>Poptávky jsou do naší firemní schránky odesílány prostřednictvím služby <strong>Resend</strong>. <strong>Vercel</strong> poskytuje hosting webu a serverový koncový bod poptávky. Tito poskytovatelé zpracovávají údaje nezbytné k poskytování svých služeb. Volitelná analytika využívá po Vašem souhlasu službu <strong>Google Analytics</strong>.</p>
<p>Přihlášky k Agency Fam Trip 2027, pokud je tento program otevřen, se odesílají prostřednictvím služby <strong>Formspree</strong>, která je doručuje do naší firemní schránky a uchovává v našem účtu Formspree. Z Vaší IP adresy také odvozujeme přibližnou zemi (neukládáme ji), abychom přizpůsobili znění pozvánky, a kód země zaznamenáme k přihlášce. Údaje používáme k posouzení přihlášky a ke kontaktování vybraných zájemců. E-mailové novinky zasíláme pouze tehdy, pokud zaškrtnete samostatné nepovinné políčko.</p>
<p>Náš tým používá informace z poptávky k posouzení projektu. Je-li to nutné k přípravě požadované nabídky, mohou být příslušné požadavky sdíleny s hotely, místy konání, dopravci či dodavateli akcí. V této počáteční fázi se snažíme sdílet požadavky na program, nikoli identifikační údaje hostů. Informace mohou být také zpřístupněny profesním poradcům nebo příslušným orgánům, je-li to nutné pro právní záležitosti nebo plnění právní povinnosti.</p>
<p>Externí odkazy na WhatsApp otevírají samostatnou službu pouze tehdy, pokud je sami použijete. Údaje, které tam odešlete, podléhají také zásadám ochrany soukromí této služby. Pokud Vás na české stránce nasměrujeme na WhatsApp, použijeme pro to výhradně číslo určené pro českou stránku.</p>
<h2>5. Zpracování mimo Türkiye</h2>
<p>Hosting, doručování e-mailů a volitelná analytika mohou zahrnovat zpracování mimo Türkiye. Resend uvádí, že jeho primární zpracování a uložená data zákazníků se nacházejí ve Spojených státech. Umístění a subdodavatelé, které využívají Vercel a Google, závisejí na jejich službách a konfiguraci.</p>
<p>Zpracování přesahující hranice států podléhá požadavkům na předávání údajů podle příslušného práva, včetně článku 9 KVKK, pokud se použije. Samotné zásady ochrany soukromí poskytovatele nezakládají opatření správce pro předávání údajů. Požádejte nás o informace o opatřeních použitelných na Vaše údaje.</p>
<p>Informace o poskytovatelích: <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener">Zásady ochrany soukromí Vercel</a>, <a href="https://resend.com/legal/privacy-policy" target="_blank" rel="noopener">Zásady ochrany soukromí Resend</a>, <a href="https://resend.com/legal/dpa" target="_blank" rel="noopener">Dodatek o zpracování údajů Resend</a>, <a href="https://formspree.io/legal/privacy-policy" target="_blank" rel="noopener">Zásady ochrany soukromí Formspree</a> a <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Zásady ochrany soukromí Google</a> (všechny v angličtině).</p>
<h2>6. Jak dlouho údaje uchováváme?</h2>
<p>Korespondenci k poptávce uchováváme po dobu nutnou k odpovědi, přípravě a navazování na Vámi požadovanou nabídku. Pokud projekt pokračuje, mohou být příslušné záznamy uchovávány pro realizaci, účetnictví, zákonné lhůty pro uchovávání a právní nároky. Doba uchování závisí na záznamu a účelu; údaje by měly být vymazány nebo anonymizovány, jakmile je tyto účely a povinnosti již nevyžadují.</p>
<p>Doby uložení v prohlížeči a postup odvolání souhlasu s analytikou jsou popsány v našich <a href="{COOKIES_PATH}">Zásadách cookies</a>. Doručovací a technické logy uchovávané poskytovateli mají samostatná nastavení uchovávání.</p>
<h2>7. Zabezpečení</h2>
<p>Web používá HTTPS. Poptávka je odesílána prostřednictvím serverového koncového bodu; API klíč pro doručování e-mailů není součástí kódu v prohlížeči. Pole formuláře jsou před vložením do e-mailů s poptávkou kontrolována a ošetřena. Žádný přenos po internetu není zcela bez rizika, proto prosím neposílejte citlivé údaje v úvodním zadání.</p>
<h2>8. Vaše práva a jak nás kontaktovat</h2>
<p>Podle článku 11 KVKK můžete za stanovených podmínek požádat o informaci, zda jsou Vaše údaje zpracovávány, vyžádat si informace o zpracování a jeho účelech, zjistit příjemce v Türkiye či v zahraničí, požádat o opravu nebo výmaz, je-li to relevantní, požádat o oznámení příslušných změn příjemcům, vznést námitku proti výsledku vůči Vám, který vyplývá výhradně z automatizované analýzy, a požadovat náhradu za protiprávní zpracování.</p>
<p>Poskytují-li další použitelné právní předpisy další práva, může jít o přístup, omezení zpracování, přenositelnost, námitku a stížnost u příslušného orgánu pro ochranu osobních údajů; v České republice je jím Úřad pro ochranu osobních údajů (<a href="https://www.uoou.gov.cz/" target="_blank" rel="noopener">uoou.gov.cz</a>). Kalkulačka rozpočtu na tomto webu vytváří orientační odhad z Vašich voleb; nečiní závaznou rezervaci ani rozhodnutí o způsobilosti.</p>
<p>Napište na <a href="mailto:{cfg.ORG_EMAIL}">{cfg.ORG_EMAIL}</a> s předmětem „Privacy request“, nebo na naši poštovní adresu. Uveďte svou žádost a dostatek informací k identifikaci příslušné poptávky. Můžeme být nuceni ověřit Vaši totožnost, ale nezasílejte prosím doklady totožnosti bez vyzvání. Odpovíme v příslušné zákonné lhůtě. Žádosti podle KVKK se obecně vyřizují do 30 dnů podle článku 13, s výhradou předepsaných požadavků na podání žádosti.</p>
<h2>9. Změny tohoto oznámení</h2>
<p>Tuto stránku aktualizujeme, kdykoli se popsané zpracování změní. Výše uvedené datum odpovídá poslední kontrole tohoto oznámení. K nastavení cookies použijte <button type="button" data-cookie-settings>Nastavení cookies</button>.</p>'''

COOKIES = f'''<div class="legal-summary"><p><strong>Volitelná analytika je vypnutá, dokud ji nepovolíte.</strong> Odmítnutí analytiky Vám nebrání web procházet, používat kalkulačku rozpočtu ani odeslat poptávku.</p><p><button type="button" class="btn btn--ghost" data-cookie-settings>Změnit nastavení cookies</button></p></div>
<h2>1. Cookies a úložiště v prohlížeči</h2>
<p>Cookies jsou malé hodnoty ukládané Vaším prohlížečem. Tento web používá také místní úložiště (local storage) a úložiště relace (session storage). Úložiště relace obvykle trvá po dobu aktuální relace karty; místní úložiště zůstává, dokud není odstraněno nebo neuplyne platnost uložené preference.</p>
<h2>2. Nezbytné preference a požadované funkce</h2>
<ul><li><strong>dmc_cookie_choice_v1 (místní úložiště):</strong> zaznamenává, zda byla volitelná analytika povolena nebo odmítnuta, a kdy bylo rozhodnutí učiněno. Web toto rozhodnutí respektuje 180 dní, poté se zeptá znovu. Uložená hodnota neobsahuje jméno, e-mail ani popis; v úložišti může zůstat, dokud není přepsána nebo vymazána.</li>
<li><strong>dtp_calculator_state (úložiště relace):</strong> uchovává Vámi zvolené předpoklady rozpočtu akce a výsledek, abyste je mohli zahrnout do poptávky. Podporuje funkci kalkulačky, kterou se rozhodnete použít, a trvá po dobu relace karty. Neukládá jméno, e-mail ani volný text popisu.</li></ul>
<p>Hostingové a síťové služby mohou rovněž zpracovávat provozní a bezpečnostní informace nutné k obsluze požadavků. Ty jsou oddělené od volitelné služby Google Analytics.</p>
<h2>3. Volitelná analytika a atribuce</h2>
<p>Google Analytics 4 je nastaven tak, že se načte až poté, co zvolíte „Povolit volitelnou analytiku“. Do té doby, a také pokud ji odmítnete, web nenačítá analytický kód Google ani neodesílá analytické události. Úložiště reklamních dat Google a souhlas s personalizací reklam zůstávají zamítnuty.</p>
<ul><li><strong>_ga a _ga_&lt;přípona měření&gt;:</strong> cookies Google Analytics sloužící k rozlišení návštěv a uchování informací o relaci. Standardní výchozí platnost cookies Google je až dva roky a může se při dalších návštěvách obnovit; omezení prohlížeče a nastavení služby ji mohou zkrátit.</li>
<li><strong>proposal_campaign (úložiště relace):</strong> po udělení souhlasu s analytikou si pamatuje kontext služby a kampaně při přechodu na formulář poptávky.</li>
<li><strong>proposal_landing_page (úložiště relace):</strong> po udělení souhlasu s analytikou uchovává adresu vstupní stránky poptávky bez řetězce dotazu.</li></ul>
<p>Volitelná data o používání nám pomáhají pochopit, které stránky a nástroje jsou užitečné. Vaše jméno, pracovní e-mail ani popis nejsou součástí polí analytických událostí. Google může zpracovávat údaje o používání mimo Türkiye; viz naše <a href="{PRIVACY_PATH}">Zásady ochrany osobních údajů</a> a <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener">informace Google o cookies</a>.</p>
<h2>4. Povolení, odmítnutí nebo odvolání</h2>
<p>Lišta nabízí samostatná, stejně dostupná tlačítka pro povolení a odmítnutí. Můžete ji znovu otevřít pomocí „Nastavení cookies“ v patičce kterékoli stránky nebo tlačítkem výše. Pokračování v procházení se za souhlas nepovažuje.</p>
<p>Pokud změníte souhlas na odmítnutí, web analytiku vypne, odstraní své přístupné cookies Google Analytics a volitelné úložiště atribuce poptávky a stránku znovu načte, aby se dříve načtený kód odstranil. Tím se zastaví budoucí sběr dat prostřednictvím tohoto webu; již odeslaná data u Google nesmaže. K žádosti o údaje použijte kontakty uvedené v Zásadách ochrany osobních údajů.</p>
<p>Můžete také vymazat data webu nebo zablokovat úložiště ve svém prohlížeči. Web se Vás pak může znovu zeptat na rozhodnutí a kalkulačka již nemusí přenášet Vaše volby mezi stránkami. Formulář poptávky zůstává dostupný. Pokud je zakázán JavaScript, volitelný zavaděč analytiky se nespustí.</p>
<h2>5. Externí odkazy a aktualizace</h2>
<p>Odkazy na WhatsApp, zásady ochrany soukromí poskytovatelů a externí referenční dokumenty Vás přesměrují na samostatné služby s vlastními postupy ochrany soukromí. Nejsou to vložené analytické funkce.</p>
<p>Toto oznámení kontrolujeme, když se změní nastavení úložiště nebo měření webu. Provozovatele, kontaktní údaje a Vaše práva najdete v <a href="{PRIVACY_PATH}">Zásadách ochrany osobních údajů</a>.</p>'''

PAGES = {
    "zasady-ochrany-osobnich-udaju": (
        "Zásady ochrany osobních údajů",
        "Jak DMC Turkey Partner nakládá s poptávkami, technickými informacemi, volitelnou analytikou, poskytovateli služeb a žádostmi o ochranu soukromí.",
        PRIVACY),
    "zasady-cookies": (
        "Zásady cookies",
        "Nezbytné úložiště v prohlížeči, volitelná služba Google Analytics a jak povolit, odmítnout či změnit nastavení cookies na webu DMC Turkey Partner.",
        COOKIES),
}
