import os
from PIL import Image, ImageDraw, ImageFont

def create_ssh_icon():
    # Taille de l'icône
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fond de l'icône (un terminal arrondi)
    bg_color = (40, 44, 52, 255) # Gris foncé
    outline_color = (97, 175, 239, 255) # Bleu clair
    margin = 20
    draw.rounded_rectangle([margin, margin, size-margin, size-margin], radius=30, fill=bg_color, outline=outline_color, width=8)

    # Dessin des boutons en haut à gauche (style macOS)
    radius = 8
    y_buttons = margin + 15
    draw.ellipse([margin+20, y_buttons, margin+20+radius*2, y_buttons+radius*2], fill=(255, 89, 89, 255))
    draw.ellipse([margin+45, y_buttons, margin+45+radius*2, y_buttons+radius*2], fill=(255, 189, 46, 255))
    draw.ellipse([margin+70, y_buttons, margin+70+radius*2, y_buttons+radius*2], fill=(39, 201, 63, 255))

    # Ligne de séparation
    draw.line([margin, margin+40, size-margin, margin+40], fill=outline_color, width=4)

    # Texte du terminal ">_ "
    try:
        # Essayer de charger une police à taille fixe
        font = ImageFont.truetype("consola.ttf", 80)
    except IOError:
        font = ImageFont.load_default()

    text_color = (152, 195, 121, 255) # Vert
    draw.text((margin + 30, margin + 70), ">_", font=font, fill=text_color)
    
    # Texte SSH
    try:
        font2 = ImageFont.truetype("consola.ttf", 60)
    except IOError:
        font2 = ImageFont.load_default()
    draw.text((margin + 30, margin + 150), "SSH", font=font2, fill=(229, 192, 123, 255)) # Jaune

    # Création du dossier assets si nécessaire
    os.makedirs('assets', exist_ok=True)

    # Sauvegarde en PNG
    png_path = 'assets/icon.png'
    img.save(png_path, format='PNG')

    # Sauvegarde en ICO (avec plusieurs tailles recommandées)
    ico_path = 'assets/icon.ico'
    icon_sizes = [(16,16), (32, 32), (48, 48), (64,64), (128, 128), (256, 256)]
    img.save(ico_path, format='ICO', sizes=icon_sizes)

if __name__ == "__main__":
    create_ssh_icon()
