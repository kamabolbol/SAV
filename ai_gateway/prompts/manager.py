TEMPLATES = {
    "product": "Génère une description SEO pour le produit :\nNom : {name}\nPrix : {price}\nDescription : {description}\nRéponse en français :",
    "email": "Rédige un email professionnel en français :\nSujet : {subject}\nMessage : {previous}\nRéponse :",
    "summary": "Résume ce texte en 5 phrases :\n{text}",
    "chat": "Réponds à l'utilisateur : {prompt}"
}

def load_template(task: str) -> str:
    return TEMPLATES.get(task, TEMPLATES["chat"])
