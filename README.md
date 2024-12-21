# IMVU Notify

IMVU Notify es una aplicación de escritorio que te permite monitorear el estado de tus amigos en IMVU en tiempo real, con la característica única de detectar usuarios que aparecen como "Offline" pero que en realidad están conectados.

## 🌟 Características Principales

- 🔍 **Detección Avanzada de Estado**: Detecta usuarios que aparecen como "Offline" pero están activamente conectados
- 🔔 **Notificaciones en Tiempo Real**: Recibe alertas cuando tus amigos se conectan
- 🖼️ **Interfaz Moderna**: Diseño elegante y fácil de usar con tema oscuro
- 💻 **Bandeja del Sistema**: Se ejecuta discretamente en la bandeja del sistema
- 🔄 **Actualizaciones Automáticas**: Monitoreo continuo del estado de los usuarios
- 👥 **Vista de Usuarios en Línea**: Visualiza todos tus amigos conectados en una ventana dedicada

## 🛠️ Requisitos del Sistema

- Python 3.x
- Conexión a Internet
- Sistema Operativo Windows

## 📦 Dependencias

```
requests==2.31.0
Pillow==10.1.0
pygame==2.5.2
pystray
plyer==2.1.0
```

## 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/[tu-usuario]/imvu-notify.git
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tus credenciales en el archivo `config.json`:
```json
{
    "user_id": "tu_id_de_usuario",
    "osCsid": "tu_cookie_oscsid",
    "update_interval": 60
}
```

## 🎮 Uso

1. Ejecuta el archivo principal:
```bash
python imvu_notify.py
```

2. La aplicación se iniciará en la bandeja del sistema
3. Haz clic derecho en el ícono para acceder a las opciones:
   - Ver usuarios en línea
   - Configuración
   - Salir

## 📱 Panel de Usuarios en Línea

IMVU Notify incluye un panel dedicado para visualizar todos los usuarios en línea:

### Características del Panel

- **Vista en Cuadrícula**: Muestra todos los usuarios en línea en un formato de tarjetas
- **Información Detallada**: 
  - Avatar del usuario
  - Nombre de usuario
  - Estado de conexión
  - Tiempo en línea
- **Actualización en Tiempo Real**: El panel se actualiza automáticamente cada 5 segundos
- **Acceso Rápido**: 
  - Haz clic derecho en el ícono de la bandeja del sistema
  - Selecciona "Ver Usuarios en Línea"
- **Interactivo**: 
  - Haz clic en cualquier usuario para visitar su perfil
  - Interfaz moderna con efectos visuales
  - Scroll suave para navegar entre usuarios

> 💡 **Tip**: Puedes mantener el panel abierto mientras usas otras aplicaciones para monitorear fácilmente quién está en línea.

## ⚙️ Configuración

Para que la aplicación funcione correctamente, necesitas configurar dos parámetros esenciales:

### Obtención de Credenciales

1. **Cookie osCsid**:
   - Inicia sesión en tu cuenta de IMVU en el navegador
   - Abre las Herramientas de Desarrollo (F12 o Ctrl+Shift+I)
   - Ve a la pestaña "Application" o "Storage"
   - En la sección "Cookies", busca el sitio "imvu.com"
   - Encuentra y copia el valor de la cookie "osCsid"

2. **CID (Client ID)**:
   - Inicia sesión en IMVU
   - Ve a tu perfil
   - Tu CID es el número que aparece en la URL de tu perfil
   - Ejemplo: En "https://es.imvu.com/catalog/web_mypage.php?user=111111111", el CID sería "111111111111"

### Configuración en la Aplicación

1. Haz clic derecho en el ícono de IMVU Notify en la bandeja del sistema
2. Selecciona "Configuración"
3. Ingresa tu CID en el campo "ID de Usuario"
4. Ingresa el valor de osCsid en el campo correspondiente
5. Guarda la configuración

> ⚠️ **Importante**: 
> - Nunca compartas estos valores con nadie
> - La cookie osCsid expira periódicamente, si la aplicación deja de funcionar, actualiza este valor
> - Estos datos son necesarios para que la aplicación pueda detectar correctamente el estado de los usuarios

## 🔐 Privacidad y Seguridad

- Las credenciales se almacenan localmente en tu equipo
- No se comparte información con terceros
- Las solicitudes se realizan directamente a la API oficial de IMVU

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Descargo de Responsabilidad

Este proyecto no está afiliado oficialmente con IMVU. Úsalo bajo tu propia responsabilidad.
