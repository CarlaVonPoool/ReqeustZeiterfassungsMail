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

# ── 1. Zeiterfassungsmail Ja/Nein ──

st.subheader("1. Möchtest du die Zeiterfassungsmail aktivieren?")

zeiterfassung_aktiv = st.radio(
    "Zeiterfassungsmail aktivieren?",
    options=["Ja", "Nein"],
    index=0,
    horizontal=True,
    label_visibility="collapsed",
)

if zeiterfassung_aktiv == "Nein":
    st.info("Die Zeiterfassungsmail ist deaktiviert. Es werden keine wöchentlichen Mails versendet.")
    st.divider()
    
    N8N_WEBHOOK_URL = "https://poool.app.n8n.cloud/webhook/7000884e-6635-4d83-a6ea-6c242857c004"
    
    if st.button("✅ Auswahl an Poool senden", type="primary"):
        payload = {
            "timestamp": datetime.now().isoformat(),
            "unternehmen": unternehmen if unternehmen else "",
            "zeiterfassungsmail_aktiv": False,
            "beschreibung": "Kunde möchte keine Zeiterfassungsmail erhalten.",
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

# ── Kosten-Info ──

st.divider()
st.subheader("2. Kosten & Versand")

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    <div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px;">
        <div style="font-size: 14px; font-weight: 600; color: #166534; margin-bottom: 8px;">💰 Kosten</div>
        <div style="font-size: 24px; font-weight: 700; color: #1a1a1a;">€ 285</div>
        <div style="font-size: 13px; color: #666;">Einmaliges Setup</div>
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

# ── 3. Blockauswahl ──

st.divider()
st.subheader("3. Welche Abschnitte soll die Mail enthalten?")

# ── Mail sections as HTML snippets (anonymized: "Orange Hive" → "Beispiel Kunde") ──

sections = {
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
<div style="color: #1a1a1a; font-size: 22px; font-weight: 700; margin-bottom: 8px;">Perfekt, Carla!</div>
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

# ── Heights per section (enough space without scrolling) ──

section_heights = {
    "Header (Wochenübersicht)": 200,
    "Fortschrittsanzeige (100% Complete)": 320,
    "Zeiterfassung Übersicht (SOLL/IST)": 520,
    "Wochentage-Status (Mo–Fr)": 140,
    "Tagesdetails (Projektzeiterfassung)": 890,
    "Nachbuchungen erforderlich (Warnung)": 320,
    "Projektübersicht (Tabelle)": 260,
    "Automatische E-Mail Hinweis": 140,
}

# ── Render each section with checkbox ──

auswahl = {}

for titel, html_content in sections.items():
    col1, col2 = st.columns([5, 1])
    h = section_heights.get(titel, 400)
    
    with col1:
        st.components.v1.html(
            f"""
            <div style="background-color: #f0f2f5; padding: 10px; border-radius: 12px; font-family: Arial, Helvetica, sans-serif;">
                {html_content}
            </div>
            """,
            height=h,
            scrolling=False,
        )
    
    with col2:
        auswahl[titel] = st.checkbox("Einschließen", value=True, key=titel)
    
    st.write("")

# ── Generate final HTML & send to Poool ──

st.divider()
st.subheader("4. Anmerkungen")
freitext = st.text_area("Hast du noch Wünsche oder Anmerkungen?", height=120, placeholder="z.B. anderer Versandtag, zusätzliche Inhalte, spezielle Anpassungen ...")

st.divider()

N8N_WEBHOOK_URL = "https://poool.app.n8n.cloud/webhook/7000884e-6635-4d83-a6ea-6c242857c004"

if st.button("✅ Ausgewählte Abschnitte zusammenbauen & an Poool senden", type="primary"):
    gewaehlte = [titel for titel, aktiv in auswahl.items() if aktiv]
    abgewaehlte = [titel for titel, aktiv in auswahl.items() if not aktiv]
    
    if gewaehlte:
        st.success(f"**{len(gewaehlte)} von {len(sections)} Abschnitten** ausgewählt")
        
        # Build final HTML
        final_html_parts = []
        for titel in gewaehlte:
            final_html_parts.append(f'<tr><td style="padding: 0 0 16px 0;">{sections[titel]}</td></tr>')
        
        final_html = f"""
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #f0f2f5; font-family: Arial, Helvetica, sans-serif;">
<tr><td align="center" style="padding: 20px 10px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width: 600px;">
{''.join(final_html_parts)}
</table></td></tr></table>
"""
        
        # ── Send to Poool ──
        payload = {
            "timestamp": datetime.now().isoformat(),
            "unternehmen": unternehmen if unternehmen else "",
            "zeiterfassungsmail_aktiv": True,
            "kosten": "€ 285 einmaliges Setup",
            "versand": "Immer Montags (Abweichung nur bei PRISM Kunden möglich)",
            "anzahl_gewählt": len(gewaehlte),
            "anzahl_gesamt": len(sections),
            "gewaehlte_abschnitte": gewaehlte,
            "entfernte_abschnitte": abgewaehlte,
            "beschreibung": f"Zeiterfassungsmail AKTIV. "
                           f"{len(gewaehlte)} von {len(sections)} E-Mail-Abschnitten ausgewählt. "
                           f"Enthalten: {', '.join(gewaehlte)}."
                           + (f" Entfernt: {', '.join(abgewaehlte)}." if abgewaehlte else ""),
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
        st.components.v1.html(final_html, height=800, scrolling=True)
        
        # Download button
        st.download_button(
            label="📥 HTML herunterladen",
            data=final_html,
            file_name="email_zusammengestellt.html",
            mime="text/html",
        )
        
        if abgewaehlte:
            st.info(f"Entfernte Abschnitte: {', '.join(abgewaehlte)}")
    else:
        st.warning("Kein Abschnitt ausgewählt!")
