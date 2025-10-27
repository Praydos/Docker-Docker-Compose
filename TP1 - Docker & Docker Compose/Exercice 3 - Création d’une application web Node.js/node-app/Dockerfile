# Utilisation d'une image Alpine plus légère
FROM node:18-alpine

# Installation uniquement des packages nécessaires en production
RUN apk add --no-cache curl

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de configuration
COPY package*.json ./

# Installation des dépendances PRODUCTION uniquement
RUN npm ci --only=production

# Copie du code source
COPY . .

# Création d'un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Exposition du port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Commande de démarrage
CMD ["npm", "start"]