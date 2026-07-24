# Etapa 1: instala dependencias y ejecuta las pruebas.
FROM node:20-alpine AS test

# Todos los comandos siguientes se ejecutan dentro de /app.
WORKDIR /app

# Se copian primero los archivos de dependencias para aprovechar la caché.
COPY package*.json ./

# npm ci instala exactamente las versiones registradas en package-lock.json.
RUN npm ci

# Se copia el código necesario para ejecutar las pruebas.
COPY server.js db.js server.test.js ./
COPY public ./public

# Si una prueba falla, este comando devuelve error y el build se detiene.
RUN npm test

# Etapa 2: crea una imagen final pequeña, sin archivos de pruebas.
FROM node:20-alpine AS production

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000

COPY package*.json ./

# Instala únicamente dependencias necesarias en producción.
RUN npm ci --omit=dev && npm cache clean --force

# Copia solo los archivos necesarios para ejecutar la aplicación.
COPY server.js db.js ./
COPY public ./public

# La aplicación creará products.json dentro de esta carpeta.
RUN mkdir -p data

# Documenta que el proceso escucha en el puerto 3000.
EXPOSE 3000

# Comando que se ejecuta cuando inicia el contenedor.
CMD ["node", "server.js"]
