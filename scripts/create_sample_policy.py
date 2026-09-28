from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = Path("output/pdf/sample_hr_policy_handbook.pdf")
NAVY = colors.HexColor("#173B64")
BLUE = colors.HexColor("#2D6AA0")
PALE_BLUE = colors.HexColor("#EAF2F8")
INK = colors.HexColor("#1E293B")
MUTED = colors.HexColor("#52657A")


def footer(canvas, document):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(colors.HexColor("#D8E1EA"))
    canvas.line(0.65 * inch, 0.55 * inch, width - 0.65 * inch, 0.55 * inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.65 * inch, 0.36 * inch, "Northstar People Policy Handbook | Fictional sample document")
    canvas.drawRightString(width - 0.65 * inch, 0.36 * inch, f"Page {document.page}")
    canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Helvetica-Bold", fontSize=29,
            leading=34, textColor=NAVY, alignment=TA_CENTER, spaceAfter=14,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Helvetica", fontSize=12,
            leading=18, textColor=MUTED, alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=19,
            leading=24, textColor=NAVY, spaceBefore=2, spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12,
            leading=16, textColor=BLUE, spaceBefore=12, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Helvetica", fontSize=10,
            leading=15, textColor=INK, spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Helvetica", fontSize=10,
            leading=15, textColor=INK, leftIndent=15, firstLineIndent=-10, spaceAfter=4,
        ),
        "callout": ParagraphStyle(
            "Callout", parent=base["BodyText"], fontName="Helvetica", fontSize=10,
            leading=15, textColor=INK, leftIndent=12, rightIndent=12, spaceBefore=8, spaceAfter=10,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["Normal"], fontName="Helvetica", fontSize=8.5,
            leading=12, textColor=MUTED,
        ),
    }


def policy_section(styles, number, title, purpose, rules, contacts=None):
    story = [Paragraph(f"{number}. {title}", styles["h1"]), Paragraph(purpose, styles["body"])]
    for heading, paragraphs, bullets in rules:
        story.append(Paragraph(heading, styles["h2"]))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, styles["body"]))
        for item in bullets:
            story.append(Paragraph(f"- {item}", styles["bullet"]))
    if contacts:
        note = Paragraph(f"<b>Where to get help:</b> {contacts}", styles["callout"])
        callout = Table([[note]], colWidths=[6.65 * inch])
        callout.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#B8D3E7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(callout)
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=0.8 * inch, leftMargin=0.8 * inch,
        topMargin=0.75 * inch, bottomMargin=0.8 * inch,
        title="Northstar People Policy Handbook",
        author="Northstar Services (fictional)",
    )
    story = []

    story.extend([
        Spacer(1, 1.3 * inch),
        Paragraph("NORTHSTAR", ParagraphStyle("Brand", parent=styles["subtitle"], fontName="Helvetica-Bold", fontSize=13, textColor=BLUE, leading=18)),
        Spacer(1, 0.18 * inch),
        Paragraph("People Policy Handbook", styles["title"]),
        Paragraph("A fictional sample policy for demonstrating a PDF question-answering assistant", styles["subtitle"]),
        Spacer(1, 0.55 * inch),
    ])
    cover_table = Table([
        ["Version", "1.0"],
        ["Effective date", "1 October 2026"],
        ["Applies to", "All Northstar Services employees"],
        ["Owner", "People Operations"],
    ], colWidths=[1.7 * inch, 4.55 * inch])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEADING", (0, 0), (-1, -1), 14),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8E1EA")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [cover_table, Spacer(1, 0.35 * inch), Paragraph("This handbook is a sample only. It does not create a contract, legal right, or real workplace policy.", styles["small"]), PageBreak()]

    story += [Paragraph("Contents", styles["h1"])]
    contents = [
        ("1", "How to use this handbook"), ("2", "Workplace conduct and respect"),
        ("3", "Working hours and attendance"), ("4", "Leave and time away"),
        ("5", "Pay, benefits, and expenses"), ("6", "Flexible and remote work"),
        ("7", "Performance and development"), ("8", "Information security and privacy"),
        ("9", "Acknowledgment"),
    ]
    table_data = [[Paragraph(f"<b>{number}</b>", styles["body"]), Paragraph(title, styles["body"])] for number, title in contents]
    contents_table = Table(table_data, colWidths=[0.55 * inch, 5.7 * inch])
    contents_table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8E1EA")),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [contents_table, Spacer(1, 0.22 * inch), Paragraph("Questions about this handbook should be directed to People Operations at peopleops@northstar.example.", styles["callout"]), PageBreak()]

    sections = [
        ("1", "How to use this handbook", "This handbook explains the working expectations and benefits offered by Northstar Services. It applies unless a written employment agreement or local law provides a more favorable requirement.", [
            ("Policy updates", ["People Operations may update this handbook when business, legal, or operational needs change. Employees will receive notice of material changes."], []),
            ("Questions and interpretation", ["Managers and People Operations can explain a policy. Only People Operations may approve an exception, and exceptions must be confirmed in writing."], []),
        ], "Contact People Operations for an explanation or a written exception request."),
        ("2", "Workplace conduct and respect", "Northstar is committed to a workplace where people are treated with dignity, respect, and professionalism.", [
            ("Expected behavior", ["Employees must communicate respectfully, avoid abusive or discriminatory conduct, and cooperate with reasonable workplace directions."], ["Do not harass, bully, threaten, or retaliate against another person.", "Do not make employment decisions based on protected personal characteristics.", "Raise concerns promptly through a manager, People Operations, or the confidential reporting channel."]),
            ("Reporting and review", ["Reports will be reviewed as promptly and fairly as practical. Northstar will handle information discreetly, but cannot promise absolute confidentiality where an investigation or legal obligation requires disclosure."], []),
        ], "Report a concern to People Operations, your manager, or ethics@northstar.example."),
        ("3", "Working hours and attendance", "Reliable attendance helps teams serve customers and each other. Standard full-time working hours are 9:00 a.m. to 5:30 p.m., Monday through Friday, including a 30-minute unpaid meal break.", [
            ("Attendance", ["Employees must be ready to work at their scheduled start time. If an employee will be late or absent, they must notify their manager as soon as possible and no later than 30 minutes before their scheduled start time."], ["Use the team-approved attendance channel when available.", "Provide the expected duration of an absence when known.", "Record working time accurately and promptly."]),
            ("Overtime", ["Non-exempt employees may work overtime only with advance manager approval. Approved overtime will be paid or compensated in accordance with applicable law."], []),
        ], "For unexpected absence, contact your manager first and People Operations if the absence lasts more than two workdays."),
        ("4", "Leave and time away", "Northstar supports planned time away and provides leave in line with this handbook and applicable law.", [
            ("Annual leave", ["Full-time employees receive 20 paid working days of annual leave per calendar year, accrued monthly. Part-time leave is prorated. Employees should request planned leave at least 10 calendar days in advance through the leave system."], ["Up to 5 unused annual leave days may carry into the next calendar year.", "Carried leave must be used by 31 March or it expires, unless local law requires otherwise.", "Managers may decline dates only when significant business coverage needs cannot reasonably be met."]),
            ("Sick leave", ["Employees may take up to 10 paid sick days each calendar year. Notify your manager before the scheduled start time where possible. A medical certificate may be requested for an absence lasting more than 3 consecutive workdays."], []),
            ("Family and other protected leave", ["Northstar provides family, parental, bereavement, jury, and other protected leave as required by applicable law. Employees should contact People Operations before taking planned protected leave whenever feasible."], []),
        ], "Request planned leave through the leave system. For protected leave questions, contact People Operations."),
        ("5", "Pay, benefits, and expenses", "Northstar aims to pay employees accurately and reimburse approved business costs promptly.", [
            ("Pay", ["Employees are paid monthly on the last business day of each month. If a pay date falls on a public holiday or weekend, payment will normally be made on the preceding business day."], []),
            ("Benefits", ["Eligible full-time employees may enroll in the medical, dental, and retirement plans described in the annual benefits guide. Eligibility, plan terms, and enrollment windows are controlled by the plan documents."], []),
            ("Expenses", ["Employees must obtain manager approval before committing material business costs. Submit receipts and an expense claim within 30 days of the expense. Alcohol, personal upgrades, and unapproved costs are not reimbursable."], []),
        ], "Contact Payroll for pay questions and Finance Operations for expense claims."),
        ("6", "Flexible and remote work", "Flexible work may help employees perform effectively while meeting team and customer needs. It is a working arrangement, not an entitlement.", [
            ("Eligibility and approval", ["Employees may request a regular remote or flexible schedule from their manager. Approval depends on role requirements, performance, team coverage, data security, and local law. Approved arrangements should be documented and reviewed at least annually."], []),
            ("Working remotely", ["Remote employees must remain reachable during agreed core hours, use approved systems, protect company information, and maintain a safe, suitable workspace."], ["Do not use public Wi-Fi for confidential work unless connected through the approved VPN.", "Do not allow family members or visitors to view confidential company information.", "Attend in-person meetings when reasonably required for the role."]),
        ], "Discuss a flexible work request with your manager before changing your normal work location."),
        ("7", "Performance and development", "Northstar gives employees regular feedback so expectations, progress, and development needs are clear.", [
            ("Check-ins", ["Managers should hold regular one-to-one meetings and at least two documented performance conversations each year. Employees are expected to prepare, discuss goals, and raise obstacles early."], []),
            ("Addressing performance concerns", ["When performance or conduct does not meet expectations, Northstar may provide coaching, a documented improvement plan, or other corrective action. The response will consider the facts, prior feedback, seriousness, and applicable law."], []),
        ], "Speak with your manager about development goals or ask People Operations for guidance on a performance process."),
        ("8", "Information security and privacy", "Employees are responsible for protecting Northstar, customer, and colleague information.", [
            ("Approved tools", ["Use only approved company accounts, storage locations, and collaboration tools for business information. Do not forward company data to personal email or copy it into unapproved AI, messaging, or file-sharing services."], []),
            ("Incidents", ["Report a suspected lost device, phishing message, unauthorized disclosure, or security incident immediately to security@northstar.example. Prompt reporting is required even when the employee is unsure whether data was exposed."], []),
        ], "For an urgent security concern, contact security@northstar.example immediately."),
        ("9", "Acknowledgment", "Employees are expected to read this handbook and ask questions when a policy is unclear.", [
            ("Acknowledgment", ["By continuing employment, employees acknowledge receipt of this handbook and understand that they are responsible for following applicable policies. This acknowledgment does not change the at-will or contractual status of employment where applicable."], []),
        ], "People Operations keeps the current handbook and answers policy questions."),
    ]
    for index, section in enumerate(sections):
        story += policy_section(styles, *section)
        if index != len(sections) - 1:
            story.append(PageBreak())

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT.resolve())


if __name__ == "__main__":
    main()
