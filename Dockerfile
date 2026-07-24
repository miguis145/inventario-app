# =====================================================
# ETAPA 1: INSTALAR DEPENDENCIAS Y EJECUTAR PRUEBAS
# =====================================================
FROM node:24-alpine3.24 AS test

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar primero los archivos de dependencias
COPY package*.json ./

# Instalar exactamente las versiones del package-lock.json
RUN npm ci

# Copiar el código, las pruebas y la interfaz
COPY server.js db.js server.test.js ./
COPY public ./public

# Si las pruebas fallan, el build se detiene
RUN npm test


# =====================================================
# ETAPA 2: IMAGEN FINAL DE PRODUCCIÓN
# =====================================================
FROM node:24-alpine3.24 AS production

WORKDIR /app

# Variables predeterminadas
ENV NODE_ENV=production
ENV PORT=3000

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias de producción y eliminar npm
RUN npm ci --omit=dev \
    && npm cache clean --force \
    && rm -rf /usr/local/lib/node_modules/npm \
    && rm -f /usr/local/bin/npm \
    && rm -f /usr/local/bin/npx

# Copiar solamente los archivos necesarios para ejecutar la aplicación
COPY server.js db.js ./
COPY public ./public

# Crear carpeta para los productos
RUN mkdir -p /app/data

# Puerto utilizado por la aplicación
EXPOSE 3000

# La aplicación se ejecuta directamente con Node.js
CMD ["node", "server.js"]