# -*- coding: utf-8 -*-
"""
Générateur du JOURNAL ANNUEL DE CLASSE — Enseignement primaire (RDC)
Année scolaire 2026–2027

Rubriques : Date et heure · Branche · Classe · Sujet · Rappel · Matière ·
            Objectif · Méthode et procédé · Application · Observation

Usage :
    pip install reportlab
    python3 generer_journal.py
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, black, white
from reportlab.pdfgen import canvas

# ---------------------------------------------------------------- constantes
PAGE_W, PAGE_H = landscape(A4)          # 842 x 595 points
MARGE_G, MARGE_D = 20, 20
MARGE_HAUT, MARGE_BAS = 16, 22

BLEU = HexColor("#1a4f8b")
GRIS_CLAIR = HexColor("#e8eef5")
GRIS_LIGNE = HexColor("#5a6b7c")
GRIS_TEXTE = HexColor("#333333")

#                rubrique            largeur (pt)
COLONNES = [
    ("Date et\nheure",       52),
    ("Branche",              52),
    ("Classe",               32),
    ("Sujet",                88),
    ("Rappel",               92),
    ("Matière",             140),
    ("Objectif",             92),
    ("Méthode et\nprocédé",  84),
    ("Application",          92),
    ("Observation",          78),
]
TOTAL_COLONNES = sum(l for _, l in COLONNES)      # 802 pt
X0 = MARGE_G

NOMBRES_PAGES_REGLAGE = 60                        # pages vierges (≈ 9 lignes/page)

# ------------------------------------------------------------------- outils
def largeur_texte(txt, police, taille):
    return canvas.Canvas.__dict__ and None  # placeholder non utilisé


from reportlab.pdfbase.pdfmetrics import stringWidth

def couper_texte(txt, police, taille, largeur_max):
    """Découpe un texte en lignes tenant dans largeur_max."""
    lignes = []
    for paragraphe in txt.split("\n"):
        mots = paragraphe.split()
        if not mots:
            lignes.append("")
            continue
        courante = mots[0]
        for mot in mots[1:]:
            essai = courante + " " + mot
            if stringWidth(essai, police, taille) <= largeur_max:
                courante = essai
            else:
                lignes.append(courante)
                courante = mot
        lignes.append(courante)
    return lignes


def ecrire_cellule(c, txt, x, y_bas, w, h, police="Helvetica", taille=7.5,
                   gras=False, couleur=GRIS_TEXTE, interligne=1.15):
    """Écrit un texte en haut d'une cellule, avec retour à la ligne."""
    police = "Helvetica-Bold" if gras else police
    c.setFillColor(couleur)
    lignes = couper_texte(txt, police, taille, w - 4)
    y = y_bas + h - taille - 3
    for ligne in lignes:
        if y < y_bas + 2:
            break
        c.setFont(police, taille)
        c.drawString(x + 2, y, ligne)
        y -= taille * interligne


# ------------------------------------------------------------- page de garde
def page_garde(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    # cadre décoratif
    c.setStrokeColor(BLEU)
    c.setLineWidth(2.5)
    c.rect(28, 28, PAGE_W - 56, PAGE_H - 56)
    c.setLineWidth(0.8)
    c.rect(34, 34, PAGE_W - 68, PAGE_H - 68)

    cx = PAGE_W / 2
    c.setFillColor(BLEU)

    def centrer(txt, y, taille, gras=True, couleur=BLEU, espacement=0):
        police = "Helvetica-Bold" if gras else "Helvetica"
        c.setFillColor(couleur)
        c.setFont(police, taille)
        if espacement:
            c.drawCentredString(cx, y, txt, charSpace=espacement)
        else:
            c.drawCentredString(cx, y, txt)

    centrer("RÉPUBLIQUE DÉMOCRATIQUE DU CONGO", PAGE_H - 80, 13)
    centrer("MINISTÈRE DE L'ENSEIGNEMENT PRIMAIRE, SECONDAIRE ET TECHNIQUE",
            PAGE_H - 98, 10)
    centrer("EPST", PAGE_H - 112, 9, gras=False)

    c.setStrokeColor(BLEU)
    c.setLineWidth(1.2)
    c.line(cx - 180, PAGE_H - 124, cx + 180, PAGE_H - 124)

    centrer("Province :  ................................................",
            PAGE_H - 150, 11, gras=False, couleur=black)
    centrer("Sous-division / Coordination :  ................................................",
            PAGE_H - 168, 11, gras=False, couleur=black)
    centrer("École :  ................................................",
            PAGE_H - 186, 11, gras=False, couleur=black)
    centrer("Code d'identification de l'école :  .........................",
            PAGE_H - 204, 11, gras=False, couleur=black)

    centrer("JOURNAL ANNUEL DE CLASSE", PAGE_H - 268, 24, espacement=2)
    centrer("Registre des leçons — Enseignement primaire",
            PAGE_H - 290, 12, gras=False, couleur=GRIS_TEXTE)

    c.setStrokeColor(BLEU)
    c.setLineWidth(1.2)
    c.line(cx - 240, PAGE_H - 308, cx + 240, PAGE_H - 308)

    centrer("Année scolaire  2026 – 2027", PAGE_H - 344, 20)

    centrer("Nom de l'enseignant(e) :  .....................................................",
            PAGE_H - 400, 12, gras=False, couleur=black)
    centrer("Fonction / Grade :  .....................................................",
            PAGE_H - 420, 12, gras=False, couleur=black)
    centrer("Classes enseignées :  .....................................................",
            PAGE_H - 440, 12, gras=False, couleur=black)

    # visa du directeur
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.rect(PAGE_W - 250, 60, 200, 64)
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    c.drawString(PAGE_W - 242, 106, "Visa du Directeur :")
    c.setFont("Helvetica", 8)
    c.drawString(PAGE_W - 242, 68, "(nom, signature et cachet)")

    c.rect(50, 60, 200, 64)
    c.setFont("Helvetica", 10)
    c.drawString(58, 106, "Visa de l'Inspection :")
    c.setFont("Helvetica", 8)
    c.drawString(58, 68, "(nom, signature et cachet)")

    c.setFont("Helvetica", 7)
    c.setFillColor(GRIS_TEXTE)
    c.drawCentredString(cx, 42,
                        "Document de travail généré pour l'année scolaire 2026–2027 · Dépôt COURS-D-INFO")

    c.showPage()


# ------------------------------------------------------------ mode d'emploi
RUBRIQUES_AIDE = [
    ("Date et heure",
     "Le jour et l'heure de la leçon. Ex. : « lundi 07/09/2026, 10h00 – 10h40 ». "
     "Une ligne = une leçon (une période de travail avec les élèves)."),
    ("Branche",
     "La discipline (ou sous-branche) enseignée. Ex. : Français – Lecture ; "
     "Mathématiques – Calcul ; Éveil scientifique ; Initiation à l'informatique ; "
     "Éducation civique et morale."),
    ("Classe",
     "La classe concernée. Ex. : 3ème A, 5ème B… (préciser l'effectif si utile)."),
    ("Sujet",
     "Le titre exact de la leçon du jour, tel qu'écrit au tableau. "
     "Ex. : « Les périphériques de l'ordinateur »."),
    ("Rappel",
     "Bref résumé de la révision de la leçon précédente : questions posées aux élèves "
     "et réponses attendues. Ex. : « Q : citer les parties de l'ordinateur »."),
    ("Matière",
     "Le contenu nouveau développé pendant la leçon : définitions, notions, "
     "exemples, schémas... C'est le cœur de la leçon."),
    ("Objectif",
     "Ce que l'élève doit être capable de faire à la fin de la leçon, sous forme "
     "opérationnelle : « À la fin de la leçon, l'élève sera capable de … ». "
     "L'objectif doit être observable et évaluable."),
    ("Méthode et procédé",
     "MÉTHODE : interrogative, démonstrative, expositive, travail de groupes / "
     "par compétences. PROCÉDÉS : questions-réponses, démonstration, observation, "
     "illustration, exercice, discussion dirigée, jeu éducatif…"),
    ("Application",
     "Les exercices d'application réalisés par les élèves en classe, avec ou sans "
     "le maître. Ex. : « exercice 3 p. 24 ; classer les appareils en entrée/sortie »."),
    ("Observation",
     "Remarques : nombre d'élèves présents/absents, difficultés rencontrées, "
     "partie non terminée, suites à donner, leçons non faites et reportées, "
     "visites du directeur ou de l'inspecteur…"),
]

def page_mode_emploi(c):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

    c.setFillColor(BLEU)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGE_G, PAGE_H - 34, "COMMENT REMPLIR CE JOURNAL")
    c.setStrokeColor(BLEU)
    c.setLineWidth(1.2)
    c.line(MARGE_G, PAGE_H - 40, PAGE_W - MARGE_D, PAGE_H - 40)

    x0, x1 = MARGE_G, MARGE_G + 130          # colonne des rubriques
    x2 = PAGE_W - MARGE_D                    # fin des explications
    y = PAGE_H - 52
    hauteur_ligne = 49

    c.setStrokeColor(GRIS_LIGNE)
    c.setLineWidth(0.5)

    for nom, explication in RUBRIQUES_AIDE:
        # cadre
        c.rect(x0, y - hauteur_ligne + 8, x2 - x0, hauteur_ligne, stroke=1, fill=0)
        c.line(x1, y - hauteur_ligne + 8, x1, y + 8)

        c.setFillColor(BLEU)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x0 + 5, y - 6, nom)

        c.setFillColor(GRIS_TEXTE)
        c.setFont("Helvetica", 7.6)
        lignes = couper_texte(explication, "Helvetica", 7.6, x2 - x1 - 10)
        yy = y - 6
        for ligne in lignes[:5]:
            c.drawString(x1 + 6, yy, ligne)
            yy -= 9
        y -= hauteur_ligne

    c.setFillColor(GRIS_TEXTE)
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(MARGE_G, y - 2,
                 "Conseil : remplissez le journal le jour même, après chaque leçon. "
                 "Il sert de preuve de travail lors des contrôles (directeur, inspecteur) "
                 "et de base pour la préparation des leçons suivantes et les bulletins.")

    c.showPage()


# ------------------------------------------------------------ pages grille
def en_tete_grille(c, titre="JOURNAL ANNUEL DE CLASSE — 2026–2027"):
    c.setFillColor(BLEU)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGE_G, PAGE_H - 26, titre)

    c.setFont("Helvetica", 9)
    c.setFillColor(GRIS_TEXTE)
    c.drawString(MARGE_G + 300, PAGE_H - 26,
                 "Trimestre : ...............")
    c.drawString(MARGE_G + 430, PAGE_H - 26,
                 "Séquence : ...............")
    c.drawString(MARGE_G + 560, PAGE_H - 26,
                 "Semaine du : ..........................")
    c.setStrokeColor(GRIS_LIGNE)
    c.setLineWidth(0.8)
    c.line(MARGE_G, PAGE_H - 31, PAGE_W - MARGE_D, PAGE_H - 31)


def entetes_colonnes(c, y_haut, hauteur, fond=GRIS_CLAIR):
    c.setFillColor(fond)
    c.rect(X0, y_haut - hauteur, TOTAL_COLONNES, hauteur, stroke=0, fill=1)
    c.setStrokeColor(GRIS_LIGNE)
    c.setLineWidth(0.6)
    c.rect(X0, y_haut - hauteur, TOTAL_COLONNES, hauteur)
    x = X0
    for nom, larg in COLONNES:
        c.line(x + larg, y_haut, x + larg, y_haut - hauteur)
        c.setFillColor(BLEU)
        c.setFont("Helvetica-Bold", 7.5)
        yy = y_haut - 11
        for ligne in nom.split("\n"):
            c.drawCentredString(x + larg / 2, yy, ligne)
            yy -= 9
        x += larg


def dessiner_grille(c, y_haut, hauteur_dispo, n_lignes, lignes_data=None):
    """Dessine la grille ; si lignes_data est fourni, écrit le contenu."""
    h_col = 20
    h_ligne = hauteur_dispo / n_lignes
    entetes_colonnes(c, y_haut, h_col)
    y = y_haut - h_col

    c.setStrokeColor(GRIS_LIGNE)
    c.setLineWidth(0.5)
    for i in range(n_lignes):
        c.rect(X0, y - h_ligne * (i + 1), TOTAL_COLONNES, h_ligne)

    # lignes verticales
    x = X0
    for _, larg in COLONNES:
        c.line(x + larg, y, x + larg, y - h_ligne * n_lignes)
        x += larg

    if lignes_data:
        for i, ligne in enumerate(lignes_data):
            y_bas = y - h_ligne * (i + 1)
            x = X0
            for j, (nom, larg) in enumerate(COLONNES):
                if j < len(ligne) and ligne[j]:
                    gras = (j == 3)  # sujet en gras
                    ecrire_cellule(c, ligne[j], x, y_bas, larg, h_ligne,
                                   gras=gras, taille=7.2)
                x += larg
    return y - h_ligne * n_lignes


def page_grille(c, numero, total_pages, lignes_data=None, note_haut=None):
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    en_tete_grille(c)

    y_haut = PAGE_H - 40
    hauteur_dispo = y_haut - MARGE_BAS
    n_lignes = 9
    bas = dessiner_grille(c, y_haut, hauteur_dispo, n_lignes, lignes_data)

    if note_haut:
        c.setFillColor(HexColor("#8a2a2a"))
        c.setFont("Helvetica-BoldOblique", 10)
        c.drawString(MARGE_G, y_haut + 4, note_haut)

    c.setFillColor(GRIS_TEXTE)
    c.setFont("Helvetica", 8)
    c.drawRightString(PAGE_W - MARGE_D, MARGE_BAS - 12, f"Page {numero} / {total_pages}")
    c.showPage()


# ------------------------------------------------------------ exemples
EXEMPLES = [
    [
        "lun. 07/09/2026\n10h00 – 10h40",
        "Initiation à l'informatique",
        "5ème A",
        "L'unité centrale et les périphériques",
        "Questions : citer les parties de l'ordinateur vues la fois passée (écran, clavier, souris, unité centrale).",
        "L'unité centrale = le « cerveau » de l'ordinateur : il contient la carte mère, le processeur, la mémoire. "
        "Périphériques d'ENTRÉE : clavier, souris, micro. De SORTIE : écran, imprimante, haut-parleurs. "
        "D'entrée/sortie : clé USB, disque externe.",
        "À la fin de la leçon, l'élève sera capable de distinguer l'unité centrale des périphériques et de citer "
        "au moins 3 périphériques d'entrée et 3 de sortie.",
        "Méthode démonstrative et interrogative. Procédés : démonstration sur un vrai ordinateur, "
        "questions-réponses, illustrations dessinées au tableau.",
        "Chaque élève classe en « entrée » ou « sortie » les 8 appareils cités par le maître, puis lit ses réponses à voix haute.",
        "42 élèves présents sur 45. Notion bien comprise par la majorité ; à reprendre avec les 3 absents.",
    ],
    [
        "mar. 08/09/2026\n08h00 – 08h40",
        "Français – Lecture",
        "3ème A",
        "Le son [a] — lecture de la syllabe et des mots",
        "Lecture individuelle de la page précédente : syllabes « pa, ma, ta ».",
        "Revue des syllabes ; lecture des mots : papa, mama, pata, tama ; lecture d'une phrase simple : "
        "« Papa tama pata. ». Explication du sens des mots par images.",
        "À la fin de la leçon, l'élève sera capable de lire correctement les syllabes en [a] et les mots de la page 8.",
        "Méthode syllabique (synthétique). Procédés : lecture simultanée, lecture individuelle, "
        "questions-réponses, images.",
        "Lecture à tour de rôle de 6 élèves ; copie des mots dans le cahier d'exercices.",
        "5 élèves peinent à déchiffrer « pata » — exercice de renforcement prévu vendredi.",
    ],
    [
        "mer. 09/09/2026\n09h20 – 10h00",
        "Mathématiques – Calcul",
        "4ème B",
        "L'addition des nombres à trois chiffres, avec retenue",
        "Rappel de l'addition sans retenue : 234 + 152 = ... ; questions-réponses au tableau.",
        "Pose et résolution au tableau : 268 + 155. Explication de la retenue : 8 + 5 = 13, je pose 3 et je retiens 1. "
        "Deuxième exemple corrigé ensemble : 347 + 265.",
        "À la fin de la leçon, l'élève sera capable de poser et de résoudre correctement une addition de deux nombres "
        "à trois chiffres avec retenue.",
        "Méthode démonstrative. Procédés : démonstration au tableau, exercices individuels, "
        "correction collective.",
        "Exercices : 1) 365 + 148   2) 478 + 236   3) problème : « Mama a 237 fc et Papa lui donne 185 fc. "
        "Combien a-t-elle en tout ? »",
        "Leçon terminée dans le temps. 38/40 élèves ont juste ; revoir le problème écrit avec quelques élèves.",
    ],
]

TOTAL_EXEMPLES_PAGES = 1 + NOMBRES_PAGES_REGLAGE

def generer(chemin):
    c = canvas.Canvas(chemin, pagesize=landscape(A4))
    c.setTitle("Journal annuel de classe 2026-2027")
    c.setAuthor("COURS-D-INFO")

    page_garde(c)                                   # 1 : page de garde
    page_mode_emploi(c)                             # 2 : mode d'emploi
    page_grille(c, 1, TOTAL_EXEMPLES_PAGES,         # 3 : exemple rempli
                lignes_data=EXEMPLES,
                note_haut="EXEMPLE DE PAGE REMPLIE — à adapter à vos classes")
    for i in range(NOMBRES_PAGES_REGLAGE):          # 4+ : pages vierges
        page_grille(c, i + 2, TOTAL_EXEMPLES_PAGES)

    c.save()
    print(f"PDF généré : {chemin} "
          f"({1 + 1 + TOTAL_EXEMPLES_PAGES} pages)")


if __name__ == "__main__":
    generer("journal_annuel_2026-2027.pdf")
