# Índice de capturas reales

Esta carpeta conserva las 63 capturas entregadas para la práctica. Los nombres se normalizaron para indicar el comando o resultado que aparece en cada imagen.

## Criterio de uso

- **Principal:** corresponde a la guía, es legible y puede mostrarse en el informe.
- **Complementaria:** sirve como apoyo, pero duplica otra evidencia, pertenece a una ejecución anterior o no reúne todos los comandos necesarios.
- **No usar:** puede confundir la entrega o expone información que la guía indica que no debe aparecer.

| N.º | Archivo | Sección de la guía | Clasificación | Observación |
|---:|---|---:|---|---|
| 1 | `01-dora-git-log.jpg` | 26 | Principal | Muestra `git log` con SHA, fecha y mensaje de los commits. |
| 2 | `02-dora-fecha-despliegue.jpg` | 26 | Principal | Registra la hora real con `Get-Date`. |
| 3 | `03-readiness-pods-watch.jpg` | 24 | Principal | Muestra el reinicio de Blue y la transición de pods en `kubectl get pods -w`. |
| 4 | `04-rollback-blue-version.jpg` | 22 | Principal | Comprueba selector `blue` y respuesta `v1`, `blue`. |
| 5 | `05-service-selector-blue.jpg` | 22 | Complementaria | Solo confirma el selector `blue`; la captura 4 contiene la validación completa. |
| 6 | `06-port-forward-blue-health-version.jpg` | 17 | Principal | Incluye URL local, `/health` y `/version` en Blue; también documenta un error de puerto previo. |
| 7 | `07-version-green-8081.jpg` | 21 | Principal | Comprueba `v2`, `green` en el puerto local 8081. |
| 8 | `08-github-actions-historial-4-runs.jpg` | 11 | Principal | Historial de cuatro ejecuciones, con éxitos y fallos reales. |
| 9 | `09-blue-version-repetida.jpg` | 22 | Complementaria | Repite cinco consultas a Blue y confirma que el tráfico permanece estable. |
| 10 | `10-rollout-blue-green.jpg` | 19 | Principal | Ambos deployments terminan correctamente. |
| 11 | `11-pods-blue-green-labels.jpg` | 19 | Principal | Muestra pods Blue y Green con sus etiquetas `slot`. |
| 12 | `12-pods-base-watch.jpg` | 16 | Complementaria | Evidencia antigua del deployment base; uno de los pods registra un reinicio. |
| 13 | `13-pods-blue-green-watch.jpg` | 19 | Complementaria | Confirma cuatro pods activos, pero la captura 11 muestra además las etiquetas. |
| 14 | `14-interfaz-producto-creado.jpg` | 18 | Principal | La interfaz muestra el producto añadido antes de recrear el pod. |
| 15 | `15-minikube-service-url.jpg` | 17 | Principal | Muestra el comando `minikube service ... --url` y la URL asignada. |
| 16 | `16-productos-despues-recreacion.jpg` | 18 | Principal | Consultas posteriores sin el producto agregado; evidencia la pérdida de datos locales. |
| 17 | `17-producto-antes-recreacion.jpg` | 18 | Principal | Lista el producto agregado antes de eliminar el pod. |
| 18 | `18-eliminacion-pod.jpg` | 18 | Principal | Muestra `kubectl delete pod` y la confirmación de eliminación. |
| 19 | `19-docker-pull-blue-green-sha.jpg` | 20 | Principal | Descarga correctamente las imágenes Blue y Green etiquetadas con SHA. |
| 20 | `20-kubernetes-health-products.jpg` | 17 | Principal | Comprueba `/health` y `/api/products` mediante la URL local del Service. |
| 21 | `21-interfaz-blue-v1.jpg` | 17 | Principal | Interfaz web servida por la versión Blue v1. |
| 22 | `22-service-nodeport.jpg` | 16 | Complementaria | Muestra el Service, pero la terminal está ubicada en otra carpeta de práctica. |
| 23 | `23-rollout-base.jpg` | 16 | Complementaria | Rollout correcto del deployment base desde otra carpeta de práctica. |
| 24 | `24-deployment-dos-replicas.jpg` | 16 | Complementaria | Confirma dos réplicas listas desde otra carpeta de práctica. |
| 25 | `25-pods-wide-dos-replicas.jpg` | 16 | Complementaria | Confirma dos pods en el nodo Minikube desde otra carpeta de práctica. |
| 26 | `26-rollout-base-duplicado.jpg` | 16 | Complementaria | Duplicado del rollout base. |
| 27 | `27-pods-watch-dos-replicas.jpg` | 16 | Complementaria | Duplicado parcial del estado de las dos réplicas. |
| 28 | `28-secret-metadata.jpg` | 15 | Principal | Muestra solo metadatos del Secret, sin revelar el valor. |
| 29 | `29-secret-creacion-con-valor-visible.jpg` | 15 | No usar | El comando deja visible el valor de `API_KEY`; contradice la regla de no capturar secretos. |
| 30 | `30-docker-pull-latest.jpg` | 12 | Principal | Descarga la etiqueta `latest` desde GHCR. |
| 31 | `31-ghcr-paquete-publico.jpg` | 12 | Principal | Página pública del paquete y comando de descarga. |
| 32 | `32-github-actions-dos-jobs.jpg` | 11 | Principal | Los dos jobs del pipeline aparecen correctos. |
| 33 | `33-github-actions-historial-3-runs.jpg` | 11 | Complementaria | Historial anterior; la captura 8 incluye una ejecución correcta más reciente. |
| 34 | `34-git-rev-parse-head-antiguo.jpg` | 20 | Complementaria | El SHA pertenece a un estado anterior y no coincide con las etiquetas finales Blue/Green. |
| 35 | `35-git-push-main.jpg` | 11 | Principal | Muestra el primer push a `main`, origen del disparo del workflow. |
| 36 | `36-docker-logs.jpg` | 10 | Principal | Confirma el arranque del servidor dentro del contenedor. |
| 37 | `37-local-products.jpg` | 9 | Principal | Respuesta local de `/api/products`. |
| 38 | `38-local-health.jpg` | 9 | Principal | Respuesta local `{"status":"ok"}`. |
| 39 | `39-local-version.jpg` | 9 | Principal | Respuesta local de `/version` en Blue v1. |
| 40 | `40-docker-ps.jpg` | 10 | Principal | Contenedor activo con el puerto `3000` publicado. |
| 41 | `41-docker-run.jpg` | 10 | Principal | Creación del contenedor con `docker run`. |
| 42 | `42-docker-images.jpg` | 10 | Principal | Lista la imagen local y la etiqueta `latest`. |
| 43 | `43-docker-build-antiguo-node20.jpg` | 10 | No usar | Corresponde al Dockerfile antiguo con Node 20 y no muestra la etapa de pruebas que exige la versión final. |
| 44 | `44-endpoints-otro-directorio.jpg` | 9 | No usar | Las respuestas son válidas, pero la ruta visible corresponde a otro directorio de práctica. |
| 45 | `45-estructura-antigua-repositorio.jpg` | 5 | No usar | La estructura es anterior y no incluye todos los archivos Docker/Kubernetes actuales. |
| 46 | `46-npm-test-start.jpg` | 8 y 9 | Principal | Las cinco pruebas pasan y luego inicia el servidor. |
| 47 | `47-npm-start.jpg` | 9 | Complementaria | Solo muestra el arranque; la captura 46 contiene pruebas y arranque. |
| 48 | `48-npm-ci-test-start.jpg` | 7, 8 y 9 | Principal | Muestra instalación, cinco pruebas correctas y el comando de inicio. |
| 49 | `49-dora-reinicio-green.png` | 26 | Complementaria | Evidencia un reinicio anterior de Green; no corresponde a los dos SHA del cálculo DORA final. |
| 50 | `50-dora-rollout-green-fecha.png` | 26 | Complementaria | Registra un despliegue anterior; se conserva como historial y no alimenta el cálculo final. |
| 51 | `51-versiones-herramientas.png` | 6 | Principal | Muestra las versiones reales de Node.js, npm, Git, Docker, kubectl y Minikube. |
| 52 | `52-pruebas-automaticas.png` | 8 | Principal | Las seis pruebas actuales terminan correctamente. |
| 53 | `53-docker-build-multistage.png` | 10 | Principal | El build real utiliza Node 24, ejecuta la etapa `test` y crea producción. |
| 54 | `54-docker-images.png` | 10 | Principal | Confirma la creación de `inventario-app:local`. |
| 55 | `55-docker-run-local.png` | 10 | Principal | Muestra la creación del contenedor `inventario-local`. |
| 56 | `56-docker-ps-local.png` | 10 | Principal | Confirma que el contenedor está activo y publica el puerto 3000. |
| 57 | `57-docker-logs-local.png` | 10 | Principal | Confirma el arranque del servidor dentro del contenedor. |
| 58 | `58-endpoints-contenedor-local.png` | 10 | Principal | Muestra las respuestas reales de `/health`, `/version` y `/api/products`. |
| 59 | `59-trivy-sin-critical.png` | 13 | Principal | El reporte real de Trivy muestra cero vulnerabilidades en los objetivos visibles. |
| 60 | `60-minikube-ready.png` | 14 | Principal | El nodo `ci-cd` está `Ready` y los componentes de Minikube están activos. |
| 61 | `61-readiness-pods-watch.png` | 24 | Principal | Muestra pods Blue pasando por `0/1` durante el reinicio. |
| 62 | `62-readiness-rollout-final.png` | 24 | Principal | Confirma el rollout correcto y los nuevos pods Blue en `1/1`. |
| 63 | `63-metricas-dora-reales.png` | 26 | No usar | Muestra valores DORA anteriores al despliegue de los dos SHA corregidos. |
| 64 | `64-rolling-update-final.png` | 16 y 27 | Principal | Confirma el Rolling Update final, la imagen SHA corregida y las dos réplicas disponibles. |
| 65 | `65-blue-green-activos-final.png` | 19 y 27 | Principal | Muestra los deployments base, Blue y Green disponibles y los pods etiquetados por slot. |
| 66 | `66-service-green-secret-final.png` | 15, 21 y 27 | Principal | Muestra metadatos seguros del Secret, selector `green` y respuesta `v2` con `apiKeyConfigured: true`. |
| 67 | `67-readiness-green-transicion-final.png` | 24 y 27 | Principal | Registra la transición real de los pods Green desde `0/1` hasta `1/1`. |
| 68 | `68-readiness-green-eventos-final.png` | 24 y 27 | Principal | Confirma rollout correcto y eventos de readiness HTTP `503` antes de quedar listo. |
| 69 | `69-dora-final.png` | 26 y 27 | Principal | Muestra los dos commits desplegados y el CSV con horas, lead times y resultados finales. |

## Selección recomendada para el informe

Las capturas finales recomendadas para los apartados auditados son la 64 a la 69. Las capturas anteriores se mantienen como historial y contexto, pero no deben reemplazar estas evidencias actuales.

La captura 29 se conserva únicamente porque formó parte del material recibido. No debe publicarse ni presentarse como evidencia: aunque el valor sea ficticio, enseña la credencial escrita en el comando. La ruta está incluida de forma explícita en `.gitignore` para impedir que `git add .` la incorpore al repositorio.
