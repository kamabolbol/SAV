#!/bin/bash
echo "🔄 Téléchargement du modèle phi3:mini..."
docker exec -it erp_ollama ollama pull phi3:mini
echo "✅ Modèle phi3:mini prêt."
