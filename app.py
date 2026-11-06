import gradio as gr
from gtts import gTTS

def generate_accent(text, accent_origin):
    # Dictionnaire étendu au maximum des capacités de Google TTS (Pays et grandes régions)
    accents = {
        # --- ANGLAIS (Forte variation selon le pays) ---
        "Anglais (États-Unis)": ("en", "us"),
        "Anglais (Royaume-Uni)": ("en", "co.uk"),
        "Anglais (Australie)": ("en", "com.au"),
        "Anglais (Irlande)": ("en", "ie"),
        "Anglais (Afrique du Sud)": ("en", "co.za"),
        "Anglais (Inde)": ("en", "co.in"),
        "Anglais (Nigeria)": ("en", "com.ng"),
        
        # --- FRANÇAIS ---
        "Français (France)": ("fr", "fr"),
        "Français (Québec/Canada)": ("fr", "ca"),
        "Français (Sénégal)": ("fr", "sn"), # Note: la variation africaine de Google reste très légère
        
        # --- ESPAGNOL ---
        "Espagnol (Espagne)": ("es", "es"),
        "Espagnol (Mexique)": ("es", "com.mx"),
        "Espagnol (États-Unis)": ("es", "com"),
        
        # --- PORTUGAIS ---
        "Portugais (Portugal)": ("pt", "pt"),
        "Portugais (Brésil)": ("pt", "com.br"),
        
        # --- AUTRES LANGUES ---
        "Allemand": ("de", "de"),
        "Italien": ("it", "it"),
        "Chinois (Mandarin)": ("zh-CN", "com"),
        "Japonais": ("ja", "co.jp"),
        "Russe": ("ru", "ru"),
        "Arabe": ("ar", "com")
    }
    
    lang, tld = accents.get(accent_origin, ("fr", "fr"))
    
    try:
        tts = gTTS(text=text, lang=lang, tld=tld)
        output_file = "audio_accent.mp3"
        tts.save(output_file)
        return output_file, f"Génération réussie avec : {accent_origin}"
    except Exception as e:
        return None, f"Erreur : {str(e)}"

# Interface Gradio
with gr.Blocks(title="Machine à Accents", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🌍 La Machine à Accents (Max gTTS)")
    gr.Markdown("**Rappel :** gTTS gère uniquement les accents liés aux pays (via les domaines Google). Pour des accents de villes ou de villages, une IA Premium (ElevenLabs) est requise.")
    
    text_input = gr.Textbox(label="Texte à prononcer", placeholder="Ex : Bonjour, comment allez-vous aujourd'hui ?")
    
    accent_dropdown = gr.Dropdown(
        choices=[
            "Anglais (États-Unis)", "Anglais (Royaume-Uni)", "Anglais (Australie)", 
            "Anglais (Irlande)", "Anglais (Afrique du Sud)", "Anglais (Inde)", "Anglais (Nigeria)",
            "Français (France)", "Français (Québec/Canada)", "Français (Sénégal)",
            "Espagnol (Espagne)", "Espagnol (Mexique)", "Espagnol (États-Unis)",
            "Portugais (Portugal)", "Portugais (Brésil)",
            "Allemand", "Italien", "Chinois (Mandarin)", "Japonais", "Russe", "Arabe"
        ], 
        label="Origine de la voix (Le filtre d'accent)", 
        value="Anglais (États-Unis)"
    )
    
    btn = gr.Button("Générer l'audio", variant="primary")
    audio_out = gr.Audio(label="Résultat", type="filepath")
    status = gr.Textbox(label="Statut", interactive=False)
    
    btn.click(generate_accent, [text_input, accent_dropdown], [audio_out, status])

if __name__ == "__main__":
    app.launch(inbrowser=True)
