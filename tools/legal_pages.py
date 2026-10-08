#!/usr/bin/env python3
"""Render the site's legal notices from documented public workflows.

Review policy text when providers, processing or commercial workflows change.
The review date is intentional; rebuilding must not make unchanged text newer.
"""
from pathlib import Path
import re
from html import escape
import site_config as cfg

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "8 October 2026"
IDENTITY = f'''<p><strong>{escape(cfg.ORG_COMPANY_NAME)}</strong> operates the registered travel agency <strong>{escape(cfg.ORG_AGENCY_NAME)}</strong> (TÜRSAB Agency No. {cfg.ORG_TURSAB_NUMBER}), through which the DMC Turkey Partner website and enquiries are handled.</p>
<p>Address: Güzeloba, 2268 Sok No:33, 07230 Muratpaşa/Antalya, Türkiye.<br>Email: <a href="mailto:{cfg.ORG_EMAIL}">{cfg.ORG_EMAIL}</a><br>Telephone: <a href="tel:{cfg.ORG_PHONE}">{cfg.ORG_PHONE_DISPLAY}</a>.</p>
<p>The agency and company names are listed together in the <a href="{cfg.ORG_AGENCY_RECORD_URL}" target="_blank" rel="noopener">published TÜRSAB agency record</a> (page 19). This published list is an identity reference, rather than a live certificate-status check.</p>'''

PRIVACY = f'''<div class="legal-summary"><p><strong>Your enquiry stays an enquiry.</strong> We use your details to review your brief, contact you and prepare a proposal. Sending a brief does not enrol you in marketing. Optional Google Analytics starts only if you accept it.</p></div>
<h2>1. Who is responsible for your information?</h2>
{IDENTITY}
<p>For the website and enquiry processing described here, the company above is the data controller. Use the email or postal address above for privacy questions and rights requests.</p>
<h2>2. What information do we collect?</h2>
<ul><li><strong>Information you submit:</strong> your name, company, work email, destination, approximate group size, travel or event dates, project type and the brief you choose to provide. A calculator enquiry may also include your selected programme assumptions and estimated budget.</li>
<li><strong>Enquiry context:</strong> the page or service from which you requested a proposal, submission page and submission time. Optional campaign attribution is stored in your browser only after analytics permission.</li>
<li><strong>Technical information:</strong> hosting and email providers may process network addresses, browser or device information, delivery records and security logs needed to serve the site, prevent misuse and deliver your enquiry.</li>
<li><strong>Optional usage information:</strong> after analytics permission, Google Analytics receives information about page views, selected features, proposal interactions and browser or device characteristics. We do not send your name, email or written brief as analytics event fields.</li></ul>
<p>The initial form does not ask for passport copies, card information, health information or passenger lists. Please do not put these in the free-text brief. If later planning requires participant information, we will explain the purpose and the appropriate way to provide it separately.</p>
<h2>3. Why do we process information, and on what basis?</h2>
<ul><li><strong>Answering enquiries and preparing proposals:</strong> to understand your requirements and communicate with you. Where applicable, the basis is taking steps at your request before a contract or performing a contract; for business representatives, processing may be based on the legitimate interest in responding to the company’s enquiry, balanced against the individual’s rights.</li>
<li><strong>Website operation, security and delivery:</strong> to keep the website available, identify misuse and deliver messages. The basis is the legitimate interest in operating and protecting the service, subject to applicable legal conditions.</li>
<li><strong>Records and legal matters:</strong> to meet applicable legal obligations or establish, exercise or defend legal rights.</li>
<li><strong>Optional analytics:</strong> your consent. You may refuse or withdraw it without losing access to the website or enquiry form.</li></ul>
<p>We do not treat submitting a brief as consent to unrelated promotional emails. Any separate marketing activity requiring permission must be handled separately from your enquiry. The applicable Turkish framework includes Law No. 6698 (KVKK); other privacy laws may also apply depending on the circumstances.</p>
<h2>4. Who receives information?</h2>
<p>Enquiries are sent to our business inbox using <strong>Resend</strong>. <strong>Vercel</strong> provides website hosting and the server-side enquiry endpoint. These providers process information necessary to deliver their services. Optional analytics uses <strong>Google Analytics</strong> after your permission.</p>
<p>Our team uses enquiry information to assess the project. When needed to prepare a requested proposal, relevant requirements may be shared with hotels, venues, transport providers or event suppliers. We aim to share programme requirements rather than identifying guest details at this initial stage. Information may also be disclosed to professional advisers or competent authorities where necessary for legal matters or a legal obligation.</p>
<p>External WhatsApp links open a separate service only when you choose to follow them. Information you send there is also subject to that service’s privacy terms.</p>
<h2>5. Processing outside Türkiye</h2>
<p>Hosting, email delivery and optional analytics can involve processing outside Türkiye. Resend states that its primary processing and stored customer data are in the United States. The location and subprocessors used by Vercel and Google depend on their services and configurations.</p>
<p>Cross-border processing is subject to the transfer requirements of the applicable law, including KVKK Article 9 where it applies. A provider’s privacy policy alone does not establish the controller’s transfer arrangements. Contact us to request information about the arrangements applicable to your data.</p>
<p>Provider information: <a href="https://vercel.com/legal/privacy-policy" target="_blank" rel="noopener">Vercel Privacy Policy</a>, <a href="https://resend.com/legal/privacy-policy" target="_blank" rel="noopener">Resend Privacy Policy</a>, <a href="https://resend.com/legal/dpa" target="_blank" rel="noopener">Resend Data Processing Addendum</a>, and <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy Policy</a>.</p>
<h2>6. How long is information kept?</h2>
<p>Enquiry correspondence is retained for the time needed to respond, prepare and follow up on your requested proposal. If a project proceeds, relevant records may be retained for delivery, accounting, applicable statutory retention requirements and legal claims. Retention depends on the record and purpose; information should be deleted or anonymised when those purposes and obligations no longer require it.</p>
<p>Browser storage lifetimes and how to withdraw analytics permission are described in our <a href="/cookie-policy/">Cookie Policy</a>. Provider-held delivery and technical logs have separate provider retention settings.</p>
<h2>7. Security</h2>
<p>The website uses HTTPS. The enquiry is sent through a server-side endpoint; the email delivery API key is not included in browser code. Form fields are checked and escaped before being included in enquiry emails. No internet transmission is risk-free, so please avoid sending sensitive data through the initial brief.</p>
<h2>8. Your rights and how to contact us</h2>
<p>Under KVKK Article 11, subject to its conditions, you may ask whether your data is processed, request information about processing and its purposes, learn about recipients in Türkiye or abroad, request correction or deletion where applicable, request that relevant changes be notified to recipients, object to a result against you arising solely from automated analysis, and seek compensation for unlawful processing.</p>
<p>Where other applicable laws provide additional rights, these may include access, restriction, portability, objection and a complaint to the competent data protection authority. This website’s budget calculator produces an indicative estimate from your selections; it does not make a binding booking or eligibility decision.</p>
<p>Email <a href="mailto:{cfg.ORG_EMAIL}">{cfg.ORG_EMAIL}</a> with the subject “Privacy request”, or write to our postal address. Tell us the request and enough information to identify the relevant enquiry. We may need to verify your identity, but please do not send identity documents unsolicited. We respond within the applicable legal timeframe. KVKK applications are generally concluded within 30 days under Article 13, subject to the prescribed application requirements.</p>
<h2>9. Changes to this notice</h2>
<p>We will update this page when the described processing changes. The date above reflects the review of this notice. For cookie choices, use <button type="button" data-cookie-settings>Cookie Settings</button>.</p>'''

COOKIES = '''<div class="legal-summary"><p><strong>Optional analytics is off until you accept it.</strong> Rejecting analytics does not prevent you from browsing, using the budget calculator or sending a proposal request.</p><p><button type="button" class="btn btn--ghost" data-cookie-settings>Change Cookie Settings</button></p></div>
<h2>1. Cookies and browser storage</h2>
<p>Cookies are small values saved by your browser. This website also uses local storage and session storage. Session storage normally lasts for the current tab session; local storage remains until it is removed or its saved preference expires.</p>
<h2>2. Essential preferences and requested features</h2>
<ul><li><strong>dmc_cookie_choice_v1 (local storage):</strong> records whether optional analytics was accepted or rejected and when the choice was made. The site honours this choice for 180 days, then asks again. The saved value contains no name, email or brief; it may remain in storage until overwritten or cleared.</li>
<li><strong>dtp_calculator_state (session storage):</strong> preserves your chosen event budget assumptions and result so that you can include them in a proposal request. This supports the calculator feature you choose to use and lasts for the tab session. It does not store your name, email or free-text brief.</li></ul>
<p>Hosting and network services may also process operational and security information needed to serve requests. These are separate from optional Google Analytics.</p>
<h2>3. Optional analytics and attribution</h2>
<p>Google Analytics 4 is configured to load only after you select “Accept optional analytics”. Before that, and when you reject it, the site does not load the Google analytics tag or send analytics events. Google advertising storage and advertising personalisation consent remain denied.</p>
<ul><li><strong>_ga and _ga_&lt;measurement suffix&gt;:</strong> Google Analytics cookies used to distinguish visits and maintain session information. Google’s standard default cookie expiry is up to two years and may be refreshed on later visits; browser limits and property settings can shorten this.</li>
<li><strong>proposal_campaign (session storage):</strong> remembers the service and campaign context while moving to the proposal form, after analytics permission.</li>
<li><strong>proposal_landing_page (session storage):</strong> retains a proposal entry-page URL without its query string, after analytics permission.</li></ul>
<p>Optional usage data helps us understand which pages and tools are useful. Your name, work email and written brief are not included in analytics event fields. Google may process usage information outside Türkiye; see our <a href="/privacy-policy/">Privacy Policy</a> and <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener">Google’s cookie information</a>.</p>
<h2>4. Accepting, rejecting or withdrawing</h2>
<p>The banner provides separate, equally accessible accept and reject buttons. You can reopen it using “Cookie Settings” in any page footer or the button above. Continuing to browse does not count as acceptance.</p>
<p>If you change from acceptance to rejection, the site disables analytics, removes its accessible Google Analytics cookies and optional proposal-attribution storage, and reloads the page to unload the previously loaded tag. This stops future collection through this website; it does not erase data already sent to Google. Use the contact details in the Privacy Policy for a data request.</p>
<p>You can also clear site data or block storage in your browser. The site may then ask again for your choice, and the calculator may no longer carry your selections between pages. The enquiry form remains available. If JavaScript is disabled, the optional analytics loader does not run.</p>
<h2>5. External links and updates</h2>
<p>Links to WhatsApp, provider privacy policies and external reference documents take you to separate services with their own privacy practices. They are not embedded analytics features.</p>
<p>This notice is reviewed when the site’s storage or measurement setup changes. See the <a href="/privacy-policy/">Privacy Policy</a> for the operator, contact details and your rights.</p>'''

TERMS = f'''<div class="legal-summary"><p><strong>A request is not a booking.</strong> This website helps international agencies and business event planners request local support in Türkiye. Submitting a brief, viewing an indicative price or using a calculator does not reserve a hotel, vehicle, venue or service.</p></div>
<h2>1. Website operator and scope</h2>
{IDENTITY}
<p>These terms cover use of this website and the initial enquiry process. The site presents destination management, MICE, group travel, event production and local operational support primarily for business buyers. Project-specific services are subject to a separate written proposal and agreement.</p>
<h2>2. Enquiries and proposals</h2>
<p>Please provide accurate requirements and contact information, and only submit information you are authorised to share. We use the brief to assess the requested scope and discuss available options. An automated acknowledgement confirms receipt of an enquiry, not acceptance of a project or a booking.</p>
<p>Supplier availability, dates, capacities and operational requirements must be checked for the particular programme. A booking or service commitment is confirmed only through the applicable written agreement and its stated confirmation process.</p>
<h2>3. Website prices and budget estimates</h2>
<p>Any website price, example programme cost or calculator result is indicative unless a specific offer expressly states otherwise. It is not a binding quote. Final pricing depends on dates, group size, supplier availability, scope, currency, applicable taxes and other requirements.</p>
<p>A written proposal should set out the currency, included services, exclusions, taxes, validity period and any assumptions. Do not assume that travel, accommodation, venue hire, staffing, equipment, permits or other services are included unless the proposal expressly includes them.</p>
<h2>4. Payment, changes and cancellation</h2>
<p>This website’s enquiry form does not collect card details or payments. If a project proceeds, the written proposal or agreement must specify the contracting party, payment recipient, deposit or instalment schedule and confirmation conditions.</p>
<p>Changes, cancellations, refunds and postponements depend on the agreed project terms and the relevant supplier commitments. No universal cancellation period, refundable deposit or free-change entitlement is offered by this website. Ask for the applicable conditions before confirming a project or making a payment. This does not limit mandatory rights under applicable law.</p>
<h2>5. Our role and supplier responsibilities</h2>
<p>The proposal should identify which services the contracting operator supplies directly, which are coordinated through third parties and who is responsible for each element. Hotels, venues, transport companies and production suppliers may have their own operating conditions. Agency and white-label arrangements must be documented for the particular project; the website alone does not establish exclusivity, representation rights or a partnership contract.</p>
<h2>6. Destination information and official event processes</h2>
<p>Travel requirements, event arrangements, schedules, venues, prices and availability can change. Confirm critical details with the relevant official authority, organiser or supplier before acting on them.</p>
<p>DMC Turkey Partner is an independent local service provider. References to COP31, UNFCCC or other event organisers do not imply official appointment, endorsement or affiliation. Accreditation, official registration and visa decisions remain with the relevant authorities; purchasing local services does not guarantee any of them.</p>
<h2>7. Project references and intellectual property</h2>
<p>Project references describe the stated scope of work by the team or production network. A listed client or event name does not by itself mean an ongoing commercial relationship or endorsement. Third-party names and trademarks belong to their owners.</p>
<p>Website text, design and original materials may be viewed for evaluating our services. Republishing or commercially reusing protected material requires permission from the relevant rights holder. You retain rights in the brief and materials you submit, while allowing us to use them as needed to respond to your request and prepare the requested proposal.</p>
<h2>8. Appropriate use and privacy</h2>
<p>Do not use the site to submit unlawful material, impersonate another person, send spam, interfere with the enquiry service, access restricted systems or extract confidential information. Please do not submit passport, payment card or sensitive personal information in the initial form.</p>
<p>How enquiry and usage information is handled is described in our <a href="/privacy-policy/">Privacy Policy</a> and <a href="/cookie-policy/">Cookie Policy</a>. Sending a brief is not agreement to unrelated marketing, and analytics permission is optional.</p>
<h2>9. Questions, concerns and governing terms</h2>
<p>For a question, complaint or suspected payment instruction issue, contact <a href="mailto:{cfg.ORG_EMAIL}">{cfg.ORG_EMAIL}</a> or <a href="tel:{cfg.ORG_PHONE}">{cfg.ORG_PHONE_DISPLAY}</a>. Include the project or proposal reference if available, without attaching sensitive information unnecessarily.</p>
<p>Website use is subject to applicable Turkish law and any mandatory rights that apply. The separate project agreement may specify governing law, dispute arrangements and service responsibilities. Nothing in these website terms excludes liability or rights that cannot lawfully be excluded.</p>
<h2>10. Changes</h2>
<p>We may update these website terms as the site or enquiry process changes. The review date appears above. Later website updates do not automatically amend an existing signed project agreement.</p>'''

PAGES = {
    'privacy-policy': ('Privacy Policy', 'How DMC Turkey Partner handles proposal enquiries, technical information, optional analytics, service providers and privacy requests.', PRIVACY),
    'cookie-policy': ('Cookie Policy', 'Essential browser storage, optional Google Analytics, and how to accept, reject or change your cookie choices on DMC Turkey Partner.', COOKIES),
    'terms': ('Terms & Conditions', 'Website and enquiry terms for DMC Turkey Partner: proposals, indicative prices, booking confirmation, payment, changes and cancellation.', TERMS),
}

def main():
    for slug, (title, description, content) in PAGES.items():
        path = ROOT / slug / 'index.html'
        original = path.read_text()
        body = f'''<main id="main-content" class="page--legal">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">{escape(title)}</li></ol></nav>
    <h1>{escape(title)}</h1>
    <p class="legal-updated">Last reviewed: <time datetime="2026-10-08">{UPDATED}</time></p>
    {content}
  </main>'''
        updated = re.sub(r'<main\b.*?</main>', lambda _: body, original, count=1, flags=re.S)
        updated = re.sub(r'(<meta (?:name|property)="(?:description|og:description)" content=")[^"]*(">)', lambda m: m[1] + escape(description, quote=True) + m[2], updated)
        if updated != original:
            path.write_text(updated)
            print('Updated', slug)

if __name__ == '__main__':
    main()
