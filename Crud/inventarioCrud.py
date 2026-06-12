import msvcrt
import os

class Product:
    def __init__(self, Codigo, Nombre, Precio, CantidadD, Categoria):
        self.Codigo = Codigo
        self.Nombre = Nombre
        self.Precio = Precio
        self.CantidadD = CantidadD
        self.Categoria = Categoria

    def __str__(self):
        return (
            f"| {self.Codigo:<8}"
            f'| {self.Nombre:<20}'
            f'| {self.Categoria:<15}'
            f'| ${self.Precio:>9.2f}'
            f'| {self.CantidadD:>8} |'
        )

class Inventario:
    def __init__(self):
        self.Opciones = ["Crear producto", "Mostrar productos", "Buscar producto", "Actualizar productos", "Eliminar producto", "Calcular valor total", "Crear un archivo de texto","Salir..."]
        self.OpcionesActualizar = ["Precio", "Cantidad", "Categoria", "Salir"]
        self.Productos = []
        self.OpcionActual = 0
        self.OpcionUpdateActual = 0
        self.Activo = False
        self.ActivoMain = True
        self.Carga = False
        self.CargaUpdate = False
        self.ProductoSeleccionado = None

    def Main(self):
        while self.ActivoMain:
            Opcion = self.Menu_Visual()

            if Opcion == 0:
                self.Crear_Productos()
            elif Opcion == 1:
                self.Mostrar_Productos()
            elif Opcion == 2:
                self.Buscar_Productos()
            elif Opcion == 3:
                if len(self.Productos) > 0:
                    self.Activo = True
                    self.ActivoMain = False
                    self.Menu_Update()
                else:
                    print("No hay productos para actualizar")
                    input("Presione Enter para continuar...")
            elif Opcion == 4:
                self.Eliminar_Producto()
            elif Opcion == 5:
                self.Calcular_Valor()
            elif Opcion == 6:
                self.Crear_txt()
            else:
                self.ActivoMain = False

    def Menu_Visual(self):
        while True:
            os.system("cls")
            print(
                "≣————————————————————————≣\n" \
                "|   Menu de inventario   |\n" \
                "≣————————————————————————≣" \
            )
            
            print(f"Productos en inventario: {len(self.Productos)}\n")

            for Num, Opc in enumerate(self.Opciones):
                Mostra = "◇"
                if self.OpcionActual == Num:
                    Mostra = "◆"
                print(f"{Mostra} {Opc}")

            Key = msvcrt.getch()

            if Key in (b'\x00', b'\xe0'):
                fecha = msvcrt.getch()
                if fecha == b'H':
                    self.OpcionActual = (self.OpcionActual - 1) % len(self.Opciones)
                elif fecha == b'P':
                    self.OpcionActual = (self.OpcionActual + 1) % len(self.Opciones)

            if Key == b'\r':
                return self.OpcionActual
            
    def Menu_Update(self):
        if len(self.Productos) == 0:
            print("No se encuentra ningun producto ahora mismo")
            self.Activo = False
            self.ActivoMain = True
            return

        while self.Activo:
            Opcion = self.Modificar_Visual()

            if Opcion == 0:
                self.Actualizar_Precio()
            elif Opcion == 1:
                self.Actualizar_Cantidad()
            elif Opcion == 2:
                self.Actualizar_Categoria()
            elif Opcion == 3:
                self.ActivoMain = True
                self.Activo = False

    def Modificar_Visual(self):
        while True:
            os.system("cls")
            print(
                "≣————————————————————————≣\n" \
                "| Menu de actualizacion  |\n" \
                "≣————————————————————————≣" \
            )

            for Num, opc in enumerate(self.OpcionesActualizar):
                Mostrar = "◇"
                if self.OpcionUpdateActual == Num:
                    Mostrar = "◆"
                print(f'{Mostrar} {opc}')

            Key = msvcrt.getch()

            if Key in (b'\x00', b'\xe0'):
                fecha = msvcrt.getch()
                if fecha == b'H':
                    self.OpcionUpdateActual = (self.OpcionUpdateActual - 1) % len(self.OpcionesActualizar)
                elif fecha == b'P':
                    self.OpcionUpdateActual = (self.OpcionUpdateActual + 1) % len(self.OpcionesActualizar)

            if Key == b'\r':
                return self.OpcionUpdateActual
    
    def Crear_Input(self, Type=str, Text="Ingrese un dato", Error="Dato erroneo", Verificar=str):
        while True:
            try:
                Dato = Type(input(f'{Text}: '))
                if Verificar == int:
                    if Dato < 0: 
                        raise ValueError("No se aceptan valores negativos")
                return Dato
            except ValueError as e:
                print(f"{Error}: {e}")
            
    def Crear_Productos(self):
        os.system("cls")
        print("≣————————————————————————≣")
        print("|  Crear nuevo producto  |")
        print("≣————————————————————————≣\n")
        
        Nombre = self.Crear_Input(Text="Ingrese el nombre - ej: Arroz", Error="El nombre es erroneo").lower()
        Categoria = self.Crear_Input(Text="Ingrese la categoria - ej: Alimentos", Error="La categoria es erronea").lower()
        Codigo = self.Crear_Input(Type=int, Text="Ingrese el codigo - ej: 01", Error="El codigo es erroneo", Verificar=int)
        Precio = self.Crear_Input(Type=float, Text="Ingrese el precio - ej: 1000", Error="El precio es erroneo", Verificar=int)
        CantidadD = self.Crear_Input(Type=int, Text="Ingrese la cantidad - ej: 1", Error="La cantidad es erronea", Verificar=int)

        Nuevo_Product = Product(Codigo, Nombre, Precio, CantidadD, Categoria)
        self.Productos.append(Nuevo_Product)
        print("\nProducto creado exitosamente")
        input("Presione Enter para continuar...")

    def Mostrar_Productos(self):
        os.system("cls")
        if len(self.Productos) == 0:
            print("No hay productos en el inventario")
            input("Presione Enter para continuar...")
            return

        print(
            "≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣\n" \
            "|   Id    |   Nombre            |   Categoria    |   Precio  | Cantidad |\n" \
            "≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣"
        )

        for List in self.Productos:
            print(List)

        print("≣—————————≣————————————————————≣—————————————————≣———————————≣——————————≣")
        input("Presione Enter para continuar...")

    def Buscar_Productos(self):
        os.system("cls")
        if len(self.Productos) == 0:
            print("No hay productos para buscar")
            input("Presione Enter para continuar...")
            return False
        
        Buscar = self.Crear_Input(Text="Ingrese la Id o el nombre del producto", Error="Ingrese el nombre correcto").lower()

        try:
            codigo_buscar = int(Buscar)
        except ValueError:
            codigo_buscar = None

        for Prod in self.Productos:
            if Buscar == Prod.Nombre.lower() or (codigo_buscar is not None and codigo_buscar == Prod.Codigo):
                print(
                    "\n≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣\n" \
                    "|   Id    |   Nombre            |   Categoria    |   Precio  | Cantidad |\n" \
                    "≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣"
                )
                print(Prod)
                print("≣—————————≣————————————————————≣—————————————————≣———————————≣——————————≣\n")
                self.ProductoSeleccionado = Prod
                input("Presione Enter para continuar...")
                return Prod
        
        print("El producto no existe")
        input("Presione Enter para continuar...")
        return False

    def Actualizar_Precio(self):
        os.system("cls")
        self.Mostrar_Productos_Simple()
        codigo = self.Crear_Input(Type=int, Text="Ingrese el código del producto a actualizar", Error="Código inválido", Verificar=int)
        
        for Prod in self.Productos:
            if Prod.Codigo == codigo:
                nuevo_precio = self.Crear_Input(Type=float, Text=f"Precio actual: {Prod.Precio}. Ingrese el nuevo precio", Error="Precio inválido", Verificar=int)
                Prod.Precio = nuevo_precio
                print("Precio actualizado exitosamente")
                input("Presione Enter para continuar...")
                return
        
        print("Producto no encontrado")
        input("Presione Enter para continuar...")

    def Actualizar_Cantidad(self):
        os.system("cls")
        self.Mostrar_Productos_Simple()
        codigo = self.Crear_Input(Type=int, Text="Ingrese el código del producto a actualizar", Error="Código inválido", Verificar=int)
        
        for Prod in self.Productos:
            if Prod.Codigo == codigo:
                nueva_cantidad = self.Crear_Input(Type=int, Text=f"Cantidad actual: {Prod.CantidadD}. Ingrese la nueva cantidad", Error="Cantidad inválida", Verificar=int)
                Prod.CantidadD = nueva_cantidad
                print("Cantidad actualizada exitosamente")
                input("Presione Enter para continuar...")
                return
        
        print("Producto no encontrado")
        input("Presione Enter para continuar...")

    def Actualizar_Categoria(self):
        os.system("cls")
        self.Mostrar_Productos_Simple()
        codigo = self.Crear_Input(Type=int, Text="Ingrese el código del producto a actualizar", Error="Código inválido", Verificar=int)
        
        for Prod in self.Productos:
            if Prod.Codigo == codigo:
                nueva_categoria = self.Crear_Input(Text=f"Categoría actual: {Prod.Categoria}. Ingrese la nueva categoría", Error="Categoría inválida").lower()
                Prod.Categoria = nueva_categoria
                print("✓ Categoría actualizada exitosamente")
                input("Presione Enter para continuar...")
                return
        
        print("Producto no encontrado")
        input("Presione Enter para continuar...")

    def Mostrar_Productos_Simple(self):
        if len(self.Productos) == 0:
            print("No hay productos")
            return
        
        print(
            "≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣\n" \
            "|   Id    |   Nombre            |   Categoria    |   Precio  | Cantidad |\n" \
            "≣—————————≣—————————————————————≣————————————————≣———————————≣——————————≣"
        )
        for Prod in self.Productos:
            print(Prod)
        print("≣—————————≣————————————————————≣—————————————————≣———————————≣——————————≣\n")

    def Eliminar_Producto(self):
        Opcion = self.Buscar_Productos()
        self.Productos.remove(Opcion)

    def Calcular_Valor(self):
        print(
            "≣—————————————————————≣———————————≣——————————≣———————————≣\n" \
            "|   Nombre            |   Precio  | Cantidad |   total   |\n" \
            "≣—————————————————————≣———————————≣——————————≣———————————≣"
        )

        Calculo = 0
        for product in self.Productos:
            print(
                f'| {product.Nombre:<20}'
                f'| {product.Precio:>10.2f}'
                f'| {product.CantidadD:>9}'
                f'| {(product.Precio * product.CantidadD):>9.2f} |'
                )
            Calculo += product.Precio * product.CantidadD
        print("≣—————————————————————≣———————————≣——————————≣———————————≣")
        print(f"El tota de de todo es: {Calculo}")
        input("Presione Enter para continuar...")
            
    def Crear_txt(self):
        if len(self.Productos) == 0:
            print("No hay productos para exportar")
            input("Preciona entre para continuar...")
            return
        
        with open("inventario.txt", "w", encoding="utf-8") as archivo:
            archivo.write(
                "≣————————≣—————————————————————≣————————————————≣——————————≣——————————≣\n"
            )
            archivo.write(
                "|   Id    |   Nombre            |   Categoria    |   Precio  | Cantidad |\n"
            )
            archivo.write(
                "≣————————≣—————————————————————≣————————————————≣——————————≣——————————≣\n"
            )

            for Product in self.Productos:
                archivo.write(str(Product) + "\n")

            archivo.write(
                "≣————————≣—————————————————————≣————————————————≣——————————≣——————————≣\n"
            )

            print("Inventario exportado con exito")
            input("Preciona entre para continuar...")

if __name__ == "__main__":
    InventarioCrud = Inventario()
    InventarioCrud.Main()