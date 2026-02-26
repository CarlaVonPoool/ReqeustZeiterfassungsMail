import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="📧 E-Mail Baukasten", layout="wide")

# Custom CSS for better styling
st.markdown("""
<style>
    .block-container { max-width: 1200px; padding-top: 2rem; }
    .stCheckbox { padding-top: 20px; }
    iframe { border: none; }
</style>
""", unsafe_allow_html=True)

st.title("📧 E-Mail Baukasten")
st.markdown("Konfiguriere hier die wöchentliche Zeiterfassungsmail für dein Team.")
st.divider()

# ── Unternehmen ──

st.subheader("Unternehmen")
unternehmen = st.text_input("Name des Unternehmens", placeholder="z.B. Muster GmbH")
st.divider()

# ── 1. Mail-Typ Auswahl ──

st.subheader("1. Welche E-Mails möchtest du aktivieren?")

col1, col2 = st.columns(2)

with col1:
    zeiterfassung_aktiv = st.checkbox("✅ Zeiterfassungsmail", value=True)

with col2:
    pm_aktiv = st.checkbox("✅ Projektmanagement-Mail", value=False)

# Mail-Optionen für Kompatibilität
mail_optionen = []
if zeiterfassung_aktiv:
    mail_optionen.append("Zeiterfassungsmail")
if pm_aktiv:
    mail_optionen.append("Projektmanagement-Mail")

if not mail_optionen:
    st.info("Keine Mail-Art ausgewählt. Es werden keine wöchentlichen Mails versendet.")
    st.divider()
    
    N8N_WEBHOOK_URL = "https://poool.app.n8n.cloud/webhook/7000884e-6635-4d83-a6ea-6c242857c004"
    
    if st.button("✅ Auswahl an Poool senden", type="primary"):
        payload = {
            "timestamp": datetime.now().isoformat(),
            "unternehmen": unternehmen if unternehmen else "",
            "zeiterfassungsmail_aktiv": False,
            "pm_mail_aktiv": False,
            "beschreibung": "Kunde möchte keine automatischen Mails erhalten.",
        }
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            if response.ok:
                st.success("📤 Auswahl erfolgreich an Poool gesendet!")
            else:
                st.error(f"Fehler: Status {response.status_code} – {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Verbindungsfehler zu Poool: {e}")
    
    st.stop()


# ── E-Mail Adresse für Beispiele ──

st.divider()
st.subheader("2. E-Mail Adresse für Beispiel-Mails")
beispiel_email = st.text_input(
    "E-Mail Adresse für die Beispiel-Vorschau", 
    placeholder="z.B. max.mustermann@firma.de",
    help="Diese Adresse wird nur für die Vorschau verwendet und nicht gespeichert"
)

# ── Mail sections as HTML snippets ──

# Zeiterfassungsmail Sektionen
zeiterfassung_sections = {
    "Header (Wochenübersicht)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 35px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 22px; font-weight: 300; margin-bottom: 6px;">Deine Woche im Überblick</div>
<div style="color: #ffffff; font-size: 26px; font-weight: 700; margin-bottom: 8px;">16.02. – 20.02.2026</div>
<div style="color: #9ca3af; font-size: 13px;">Datenstand: 26.02.2026 03:01</div>
</td></tr></table>
""",

    "Fortschrittsanzeige (100% Complete)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #e5e7eb;">
<tr><td style="padding: 35px 30px; text-align: center;">
<div style="color: #1a1a1a; font-size: 48px; font-weight: 700; margin-bottom: 4px;">100%</div>
<div style="color: #94a3b8; font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;">COMPLETE</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="80%" align="center" style="height: 14px; border-radius: 7px; overflow: hidden; margin-bottom: 20px;">
<tr><td width="100%" style="background-color: #34A853; height: 14px;"></td></tr></table>
<div style="color: #1a1a1a; font-size: 22px; font-weight: 700; margin-bottom: 8px;">Perfekt, {{Vorname}}!</div>
<div style="color: #666666; font-size: 15px; margin-bottom: 25px;">Alle Stunden sind vollstaendig gebucht.</div>
</td></tr></table>
""",

    "Zeiterfassung Übersicht (SOLL/IST)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Zeiterfassung in der KW 2026/08</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border: 1px solid #e5e7eb; border-radius: 12px; margin-bottom: 16px;">
<tr><td style="padding: 20px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td style="color: #666666; font-size: 14px; padding: 8px 0;">SOLL Arbeitszeit:</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 8px 0;">32:00 h</td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 8px 0;">IST Arbeitszeit erfasst:</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 8px 0;">32:00 h <span style="color: #94a3b8; font-size: 12px;">(100%)</span></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td colspan="2" style="height: 1px; background-color: #e5e7eb; padding: 0;"></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 6px 0;">Operative Stunden (abrechenbar):</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 6px 0;">19:00 h <span style="color: #94a3b8; font-size: 12px;">(59%)</span></td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 6px 0;">Interne Stunden (nicht abrechenbar):</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 6px 0;">13:00 h <span style="color: #94a3b8; font-size: 12px;">(41%)</span></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td colspan="2" style="height: 1px; background-color: #e5e7eb; padding: 0;"></td></tr>
<tr><td colspan="2" style="height: 4px;"></td></tr>
<tr><td style="color: #1a1a1a; font-size: 15px; font-weight: 700; padding: 8px 0;">Gesamt gebucht (Projektzeit):</td><td align="right" style="color: #1a1a1a; font-size: 16px; font-weight: 700; padding: 8px 0;">32:00 h <span style="color: #94a3b8; font-size: 12px;">(100%)</span></td></tr>
</table></td></tr></table>
<div style="color: #666666; font-size: 13px; font-weight: 600; margin-bottom: 10px;">Buchungsstand Projektzeit von SOLL:</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 32px; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
<tr><td width="59.0%" style="background-color: #86EFAC; height: 32px; color: #ffffff; font-size: 11px; font-weight: 700; text-align: center; vertical-align: middle;">59%</td>
<td width="41.0%" style="background-color: #60A5FA; height: 32px; color: #ffffff; font-size: 11px; font-weight: 700; text-align: center; vertical-align: middle;">41%</td></tr></table>
<div style="padding: 10px 16px; background-color: #fafafa; border-radius: 10px; margin-top: 6px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
<tr><td style="padding: 3px 14px 3px 0; font-size: 11px; color: #666666;"><span style="display: inline-block; width: 12px; height: 12px; background-color: #86EFAC; border-radius: 3px; vertical-align: middle; margin-right: 5px;"></span>Operativ</td>
<td style="padding: 3px 14px 3px 0; font-size: 11px; color: #666666;"><span style="display: inline-block; width: 12px; height: 12px; background-color: #60A5FA; border-radius: 3px; vertical-align: middle; margin-right: 5px;"></span>Intern</td>
<td style="padding: 3px 14px 3px 0; font-size: 11px; color: #666666;"><span style="display: inline-block; width: 12px; height: 12px; background-color: #f3f4f6; border-radius: 3px; vertical-align: middle; margin-right: 5px;"></span>Fehlend</td></tr></table></div>
</td></tr></table>
""",

    "Wochentage-Status (Mo–Fr)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 20px 10px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #d1fae5; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #065f46; font-size: 16px; font-weight: 700; margin-bottom: 2px;">✓</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Mo</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #d1fae5; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #065f46; font-size: 16px; font-weight: 700; margin-bottom: 2px;">✓</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Di</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #d1fae5; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #065f46; font-size: 16px; font-weight: 700; margin-bottom: 2px;">✓</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Mi</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #d1fae5; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #065f46; font-size: 16px; font-weight: 700; margin-bottom: 2px;">✓</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Do</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #f3f4f6; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #666666; font-size: 16px; font-weight: 700; margin-bottom: 2px;">Frei</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Fr</div></div></td>
</tr></table></td></tr></table>
""",

    "Tagesdetails (Projektzeiterfassung)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Projektzeiterfassung in der KW 2026/08</div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Montag, 16.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:00h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 08:00h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #d1fae5; border-radius: 8px; margin-bottom: 10px;"><span style="color: #065f46; font-size: 11px; font-weight: 700;">Vollstaendig</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="100%" style="background-color: #9CA3AF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">100%</td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Dienstag, 17.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:00h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 08:00h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #d1fae5; border-radius: 8px; margin-bottom: 10px;"><span style="color: #065f46; font-size: 11px; font-weight: 700;">Vollstaendig</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="100%" style="background-color: #9CA3AF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">100%</td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Mittwoch, 18.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:00h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 08:00h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #d1fae5; border-radius: 8px; margin-bottom: 10px;"><span style="color: #065f46; font-size: 11px; font-weight: 700;">Vollstaendig</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="100%" style="background-color: #9CA3AF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">100%</td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Donnerstag, 19.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:00h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 08:00h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #d1fae5; border-radius: 8px; margin-bottom: 10px;"><span style="color: #065f46; font-size: 11px; font-weight: 700;">Vollstaendig</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="100%" style="background-color: #9CA3AF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">100%</td></tr></table></div>
<div style="margin-bottom: 0px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Freitag, 20.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Keine Sollarbeitszeit (frei)</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 00:00h</div></td></tr></table>
<div style="text-align: center; padding: 10px; background-color: #f3f4f6; border-radius: 8px;"><span style="color: #94a3b8; font-size: 13px; font-weight: 600;">Kein Arbeitstag</span></div></div>
</td></tr></table>
""",

    "Nachbuchungen erforderlich (Warnung)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #f59e0b;">
<tr><td style="padding: 25px 30px;">
<div style="color: #8b5a13; font-size: 17px; font-weight: 700; margin-bottom: 12px;">Nachbuchungen erforderlich</div>
<div style="color: #8b5a13; font-size: 13px; margin-bottom: 12px;">An folgenden Tagen fehlen noch Buchungen:</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Montag, 16.02.2026: Arbeitszeit – 00:15h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Dienstag, 17.02.2026: Projektzeit – 01:45h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Mittwoch, 18.02.2026: Projektzeit – 01:45h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Donnerstag, 19.02.2026: Projektzeit – 01:45h fehlen</div>
<div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #D88E20; color: #8b5a13; font-size: 13px; font-weight: 700;">Bitte buche alle fehlenden Zeiten zeitnah nach.</div>
</td></tr></table>
""",

    "Projektübersicht (Tabelle)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb;">
<tr><td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; width: 45%;">Projekt:</td>
<td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; text-align: center; width: 30%;">Kategorie</td>
<td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; text-align: right; width: 25%;">Stunden</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Beispiel Kunde GmbH – Basislizenz: Altvertrag (Pro)</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">14:00 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Muster Software &amp; Consulting – Förderprojekt AI</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">05:00 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Beispiel Firma – Internes Projekt</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Intern</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">13:00 h</td></tr>
</table></td></tr></table>
""",

    "Automatische E-Mail Hinweis": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 25px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 14px; font-weight: 300; margin-bottom: 6px;">Dies ist eine automatische E-Mail von Poool.</div>
<div style="color: #9ca3af; font-size: 13px;">Bei Fragen wende dich bitte an <a href="mailto:support@poool.cc" style="color: #9ca3af; text-decoration: underline;">support@poool.cc</a></div>
</td></tr></table>
""",

}

# Projektmanagement-Mail Sektionen
pm_sections = {
    "PM Header (Projekt-Übersicht)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 35px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 22px; font-weight: 300; margin-bottom: 6px;">Deine Projekt-Übersicht</div>
<div style="color: #ffffff; font-size: 26px; font-weight: 700; margin-bottom: 8px;">Donnerstag, 26. Februar 2026</div>
<div style="color: #9ca3af; font-size: 13px;">Hallo {{Vorname}}, hier ist dein wöchentlicher PM-Report.</div>
<div style="color: #6b7280; font-size: 11px; margin-top: 10px;">Datenstand: 26.02.2026, 08:41 Uhr</div>
</td></tr></table>
""",

    "Handlungsbedarf (Kritische Projekte)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #ef4444;">
<tr><td style="padding: 25px 30px;">
<div style="color: #991b1b; font-size: 17px; font-weight: 700; margin-bottom: 16px;">⚠️ Handlungsbedarf</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td width="50%" style="padding:4px 8px 4px 0;font-size:13px;color:#991b1b;">🔴 1 kritische Projekte</td><td width="50%" style="padding:4px 0 4px 8px;font-size:13px;color:#991b1b;">🚨 2 inaktive Projekte (>14d)</td></tr>
<tr><td width="50%" style="padding:4px 8px 4px 0;font-size:13px;color:#991b1b;">🟡 1 Projekte im Blick behalten</td><td width="50%" style="padding:4px 0 4px 8px;font-size:13px;color:#991b1b;">🎫 5 überfällige Tickets</td></tr>
</table>
<div style="margin-top:6px;padding-top:8px;border-top:1px solid #e5e7eb;font-size:12px;color:#666666;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td style="padding:2px 0;font-size:12px;color:#666666;">4 aktive Projekte  ·  DB II Marge: 18%</td></tr>
<tr><td style="padding:2px 0;font-size:12px;color:#666666;">Team-Projektauslastung: ⌀ 63% (5 MA)</td></tr>
<tr><td style="padding:2px 0;font-size:12px;color:#666666;">Nicht fakturiert: 100.225,00 € (771.2 h)</td></tr>
<tr><td style="padding:2px 0;font-size:12px;color:#666666;">Deckungsbeitrag: 4 kritisch</td></tr>
</table></div>
</td></tr></table>
""",

    "Kennzahlen Übersicht": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 6px;">Deine Kennzahlen</div>
<div style="color: #94a3b8; font-size: 11px; margin-bottom: 20px;">* Kostenansatz: <strong style="color:#333333;">Selbstkostensatz</strong>  |  * Umsatz: <strong style="color:#333333;">Abgerechnet + Auftrag</strong></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:12px;">
<tr>
<td style="vertical-align:top;padding:0 2px;"><div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#666666;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">UMSATZ*</div><div style="color:#1a1a1a;font-size:14px;font-weight:700;">€ 97.292</div></div></div></td>
<td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#94a3b8;font-size:14px;font-weight:300;">−</span></td>
<td style="vertical-align:top;padding:0 2px;"><div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#666666;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">FREMDKOSTEN</div><div style="color:#1a1a1a;font-size:14px;font-weight:700;">€ 2.755</div></div></div></td>
<td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#94a3b8;font-size:14px;font-weight:300;">=</span></td>
<td style="vertical-align:top;padding:0 2px;"><div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#666666;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">ROHERTRAG</div><div style="color:#065f46;font-size:14px;font-weight:700;">€ 94.537</div><div style="color:#94a3b8;font-size:9px;margin-top:2px;">97%</div></div></div></td>
<td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#94a3b8;font-size:14px;font-weight:300;">−</span></td>
<td style="vertical-align:top;padding:0 2px;"><div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#666666;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">STUNDEN*</div><div style="color:#1a1a1a;font-size:14px;font-weight:700;">€ 76.614</div></div></div></td>
<td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#94a3b8;font-size:14px;font-weight:300;">=</span></td>
<td style="vertical-align:top;padding:0 2px;"><div style="padding:10px 6px;background:#d1fae5;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#065f46;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">DB II</div><div style="color:#065f46;font-size:14px;font-weight:700;">€ 17.923</div><div style="color:#065f46;font-size:9px;margin-top:2px;opacity:0.8;">18%</div></div></div></td>
</tr></table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:8px;">
<tr>
<td width="33%" style="padding-right:6px;"><div style="padding:10px;background:#fafafa;border-radius:10px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#666666;font-size:9px;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">Letzte KW</div><div style="color:#1a1a1a;font-size:14px;font-weight:700;">42.0 h</div><div style="color:#94a3b8;font-size:10px;font-weight:400;margin-top:2px;">▲1.8h vs. KW-1</div></div></td>
<td width="33%" style="padding-right:6px;"><div style="padding:10px;background:#fafafa;border-radius:10px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#666666;font-size:9px;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">Nicht fakturiert</div><div style="color:#991b1b;font-size:14px;font-weight:700;">100.225,00 €</div><div style="color:#94a3b8;font-size:10px;margin-top:2px;">771.2 h offen</div></div></td>
<td width="33%"><div style="padding:10px;background:#fafafa;border-radius:10px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#666666;font-size:9px;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">Projekte</div><div style="color:#1a1a1a;font-size:14px;font-weight:700;">4</div><div style="font-size:10px;margin-top:2px;"><span style="color:#065f46;">🟢 2</span>  <span style="color:#92400e;">🟡 1</span>  <span style="color:#991b1b;">🔴 1</span></div></div></td>
</tr></table>
</td></tr></table>
""",

    "Projekt Details (Kurz)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Projekte (4)</div>
<div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td><div style="font-size:14px;font-weight:700;color:#1a1a1a;">Marketing 2026</div><div style="font-size:11px;color:#94a3b8;margin-top:2px;">LEZ-003-01 · Beispiel Kunde GmbH</div></td></tr>
</table>
<div style="margin-top:8px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="font-size:11px;color:#666666;">KW 8: <strong style="color:#1a1a1a;">41.3 h</strong> <span style="color:#94a3b8;font-size:10px;font-weight:700;">▲ 5.3 h</span></td><td align="right" style="font-size:11px;color:#666666;">Ges: 253.4 h   </td></tr></table></div>
</div>
<div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td><div style="font-size:14px;font-weight:700;color:#1a1a1a;">Marketing- und Design- Support 2026</div><div style="font-size:11px;color:#94a3b8;margin-top:2px;">HFKK-002-01 · Beispiel Verein e.V.</div></td></tr>
</table>
<div style="margin-top:8px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="font-size:11px;color:#666666;">KW 8: <strong style="color:#1a1a1a;">0.8 h</strong> <span style="color:#94a3b8;font-size:10px;font-weight:700;">▼ 3.0 h</span></td><td align="right" style="font-size:11px;color:#666666;">Ges: 107.0 h   </td></tr></table></div>
</div>
<div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td><div style="font-size:14px;font-weight:700;color:#1a1a1a;">Digitale Visitenkarte & Nachproduktion Visitenkarten</div><div style="font-size:11px;color:#94a3b8;margin-top:2px;">BVA-007 · Muster Firma</div></td></tr>
</table>
<div style="margin-top:8px;"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="font-size:11px;color:#666666;">KW 8: <strong style="color:#1a1a1a;">0.0 h</strong> <span style="color:#94a3b8;font-size:10px;font-weight:700;">▼ 0.5 h</span></td><td align="right" style="font-size:11px;color:#666666;">Ges: 9.5 h   <span style="color:#991b1b;font-size:10px;font-weight:700;">🚨 16d inaktiv</span></td></tr></table></div>
</div>
</td></tr></table>
""",

    "Teamauslastung": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 6px;">Teamauslastung KW 8</div>
<div style="color: #94a3b8; font-size: 12px; margin-bottom: 20px;">Projektauslastung der Mitarbeiter auf deinen Projekten</div>
<div style="margin-bottom:16px;padding:14px 18px;background:#fff7ed;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td><span style="font-size:13px;color:#92400e;font-weight:700;">⌀ Team-Projektauslastung</span></td><td align="right"><span style="font-size:18px;font-weight:700;color:#92400e;">63%</span><span style="font-size:11px;color:#94a3b8;margin-left:4px;">(5 MA)</span></td></tr>
</table></div>
<div style="margin-bottom:8px;padding:12px 14px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td width="30%" style="vertical-align:middle;"><div style="font-size:13px;font-weight:700;color:#1a1a1a;">Max Mustermann</div></td><td width="40%" style="vertical-align:middle;padding:0 12px;"><div style="background:#f3f4f6;border-radius:7px;height:14px;width:100%;"><div style="background:#10b981;border-radius:7px;height:14px;width:86%;min-width:2px;"></div></div></td><td width="30%" style="vertical-align:middle;text-align:right;"><span style="font-size:15px;font-weight:700;color:#065f46;">86%</span><div style="font-size:10px;color:#94a3b8;margin-top:2px;">17.3 h / 20.0 h Soll</div></td></tr>
</table>
<div style="margin-top:8px;padding-top:8px;border-top:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="font-size:10px;color:#666666">
<tr><td>Deine Projekte: <strong style="color:#1a1a1a;">16.5 h</strong></td><td>Intern: 2.8 h</td><td align="right">Buchungsquote: <strong>100%</strong></td></tr>
</table></div></div>
<div style="margin-bottom:8px;padding:12px 14px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td width="30%" style="vertical-align:middle;"><div style="font-size:13px;font-weight:700;color:#1a1a1a;">Anna Beispiel</div></td><td width="40%" style="vertical-align:middle;padding:0 12px;"><div style="background:#f3f4f6;border-radius:7px;height:14px;width:100%;"><div style="background:#f59e0b;border-radius:7px;height:14px;width:41%;min-width:2px;"></div></div></td><td width="30%" style="vertical-align:middle;text-align:right;"><span style="font-size:15px;font-weight:700;color:#92400e;">41%</span><div style="font-size:10px;color:#94a3b8;margin-top:2px;">16.5 h / 40.0 h Soll</div></td></tr>
</table>
<div style="margin-top:8px;padding-top:8px;border-top:1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="font-size:10px;color:#666666">
<tr><td>Deine Projekte: <strong style="color:#1a1a1a;">16.0 h</strong></td><td>Intern: 18.8 h</td><td align="right">Buchungsquote: <strong>88%</strong></td></tr>
</table></div></div>
</td></tr></table>
""",

    "Inaktive Projekte (Warnung)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #ef4444;">
<tr><td style="padding: 25px 30px;">
<div style="color: #991b1b; font-size: 17px; font-weight: 700; margin-bottom: 12px;">Projekte ohne Buchung seit >14 Tagen</div>
<div style="padding:6px 0;color:#991b1b;font-size:13px;font-weight:600;">• Digitale Visitenkarte & Nachproduktion Visitenkarten — 16 Tage</div>
<div style="padding:6px 0;color:#991b1b;font-size:13px;font-weight:600;">• Beispiel Projekt - Logo Update & Website One Pager — 36 Tage</div>
</td></tr></table>
""",

    "PM Automatische E-Mail Hinweis": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 20px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 13px; font-weight: 600; margin-bottom: 6px;">Dies ist eine automatische E-Mail von Poool.</div>
<div style="color: #9ca3af; font-size: 12px;">Bei Fragen wende dich bitte an <a href="mailto:support@poool.cc" style="color: #9ca3af; text-decoration: underline;">support@poool.cc</a></div>
</td></tr></table>
""",
}

# ── Heights per section (enough space without scrolling) ──

zeiterfassung_heights = {
    "Header (Wochenübersicht)": 200,
    "Fortschrittsanzeige (100% Complete)": 320,
    "Zeiterfassung Übersicht (SOLL/IST)": 520,
    "Wochentage-Status (Mo–Fr)": 140,
    "Tagesdetails (Projektzeiterfassung)": 890,
    "Nachbuchungen erforderlich (Warnung)": 320,
    "Projektübersicht (Tabelle)": 260,
    "Automatische E-Mail Hinweis": 140,
}

pm_heights = {
    "PM Header (Projekt-Übersicht)": 220,
    "Handlungsbedarf (Kritische Projekte)": 320,
    "Kennzahlen Übersicht": 400,
    "Projekt Details (Kurz)": 460,
    "Teamauslastung": 380,
    "Inaktive Projekte (Warnung)": 180,
    "PM Automatische E-Mail Hinweis": 140,
}

# ── Render sections for each selected mail type ──

auswahl_zeiterfassung = {}
auswahl_pm = {}

# Zeiterfassungsmail Sektionen
if "Zeiterfassungsmail" in mail_optionen:
    st.divider()
    st.subheader("3. Zeiterfassungsmail - Abschnitte auswählen")
    
    for titel, html_content in zeiterfassung_sections.items():
        # E-Mail Platzhalter ersetzen für Vorschau
        display_content = html_content.replace("{{Vorname}}", beispiel_email.split('@')[0] if beispiel_email and '@' in beispiel_email else "Vorname")
        
        col1, col2 = st.columns([5, 1])
        h = zeiterfassung_heights.get(titel, 400)
        
        with col1:
            st.components.v1.html(
                f"""
                <div style="background-color: #f0f2f5; padding: 10px; border-radius: 12px; font-family: Arial, Helvetica, sans-serif;">
                    {display_content}
                </div>
                """,
                height=h,
                scrolling=False,
            )
        
        with col2:
            auswahl_zeiterfassung[titel] = st.checkbox("Einschließen", value=True, key=f"zeit_{titel}")
        
        st.write("")

# PM-Mail Sektionen  
if "Projektmanagement-Mail" in mail_optionen:
    st.divider()
    st.subheader("4. Projektmanagement-Mail - Abschnitte auswählen")
    
    for titel, html_content in pm_sections.items():
        # E-Mail Platzhalter ersetzen für Vorschau
        display_content = html_content.replace("{{Vorname}}", beispiel_email.split('@')[0] if beispiel_email and '@' in beispiel_email else "Vorname")
        
        col1, col2 = st.columns([5, 1])
        h = pm_heights.get(titel, 400)
        
        with col1:
            st.components.v1.html(
                f"""
                <div style="background-color: #f5f5f5; padding: 10px; border-radius: 12px; font-family: Arial, Helvetica, sans-serif;">
                    {display_content}
                </div>
                """,
                height=h,
                scrolling=False,
            )
        
        with col2:
            auswahl_pm[titel] = st.checkbox("Einschließen", value=True, key=f"pm_{titel}")
        
        st.write("")

# ── Generate final HTML & send to Poool ──

st.divider()

# ── Kosten-Info ──
st.subheader("4. Kosten & Versand")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px;">
        <div style="font-size: 14px; font-weight: 600; color: #166534; margin-bottom: 8px;">💰 Kosten</div>
        <div style="font-size: 24px; font-weight: 700; color: #1a1a1a;">€ 285</div>
        <div style="font-size: 13px; color: #666;">Einmaliges Setup (pro Mail-Typ)</div>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 20px;">
        <div style="font-size: 14px; font-weight: 600; color: #1e40af; margin-bottom: 8px;">📅 Versand</div>
        <div style="font-size: 18px; font-weight: 700; color: #1a1a1a;">Immer Montags</div>
        <div style="font-size: 13px; color: #666;">Abweichung nur bei PRISM Kunden möglich</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.divider()
st.subheader("5. Anmerkungen")
freitext = st.text_area("Hast du noch Wünsche oder Anmerkungen?", height=120, placeholder="z.B. anderer Versandtag, zusätzliche Inhalte, spezielle Anpassungen ...")

st.divider()

N8N_WEBHOOK_URL = "https://poool.app.n8n.cloud/webhook/7000884e-6635-4d83-a6ea-6c242857c004"

if st.button("✅ Ausgewählte Abschnitte zusammenbauen & an Poool senden", type="primary"):
    # Sammle alle gewählten Abschnitte
    alle_html_teile = []
    gesamt_info = []
    
    if "Zeiterfassungsmail" in mail_optionen:
        zeit_gewaehlte = [titel for titel, aktiv in auswahl_zeiterfassung.items() if aktiv]
        zeit_abgewaehlte = [titel for titel, aktiv in auswahl_zeiterfassung.items() if not aktiv]
        
        if zeit_gewaehlte:
            gesamt_info.append(f"Zeiterfassung: {len(zeit_gewaehlte)}/{len(zeiterfassung_sections)} Abschnitte")
            
            # Build Zeiterfassung HTML
            for titel in zeit_gewaehlte:
                content = zeiterfassung_sections[titel].replace("{{Vorname}}", "{{Vorname}}")  # Keep placeholder
                alle_html_teile.append(f'<tr><td style="padding: 0 0 16px 0;">{content}</td></tr>')
    
    if "Projektmanagement-Mail" in mail_optionen:
        pm_gewaehlte = [titel for titel, aktiv in auswahl_pm.items() if aktiv]
        pm_abgewaehlte = [titel for titel, aktiv in auswahl_pm.items() if not aktiv]
        
        if pm_gewaehlte:
            gesamt_info.append(f"Projektmanagement: {len(pm_gewaehlte)}/{len(pm_sections)} Abschnitte")
            
            # Build PM HTML mit 640px breite (wie im Original)
            for titel in pm_gewaehlte:
                content = pm_sections[titel].replace("{{Vorname}}", "{{Vorname}}")  # Keep placeholder
                alle_html_teile.append(f'<tr><td style="padding: 0 0 16px 0;">{content}</td></tr>')
    
    if alle_html_teile:
        st.success(f"**Ausgewählt:** {' | '.join(gesamt_info)}")
        
        # Build final HTML - verwende 640px für PM, 600px für Zeiterfassung
        width = "640" if "Projektmanagement-Mail" in mail_optionen else "600"
        bg_color = "#f5f5f5" if "Projektmanagement-Mail" in mail_optionen else "#f0f2f5"
        
        final_html = f"""
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: {bg_color}; font-family: Arial, Helvetica, sans-serif;">
<tr><td align="center" style="padding: 20px 10px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="{width}" style="max-width: {width}px;">
{''.join(alle_html_teile)}
</table></td></tr></table>
"""
        
        # ── Send to Poool ──
        payload = {
            "timestamp": datetime.now().isoformat(),
            "unternehmen": unternehmen if unternehmen else "",
            "beispiel_email": beispiel_email if beispiel_email else "",
            "zeiterfassungsmail_aktiv": "Zeiterfassungsmail" in mail_optionen,
            "pm_mail_aktiv": "Projektmanagement-Mail" in mail_optionen,
            "kosten": "€ 285 einmaliges Setup (pro Mail-Typ)",
            "versand": "Immer Montags (Abweichung nur bei PRISM Kunden möglich)",
            "mail_typen": mail_optionen,
            "zeiterfassung_abschnitte": auswahl_zeiterfassung if "Zeiterfassungsmail" in mail_optionen else {},
            "pm_abschnitte": auswahl_pm if "Projektmanagement-Mail" in mail_optionen else {},
            "beschreibung": f"Mail-Typen aktiv: {', '.join(mail_optionen)}. {' | '.join(gesamt_info)}",
            "finale_email_html": final_html,
            "anmerkungen": freitext if freitext else "",
        }
        
        try:
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=10)
            if response.ok:
                st.success("📤 Auswahl erfolgreich an Poool gesendet!")
            else:
                st.error(f"Fehler: Status {response.status_code} – {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Verbindungsfehler zu Poool: {e}")
        
        # ── Preview ──
        st.markdown("### Vorschau der finalen E-Mail:")
        preview_html = final_html.replace("{{Vorname}}", beispiel_email.split('@')[0] if beispiel_email and '@' in beispiel_email else "Vorname")
        st.components.v1.html(preview_html, height=800, scrolling=True)
        
        # Download button
        st.download_button(
            label="📥 HTML herunterladen",
            data=final_html,
            file_name="email_zusammengestellt.html",
            mime="text/html",
        )
        
    else:
        st.warning("Keine Abschnitte ausgewählt!")
