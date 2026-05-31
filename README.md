# Hospital Veterinario Sally — Sistema Digital

## Instrucciones para subir a Railway

### Opción A: Subida con GitHub (recomendada)

1. Crear cuenta en GitHub (github.com) si no tiene una
2. Crear repositorio nuevo llamado `hvs-sally`
3. Subir todos los archivos de esta carpeta al repositorio
4. Ir a railway.app y crear cuenta gratuita
5. Clic en "New Project" → "Deploy from GitHub repo"
6. Seleccionar el repositorio `hvs-sally`
7. Railway detecta automáticamente la configuración y despliega
8. En 2-3 minutos obtendrá un link como: `hvs-sally.railway.app`

### Opción B: Railway CLI (más técnico)

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Variables de entorno (opcional, para mayor seguridad)

En Railway → Settings → Variables, puede agregar:
- `SECRET_KEY`: cualquier texto largo aleatorio
- `ADMIN_PASSWORD`: contraseña del administrador

### Credenciales por defecto
- Usuario: `hvs` / Contraseña: `sally2025`
- Admin: `admin` / Contraseña: `hvs2025`

⚠️ Cambie las contraseñas inmediatamente después del primer acceso
desde el Panel Admin → Seguridad.

### Acceso desde celular como app

1. Abrir el link de Railway en Chrome del celular
2. Menú (tres puntos) → "Agregar a pantalla de inicio"
3. Se instala como app nativa en el celular

### Estructura del proyecto

```
hvs_railway/
├── app.py              ← Backend Flask (servidor)
├── requirements.txt    ← Dependencias Python
├── Procfile            ← Comando de inicio para Railway
├── railway.json        ← Configuración de Railway
├── .gitignore          ← Archivos a ignorar en Git
└── static/
    ├── index.html      ← Frontend completo (toda la app)
    ├── manifest.json   ← Configuración PWA
    ├── icon-192.png    ← Ícono de la app
    └── icon-512.png    ← Ícono de la app (alta resolución)
```

### Respaldo de datos

Los datos se guardan en `hvs_data.json` en el servidor Railway.
Desde el sistema: Admin → Respaldo → Descargar Respaldo
Guarde el archivo JSON en su computadora regularmente.

### Soporte
Desarrollado con Claude (Anthropic) para Hospital Veterinario Sally.
