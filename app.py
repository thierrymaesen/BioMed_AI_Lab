import os
import cv2
import numpy as np
import streamlit as st

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
# On importe Image sous le nom RLImage pour éviter le conflit avec PIL
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="BioMed AI Lab", page_icon="🔬", layout="wide")

# --- SYSTÈME DE MÉMOIRE (Session State) ---
if 'sensibilite_actuelle' not in st.session_state:
    st.session_state.sensibilite_actuelle = 50
if 'tolerance_actuelle' not in st.session_state:
    st.session_state.tolerance_actuelle = 5
if 'is_calibrated' not in st.session_state:
    st.session_state.is_calibrated = False

# --- MOTEUR MATHÉMATIQUE D'AUTO-CALIBRATION ---
def auto_calibration(image_cv2, masque_ia):
    gris = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) if len(image_cv2.shape) == 3 else image_cv2.copy()
    gris_lisse = cv2.GaussianBlur(gris, (5, 5), 0)
    
    sobelx = cv2.Sobel(gris_lisse, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gris_lisse, cv2.CV_64F, 0, 1, ksize=3)
    contours = cv2.magnitude(sobelx, sobely)
    contours_8u = cv2.normalize(contours, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    
    pixels_in_mask = contours_8u[masque_ia == 255]
    
    if len(pixels_in_mask) > 0:
        seuil_calcule = int(np.mean(pixels_in_mask) + np.std(pixels_in_mask))
        seuil_calcule = max(10, min(int(round(seuil_calcule / 5.0) * 5), 200))
    else:
        seuil_calcule = 50
        
    _, contours_forts = cv2.threshold(contours, seuil_calcule, 255, cv2.THRESH_BINARY)
    contours_forts = contours_forts.astype(np.uint8)
    anomalies_cibles = cv2.bitwise_and(contours_forts, contours_forts, mask=masque_ia)
    
    pixels_cellule = cv2.countNonZero(masque_ia)
    pixels_anormaux = cv2.countNonZero(anomalies_cibles)
    densite = (pixels_anormaux / pixels_cellule) * 100 if pixels_cellule > 0 else 0
    
    tolerance_calculee = int(densite) + 2
    tolerance_calculee = max(1, min(tolerance_calculee, 50))
    
    return seuil_calcule, tolerance_calculee

# --- BARRE LATÉRALE DE RÉGLAGE ---
st.sidebar.header("⚙️ Calibration du Laboratoire")

if st.session_state.is_calibrated:
    st.sidebar.success("✅ Appareil Calibré Automatiquement")
else:
    st.sidebar.warning("⚠️ Non Calibré (Réglages par défaut ou manuels)")

st.sidebar.info("💡 **Note Importante :** Si vous changez de microscope ou modifiez l'éclairage, refaites une Auto-Calibration avec une image saine de référence.")
st.sidebar.markdown("---")

val_sensibilite = st.sidebar.slider(
    "Sensibilité aux contrastes", min_value=10, max_value=200, value=st.session_state.sensibilite_actuelle, step=5
)

val_tolerance = st.sidebar.slider(
    "Tolérance de surface (%)", min_value=1, max_value=50, value=st.session_state.tolerance_actuelle, step=1
)

if val_sensibilite != st.session_state.sensibilite_actuelle or val_tolerance != st.session_state.tolerance_actuelle:
    st.session_state.sensibilite_actuelle = val_sensibilite
    st.session_state.tolerance_actuelle = val_tolerance
    st.session_state.is_calibrated = False 
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 **Créé par Thierry Maesen**")
st.sidebar.markdown("[📂 Code Source sur GitHub](https://github.com/thierrymaesen/BioMed_AI_Lab)")

# --- EN-TÊTE PRINCIPAL ---
st.title("🔬 BioMed AI : Analyse & Segmentation Cellulaire")
st.markdown("**Outil d'assistance au tri.** L'IA isole la matière biologique, puis analyse la densité des anomalies structurelles.")

# --- MOTEUR 1 : INTELLIGENCE ARTIFICIELLE ---
def segmenter_avec_ia(image_cv2):
    pixels = image_cv2.reshape((-1, 3)) if len(image_cv2.shape) == 3 else image_cv2.reshape((-1, 1))
    pixels = np.float32(pixels)
    criteres = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centres = cv2.kmeans(pixels, 3, None, criteres, 10, cv2.KMEANS_RANDOM_CENTERS)
    centres = np.uint8(centres)
    image_segmentee_ia = centres[labels.flatten()].reshape(image_cv2.shape)
    valeur_fond = np.argmax(np.sum(centres, axis=1) if len(centres.shape) > 1 else centres)
    masque_ia = np.zeros(labels.shape, dtype=np.uint8)
    masque_ia[labels != valeur_fond] = 255
    masque_ia = masque_ia.reshape((image_cv2.shape[0], image_cv2.shape[1]))
    return image_segmentee_ia, masque_ia

# --- MOTEUR 2 : COMPUTER VISION ---
def analyser_cellule(image_cv2, masque_ia, seuil_sobel):
    gris = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY) if len(image_cv2.shape) == 3 else image_cv2.copy()
    gris_lisse = cv2.GaussianBlur(gris, (5, 5), 0)
    sobelx = cv2.Sobel(gris_lisse, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gris_lisse, cv2.CV_64F, 0, 1, ksize=3)
    contours = cv2.magnitude(sobelx, sobely)
    _, contours_forts = cv2.threshold(contours, seuil_sobel, 255, cv2.THRESH_BINARY)
    contours_forts = contours_forts.astype(np.uint8)
    anomalies_cibles = cv2.bitwise_and(contours_forts, contours_forts, mask=masque_ia)
    pixels_cellule = cv2.countNonZero(masque_ia)
    pixels_anormaux = cv2.countNonZero(anomalies_cibles)
    densite_anomalie = (pixels_anormaux / pixels_cellule) * 100 if pixels_cellule > 0 else 0
    return densite_anomalie, gris, anomalies_cibles


# --- GÉNÉRATION DU RAPPORT PDF ---
def generer_rapport_pdf(image_originale, image_ia, image_resultat, densite, tolerance, is_calibrated):
    img_orig_pil = Image.fromarray(image_originale)
    img_ia_pil = Image.fromarray(image_ia)
    img_result_pil = Image.fromarray(image_resultat)
    
    img_orig_bytes = BytesIO()
    img_ia_bytes = BytesIO()
    img_result_bytes = BytesIO()
    
    img_orig_pil.save(img_orig_bytes, format="PNG")
    img_ia_pil.save(img_ia_bytes, format="PNG")
    img_result_pil.save(img_result_bytes, format="PNG")
    
    img_orig_bytes.seek(0)
    img_ia_bytes.seek(0)
    img_result_bytes.seek(0)
    
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'], fontSize=24,
        textColor=colors.HexColor('#1f2121'), spaceAfter=6, alignment=1
    )
    story.append(Paragraph("🔬 BioMed AI Lab", title_style))
    story.append(Paragraph("Rapport d'Analyse Cellulaire", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    date_str = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    status = "✅ Calibration Automatique" if is_calibrated else "⚠️ Calibration Manuelle"
    
    info_data = [["Date d'analyse :", date_str], ["Statut de calibration :", status]]
    info_table = Table(info_data, colWidths=[2*inch, 3.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8e8e8')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Résultats de l'Analyse", styles['Heading2']))
    
    if densite <= tolerance:
        diagnostic = "🟢 NORMAL"
        diagnostic_color = colors.HexColor('#22c55e')
        message = f"Biologie conforme. Niveau de perturbation : {densite:.1f}%"
    else:
        diagnostic = "🔴 ANOMALIE DÉTECTÉE"
        diagnostic_color = colors.HexColor('#ef4444')
        message = f"Anomalie détectée. Niveau de perturbation : {densite:.1f}%"
    
    result_data = [
        ["Diagnostic :", diagnostic],
        ["Perturbation mesurée :", f"{densite:.1f}%"],
        ["Tolérance machine :", f"{tolerance}%"],
        ["Message :", message],
    ]
    result_table = Table(result_data, colWidths=[2*inch, 3.5*inch])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8e8e8')),
        ('BACKGROUND', (1, 0), (1, 0), diagnostic_color),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(PageBreak())
    story.append(Paragraph("Visualisation de l'Analyse", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
    
    img_width = 1.8*inch
    img_height = 1.35*inch
    img_table = Table([
        ["Image Originale", "Cartographie IA", "Détection Anomalies"],
        [
            RLImage(img_orig_bytes, width=img_width, height=img_height),
            RLImage(img_ia_bytes, width=img_width, height=img_height),
            RLImage(img_result_bytes, width=img_width, height=img_height),
        ]
    ], colWidths=[2*inch, 2*inch, 2*inch])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    story.append(img_table)
    
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Rapport généré par BioMed AI Lab | GitHub: thierrymaesen", styles['Normal']))
    
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer


# --- INTERFACE ---
fichier_upload = st.file_uploader("Insérez une image issue du microscope :", type=["png", "jpg", "jpeg"])

if fichier_upload is not None:
    image_pil = Image.open(fichier_upload)
    img_cv2 = np.array(image_pil)
    
    vue_ia, masque_ia = segmenter_avec_ia(img_cv2)
    
    if st.button("🎯 Prendre cette image comme référence saine (Auto-Calibrer)"):
        nouveau_seuil, nouvelle_tol = auto_calibration(img_cv2, masque_ia)
        st.session_state.sensibilite_actuelle = nouveau_seuil
        st.session_state.tolerance_actuelle = nouvelle_tol
        st.session_state.is_calibrated = True
        st.rerun()
    
    densite, vue_grise, vue_alerte = analyser_cellule(img_cv2, masque_ia, st.session_state.sensibilite_actuelle)
    
    st.markdown("---")
    if densite <= st.session_state.tolerance_actuelle:
        st.success(f"🟢 NORMAL : Biologie conforme. (Perturbation : {densite:.1f}% / Tolérance de la machine : {st.session_state.tolerance_actuelle}%)")
    else:
        st.error(f"🔴 ANOMALIE DÉTECTÉE ! Le niveau de perturbation ({densite:.1f}%) dépasse la tolérance de la machine ({st.session_state.tolerance_actuelle}%) calibrée.")
        
    img_resultat = cv2.cvtColor(vue_grise, cv2.COLOR_GRAY2BGR)
    img_resultat[vue_alerte > 0] = [255, 0, 0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(image_pil, caption="1. Image originale", use_container_width=True)
    with col2:
        st.image(vue_ia, caption="2. Cartographie IA", use_container_width=True)
    with col3:
        st.image(img_resultat, caption="3. Détection des anomalies", use_container_width=True)
        
    # --- BOUTON DE TÉLÉCHARGEMENT PDF ---
    st.markdown("---")
    col_pdf1, col_pdf2, col_pdf3 = st.columns([1, 2, 1])
    with col_pdf2:
        pdf_rapport = generer_rapport_pdf(img_cv2, vue_ia, img_resultat, densite, st.session_state.tolerance_actuelle, st.session_state.is_calibrated)
        st.download_button(
            label="📥 Télécharger le Rapport PDF",
            data=pdf_rapport,
            file_name=f"rapport_biomed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'><small>BioMed AI Lab - Développé par Thierry Maesen | <a href='https://github.com/thierrymaesen/BioMed_AI_Lab' target='_blank'>Voir le code sur GitHub</a></small></div>", unsafe_allow_html=True)
