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

st.title("Poool Wöchentliche Mails")
st.markdown("**Zeiterfassung & Projektmanager individuell konfigurieren**")
st.divider()

# ── Unternehmen ──

st.subheader("Unternehmen")
unternehmen = st.text_input("Name des Unternehmens", placeholder="z.B. Muster GmbH")

# ── E-Mail Adresse für Beispiele ──

st.divider()
st.subheader("E-Mail Adresse für Beispiel-Mails")
beispiel_email = st.text_input(
    "E-Mail Adresse für die Beispiel-Vorschau", 
    placeholder="z.B. max.mustermann@firma.de",
    help="Diese Adresse wird nur für die Vorschau verwendet und nicht gespeichert"
)

# ── Mail-Typ Auswahl ──

st.divider()
st.subheader("Welche E-Mails möchtest du aktivieren?")

zeiterfassung_aktiv = st.checkbox("Zeiterfassungs-Mail", value=True)
pm_aktiv = st.checkbox("Projektmanagement-Mail", value=False)

# PM-Mail Konfiguration
if pm_aktiv:
    st.markdown("**Projektmanagement-Mail Konfiguration:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stundenkosten_option = st.selectbox(
            "Stundenkosten",
            ["Fremdkostenansatz", "Interner Kostenansatz"],
            index=0
        )
    
    with col2:
        rohertrag_option = st.selectbox(
            "Rohertragsberechnung",
            ["Abgerechnet", "Auftrag + Ausgangsrechnung"],
            index=0
        )
else:
    stundenkosten_option = "Fremdkostenansatz"
    rohertrag_option = "Abgerechnet"

# Mail-Optionen für Kompatibilität
mail_optionen = []
if zeiterfassung_aktiv:
    mail_optionen.append("Zeiterfassungs-Mail")
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

# ── Mail sections as HTML snippets ──

# Zeiterfassungsmail Sektionen
zeiterfassung_sections = {
    "Header (Wochenübersicht)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 35px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 22px; font-weight: 300; margin-bottom: 6px;">Deine Woche im Überblick</div>
<div style="color: #ffffff; font-size: 26px; font-weight: 700; margin-bottom: 8px;">23.02. – 27.02.2026</div>
<div style="color: #9ca3af; font-size: 13px;">Datenstand: 03.03.2026 03:00</div>
</td></tr></table>
""",

    "Fortschrittsanzeige (44% Complete)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #e5e7eb;">
<tr><td style="padding: 35px 30px; text-align: center;">
<div style="color: #1a1a1a; font-size: 48px; font-weight: 700; margin-bottom: 4px;">44%</div>
<div style="color: #94a3b8; font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;">COMPLETE</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="80%" align="center" style="height: 14px; border-radius: 7px; overflow: hidden; margin-bottom: 20px;">
<tr><td width="44%" style="background-color: #EA4335; height: 14px;"></td><td width="56%" style="background-color: #f3f4f6; height: 14px;"></td></tr></table>
<div style="color: #1a1a1a; font-size: 22px; font-weight: 700; margin-bottom: 8px;">Hallo {{Vorname}}!</div>
<div style="color: #666666; font-size: 15px; margin-bottom: 25px;">21:45 Std. sind in der letzten Woche noch nicht gebucht</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td style="background-color: #1F3A47; border-radius: 25px; padding: 14px 35px;"><a href="https://app-next.poool.cc/login" style="color: #ffffff; font-size: 15px; font-weight: 700; text-decoration: none;">Jetzt Stunden nachbuchen!</a></td></tr></table>
</td></tr></table>
""",

    "Zeiterfassung Übersicht (SOLL/IST)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Zeiterfassung in der KW 2026/09</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border: 1px solid #e5e7eb; border-radius: 12px; margin-bottom: 16px;">
<tr><td style="padding: 20px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
<tr><td style="color: #666666; font-size: 14px; padding: 8px 0;">SOLL Arbeitszeit:</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 8px 0;">38:30 h</td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 8px 0;">IST Arbeitszeit erfasst:</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 8px 0;">41:16 h <span style="color: #94a3b8; font-size: 12px;">(107%)</span></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td colspan="2" style="height: 1px; background-color: #e5e7eb; padding: 0;"></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 6px 0;">Operative Stunden (abrechenbar):</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 6px 0;">11:45 h <span style="color: #94a3b8; font-size: 12px;">(31%)</span></td></tr>
<tr><td style="color: #666666; font-size: 14px; padding: 6px 0;">Interne Stunden (nicht abrechenbar):</td><td align="right" style="color: #1a1a1a; font-size: 14px; font-weight: 700; padding: 6px 0;">05:00 h <span style="color: #94a3b8; font-size: 12px;">(13%)</span></td></tr>
<tr><td colspan="2" style="height: 12px;"></td></tr>
<tr><td colspan="2" style="height: 1px; background-color: #e5e7eb; padding: 0;"></td></tr>
<tr><td colspan="2" style="height: 4px;"></td></tr>
<tr><td style="color: #1a1a1a; font-size: 15px; font-weight: 700; padding: 8px 0;">Gesamt gebucht (Projektzeit):</td><td align="right" style="color: #1a1a1a; font-size: 16px; font-weight: 700; padding: 8px 0;">16:45 h <span style="color: #94a3b8; font-size: 12px;">(44%)</span></td></tr>
</table></td></tr></table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 12px;">
<tr><td style="padding: 14px 18px; background-color: #fee2e2; border-radius: 12px;"><span style="color: #991b1b; font-size: 13px; font-weight: 700;">Projektzeit fehlt: 24:31h nicht gebucht</span></td></tr></table>
<div style="color: #666666; font-size: 13px; font-weight: 600; margin-bottom: 10px;">Buchungsstand Projektzeit von SOLL:</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 32px; border-radius: 10px; overflow: hidden; margin-bottom: 10px;">
<tr><td width="31.0%" style="background-color: #86EFAC; height: 32px; color: #ffffff; font-size: 11px; font-weight: 700; text-align: center; vertical-align: middle;">31%</td>
<td width="13.0%" style="background-color: #60A5FA; height: 32px; color: #ffffff; font-size: 11px; font-weight: 700; text-align: center; vertical-align: middle;">13%</td>
<td width="56.0%" style="background-color: #f3f4f6; height: 32px; color: #94a3b8; font-size: 11px; font-weight: 700; text-align: center; vertical-align: middle;">56%</td></tr></table>
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
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #fef3c7; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #92400e; font-size: 16px; font-weight: 700; margin-bottom: 2px;">⚠</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Mo</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #fef3c7; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #92400e; font-size: 16px; font-weight: 700; margin-bottom: 2px;">⚠</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Di</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #fef3c7; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #92400e; font-size: 16px; font-weight: 700; margin-bottom: 2px;">⚠</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Mi</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #fef3c7; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #92400e; font-size: 16px; font-weight: 700; margin-bottom: 2px;">⚠</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Do</div></div></td>
<td align="center" style="width: 20%; padding: 0 4px;"><div style="background-color: #fef3c7; border-radius: 10px; padding: 10px 0; text-align: center;"><div style="color: #92400e; font-size: 16px; font-weight: 700; margin-bottom: 2px;">⚠</div><div style="color: #666666; font-size: 11px; font-weight: 600;">Fr</div></div></td>
</tr></table></td></tr></table>
""",

    "Tagesdetails (Projektzeiterfassung)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
<div style="color: #1a1a1a; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Projektzeiterfassung in der KW 2026/09</div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Montag, 23.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 07:31h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 03:30h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #fff7ed; border-radius: 8px; margin-bottom: 10px; margin-right: 6px;"><span style="color: #92400e; font-size: 11px; font-weight: 700;">Weniger Arbeitszeit als SOLL: 00:29h</span></div>
<div style="display: inline-block; padding: 4px 12px; background-color: #fee2e2; border-radius: 8px; margin-bottom: 10px;"><span style="color: #991b1b; font-size: 11px; font-weight: 700;">Projektzeit: 04:01h nicht gebucht</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="44%" style="background-color: #B7CFFF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">44%</td><td width="56%" style="background-color: #fee2e2; height: 28px;"></td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Dienstag, 24.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 09:25h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 03:00h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #fee2e2; border-radius: 8px; margin-bottom: 10px;"><span style="color: #991b1b; font-size: 11px; font-weight: 700;">Projektzeit: 06:25h nicht gebucht</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="38%" style="background-color: #B7CFFF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">38%</td><td width="62%" style="background-color: #fee2e2; height: 28px;"></td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Mittwoch, 25.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:59h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 04:15h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #fee2e2; border-radius: 8px; margin-bottom: 10px;"><span style="color: #991b1b; font-size: 11px; font-weight: 700;">Projektzeit: 04:44h nicht gebucht</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="53%" style="background-color: #B7CFFF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">53%</td><td width="47%" style="background-color: #fee2e2; height: 28px;"></td></tr></table></div>
<div style="margin-bottom: 16px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Donnerstag, 26.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 08:00h | <strong>IST:</strong> 08:56h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 03:30h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #fee2e2; border-radius: 8px; margin-bottom: 10px;"><span style="color: #991b1b; font-size: 11px; font-weight: 700;">Projektzeit: 05:26h nicht gebucht</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="44%" style="background-color: #B7CFFF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">44%</td><td width="56%" style="background-color: #fee2e2; height: 28px;"></td></tr></table></div>
<div style="margin-bottom: 0px; padding: 18px; background-color: #fafafa; border-radius: 12px; border: 1px solid #e5e7eb;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 10px;">
<tr><td><div style="color: #1a1a1a; font-size: 15px; font-weight: 700;">Freitag, 27.02.2026</div><div style="color: #94a3b8; font-size: 12px;">Arbeitstag</div></td>
<td align="right"><div style="color: #666666; font-size: 12px;"><strong>SOLL:</strong> 06:30h | <strong>IST:</strong> 06:25h</div><div style="color: #94a3b8; font-size: 11px;">Projektzeit gebucht: 02:30h</div></td></tr></table>
<div style="display: inline-block; padding: 4px 12px; background-color: #fff7ed; border-radius: 8px; margin-bottom: 10px; margin-right: 6px;"><span style="color: #92400e; font-size: 11px; font-weight: 700;">Weniger Arbeitszeit als SOLL: 00:05h</span></div>
<div style="display: inline-block; padding: 4px 12px; background-color: #fee2e2; border-radius: 8px; margin-bottom: 10px;"><span style="color: #991b1b; font-size: 11px; font-weight: 700;">Projektzeit: 03:55h nicht gebucht</span></div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="height: 28px; border-radius: 8px; overflow: hidden;">
<tr><td width="38%" style="background-color: #B7CFFF; height: 28px; color: #ffffff; font-size: 12px; font-weight: 700; text-align: center; vertical-align: middle;">38%</td><td width="62%" style="background-color: #fee2e2; height: 28px;"></td></tr></table></div>
</td></tr></table>
""",

    "Nachbuchungen erforderlich (Warnung)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 2px solid #f59e0b;">
<tr><td style="padding: 60px;">
<div style="color: #8b5a13; font-size: 17px; font-weight: 700; margin-bottom: 12px;">⚠️ Nachbuchungen erforderlich</div>
<div style="color: #8b5a13; font-size: 13px; margin-bottom: 12px;">An folgenden Tagen fehlen noch Buchungen:</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Montag, 23.02.2026: Arbeitszeit – 00:29h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Dienstag, 24.02.2026: Projektzeit – 06:25h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Mittwoch, 25.02.2026: Projektzeit – 04:44h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Donnerstag, 26.02.2026: Projektzeit – 05:26h fehlen</div>
<div style="padding: 6px 0; color: #8b5a13; font-size: 13px; font-weight: 600;">• Freitag, 27.02.2026: Arbeitszeit – 00:05h fehlen</div>
<div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #D88E20; color: #8b5a13; font-size: 13px; font-weight: 700;">⏰ Bitte buche alle fehlenden Zeiten zeitnah nach.</div>
<div style="margin-top: 8px; color: #666666; font-size: 12px;">Hinweis: Unvollständige Zeiterfassung kann zu Problemen bei der Abrechnung führen.</div>
</td></tr></table>
""",

    "Projektübersicht (Tabelle)": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 60px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-radius: 12px; overflow: hidden; border: 1px solid #e5e7eb;">
<tr><td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; width: 45%;">Projekt:</td>
<td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; text-align: center; width: 30%;">Kategorie</td>
<td style="background-color: #1F3A47; color: #ffffff; font-size: 13px; font-weight: 700; padding: 12px 16px; text-align: right; width: 25%;">Stunden</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Alpha GmbH – Marketingkonzept 2026</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">06:00 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Beta Solutions – Website Redesign</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">03:00 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Gamma Corp – ERP Integration</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:45 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Delta Services – App Development</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:30 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Epsilon AG – IT Consulting</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:30 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Zeta Industries – Digital Transformation</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:30 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Eta Technologies – Cloud Migration</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:15 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Theta Networks – Network Analysis</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #d1fae5; color: #065f46; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Operativ</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">00:15 h</td></tr>
<tr><td style="color: #333333; font-size: 13px; padding: 12px 16px; border-bottom: 1px solid #f3f4f6;">Poool – Internes Projekt</td>
<td style="padding: 12px 16px; border-bottom: 1px solid #f3f4f6; text-align: center;"><span style="display: inline-block; background-color: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 700; padding: 4px 14px; border-radius: 12px;">Intern</span></td>
<td style="color: #1a1a1a; font-size: 13px; font-weight: 600; padding: 12px 16px; text-align: right; border-bottom: 1px solid #f3f4f6;">05:00 h</td></tr>
</table></td></tr></table>
""",

    "Automatische E-Mail Hinweis": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #1F3A47; border-radius: 16px;">
<tr><td style="padding: 25px 30px; text-align: center;">
<div style="color: #ffffff; font-size: 14px; font-weight: 300; margin-bottom: 6px;">Dies ist eine automatische E-Mail von Poool.</div>
<div style="color: #9ca3af; font-size: 13px;">Bei Fragen wende dich bitte an <a href="mailto:support@poool.de" style="color: #9ca3af; text-decoration: underline;">support@poool.de</a></div>
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
  
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom: 16px;">
    <tr>
      <td width="50%" style="vertical-align: top; padding-right: 10px;">
        <div style="color: #9ca3af; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">PROJEKTE</div>
        <div style="margin-bottom: 6px;"><span style="color: #991b1b; font-size: 13px;">🔴 1 Projekt kritisch</span></div>
        <div style="margin-bottom: 6px;"><span style="color: #92400e; font-size: 13px;">🟡 1 Projekt im Blick behalten</span></div>
      </td>
      <td width="50%" style="vertical-align: top; padding-left: 10px;">
        <div style="color: #9ca3af; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">TICKETS</div>
        <div style="margin-bottom: 6px;"><span style="color: #991b1b; font-size: 13px;">🔴 4 Zeitkontingent kritisch (≥90%)</span></div>
        <div style="margin-bottom: 6px;"><span style="color: #92400e; font-size: 13px;">🟡 1 Zeitkontingent Warnung (70-89%)</span></div>
        <div style="margin-bottom: 6px;"><span style="color: #991b1b; font-size: 13px;">🏷️ 3 Tickets überfällig</span></div>
      </td>
    </tr>
  </table>
  
  <div style="padding-top: 8px; border-top: 1px solid #e5e7eb; font-size: 12px; color: #333333;">
    3 aktive Projekte
  </div>
</td></tr>
</table>
""",

    "Kennzahlen Übersicht": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
  <div style="color: #000000; font-size: 20px; font-weight: 700; margin-bottom: 6px;">Deine Kennzahlen</div>
  <div style="color: #666666; font-size: 11px; margin-bottom: 20px;">* Kostenansatz: <strong style="color:#000000;">Selbstkostensatz</strong> &nbsp;|&nbsp; * Umsatz: <strong style="color:#000000;">Abgerechnet + Auftrag</strong></div>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-bottom:12px;">
  <tr>
    <td style="vertical-align:top;padding:0 2px;">
      <div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;">
        <div style="display:table-cell;vertical-align:middle;">
          <div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">UMSATZ*</div>
          <div style="color:#000000;font-size:14px;font-weight:700;">EUR 94.325</div>
        </div>
      </div>
    </td>
    <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
    <td style="vertical-align:top;padding:0 2px;">
      <div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;">
        <div style="display:table-cell;vertical-align:middle;">
          <div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">FREMDKOSTEN</div>
          <div style="color:#000000;font-size:14px;font-weight:700;">EUR 2.092</div>
        </div>
      </div>
    </td>
    <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
    <td style="vertical-align:top;padding:0 2px;">
      <div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;">
        <div style="display:table-cell;vertical-align:middle;">
          <div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">ROHERTRAG</div>
          <div style="color:#065f46;font-size:14px;font-weight:700;">EUR 92.233</div>
          <div style="color:#666666;font-size:9px;margin-top:2px;">98%</div>
        </div>
      </div>
    </td>
    <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
    <td style="vertical-align:top;padding:0 2px;">
      <div style="padding:10px 6px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;">
        <div style="display:table-cell;vertical-align:middle;">
          <div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">STUNDEN*</div>
          <div style="color:#000000;font-size:14px;font-weight:700;">EUR 76.203</div>
        </div>
      </div>
    </td>
    <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
    <td style="vertical-align:top;padding:0 2px;">
      <div style="padding:10px 6px;background:#d1fae5;border-radius:10px;border:1px solid #e5e7eb;text-align:center;min-height:58px;display:table;width:100%;">
        <div style="display:table-cell;vertical-align:middle;">
          <div style="color:#065f46;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">DB II</div>
          <div style="color:#065f46;font-size:14px;font-weight:700;">EUR 16.030</div>
          <div style="color:#065f46;font-size:9px;margin-top:2px;opacity:0.8;">17%</div>
        </div>
      </div>
    </td>
  </tr>
  </table>
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:8px;">
  <tr>
    <td width="50%" style="padding-right:6px;">
      <div style="padding:10px;background:#fafafa;border-radius:10px;border:1px solid #e5e7eb;text-align:center;">
        <div style="color:#333333;font-size:9px;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">Letzte KW</div>
        <div style="color:#000000;font-size:14px;font-weight:700;">39.5 h</div>
        <div style="color:#666666;font-size:10px;font-weight:400;margin-top:2px;">▼2.5h vs. KW-1</div>
      </div>
    </td>
    <td width="50%">
      <div style="padding:10px;background:#fafafa;border-radius:10px;border:1px solid #e5e7eb;text-align:center;">
        <div style="color:#333333;font-size:9px;text-transform:uppercase;letter-spacing:0.7px;margin-bottom:4px;">Projekte</div>
        <div style="color:#000000;font-size:14px;font-weight:700;">3</div>
        <div style="font-size:10px;margin-top:2px;"><span style="color:#065f46;">🟢 1</span> &nbsp;<span style="color:#92400e;">🟡 1</span> &nbsp;<span style="color:#991b1b;">🔴 1</span></div>
      </div>
    </td>
  </tr>
  </table>
</td></tr>
</table>
""",

    "Projekt Details": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
  <div style="color: #000000; font-size: 20px; font-weight: 700; margin-bottom: 20px;">Deine Projekte (3)</div>

  <!-- PROJEKT A -->
  <div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr><td>
        <div style="font-size:14px;font-weight:700;color:#000000;">Marketing 2026</div>
        <div style="font-size:11px;color:#666666;margin-top:2px;">KND-A-001 &middot; Kunde Alpha GmbH</div>
      </td></tr>
    </table>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:8px;">
      <tr>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Abgerechnet</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 17.400</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftr.+Abger.</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 26.825</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftrag offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 9.425</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Angebot offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 0</div></div></td>
      </tr>
    </table>
    <div style="margin-top:8px;">
      <div style="color:#666666;font-size:11px;font-weight:700;margin-bottom:8px;">Projektergebnis</div>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">UMSATZ*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 26.825</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">FREMDKOSTEN</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 1.851</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">ROHERTRAG</div><div style="color:#065f46;font-size:13px;font-weight:700;line-height:1.2;">EUR 24.974</div><div style="color:#666666;font-size:9px;margin-top:2px;opacity:0.8;">93.10%</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">STUNDEN*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 25.217</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#fee2e2;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#991b1b;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">DB II</div><div style="color:#991b1b;font-size:13px;font-weight:700;line-height:1.2;">EUR -242</div><div style="color:#991b1b;font-size:9px;margin-top:2px;opacity:0.8;">-0.90%</div></div></div></td>
        </tr>
      </table>
    </div>
    <div style="margin-top:8px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="font-size:11px;color:#333333;">KW 9: <strong style="color:#000000;">39.0 h</strong> <span style="color:#666666;font-size:10px;font-weight:700;">▼ 2.3 h</span></td>
          <td align="right" style="font-size:11px;color:#333333;">Ges: 259.2 h</td>
        </tr>
      </table>
    </div>
  </div>

  <!-- PROJEKT B -->
  <div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr><td>
        <div style="font-size:14px;font-weight:700;color:#000000;">Marketing- und Design-Support 2026</div>
        <div style="font-size:11px;color:#666666;margin-top:2px;">KND-B-001 &middot; Kunde Beta e.V.</div>
      </td></tr>
    </table>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:8px;">
      <tr>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Abgerechnet</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 10.000</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftr.+Abger.</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 60.000</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftrag offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 50.000</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Angebot offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 0</div></div></td>
      </tr>
    </table>
    <div style="margin-top:8px;">
      <div style="color:#666666;font-size:11px;font-weight:700;margin-bottom:8px;">Projektergebnis</div>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">UMSATZ*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 60.000</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">FREMDKOSTEN</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 203</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">ROHERTRAG</div><div style="color:#065f46;font-size:13px;font-weight:700;line-height:1.2;">EUR 59.797</div><div style="color:#666666;font-size:9px;margin-top:2px;opacity:0.8;">99.66%</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">STUNDEN*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 11.423</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#d1fae5;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#065f46;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">DB II</div><div style="color:#065f46;font-size:13px;font-weight:700;line-height:1.2;">EUR 48.375</div><div style="color:#065f46;font-size:9px;margin-top:2px;opacity:0.8;">80.62%</div></div></div></td>
        </tr>
      </table>
    </div>
    <div style="margin-top:8px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="font-size:11px;color:#333333;">KW 9: <strong style="color:#000000;">0.5 h</strong> <span style="color:#666666;font-size:10px;font-weight:700;">▼ 0.3 h</span></td>
          <td align="right" style="font-size:11px;color:#333333;">Ges: 107.0 h</td>
        </tr>
      </table>
    </div>
  </div>

  <!-- PROJEKT C -->
  <div style="margin-bottom:14px;padding:16px;background:#fafafa;border-radius:12px;border:1px solid #e5e7eb;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr><td>
        <div style="font-size:14px;font-weight:700;color:#000000;">Logo Update &amp; Website One Pager</div>
        <div style="font-size:11px;color:#666666;margin-top:2px;">KND-C-001 &middot; Kunde Gamma GmbH</div>
      </td></tr>
    </table>
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:8px;">
      <tr>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Abgerechnet</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 0</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftr.+Abger.</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 7.500</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Auftrag offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 7.500</div></div></td>
        <td style="vertical-align:top;padding:0 3px;"><div style="padding:8px 3px;background:#f3f4f6;border-radius:6px;border:1px solid #e5e7eb;text-align:center;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.3px;margin-bottom:3px;">Angebot offen</div><div style="color:#000000;font-size:11px;font-weight:700;">EUR 109.100</div></div></td>
      </tr>
    </table>
    <div style="margin-top:8px;">
      <div style="color:#666666;font-size:11px;font-weight:700;margin-bottom:8px;">Projektergebnis</div>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">UMSATZ*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 7.500</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">FREMDKOSTEN</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 38</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">ROHERTRAG</div><div style="color:#065f46;font-size:13px;font-weight:700;line-height:1.2;">EUR 7.462</div><div style="color:#666666;font-size:9px;margin-top:2px;opacity:0.8;">99.49%</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">-</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#f3f4f6;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#333333;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">STUNDEN*</div><div style="color:#000000;font-size:13px;font-weight:700;line-height:1.2;">EUR 39.563</div></div></div></td>
          <td style="vertical-align:middle;padding:0 1px;text-align:center;width:16px;"><span style="color:#666666;font-size:14px;font-weight:300;">=</span></td>
          <td style="vertical-align:top;padding:0 2px;"><div style="padding:8px 6px;background:#fee2e2;border-radius:8px;border:1px solid #e5e7eb;text-align:center;min-height:52px;display:table;width:100%;"><div style="display:table-cell;vertical-align:middle;"><div style="color:#991b1b;font-size:8px;text-transform:uppercase;letter-spacing:0.6px;margin-bottom:3px;font-weight:600;">DB II</div><div style="color:#991b1b;font-size:13px;font-weight:700;line-height:1.2;">EUR -32.101</div><div style="color:#991b1b;font-size:9px;margin-top:2px;opacity:0.8;">-428.01%</div></div></div></td>
        </tr>
      </table>
    </div>
    <div style="margin-top:8px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="font-size:11px;color:#333333;">KW 9: <strong style="color:#000000;">0.0 h</strong></td>
          <td align="right" style="font-size:11px;color:#333333;">Ges: 369.3 h &nbsp; <span style="color:#991b1b;font-size:10px;font-weight:700;">🚨 41d inaktiv</span></td>
        </tr>
      </table>
    </div>
  </div>

</td></tr>
</table>
""",

    "Ticket-Stundenuebersicht": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 30px;">
  <div style="color: #000000; font-size: 20px; font-weight: 700; margin-bottom: 6px;">Ticket-Stundenuebersicht</div>
  <div style="color: #666666; font-size: 12px; margin-bottom: 20px;">Plan vs. Ist - Zeitkontingent-Auslastung pro Ticket</div>

  <div style="margin-bottom:16px;padding:14px 18px;background:#fee2e2;border-radius:12px;border:1px solid #e5e7eb;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td><span style="font-size:13px;color:#991b1b;font-weight:700;">Gesamt: 480.2 / 388.5 h</span></td>
        <td align="right"><span style="color:#991b1b;font-size:11px;font-weight:700;">🔴 4 kritisch</span> <span style="color:#92400e;font-size:11px;font-weight:700;">🟡 1 Warnung</span></td>
      </tr>
    </table>
  </div>

  <!-- KUNDE BETA – Marketing- und Design-Support -->
  <div style="margin-bottom:16px;">
    <div style="padding:10px 14px;background:#f3f4f6;border-radius:12px 12px 0 0;border:1px solid #e5e7eb;border-bottom:none;">
      <div style="font-size:14px;font-weight:700;color:#000000;">Kunde Beta e.V.</div>
      <div style="font-size:11px;color:#666666;margin-top:2px;">KND-B-001 &middot; Marketing- und Design-Support 2026</div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">Januar 2026</div><div style="font-size:10px;color:#666666;margin-top:2px;">03229 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#991b1b;">75.5 / 34.5 h</div><div style="font-size:11px;color:#991b1b;font-weight:600;">219%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#ef4444;border-radius:7px;height:12px;width:100%;min-width:2px;"></div></div>
        <span style="color:#991b1b;font-size:10px;font-weight:700;margin-left:6px;">⚠️ 41.0 h ueber Plan!</span>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb;">
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter S.: <strong style="color:#000000;">32.0 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter F.: <strong style="color:#000000;">23.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;">15.0 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter C.: <strong style="color:#000000;">3.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter T.: <strong style="color:#000000;">0.8 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter H.: <strong style="color:#000000;">0.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter R.: <strong style="color:#000000;">0.3 h</strong></div>
      </div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">Februar 2026</div><div style="font-size:10px;color:#666666;margin-top:2px;">03280 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#991b1b;">31.5 / 34.5 h</div><div style="font-size:11px;color:#991b1b;font-weight:600;">91%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#ef4444;border-radius:7px;height:12px;width:91%;min-width:2px;"></div></div>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb;">
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;">14.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Zeituebernahme: <strong style="color:#000000;">10.0 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter C.: <strong style="color:#000000;">4.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter R.: <strong style="color:#000000;">2.5 h</strong></div>
      </div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 12px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">Maerz 2026</div><div style="font-size:10px;color:#666666;margin-top:2px;">03325 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#065f46;">0.0 / 34.5 h</div><div style="font-size:11px;color:#065f46;font-weight:600;">0%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#10b981;border-radius:7px;height:12px;width:0%;min-width:2px;"></div></div>
      </div>
    </div>
  </div>

  <!-- KUNDE ALPHA – Marketing 2026 (nur Februar) -->
  <div style="margin-bottom:16px;">
    <div style="padding:10px 14px;background:#f3f4f6;border-radius:12px 12px 0 0;border:1px solid #e5e7eb;border-bottom:none;">
      <div style="font-size:14px;font-weight:700;color:#000000;">Kunde Alpha GmbH</div>
      <div style="font-size:11px;color:#666666;margin-top:2px;">KND-A-001 &middot; Marketing 2026</div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 12px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">Februar 2026</div><div style="font-size:10px;color:#666666;margin-top:2px;">03279 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#991b1b;">139.2 / 120.0 h</div><div style="font-size:11px;color:#991b1b;font-weight:600;">116%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#ef4444;border-radius:7px;height:12px;width:100%;min-width:2px;"></div></div>
        <span style="color:#991b1b;font-size:10px;font-weight:700;margin-left:6px;">⚠️ 19.2 h ueber Plan!</span> • <span style="color:#991b1b;font-size:10px;font-weight:700;">🚨 4d überfällig</span> • <span style="color:#666666;font-size:10px;">DL: 27.02.2026</span>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb;">
        <div style="margin-bottom:8px;padding:8px 10px;background:#ffffff;border-radius:8px;border:1px solid #e5e7eb;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="vertical-align:middle;"><div style="font-size:12px;font-weight:600;color:#000000;">Event</div></td><td align="right" style="vertical-align:middle;"><span style="font-size:12px;font-weight:700;color:#065f46;">24.3 / 0.0 h (0%)</span></td></tr></table>
          <div style="margin-top:6px;padding-left:8px;">
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter R.: <strong style="color:#000000;"> 14.5 h</strong></div>
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter P.: <strong style="color:#000000;"> 8.0 h</strong></div>
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;"> 1.8 h</strong></div>
          </div>
        </div>
        <div style="margin-bottom:8px;padding:8px 10px;background:#ffffff;border-radius:8px;border:1px solid #e5e7eb;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="vertical-align:middle;"><div style="font-size:12px;font-weight:600;color:#000000;">PM</div></td><td align="right" style="vertical-align:middle;"><span style="font-size:12px;font-weight:700;color:#065f46;">29.3 / 0.0 h (0%)</span></td></tr></table>
          <div style="margin-top:6px;padding-left:8px;">
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;"> 26.5 h</strong></div>
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter C.: <strong style="color:#000000;"> 2.8 h</strong></div>
          </div>
        </div>
        <div style="margin-bottom:8px;padding:8px 10px;background:#ffffff;border-radius:8px;border:1px solid #e5e7eb;">
          <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="vertical-align:middle;"><div style="font-size:12px;font-weight:600;color:#000000;">Video</div></td><td align="right" style="vertical-align:middle;"><span style="font-size:12px;font-weight:700;color:#065f46;">19.5 / 0.0 h (0%)</span></td></tr></table>
          <div style="margin-top:6px;padding-left:8px;">
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter E.: <strong style="color:#000000;"> 9.0 h</strong></div>
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter C.: <strong style="color:#000000;"> 6.5 h</strong></div>
            <div style="font-size:10px;color:#333333;padding:2px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;"> 4.0 h</strong></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- KUNDE GAMMA – Logo Update & Website -->
  <div style="margin-bottom:16px;">
    <div style="padding:10px 14px;background:#f3f4f6;border-radius:12px 12px 0 0;border:1px solid #e5e7eb;border-bottom:none;">
      <div style="font-size:14px;font-weight:700;color:#000000;">Kunde Gamma GmbH</div>
      <div style="font-size:11px;color:#666666;margin-top:2px;">KND-C-001 &middot; Logo Update &amp; Website One Pager</div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">PM</div><div style="font-size:10px;color:#666666;margin-top:2px;">02925 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#991b1b;">50.3 / 10.0 h</div><div style="font-size:11px;color:#991b1b;font-weight:600;">503%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#ef4444;border-radius:7px;height:12px;width:100%;min-width:2px;"></div></div>
        <span style="color:#991b1b;font-size:10px;font-weight:700;margin-left:6px;">⚠️ 40.3 h ueber Plan!</span> • <span style="color:#991b1b;font-size:10px;font-weight:700;">🚨 62d überfällig</span> • <span style="color:#666666;font-size:10px;">DL: 31.12.2025</span>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb;">
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter M.: <strong style="color:#000000;">34.3 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter C.: <strong style="color:#000000;">7.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter O.: <strong style="color:#000000;">5.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter K.: <strong style="color:#000000;">1.5 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter H.: <strong style="color:#000000;">1.5 h</strong></div>
      </div>
    </div>
    <div style="padding:14px;background:#fafafa;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 12px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td style="vertical-align:top;width:55%;"><div style="font-size:13px;font-weight:700;color:#000000;">Design One Pager</div><div style="font-size:10px;color:#666666;margin-top:2px;">02954 &middot; Status: open</div></td>
          <td style="vertical-align:top;text-align:right;width:45%;"><div style="font-size:15px;font-weight:700;color:#991b1b;">157.8 / 28.0 h</div><div style="font-size:11px;color:#991b1b;font-weight:600;">563%</div></td>
        </tr>
      </table>
      <div style="margin-top:8px;">
        <div style="background:#f3f4f6;border-radius:7px;height:12px;width:100%;position:relative;"><div style="background:#ef4444;border-radius:7px;height:12px;width:100%;min-width:2px;"></div></div>
        <span style="color:#991b1b;font-size:10px;font-weight:700;margin-left:6px;">⚠️ 129.8 h ueber Plan!</span> • <span style="color:#991b1b;font-size:10px;font-weight:700;">🚨 31d überfällig</span> • <span style="color:#666666;font-size:10px;">DL: 31.01.2026</span>
      </div>
      <div style="margin-top:10px;padding-top:10px;border-top:1px solid #e5e7eb;">
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter F.: <strong style="color:#000000;">129.8 h</strong></div>
        <div style="font-size:11px;color:#333333;padding:3px 0;">👤 Mitarbeiter Fr.: <strong style="color:#000000;">28.0 h</strong></div>
      </div>
    </div>
  </div>

  <div style="margin-top:12px;padding:10px 14px;font-size:10px;color:#666666;background:#f3f4f6;border-radius:8px;">🟢 &lt;70% &middot; 🟡 70-89% &middot; 🔴 >=90% &middot; Kontingent aus Ticket-Zeitkontingent (Poool)</div>
</td></tr>
</table>
""",


    "Legende": """
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color: #ffffff; border-radius: 16px; border: 1px solid #e5e7eb;">
<tr><td style="padding: 20px 30px;">
  <div style="font-size: 13px; color: #333333; line-height: 1.6; margin-bottom: 8px;">
    <strong>DB II:</strong> 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #22c55e; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>&gt;30% · 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #f59e0b; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>0–30% · 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #ef4444; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>&lt;0% · 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #9ca3af; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>Kein Umsatz
  </div>
  <div style="font-size: 11px; color: #666666; margin-bottom: 12px;">
    Formel: Umsatz – Fremdkosten = Rohertrag – Stundenkosten = DB II
  </div>
  <div style="font-size: 13px; color: #333333; line-height: 1.6; margin-bottom: 8px;">
    <strong>Ticket-Stunden:</strong> 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #22c55e; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>&lt;70% · 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #f59e0b; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>70–89% · 
    <span style="display: inline-block; width: 12px; height: 12px; background-color: #ef4444; border-radius: 50%; margin: 0 4px; vertical-align: middle;"></span>≥90%
  </div>
  <div style="font-size: 11px; color: #666666;">
    * Konfigurierbar: * Umsatz (Abgerechnet + Auftrag) | * Stunden (Selbstkostensatz)
  </div>
</td></tr>
</table>
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
    "Header (Wochenübersicht)": 180,
    "Fortschrittsanzeige (100% Complete)": 280,
    "Zeiterfassung Übersicht (SOLL/IST)": 450,
    "Wochentage-Status (Mo–Fr)": 120,
    "Tagesdetails (Projektzeiterfassung)": 750,
    "Nachbuchungen erforderlich (Warnung)": 350,
    "Projektübersicht (Tabelle)": 350,
    "Automatische E-Mail Hinweis": 120,
}

pm_heights = {
    "PM Header (Projekt-Übersicht)": 200,
    "Handlungsbedarf (Kritische Projekte)": 280,
    "Kennzahlen Übersicht": 350,
    "Projekt Details": 850,
    "Ticket-Stundenuebersicht": 1300,
    "Legende": 120,
    "PM Automatische E-Mail Hinweis": 120,
}

# ── Render sections for each selected mail type ──

auswahl_zeiterfassung = {}
auswahl_pm = {}

# Zeiterfassungsmail Sektionen
st.markdown("### Zeiterfassungs-Mail - Abschnitte auswählen")
st.markdown("---")

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

# PM-Mail Sektionen  
st.markdown("### Projektmanagement-Mail - Abschnitte auswählen")
st.markdown("---")

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

# ── Generate final HTML & send to Poool ──

st.markdown("---")

# ── Kosten-Info ──
st.subheader("Kosten & Versand")

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

st.divider()
st.subheader("Anmerkungen")
freitext = st.text_area("Hast du noch Wünsche oder Anmerkungen?", height=120, placeholder="z.B. anderer Versandtag, zusätzliche Inhalte, spezielle Anpassungen ...")

st.divider()

N8N_WEBHOOK_URL = "https://poool.app.n8n.cloud/webhook/7000884e-6635-4d83-a6ea-6c242857c004"

if st.button("kostenpflichtig bestellen", type="primary"):
    # Sammle alle gewählten Abschnitte
    alle_html_teile = []
    gesamt_info = []
    
    if "Zeiterfassungs-Mail" in mail_optionen:
        zeit_gewaehlte = [titel for titel, aktiv in auswahl_zeiterfassung.items() if aktiv]
        zeit_abgewaehlte = [titel for titel, aktiv in auswahl_zeiterfassung.items() if not aktiv]
        
        if zeit_gewaehlte:
            gesamt_info.append(f"Zeiterfassung: {len(zeit_gewaehlte)}/{len(zeiterfassung_sections)} Abschnitte")
            
            # Build Zeiterfassung HTML
            for titel in zeit_gewaehlte:
                content = zeiterfassung_sections[titel].replace("{{Vorname}}", "{{Vorname}}")  # Keep placeholder
                alle_html_teile.append(f'<tr><td style="padding: 0 0 8px 0;">{content}</td></tr>')
    
    if "Projektmanagement-Mail" in mail_optionen:
        pm_gewaehlte = [titel for titel, aktiv in auswahl_pm.items() if aktiv]
        pm_abgewaehlte = [titel for titel, aktiv in auswahl_pm.items() if not aktiv]
        
        if pm_gewaehlte:
            gesamt_info.append(f"Projektmanagement: {len(pm_gewaehlte)}/{len(pm_sections)} Abschnitte")
            
            # Build PM HTML mit 640px breite (wie im Original)
            for titel in pm_gewaehlte:
                content = pm_sections[titel].replace("{{Vorname}}", "{{Vorname}}")  # Keep placeholder
                alle_html_teile.append(f'<tr><td style="padding: 0 0 8px 0;">{content}</td></tr>')
    
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
            "zeiterfassungsmail_aktiv": "Zeiterfassungs-Mail" in mail_optionen,
            "pm_mail_aktiv": "Projektmanagement-Mail" in mail_optionen,
            "pm_stundenkosten_option": stundenkosten_option if pm_aktiv else None,
            "pm_rohertrag_option": rohertrag_option if pm_aktiv else None,
            "kosten": "€ 285 einmaliges Setup (pro Mail-Typ)",
            "versand": "Immer Montags (Abweichung nur bei PRISM Kunden möglich)",
            "mail_typen": mail_optionen,
            "zeiterfassung_abschnitte": auswahl_zeiterfassung if "Zeiterfassungs-Mail" in mail_optionen else {},
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
