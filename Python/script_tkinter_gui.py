import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple, Union

class ComponenteCPU:
    """Clase base para representar componentes del CPU"""
    def __init__(self, nombre: str, bits: int, valor_inicial: int = 0):
        self.nombre = nombre
        self.bits = bits
        self.valor = valor_inicial
    
    def actualizar(self, nuevo_valor: int):
        self.valor = nuevo_valor
    
    def obtener_valor_hex(self) -> str:
        if self.bits == 12:
            return f"0x{self.valor:03X}"
        elif self.bits == 8:
            return f"0x{self.valor:02X}"
        else:
            return f"0x{self.valor:010X}"

class SimuladorMaquinaHipotetica:
    """Simulador de la máquina hipotética basado en el HTML"""
    
    def __init__(self):
        # Inicializar registros
        self.registros = {
            'PC': ComponenteCPU('PC', 12, 0),
            'MAR': ComponenteCPU('MAR', 12, 0),
            'MBR': ComponenteCPU('MBR', 16, 0),
            'IR': ComponenteCPU('IR', 16, 0),
            'AC': ComponenteCPU('AC', 16, 0)
        }
        
        # Inicializar control
        self.control = {
            'ALU': 'INACTIVA',
            'Control': 'INACTIVA'
        }
        
        # Memoria (4096 palabras de 16 bits)
        self.memoria = [0] * 4096
        
        # Casos de prueba
        self.casos_prueba = {
            1: {
                'nombre': 'Suma Básica (5 + 10)',
                'memoria': {
                    0x100: 0x1200,  # LOAD M(0x200)
                    0x101: 0x5201,  # ADD M(0x201)
                    0x102: 0x2202,  # STOR M(0x202)
                    0x200: 5,
                    0x201: 10,
                    0x202: 0
                },
                'PC_inicial': 0x100,
                'pasos': [
                    # Fetch instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x100, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x1200, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x101, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x1200, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute LOAD
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción LOAD M(0x200)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x200, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x200) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Transferir dato de MBR a AC'},
                    
                    # Fetch next instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x101, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x5201, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x102, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x5201, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute ADD
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción ADD M(0x201)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x201, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x201) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 10, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'control': 'ALU', 'valor': 'SUMANDO', 'mensaje': 'Ciclo de ejecución - ALU realizando operación de suma'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 15, 'mensaje': 'Ciclo de ejecución - Sumar MBR (10) a AC (5) = 15'},
                    
                    # Fetch next instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x102, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x2202, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x103, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x2202, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute STOR
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción STOR M(0x202)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x202, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x202) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 15, 'mensaje': 'Ciclo de ejecución - Copiar AC (15) a MBR'},
                    {'accion': 'memoria', 'direccion': 0x202, 'valor': 15, 'mensaje': 'Ciclo de ejecución - Escribir MBR (15) en memoria (0x202)'}
                ]
            },
            2: {
                'nombre': 'Resta Básica (20 - 8)',
                'memoria': {
                    0x110: 0x1210,  # LOAD M(0x210)
                    0x111: 0x6211,  # SUB M(0x211)
                    0x112: 0x2212,  # STOR M(0x212)
                    0x210: 20,
                    0x211: 8,
                    0x212: 0
                },
                'PC_inicial': 0x110,
                'pasos': [
                    # Fetch instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x110, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x1210, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x111, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x1210, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute LOAD
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción LOAD M(0x210)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x210, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x210) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 20, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 20, 'mensaje': 'Ciclo de ejecución - Transferir dato de MBR a AC'},
                    
                    # Fetch next instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x111, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x6211, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x112, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x6211, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute SUB
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción SUB M(0x211)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x211, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x211) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 8, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'control': 'ALU', 'valor': 'RESTANDO', 'mensaje': 'Ciclo de ejecución - ALU realizando operación de resta'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 12, 'mensaje': 'Ciclo de ejecución - Restar MBR (8) de AC (20) = 12'},
                    
                    # Fetch next instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x112, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x2212, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x113, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x2212, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    
                    # Decode and execute STOR
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción STOR M(0x212)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x212, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x212) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 12, 'mensaje': 'Ciclo de ejecución - Copiar AC (12) a MBR'},
                    {'accion': 'memoria', 'direccion': 0x212, 'valor': 12, 'mensaje': 'Ciclo de ejecución - Escribir MBR (12) en memoria (0x212)'}
                ]
            },
            3: {
                'nombre': 'Suma Triple (4 + 7 + 9)',
                'memoria': {
                    0x120: 0x1220,  # LOAD M(0x220)
                    0x121: 0x5221,  # ADD M(0x221)
                    0x122: 0x5222,  # ADD M(0x222)
                    0x123: 0x2223,  # STOR M(0x223)
                    0x220: 4,
                    0x221: 7,
                    0x222: 9,
                    0x223: 0
                },
                'PC_inicial': 0x120,
                'pasos': [
                    # Fetch and execute LOAD
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x120, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x1220, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x121, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x1220, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción LOAD M(0x220)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x220, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x220) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 4, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 4, 'mensaje': 'Ciclo de ejecución - Transferir dato de MBR a AC'},
                    
                    # Fetch and execute first ADD
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x121, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x5221, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x122, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x5221, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción ADD M(0x221)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x221, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x221) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 7, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'control': 'ALU', 'valor': 'SUMANDO', 'mensaje': 'Ciclo de ejecución - ALU realizando operación de suma'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 11, 'mensaje': 'Ciclo de ejecución - Sumar MBR (7) a AC (4) = 11'},
                    
                    # Fetch and execute second ADD
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x122, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x5222, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x123, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x5222, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción ADD M(0x222)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x222, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x222) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 9, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'control': 'ALU', 'valor': 'SUMANDO', 'mensaje': 'Ciclo de ejecución - ALU realizando operación de suma'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 20, 'mensaje': 'Ciclo de ejecución - Sumar MBR (9) a AC (11) = 20'},
                    
                    # Fetch and execute STOR
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x123, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x2223, 'mensaje': 'Ciclo de captación - Leer instrucción de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x124, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x2223, 'mensaje': 'Ciclo de captación - Transferir instrucción de MBR a IR'},
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción STOR M(0x223)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0x223, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0x223) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 20, 'mensaje': 'Ciclo de ejecución - Copiar AC (20) a MBR'},
                    {'accion': 'memoria', 'direccion': 0x223, 'valor': 20, 'mensaje': 'Ciclo de ejecución - Escribir MBR (20) en memoria (0x223)'}
                ]
            }
        }
        
        self.paso_actual = 0
        self.caso_seleccionado = None
    
    def reiniciar(self):
        """Reinicia el simulador al estado inicial"""
        for registro in self.registros.values():
            registro.valor = 0
        
        self.control['ALU'] = 'INACTIVA'
        self.control['Control'] = 'INACTIVA'
        
        self.memoria = [0] * 4096
        self.paso_actual = 0
    
    def cargar_caso_prueba(self, caso: int):
        """Carga un caso de prueba en memoria y establece el PC inicial"""
        self.reiniciar()
        
        if caso not in self.casos_prueba:
            return False
        
        self.caso_seleccionado = caso
        caso_prueba = self.casos_prueba[caso]
        
        # Cargar memoria
        for direccion, valor in caso_prueba['memoria'].items():
            self.memoria[direccion] = valor
        
        # Establecer PC inicial
        self.registros['PC'].valor = caso_prueba['PC_inicial']
        
        return True
    
    def ejecutar_paso(self):
        """Ejecuta un paso de la simulación"""
        if not self.caso_seleccionado or self.paso_actual >= len(self.casos_prueba[self.caso_seleccionado]['pasos']):
            return False
        
        paso = self.casos_prueba[self.caso_seleccionado]['pasos'][self.paso_actual]
        
        # Ejecutar la acción del paso
        if paso['accion'] == 'actualizar':
            if 'registro' in paso:
                self.registros[paso['registro']].actualizar(paso['valor'])
            elif 'control' in paso:
                self.control[paso['control']] = paso['valor']
        elif paso['accion'] == 'memoria':
            self.memoria[paso['direccion']] = paso['valor']
        
        self.paso_actual += 1
        return True
    
    def obtener_mensaje_actual(self) -> str:
        """Obtiene el mensaje del paso actual"""
        if not self.caso_seleccionado or self.paso_actual == 0:
            return "Esperando inicio de ejecución..."
        
        if self.paso_actual > len(self.casos_prueba[self.caso_seleccionado]['pasos']):
            return "Ejecución completada."
        
        paso = self.casos_prueba[self.caso_seleccionado]['pasos'][self.paso_actual - 1]
        return f"Paso {self.paso_actual}: {paso['mensaje']}"

class SimuladorGUI:
    """Interfaz gráfica para el simulador"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Arquitectura de Computadores")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Configurar estilo
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.configurar_estilo()
        
        # Inicializar simulador
        self.simulador = SimuladorMaquinaHipotetica()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar primer caso por defecto
        self.cambiar_caso("1")
    
    def configurar_estilo(self):
        """Configura el estilo de los widgets"""
        self.estilo.configure('TFrame', background='#2d2d2d')
        self.estilo.configure('TLabel', background='#2d2d2d', foreground='#ffffff')
        self.estilo.configure('TButton', background='#3c3c3c', foreground='#ffffff')
        self.estilo.map('TButton', background=[('active', '#4a4a4a')])
        self.estilo.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        self.estilo.configure('Registro.TLabel', font=('Courier', 10))
        self.estilo.configure('Valor.TLabel', font=('Courier', 10, 'bold'))
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel superior - Selección de caso
        self.crear_panel_seleccion(main_frame)
        
        # Panel central - Componentes del CPU
        self.crear_panel_componentes(main_frame)
        
        # Panel inferior - Controles y mensajes
        self.crear_panel_controles(main_frame)
    
    def crear_panel_seleccion(self, parent):
        """Crea el panel de selección de caso de prueba"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(frame, text="Simulador de Máquina Hipotética", style='Header.TLabel').pack(side=tk.LEFT, padx=10)
        
        ttk.Label(frame, text="Caso de prueba:").pack(side=tk.LEFT, padx=(20, 5))
        
        self.caso_var = tk.StringVar(value="1")
        casos_combo = ttk.Combobox(frame, textvariable=self.caso_var, values=["1", "2", "3"], width=15, state="readonly")
        casos_combo.pack(side=tk.LEFT, padx=5)
        casos_combo.bind("<<ComboboxSelected>>", self.cambiar_caso)
        
        self.nombre_caso_label = ttk.Label(frame, text="")
        self.nombre_caso_label.pack(side=tk.LEFT, padx=10)
    
    def crear_panel_componentes(self, parent):
        """Crea el panel con los componentes del CPU"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Registros
        self.crear_panel_registros(frame)
        
        # Panel central - Unidades de control
        self.crear_panel_control(frame)
        
        # Panel derecho - Memoria
        self.crear_panel_memoria(frame)
    
    def crear_panel_registros(self, parent):
        """Crea el panel de registros"""
        frame = ttk.LabelFrame(parent, text="Registros", padding=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Crear widgets para cada registro
        self.registro_widgets = {}
        
        for nombre, registro in self.simulador.registros.items():
            reg_frame = ttk.Frame(frame)
            reg_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(reg_frame, text=f"{nombre}:", width=5).pack(side=tk.LEFT)
            
            valor_label = ttk.Label(reg_frame, text="", style='Valor.TLabel', width=10)
            valor_label.pack(side=tk.LEFT, padx=(5, 10))
            
            ttk.Label(reg_frame, text=f"{registro.bits} bits", foreground='#888888').pack(side=tk.LEFT)
            
            self.registro_widgets[nombre] = valor_label
    
    def crear_panel_control(self, parent):
        """Crea el panel de unidades de control"""
        frame = ttk.LabelFrame(parent, text="Unidades de Control", padding=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Crear widgets para cada unidad de control
        self.control_widgets = {}
        
        for nombre, estado in self.simulador.control.items():
            ctrl_frame = ttk.Frame(frame)
            ctrl_frame.pack(fill=tk.X, pady=10)
            
            ttk.Label(ctrl_frame, text=f"{nombre}:", width=8).pack(side=tk.LEFT)
            
            estado_label = ttk.Label(ctrl_frame, text="", style='Valor.TLabel', width=15)
            estado_label.pack(side=tk.LEFT, padx=(5, 0))
            
            self.control_widgets[nombre] = estado_label
    
    def crear_panel_memoria(self, parent):
        """Crea el panel de memoria"""
        frame = ttk.LabelFrame(parent, text="Memoria Relevante", padding=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Crear treeview para mostrar memoria
        columns = ('direccion', 'valor', 'tipo')
        self.memoria_tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.memoria_tree.heading('direccion', text='Dirección')
        self.memoria_tree.heading('valor', text='Valor')
        self.memoria_tree.heading('tipo', text='Tipo')
        
        self.memoria_tree.column('direccion', width=80)
        self.memoria_tree.column('valor', width=200)
        self.memoria_tree.column('tipo', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.memoria_tree.yview)
        self.memoria_tree.configure(yscrollcommand=scrollbar.set)
        
        self.memoria_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def crear_panel_controles(self, parent):
        """Crea el panel de controles y mensajes"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(10, 0))
        
        # Panel de botones
        botones_frame = ttk.Frame(frame)
        botones_frame.pack(side=tk.LEFT, fill=tk.X)
        
        self.siguiente_btn = ttk.Button(botones_frame, text="Siguiente Paso", command=self.siguiente_paso)
        self.siguiente_btn.pack(side=tk.LEFT, padx=5)
        
        self.reiniciar_btn = ttk.Button(botones_frame, text="Reiniciar", command=self.reiniciar_simulacion)
        self.reiniciar_btn.pack(side=tk.LEFT, padx=5)
        
        # Panel de mensajes
        mensaje_frame = ttk.LabelFrame(frame, text="Mensaje Actual", padding=10)
        mensaje_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        self.mensaje_label = ttk.Label(mensaje_frame, text="", wraplength=600)
        self.mensaje_label.pack(fill=tk.BOTH)
    
    def cambiar_caso(self, event):
        """Cambia el caso de prueba seleccionado"""
        caso = int(self.caso_var.get())
        if self.simulador.cargar_caso_prueba(caso):
            nombre = self.simulador.casos_prueba[caso]['nombre']
            self.nombre_caso_label.config(text=nombre)
            self.actualizar_interfaz()
    
    def siguiente_paso(self):
        """Ejecuta el siguiente paso de la simulación"""
        if self.simulador.ejecutar_paso():
            self.actualizar_interfaz()
        else:
            messagebox.showinfo("Simulación", "La simulación ha finalizado.")
    
    def reiniciar_simulacion(self):
        """Reinicia la simulación actual"""
        caso = int(self.caso_var.get())
        self.simulador.cargar_caso_prueba(caso)
        self.actualizar_interfaz()
    
    def actualizar_interfaz(self):
        """Actualiza todos los widgets con los valores actuales"""
        # Actualizar registros
        for nombre, widget in self.registro_widgets.items():
            valor = self.simulador.registros[nombre].obtener_valor_hex()
            widget.config(text=valor)
        
        # Actualizar unidades de control
        for nombre, widget in self.control_widgets.items():
            estado = self.simulador.control[nombre]
            color = '#4CAF50' if estado != 'INACTIVA' else '#ffffff'
            widget.config(text=estado, foreground=color)
        
        # Actualizar memoria
        self.actualizar_memoria()
        
        # Actualizar mensaje
        mensaje = self.simulador.obtener_mensaje_actual()
        self.mensaje_label.config(text=mensaje)
        
        # Actualizar estado de botones
        if self.simulador.paso_actual > len(self.simulador.casos_prueba[self.simulador.caso_seleccionado]['pasos']):
            self.siguiente_btn.config(state='disabled')
        else:
            self.siguiente_btn.config(state='normal')
    
    def actualizar_memoria(self):
        """Actualiza la visualización de la memoria"""
        # Limpiar treeview
        for item in self.memoria_tree.get_children():
            self.memoria_tree.delete(item)
        
        if not self.simulador.caso_seleccionado:
            return
        
        caso_prueba = self.simulador.casos_prueba[self.simulador.caso_seleccionado]
        direcciones = sorted(caso_prueba['memoria'].keys())
        
        for direccion in direcciones:
            valor = self.simulador.memoria[direccion]
            
            # Determinar si es una instrucción o un dato
            if direccion < 0x200:  # Heurística simple: las instrucciones están en direcciones bajas
                opcode = (valor >> 12) & 0xF
                addr = valor & 0xFFF
                
                # Mapeo de códigos de operación a nombres
                opcodes = {
                    0x1: "LOAD",
                    0x2: "STOR",
                    0x3: "LOADIO",
                    0x4: "STORIO",
                    0x5: "ADD",
                    0x6: "SUB",
                    0x7: "JUMP",
                    0x8: "JNEG",
                    0x9: "JPOS",
                    0xA: "JZERO"
                }
                op_name = opcodes.get(opcode, "???")
                valor_str = f"{op_name} M(0x{addr:03X})"
                tipo = "Instrucción"
            else:
                valor_str = str(valor)
                tipo = "Dato"
            
            # Insertar en treeview
            self.memoria_tree.insert('', 'end', values=(
                f"0x{direccion:03X}",
                valor_str,
                tipo
            ))

def main():
    """Función principal"""
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()