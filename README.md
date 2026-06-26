# Local AI ERP Assistant

Plateforme IA locale intégrée à Odoo 18 avec Ollama , FastAPI et ChromaDB.



## Installation
```bash
cd docker
docker compose up -d
./init-ollama.sh
Voici une description complète du projet **Local AI ERP Assistant**, structurée selon les axes **technique**, **fonctionnel**,
 **modulaire** et **architectural**.

---

## 📌 Vue d’ensemble (Executive Summary)

**Local AI ERP Assistant** est une plateforme d’intelligence artificielle générative **100 % locale**
 intégrée à l’ERP Odoo 18. Elle vise à transformer les processus métier en permettant aux utilisateurs
d’interagir avec leurs données via le langage naturel, sans jamais exposer les informations sensibles à
 des services cloud externes. La solution repose sur une architecture conteneurisée (Docker) orchestrant
un LLM open-source, une base de données vectorielle pour la recherche sémantique, et une API Gateway assurant la sécurité, le routage
des modèles et l’audit.

---

## 🎯 Description Fonctionnelle


La plateforme couvre quatre cas d’usage métier essentiels. Elle propose d’abord un **assistant conversationnel
 intelligent**, accessible via une fenêtre modale dans Odoo, qui guide les utilisateurs et répond aux questions
 générales sur l’ERP et les processus internes. Elle assure également la **génération automatique de contenu métier**,
en rédigeant des descriptions SEO pour les fiches produits ou en proposant des réponses professionnelles aux emails clients,
 directement intégrées au CRM ou au Helpdesk. Au-delà du simple dialogue, le système exploite un mécanisme de
**RAG (Retrieval-Augmented Generation)** qui lui permet d’interroger la documentation interne de l’entreprise
 (PDF, contrats, procédures, historiques de tickets) stockée dans une base vectorielle, afin de fournir des réponses
 factuelles et précises, par exemple sur une politique de retour ou une clause contractuelle.
Enfin, il est capable d’**analyser les données structurées
** de PostgreSQL (ventes, stocks, clients) pour en extraire des tendances,
 des indicateurs de performance et des recommandations stratégiques,
 comme l’identification des cinq produits les plus rentables du mois.
---

## 🧱 Modularité du système

L’architecture est découpée en modules logiques faiblement couplés, facilitant la maintenance et l’évolution :

1.  **Module Odoo (`local_llm`)** : Interface utilisateur et connecteur métier.
    *   Définit les modèles de données (`llm.config`, `llm.conversation`, `llm.message`).
    *   Expose des endpoints internes (`/ai/chat`) et des assistants (wizards).
    *   S’interface avec l’API Gateway via des appels REST.

2.  **Module d’Orchestration (AI Gateway)** : Cerveau logique de la plateforme.
    *   **Security Layer** : Filtrage des prompts (injections, mots sensibles) et authentification.
    *   **Prompt Engine** : Gestion de templates de prompts versionnés (pour éviter le "hard-coding").
    *   **Model Router** : Sélection automatique du modèle LLM en fonction de la tâche (ex: `tinyllama` pour le chat,
`gemma` pour le résumé, `mistral` pour l’analyse).
    *   **Context Manager** : Enrichissement du contexte avant l’envoi au LLM (données utilisateur, métadonnées).
    *   **Audit Logger** : Traçabilité de toutes les interactions (utilisateur, prompt, réponse, latence, modèle utilisé).

3.  **Module de RAG (Vector Store)** :
    *   Pipeline d’ingestion : découpage (chunking) des documents → génération d’embeddings (via `sentence-transformers`)
→ stockage dans **ChromaDB** (mode embarqué).
    *   Pipeline de requête : similarité cosinus → récupération des chunks pertinents → injection dans le prompt.

4.  **Module d’Inférence (LLM Engine)** :
    *   Wrapper autour de l’API d’**Ollama**.
    *   Gère les appels aux modèles locaux (`phi3:mini` ou `tinyllama` pour respecter la limite de 8 Go de RAM).
    *   Gère les timeouts et les tentatives de rechargement.

5.  **Module de Persistance** :
    *   **PostgreSQL** pour les données ERP et les logs d'audit.
    *   **Volumes Docker** pour la persistance des embeddings (Chroma) et des modèles Ollama.

---

## 🏛️ Architecture Technique

L’architecture suit un pattern **monolithique modulaire** (pour la simplicité de déploiement) mais conçue pour évoluer
vers des microservices (via une séparation stricte des responsabilités et une communication standardisée en REST/JSON).

### Vue globale (couches)

```
<img width="561" height="451" alt="image" src="https://github.com/user-attachments/assets/285768e3-aa3e-48b7-b8e2-f0fec84467ab" />

### Flux de données (requête IA)

1.  **Déclenchement** : L'utilisateur saisit une requête dans Odoo.
2.  **Appel API** : Odoo envoie la requête au Gateway (`/chat` ou `/generate`).
3.  **Sécurité** : Le Security Layer analyse la requête (blocage des injections, mots sensibles).
4.  **Contexte / RAG (si besoin)** :
    *   Si la tâche nécessite des données métier, le Context Manager interroge PostgreSQL.
    *   Si la tâche nécessite de la documentation, le RAG interroge ChromaDB.
5.  **Prompt Engineering** : Le Prompt Engine construit le prompt final avec les consignes et le contexte.
6.  **Routage** : Le Model Router sélectionne le LLM (ex: `tinyllama` pour la rapidité).
7.  **Inférence** : Le Gateway interroge Ollama via son API `/api/generate`.
8.  **Réponse** : La réponse est renvoyée à Odoo, puis affichée à l'utilisateur.
9.  **Audit** : Un log JSON est écrit (contenant l’action, l’utilisateur, la latence, etc.).

---

## 💡 Points d’innovation et atouts techniques

- **Souveraineté des données** : Aucun appel externe ; tout s’exécute dans l’infrastructure de l’entreprise.
- **Sécurité IA intégrée** : Filtrage proactif des "prompt injections" et détection des demandes sensibles (ex: *“donne-moi les salaires”*).
- **RAG hybride** : Combinaison de connaissances interne du LLM + données métier en temps réel + documents externes.
- **Modularité Future** : La séparation Gateway / LLM / Vector Store permet de remplacer facilement le modèle (ex: passer à Mistral) ou d’ajouter un cache Redis sans impacter Odoo.
- **Adaptabilité Matérielle** : Choix de modèles quantifiés (Q4_0) et réduction de la taille des contextes pour garantir la stabilité sur 8 Go de RAM.




---

## 🔍 Observabilité & Monitoring

La plateforme intègre une stack d'observabilité complète pour le monitoring, le debugging et l'analyse de performance. Elle est entièrement conteneurisée et préconfigurée.

### 🧩 Composants intégrés

| Outil | Rôle | Port |
| :--- | :--- | :--- |
| **Grafana** | Visualisation unifiée (métriques, logs, traces) | 3000 |
| **Prometheus** | Collecte et stockage des métriques (requêtes/sec, latence, erreurs) | 9090 |
| **Loki** | Agrégation de logs structurés (JSON) | 3100 |
| **Tempo** | Traçage distribué (OpenTelemetry) | 3200, 4317, 4318 |
| **Promtail** | Collecteur de logs Docker (scraping intelligent) | 9080 |

### 🚀 Accès rapide

| Service | URL | Identifiants |
| :--- | :--- | :--- |
| **Grafana** | http://localhost:3000 | `admin` / `admin` |
| **Prometheus** | http://localhost:9090 | – |
| **Loki** | http://localhost:3100 | – |
| **Tempo** | http://localhost:3200 | – |

### 📊 Métriques exposées

L’API Gateway (`ai-gateway`) expose les métriques suivantes via `/metrics` :

- `ai_requests_total` : nombre total de requêtes IA
- `ai_request_latency_seconds` : latence des requêtes (p50/p95/p99)
- `ai_errors_total` : nombre d’erreurs par type

### 🧪 Exemple de requête dans Grafana

1. Connectez-vous à **Grafana** (`http://localhost:3000`).
2. Allez dans **Explore**.
3. Sélectionnez **Prometheus** comme source.
4. Exécutez la requête : `rate(ai_requests_total[1m])`
5. Visualisez le débit de requêtes en temps réel.

### 📝 Logs structurés

Les logs de l’API Gateway sont au format JSON et incluent :

```json
{
  "timestamp": "2026-06-27T10:00:00Z",
  "severity": "INFO",
  "name": "ai-gateway",
  "message": "Request processed",
  "request_id": "abc-123",
  "trace_id": "4bf92f3577b34da6"
}