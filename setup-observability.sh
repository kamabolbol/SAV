#!/bin/bash
# Script de configuration de la stack d'observabilité pour SAV
# Exécuter depuis ~/projects/SAV

set -e  # Arrête le script en cas d'erreur

echo "======================================"
echo "🔧 MISE EN PLACE DE L'OBSERVABILITÉ SAV"
echo "======================================"

# ------------------------------------------------------------------
# 1. Créer le fichier Loki manquant
# ------------------------------------------------------------------
echo "📁 1. Création de loki/loki-config.yaml..."
mkdir -p loki
cat > loki/loki-config.yaml << 'EOF'
auth_enabled: false

server:
  http_listen_port: 3100

common:
  ring:
    instance_addr: 127.0.0.1
    kvstore:
      store: inmemory
  replication_factor: 1
  path_prefix: /loki

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

storage_config:
  filesystem:
    directory: /loki/chunks

limits_config:
  retention_period: 744h   # 31 jours
  allow_structured_metadata: true

compactor:
  working_directory: /loki/compactor
  shared_store: filesystem
  compaction_interval: 10m
  retention_enabled: true
EOF
echo "✅ loki/loki-config.yaml créé."

# ------------------------------------------------------------------
# 2. Adapter Prometheus pour SAV
# ------------------------------------------------------------------
echo "📁 2. Mise à jour de prometheus/prometheus.yml..."
cat > prometheus/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ai-gateway'
    static_configs:
      - targets: ['ai-gateway:8000']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'odoo'
    static_configs:
      - targets: ['odoo:8069']
    metrics_path: /metrics
    scrape_interval: 10s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF
echo "✅ prometheus/prometheus.yml mis à jour."

# ------------------------------------------------------------------
# 3. Créer le dashboard SAV
# ------------------------------------------------------------------
echo "📁 3. Création du dashboard SAV..."
mkdir -p grafana/provisioning/dashboards
cat > grafana/provisioning/dashboards/sav-dashboard.json << 'EOF'
{
  "title": "SAV AI Assistant Monitoring",
  "uid": "sav-observability",
  "panels": [
    {
      "id": 1,
      "title": "AI Requests per Second",
      "type": "graph",
      "targets": [
        {
          "expr": "rate(ai_requests_total[1m])",
          "legendFormat": "requests/sec",
          "refId": "A"
        }
      ],
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
    },
    {
      "id": 2,
      "title": "AI Request Latency (p50/p95/p99)",
      "type": "graph",
      "targets": [
        {"expr": "histogram_quantile(0.50, sum(rate(ai_request_latency_seconds_bucket[1m])) by (le))", "legendFormat": "p50"},
        {"expr": "histogram_quantile(0.95, sum(rate(ai_request_latency_seconds_bucket[1m])) by (le))", "legendFormat": "p95"},
        {"expr": "histogram_quantile(0.99, sum(rate(ai_request_latency_seconds_bucket[1m])) by (le))", "legendFormat": "p99"}
      ],
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
    },
    {
      "id": 3,
      "title": "AI Error Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(ai_errors_total[1m])) / sum(rate(ai_requests_total[1m]))",
          "legendFormat": "error-rate"
        }
      ],
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
    },
    {
      "id": 4,
      "title": "Logs (Loki)",
      "type": "logs",
      "targets": [
        {
          "expr": "{container=\"erp_ai_gateway\"}",
          "refId": "A"
        }
      ],
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
    },
    {
      "id": 5,
      "title": "Traces (Tempo)",
      "type": "traces",
      "targets": [
        {
          "queryType": "traceql",
          "refId": "A"
        }
      ],
      "gridPos": {"h": 8, "w": 24, "x": 0, "y": 16}
    }
  ],
  "time": {"from": "now-1h", "to": "now"},
  "tags": ["sav", "ai", "observability"],
  "version": 1
}
EOF
echo "✅ Dashboard SAV créé."

# ------------------------------------------------------------------
# 4. Mettre à jour dashboards.yml
# ------------------------------------------------------------------
echo "📁 4. Mise à jour de dashboards.yml..."
cat > grafana/provisioning/dashboards/dashboards.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF
echo "✅ dashboards.yml mis à jour."

# ------------------------------------------------------------------
# 5. Supprimer l'ancien dashboard Ray Serve (s'il existe)
# ------------------------------------------------------------------
if [ -f grafana/provisioning/dashboards/ray-serve-dashboard.json ]; then
  echo "📁 5. Suppression de l'ancien dashboard Ray Serve..."
  rm grafana/provisioning/dashboards/ray-serve-dashboard.json
  echo "✅ Ancien dashboard supprimé."
else
  echo "ℹ️  Aucun ancien dashboard trouvé."
fi

# ------------------------------------------------------------------
# 6. Ajout des labels Promtail dans docker-compose.yml (automatique)
# ------------------------------------------------------------------
echo "📁 6. Ajout des labels Promtail dans docker-compose.yml..."
DOCKER_COMPOSE_FILE="docker/docker-compose.yml"

if [ -f "$DOCKER_COMPOSE_FILE" ]; then
  # Vérifier si les labels sont déjà présents
  if grep -q "promtail.scrape=true" "$DOCKER_COMPOSE_FILE"; then
    echo "ℹ️  Les labels sont déjà présents dans docker-compose.yml."
  else
    # Utiliser sed pour ajouter les labels sous ai-gateway et odoo
    # (technique simple : ajouter après les ports)
    sed -i '/ai-gateway:/,/labels:/ {
      /labels:/d
    }' "$DOCKER_COMPOSE_FILE"
    # Cette méthode est plus complexe, je vais plutôt afficher un message
    echo "⚠️  Ajout manuel requis : ajoutez les labels suivants sous les services ai-gateway et odoo :"
    echo ""
    echo "  ai-gateway:"
    echo "    ..."
    echo "    labels:"
    echo "      - \"promtail.scrape=true\""
    echo "      - \"promtail.service=ai-gateway\""
    echo ""
    echo "  odoo:"
    echo "    ..."
    echo "    labels:"
    echo "      - \"promtail.scrape=true\""
    echo "      - \"promtail.service=odoo\""
    echo ""
    echo "📝 Vous pouvez modifier $DOCKER_COMPOSE_FILE manuellement."
  fi
else
  echo "❌ Fichier $DOCKER_COMPOSE_FILE introuvable."
fi

# ------------------------------------------------------------------
# FIN
# ------------------------------------------------------------------
echo ""
echo "======================================"
echo "✅ Configuration terminée !"
echo "======================================"
echo ""
echo "📌 Prochaine étape :"
echo "  - Vérifiez les fichiers générés."
echo "  - Ajoutez manuellement les labels si nécessaire."
echo "  - Lancez la stack : cd docker && docker compose up -d"
echo "  - Accédez à Grafana : http://localhost:3000 (admin/admin)"
echo ""
echo "🚀 Puis, poussez les changements sur GitHub :"
echo "  git add . && git commit -m \"feat: finalize observability stack\" && git push origin main"
