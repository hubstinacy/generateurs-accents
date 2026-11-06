import gradio as gr
from gtts import gTTS

def generate_accent(text, accent_origin):
    # Dictionnaire des langues (le moteur vocal)
    # L'astuce : Le moteur lit le texte fourni avec les règles de prononciation de son pays d'origine.
    accents = {
        "Voix Américaine (US)": ("en", "us"),
        "Voix Britannique (UK)": ("en", "co.uk"),
        "Voix Française (France)": ("fr", "fr"),
        "Voix Française (Sénégal/Afrique)": ("fr", "sn"),
        "Voix Québécoise": ("fr", "ca"),
        "Voix Espagnole": ("es", "es"),
        "Voix Mexicaine": ("es", "com.mx"),
        "Voix Allemande": ("de", "de"),
        "Voix Italienne": ("it", "it"),
        "Voix Chinoise (Mandarin)": ("zh-CN", "com"),
        "Voix Japonaise": ("ja", "co.jp"),
        "Voix Indienne (Hindi)": ("hi", "co.in")
    }
    
    lang, tld = accents.get(accent_origin, ("fr", "fr"))
    
    try:
        tts = gTTS(text=text, lang=lang, tld=tld)
        output_file = "audio_accent.mp3"
        tts.save(output_file)
        return output_file, f"Génération réussie avec : {accent_origin}"
    except Exception as e:
        return None, f"Erreur : {str(e)}"

with gr.Blocks(title="Machine à Accents", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌍 La Machine à Accents")
    gr.Markdown("**L'astuce :** Écris ton texte dans la langue que tu souhaites, puis choisis la voix d'un autre pays. Exemple : Tape du Français, choisis *Voix Américaine*, et écoute le résultat !")
    
    text_input = gr.Textbox(label="Texte à prononcer", placeholder="Ex : Bonjour, je voudrais manger une pomme...")
    
    accent_dropdown = gr.Dropdown(
        choices=[
            "Voix Américaine (US)", "Voix Britannique (UK)", 
            "Voix Française (France)", "Voix Française (Sénégal/Afrique)", "Voix Québécoise",
            "Voix Espagnole", "Voix Mexicaine", "Voix Allemande", "Voix Italienne", 
            "Voix Chinoise (Mandarin)", "Voix Japonaise", "Voix Indienne (Hindi)"
        ], 
        label="Origine de la voix (Le filtre d'accent)", 
        value="Voix Américaine (US)"
    )
    
    btn = gr.Button("Générer l'audio", variant="primary")
    audio_out = gr.Audio(label="Résultat", type="filepath")
    status = gr.Textbox(label="Statut", interactive=False)
    
    btn.click(generate_accent, [text_input, accent_dropdown], [audio_out, status])

if __name__ == "__main__":
    app.launch(inbrowser=True)
