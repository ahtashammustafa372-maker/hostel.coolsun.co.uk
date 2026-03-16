from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_pdf(filename, title, content_blocks):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.black
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=12,
        spaceBefore=5,
        spaceAfter=5,
        leading=16
    )

    story = []
    
    # Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    for block in content_blocks:
        if block['type'] == 'heading':
            story.append(Paragraph(block['text'], heading_style))
        elif block['type'] == 'body':
            story.append(Paragraph(block['text'], body_style))
        elif block['type'] == 'bullet':
            story.append(Paragraph(f"• {block['text']}", body_style))
            
    doc.build(story)
    print(f"✅ Generated: {filename}")

# --- English Content ---
english_content = [
    {'type': 'heading', 'text': '1. Morning Briefing & Dashboard'},
    {'type': 'body', 'text': 'Open the "War Room" Dashboard every morning.'},
    {'type': 'bullet', 'text': '<b>Green Light:</b> All tenants are compliant.'},
    {'type': 'bullet', 'text': '<b>Yellow Light:</b> Warning - Documents are aging.'},
    {'type': 'bullet', 'text': '<b>Red Light:</b> URGENT - Missing Police Forms or Expired CNICs.'},
    {'type': 'body', 'text': '<b>Action:</b> Address all Red lights before 12:00 PM daily.'},

    {'type': 'heading', 'text': '2. Onboarding New Tenants (The Wizard)'},
    {'type': 'body', 'text': 'Click "New Onboarding" for every new arrival.'},
    {'type': 'bullet', 'text': '<b>Step 1:</b> Select the Bed from the visual map.'},
    {'type': 'bullet', 'text': '<b>Step 2:</b> Enter Name and Phone.'},
    {'type': 'bullet', 'text': '<b>Step 3:</b> Upload photos of CNIC (Front/Back) and a Live Face Photo.'},
    {'type': 'bullet', 'text': '<b>15-Day Rule:</b> If after the 15th, the system charges pro-rata + next month rent automatically.'},

    {'type': 'heading', 'text': '3. Maintenance & Cash Logic'},
    {'type': 'body', 'text': 'Log every repair (Fan, Leak, etc.) in the Issue Inbox.'},
    {'type': 'bullet', 'text': 'Mark as "Critical" if urgent.'},
    {'type': 'bullet', 'text': 'When resolving, if you paid the plumber from the hostel drawer, select "Paid from Cash Drawer."'},
    {'type': 'bullet', 'text': 'Enter the exact amount to keep the ledger balanced.'},

    {'type': 'heading', 'text': '4. Daily Closing (Shift Handover)'},
    {'type': 'body', 'text': 'At 10:00 PM, open "Daily Closing."'},
    {'type': 'bullet', 'text': 'Compare Physical Cash in your hand to "Expected Cash" on screen.'},
    {'type': 'bullet', 'text': 'If they match, click "Submit Handover." This sends a report to the Owner.'},

    {'type': 'heading', 'text': '5. Offline & Troubleshooting'},
    {'type': 'bullet', 'text': '<b>Internet Down:</b> Use a physical register, then sync to the system as soon as the web returns.'},
    {'type': 'bullet', 'text': '<b>Cash Discrepancy:</b> Re-check your expenses before submitting if the totals don\'t match.'},
]

# --- Urdu Content ---
urdu_content = [
    {'type': 'heading', 'text': '1. Subha ki Routine (War Room)'},
    {'type': 'body', 'text': 'Har subha "War Room" Dashboard kholain aur Traffic Lights check karain.'},
    {'type': 'bullet', 'text': '<b>Sabz (Green):</b> Sab theek hai.'},
    {'type': 'bullet', 'text': '<b>Peela (Yellow):</b> Warning - Kaghzat mangwa lain.'},
    {'type': 'bullet', 'text': '<b>Laal (Red):</b> FORAN KAAM KARAIN - Police form ya ID card expire hai.'},
    {'type': 'body', 'text': '<b>Zaroori:</b> Rozana 12 baje se pehle Laal lights ko clear karain.'},

    {'type': 'heading', 'text': '2. Naya Kirayedar (The Wizard)'},
    {'type': 'body', 'text': 'Naye kirayedar ke liye "New Onboarding" dabain.'},
    {'type': 'bullet', 'text': '<b>Step 1:</b> Nakshay se Bed select karain.'},
    {'type': 'bullet', 'text': '<b>Step 2:</b> Naam aur Phone number likhain.'},
    {'type': 'bullet', 'text': '<b>Step 3:</b> CNIC (Aagay/Peechay) aur Kirayedar ke chehray ki saaf tasveer lain.'},
    {'type': 'bullet', 'text': '<b>15-Day Rule:</b> 15 tareekh ke baad system aglay mahine ka kiraya khud hi shamil kar dega.'},

    {'type': 'heading', 'text': '3. Maintenance aur Cash'},
    {'type': 'body', 'text': 'Har shikayat (Pankha, Leakage) "Issue Inbox" mein likhain.'},
    {'type': 'bullet', 'text': 'Masla bara ho to "Critical" mark karain.'},
    {'type': 'bullet', 'text': 'Resolution ke waqt agar hostel ke paison se payment ki hai, to "Paid from Cash Drawer" select karain.'},
    {'type': 'bullet', 'text': 'Sahi raqam likhain taake hisab saaf rahe.'},

    {'type': 'heading', 'text': '4. Raat ki Closing (Shift Handover)'},
    {'type': 'body', 'text': 'Raat 10 baje "Daily Closing" card kholain.'},
    {'type': 'bullet', 'text': 'Apne paas maujood Cash ko screen par "Expected Cash" se milain.'},
    {'type': 'bullet', 'text': 'Agar barabar hai to "Submit Handover" dabain. Malik ko report chali jaye gi.'},

    {'type': 'heading', 'text': '5. Offline aur Troubleshooting'},
    {'type': 'bullet', 'text': '<b>Internet Band:</b> Details register mein likh lain, internet aate hi system mein entry karain.'},
    {'type': 'bullet', 'text': '<b>Hisab mein Ghalti:</b> Agar cash kam ho to pehle apne Expenses check karain ke koi kharcha likhna to nahi bhool gaye.'},
]

if __name__ == '__main__':
    create_pdf('STAFF_GUIDE_ENGLISH.pdf', 'Coolsun Hostel ERP: Official English Staff Manual (2026)', english_content)
    create_pdf('STAFF_GUIDE_URDU.pdf', 'Coolsun Hostel ERP: Roman Urdu Staff Manual (2026)', urdu_content)
