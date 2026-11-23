# Publicar Escòla (escola.efva.app)

`web/index.html` es la app completa (se regenera sola con `python3 motor/build_app.py`).

## Cloudflare Pages (gratis)
1. Cuenta gratuita en Cloudflare → Workers y Pages → Crear → Pages → Conectar con Git → repositorio `pretzhet-ink`.
2. Comando de compilación: vacío. Directorio de salida: `web`.
3. Pages → Dominios personalizados → añadir `escola.efva.app`.
4. En el DNS de `efva.app`, crear un registro CNAME `escola` → `<proyecto>.pages.dev` (Cloudflare indica el valor exacto).

Cada cambio subido a la rama principal se publica solo en unos minutos.
