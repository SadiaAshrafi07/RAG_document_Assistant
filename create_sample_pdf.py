"""Generates TechCorp_Official_Employee_Handbook.pdf, the sample document for the demo.

Run:  python create_sample_pdf.py
(Requires: pip install reportlab)
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

SECTIONS = [
    ("1. Welcome to TechCorp", [
        "Welcome to TechCorp! This handbook explains how we work, what you can expect from us, "
        "and what we expect from you. It applies to all full-time employees.",
        "If something in this handbook is unclear, please contact the People Operations team at "
        "people@techcorp.example. This handbook is updated every year in January.",
    ]),
    ("2. Working Hours and Remote Work", [
        "Our core working hours are 10:00 AM to 4:00 PM local time, Monday to Friday. Outside of "
        "core hours you may arrange your schedule with your manager.",
        "You are permitted to work from home on Tuesdays and Thursdays. Additional remote "
        "flexibility may also be approved by your department manager.",
        "Employees working from home must be reachable on Slack and attend all scheduled "
        "meetings with their camera on, unless the meeting organizer says otherwise.",
    ]),
    ("3. Leave and Time Off", [
        "Every full-time employee receives 20 days of paid time off (PTO) per calendar year. "
        "PTO accrues monthly and up to 5 unused days can be carried over into the next year.",
        "Sick leave is separate from PTO. Employees receive 10 days of paid sick leave per year. "
        "A doctor's note is required for sick leave longer than 3 consecutive days.",
        "Parental leave: primary caregivers receive 16 weeks of fully paid leave and secondary "
        "caregivers receive 6 weeks of fully paid leave.",
        "To request PTO, submit a request in the HR portal at least 2 weeks in advance for "
        "absences longer than 3 days.",
    ]),
    ("4. Dress Code", [
        "TechCorp has a business casual dress code. Jeans and sneakers are allowed on any day "
        "of the week. Clothing with offensive slogans is not permitted.",
        "On client visit days, employees are expected to wear business attire such as a "
        "collared shirt or blouse and smart trousers.",
    ]),
    ("5. Expenses and Equipment", [
        "TechCorp provides every new employee with a laptop, a monitor, and a headset. "
        "Remote employees also receive a one-time home office allowance of $500.",
        "Business travel must be booked through the company travel portal. Meals during travel "
        "are reimbursed up to $60 per day. All expense reports must be submitted within 30 days "
        "of the expense.",
        "The annual learning and development budget is $1,200 per employee. It can be used for "
        "courses, books, certifications, and conferences.",
    ]),
    ("6. Information Security", [
        "All employees must use the company password manager and enable two-factor "
        "authentication on every work account.",
        "Never share customer data over personal email or personal messaging apps. Report lost "
        "devices or suspected phishing emails to security@techcorp.example within one hour.",
        "Company laptops must be locked whenever you leave your desk, and software may only be "
        "installed from the approved company software catalog.",
    ]),
    ("7. Performance Reviews and Promotions", [
        "Performance reviews take place twice a year, in June and December. Each review includes "
        "a self-assessment, peer feedback, and a manager assessment.",
        "Promotions are considered during the December review cycle. Employees must have been "
        "in their current role for at least 12 months to be eligible.",
    ]),
    ("8. Code of Conduct", [
        "TechCorp is committed to a respectful, inclusive workplace. Harassment or discrimination "
        "of any kind is not tolerated and may result in termination.",
        "Employees may report concerns confidentially through the ethics hotline or directly to "
        "People Operations. Retaliation against anyone who reports a concern in good faith is "
        "strictly prohibited.",
    ]),
]


def build(path="TechCorp_Official_Employee_Handbook.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=A4, title="TechCorp Official Employee Handbook")
    story = [
        Paragraph("TechCorp Official Employee Handbook", styles["Title"]),
        Paragraph("Version 2026 - for internal use", styles["Normal"]),
        Spacer(1, 24),
    ]
    for i, (heading, paragraphs) in enumerate(SECTIONS):
        story.append(Paragraph(heading, styles["Heading2"]))
        for p in paragraphs:
            story.append(Paragraph(p, styles["BodyText"]))
            story.append(Spacer(1, 8))
        story.append(Spacer(1, 10))
        if i in (2, 5):  # force a few page breaks so the PDF has several pages
            story.append(PageBreak())
    doc.build(story)
    print(f"Created {path}")


if __name__ == "__main__":
    build()
