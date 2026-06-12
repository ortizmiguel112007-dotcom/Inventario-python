from flask import Blueprint

aprendiz_router = Blueprint('aprendiz', __name__)

# Rutas normales
# /Saludo
@aprendiz_router.route('/saludo')
def Saludar_aprendiz():
    return "Hola aprendiz ADSO"

# /Inventario
@aprendiz_router.route('/inventario')
def Inventario_aprendiz():
    return "Sistema de inventario activo"

# /Saludo
@aprendiz_router.route('/usuario')
def Usuario_aprendiz():
    return "Sistema de usuario activo"

# Rutas compartidas con <id>
@aprendiz_router.route('/producto/<id>')
def Inventario_Id_Productos(id):
    return f"inventario {id}"