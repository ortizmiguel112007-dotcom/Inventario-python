import msvcrt
import os
import re

ROLES_VALIDOS = ["administrador", "aprendiz", "instructor"]

class Usuario:
    def __init__(self, documento, nombre, correo, rol, estado):
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.rol = rol
        self.estado = estado

    def __str__(self):
        return (
            f"| {self.documento:<12}"
            f"| {self.nombre:<20}"
            f"| {self.correo:<25}"
            f"| {self.rol:<14}"
            f"| {self.estado:>9} |"
        )


class SistemaUsuarios:
    def __init__(self):
        self.Opciones = [
            "Registrar usuario",
            "Mostrar usuarios",
            "Buscar usuario",
            "Actualizar usuario",
            "Eliminar usuario",
            "Mostrar usuarios activos",
            "Contar usuarios por rol",
            "Exportar a archivo .txt",
            "Salir..."
        ]
        self.OpcionesActualizar = ["Nombre", "Correo", "Rol", "Estado", "Volver"]
        self.usuarios = []
        self.OpcionActual = 0
        self.OpcionUpdateActual = 0
        self.Activo = False
        self.ActivoMain = True

    # ──────────────────────────────────────────────
    #  MENÚ PRINCIPAL
    # ──────────────────────────────────────────────
    def Main(self):
        while self.ActivoMain:
            opcion = self.Menu_Visual()

            if opcion == 0:
                self.registrar_usuario()
            elif opcion == 1:
                self.mostrar_usuarios()
            elif opcion == 2:
                self.buscar_usuario()
            elif opcion == 3:
                if len(self.usuarios) > 0:
                    self.Activo = True
                    self.ActivoMain = False
                    self.Menu_Update()
                else:
                    print("No hay usuarios para actualizar.")
                    input("Presione Enter para continuar...")
            elif opcion == 4:
                self.eliminar_usuario()
            elif opcion == 5:
                self.mostrar_activos()
            elif opcion == 6:
                self.contar_roles()
            elif opcion == 7:
                self.guardar_archivo()
            else:
                self.ActivoMain = False

    def Menu_Visual(self):
        while True:
            os.system("cls")
            print(
                "≣————————————————————————————≣\n"
                "|   Sistema de Usuarios      |\n"
                "≣————————————————————————————≣"
            )
            print(f"Usuarios registrados: {len(self.usuarios)}\n")

            for num, opc in enumerate(self.Opciones):
                marca = "◆" if self.OpcionActual == num else "◇"
                print(f"{marca} {opc}")

            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                flecha = msvcrt.getch()
                if flecha == b'H':
                    self.OpcionActual = (self.OpcionActual - 1) % len(self.Opciones)
                elif flecha == b'P':
                    self.OpcionActual = (self.OpcionActual + 1) % len(self.Opciones)
            if key == b'\r':
                return self.OpcionActual

    # ──────────────────────────────────────────────
    #  MENÚ ACTUALIZAR
    # ──────────────────────────────────────────────
    def Menu_Update(self):
        if len(self.usuarios) == 0:
            print("No hay usuarios registrados.")
            self.Activo = False
            self.ActivoMain = True
            return

        usuario = self._seleccionar_usuario("actualizar")
        if not usuario:
            self.Activo = False
            self.ActivoMain = True
            return

        while self.Activo:
            opcion = self.Modificar_Visual(usuario)
            if opcion == 0:
                self.actualizar_nombre(usuario)
            elif opcion == 1:
                self.actualizar_correo(usuario)
            elif opcion == 2:
                self.actualizar_rol(usuario)
            elif opcion == 3:
                self.actualizar_estado(usuario)
            else:
                self.Activo = False
                self.ActivoMain = True

    def Modificar_Visual(self, usuario):
        while True:
            os.system("cls")
            print(
                "≣————————————————————————————≣\n"
                "|   Menú de Actualización    |\n"
                "≣————————————————————————————≣"
            )
            print(f"Usuario seleccionado: {usuario.nombre} (Doc: {usuario.documento})\n")
            for num, opc in enumerate(self.OpcionesActualizar):
                marca = "◆" if self.OpcionUpdateActual == num else "◇"
                print(f"{marca} {opc}")

            key = msvcrt.getch()
            if key in (b'\x00', b'\xe0'):
                flecha = msvcrt.getch()
                if flecha == b'H':
                    self.OpcionUpdateActual = (self.OpcionUpdateActual - 1) % len(self.OpcionesActualizar)
                elif flecha == b'P':
                    self.OpcionUpdateActual = (self.OpcionUpdateActual + 1) % len(self.OpcionesActualizar)
            if key == b'\r':
                return self.OpcionUpdateActual

    # ──────────────────────────────────────────────
    #  VALIDACIONES / INPUT
    # ──────────────────────────────────────────────
    def _correo_valido(self, correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(patron, correo) is not None

    def _documento_unico(self, documento):
        return all(u.documento != documento for u in self.usuarios)

    def Crear_Input(self, Type=str, Text="Ingrese un dato", Error="Dato erróneo", Verificar=None):
        while True:
            try:
                dato = Type(input(f"{Text}: ").strip())
                if not str(dato):
                    raise ValueError("El campo no puede estar vacío.")
                if Verificar == int:
                    if dato < 0:
                        raise ValueError("No se aceptan valores negativos.")
                if Verificar == "estado":
                    if dato.lower() not in ["activo", "inactivo"]:
                        raise ValueError("Solo se acepta 'activo' o 'inactivo'.")
                if Verificar == "rol":
                    if dato.lower() not in ROLES_VALIDOS:
                        raise ValueError(f"Rol inválido. Use: {', '.join(ROLES_VALIDOS)}.")
                if Verificar == "correo":
                    if not self._correo_valido(dato):
                        raise ValueError("Correo electrónico inválido.")
                return dato
            except ValueError as e:
                print(f"  ✗ {Error}: {e}")

    def _encabezado_tabla(self):
        linea = "≣——————————————≣——————————————————————≣———————————————————————————≣————————————————≣———————————≣"
        cabecera = "|  Documento   |  Nombre              |  Correo                   |  Rol           |  Estado   |"
        print(linea)
        print(cabecera)
        print(linea)

    def _pie_tabla(self):
        print("≣——————————————≣——————————————————————≣———————————————————————————≣————————————————≣———————————≣")

    # ──────────────────────────────────────────────
    #  1. REGISTRAR USUARIO
    # ──────────────────────────────────────────────
    def registrar_usuario(self):
        os.system("cls")
        print("≣————————————————————————————≣")
        print("|    Registrar nuevo usuario |\n≣————————————————————————————≣\n")

        while True:
            doc = self.Crear_Input(Type=int, Text="Documento (número)", Error="Documento inválido", Verificar=int)
            if self._documento_unico(doc):
                break
            print("  ✗ Ese documento ya está registrado. Ingrese uno diferente.")

        nombre = self.Crear_Input(Text="Nombre completo", Error="Nombre inválido").title()

        while True:
            correo = self.Crear_Input(Text="Correo electrónico", Error="Correo inválido", Verificar="correo").lower()
            if all(u.correo != correo for u in self.usuarios):
                break
            print("  ✗ Ese correo ya está registrado.")

        rol = self.Crear_Input(
            Text=f"Rol ({'/'.join(ROLES_VALIDOS)})",
            Error="Rol inválido",
            Verificar="rol"
        ).lower()

        estado = self.Crear_Input(
            Text="Estado (activo/inactivo)",
            Error="Estado inválido",
            Verificar="estado"
        ).lower()

        nuevo = Usuario(doc, nombre, correo, rol, estado)
        self.usuarios.append(nuevo)
        print("\n  ✓ Usuario registrado correctamente.")
        input("Presione Enter para continuar...")

    # ──────────────────────────────────────────────
    #  2. MOSTRAR USUARIOS
    # ──────────────────────────────────────────────
    def mostrar_usuarios(self, lista=None, titulo="Todos los usuarios"):
        os.system("cls")
        datos = lista if lista is not None else self.usuarios
        print(f"≣————————————————————————————≣\n|  {titulo:<27}|\n≣————————————————————————————≣\n")

        if not datos:
            print("  No hay usuarios para mostrar.")
            input("Presione Enter para continuar...")
            return

        self._encabezado_tabla()
        for u in datos:
            print(u)
        self._pie_tabla()
        print(f"\n  Total: {len(datos)} usuario(s).")
        input("Presione Enter para continuar...")

    # ──────────────────────────────────────────────
    #  3. BUSCAR USUARIO
    # ──────────────────────────────────────────────
    def buscar_usuario(self):
        os.system("cls")
        print("≣————————————————————————————≣\n|      Buscar usuario        |\n≣————————————————————————————≣\n")

        if not self.usuarios:
            print("  No hay usuarios registrados.")
            input("Presione Enter para continuar...")
            return None

        criterio = input("Ingrese documento o correo electrónico: ").strip().lower()
        if not criterio:
            print("  ✗ El campo no puede estar vacío.")
            input("Presione Enter para continuar...")
            return None

        try:
            doc_buscar = int(criterio)
        except ValueError:
            doc_buscar = None

        resultado = None
        for u in self.usuarios:
            if (doc_buscar is not None and u.documento == doc_buscar) or u.correo == criterio:
                resultado = u
                break

        if resultado:
            self._encabezado_tabla()
            print(resultado)
            self._pie_tabla()
        else:
            print("  ✗ Usuario no encontrado.")

        input("Presione Enter para continuar...")
        return resultado

    # ──────────────────────────────────────────────
    #  4. ACTUALIZAR — sub-métodos
    # ──────────────────────────────────────────────
    def _seleccionar_usuario(self, accion="seleccionar"):
        os.system("cls")
        print(f"  Ingrese el documento del usuario a {accion}:")
        try:
            doc = int(input("  Documento: ").strip())
        except ValueError:
            print("  ✗ Documento inválido.")
            input("Presione Enter para continuar...")
            return None

        for u in self.usuarios:
            if u.documento == doc:
                return u

        print("  ✗ Usuario no encontrado.")
        input("Presione Enter para continuar...")
        return None

    def actualizar_nombre(self, usuario):
        os.system("cls")
        print(f"  Nombre actual: {usuario.nombre}")
        nuevo = self.Crear_Input(Text="Nuevo nombre", Error="Nombre inválido").title()
        usuario.nombre = nuevo
        print("  ✓ Nombre actualizado.")
        input("Presione Enter para continuar...")

    def actualizar_correo(self, usuario):
        os.system("cls")
        print(f"  Correo actual: {usuario.correo}")
        while True:
            nuevo = self.Crear_Input(Text="Nuevo correo", Error="Correo inválido", Verificar="correo").lower()
            if all(u.correo != nuevo or u is usuario for u in self.usuarios):
                break
            print("  ✗ Ese correo ya está en uso.")
        usuario.correo = nuevo
        print("  ✓ Correo actualizado.")
        input("Presione Enter para continuar...")

    def actualizar_rol(self, usuario):
        os.system("cls")
        print(f"  Rol actual: {usuario.rol}")
        nuevo = self.Crear_Input(
            Text=f"Nuevo rol ({'/'.join(ROLES_VALIDOS)})",
            Error="Rol inválido",
            Verificar="rol"
        ).lower()
        usuario.rol = nuevo
        print("  ✓ Rol actualizado.")
        input("Presione Enter para continuar...")

    def actualizar_estado(self, usuario):
        os.system("cls")
        print(f"  Estado actual: {usuario.estado}")
        nuevo = self.Crear_Input(
            Text="Nuevo estado (activo/inactivo)",
            Error="Estado inválido",
            Verificar="estado"
        ).lower()
        usuario.estado = nuevo
        print("  ✓ Estado actualizado.")
        input("Presione Enter para continuar...")

    # ──────────────────────────────────────────────
    #  5. ELIMINAR USUARIO
    # ──────────────────────────────────────────────
    def eliminar_usuario(self):
        os.system("cls")
        if not self.usuarios:
            print("  No hay usuarios para eliminar.")
            input("Presione Enter para continuar...")
            return

        usuario = self._seleccionar_usuario("eliminar")
        if not usuario:
            return

        self._encabezado_tabla()
        print(usuario)
        self._pie_tabla()

        confirmar = input("\n  ¿Confirma la eliminación? (s/n): ").strip().lower()
        if confirmar == "s":
            self.usuarios.remove(usuario)
            print("  ✓ Usuario eliminado correctamente.")
        else:
            print("  Operación cancelada.")
        input("Presione Enter para continuar...")

    # ──────────────────────────────────────────────
    #  6. MOSTRAR USUARIOS ACTIVOS
    # ──────────────────────────────────────────────
    def mostrar_activos(self):
        activos = [u for u in self.usuarios if u.estado == "activo"]
        self.mostrar_usuarios(lista=activos, titulo="Usuarios activos")

    # ──────────────────────────────────────────────
    #  7. CONTAR USUARIOS POR ROL
    # ──────────────────────────────────────────────
    def contar_roles(self):
        os.system("cls")
        print("≣————————————————————————————≣")
        print("|   Conteo de usuarios       |")
        print("≣————————————————————————————≣\n")

        conteo = {rol: 0 for rol in ROLES_VALIDOS}
        for u in self.usuarios:
            if u.rol in conteo:
                conteo[u.rol] += 1

        print(f"  {'Rol':<18} {'Cantidad':>8}")
        print("  " + "─" * 28)
        for rol, cantidad in conteo.items():
            print(f"  {rol.capitalize():<18} {cantidad:>8}")
        print("  " + "─" * 28)
        print(f"  {'TOTAL':<18} {sum(conteo.values()):>8}")
        input("\nPresione Enter para continuar...")

    # ──────────────────────────────────────────────
    #  8. EXPORTAR A ARCHIVO .TXT
    # ──────────────────────────────────────────────
    def guardar_archivo(self):
        if not self.usuarios:
            print("  No hay usuarios para exportar.")
            input("Presione Enter para continuar...")
            return

        nombre_archivo = "usuarios.txt"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            encabezado = (
                "≣——————————————≣——————————————————————≣———————————————————————————≣————————————————≣———————————≣\n"
                "|  Documento   |  Nombre              |  Correo                   |  Rol           |  Estado   |\n"
                "≣——————————————≣——————————————————————≣———————————————————————————≣————————————————≣———————————≣\n"
            )
            f.write(encabezado)
            for u in self.usuarios:
                f.write(str(u) + "\n")
            f.write("≣——————————————≣——————————————————————≣———————————————————————————≣————————————————≣———————————≣\n")
            f.write(f"\nTotal de usuarios: {len(self.usuarios)}\n")

            # Conteo por rol
            f.write("\nConteo por rol:\n")
            conteo = {rol: 0 for rol in ROLES_VALIDOS}
            for u in self.usuarios:
                if u.rol in conteo:
                    conteo[u.rol] += 1
            for rol, cantidad in conteo.items():
                f.write(f"  {rol.capitalize()}: {cantidad}\n")

        print(f"\n  ✓ Archivo '{nombre_archivo}' exportado exitosamente.")
        input("Presione Enter para continuar...")


if __name__ == "__main__":
    sistema = SistemaUsuarios()
    sistema.Main()