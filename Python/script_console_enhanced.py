import os
import sys
from typing import Dict, List, Tuple, Union

# Definir códigos de color ANSI
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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

def limpiar_consola():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Muestra el menú principal"""
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}SIMULADOR DE ARQUITECTURA DE COMPUTADORES{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}1. Máquina Hipotética{Colors.ENDC}")
    print(f"{Colors.OKCYAN}2. Salir{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")

def mostrar_casos_prueba(simulador):
    """Muestra los casos de prueba disponibles"""
    print(f"\n{Colors.OKBLUE}Casos de prueba disponibles:{Colors.ENDC}")
    print(f"{Colors.WARNING}{'-'*40}{Colors.ENDC}")
    for num, caso in simulador.casos_prueba.items():
        print(f"{Colors.OKGREEN}{num}. {caso['nombre']}{Colors.ENDC}")
    print(f"{Colors.WARNING}{'-'*40}{Colors.ENDC}")

def dibujar_caja(texto, ancho=60):
    """Dibuja una caja alrededor del texto"""
    linea = f"{Colors.WARNING}+{'-'*ancho}+{Colors.ENDC}"
    print(linea)
    for linea_texto in texto.split('\n'):
        print(f"{Colors.WARNING}|{Colors.ENDC} {linea_texto.ljust(ancho-2)} {Colors.WARNING}|{Colors.ENDC}")
    print(linea)

def ejecutar_simulacion(simulador):
    """Ejecuta la simulación paso a paso con control del usuario"""
    limpiar_consola()
    print(f"{Colors.BOLD}{Colors.HEADER}SIMULACIÓN DE MÁQUINA HIPOTÉTICA{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Instrucciones:{Colors.ENDC}")
    print(f"- Presione {Colors.OKGREEN}Enter{Colors.ENDC} para avanzar al siguiente paso")
    print(f"- Escriba {Colors.WARNING}'salir'{Colors.ENDC} para terminar la simulación")
    print(f"- Escriba {Colors.WARNING}'reiniciar'{Colors.ENDC} para reiniciar la simulación")
    print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
    
    while True:
        # Mostrar registros
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}REGISTROS:{Colors.ENDC}")
        registros_texto = ""
        for nombre, registro in simulador.registros.items():
            registros_texto += f"{Colors.BOLD}{nombre}:{Colors.ENDC} {Colors.OKGREEN}{registro.obtener_valor_hex()}{Colors.ENDC} ({registro.bits} bits)\n"
        dibujar_caja(registros_texto.strip())
        
        # Mostrar unidades de control
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}UNIDADES DE CONTROL:{Colors.ENDC}")
        control_texto = ""
        for nombre, estado in simulador.control.items():
            color = Colors.OKGREEN if estado != 'INACTIVA' else Colors.ENDC
            control_texto += f"{Colors.BOLD}{nombre}:{Colors.ENDC} {color}{estado}{Colors.ENDC}\n"
        dibujar_caja(control_texto.strip())
        
        # Mostrar memoria
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}MEMORIA RELEVANTE:{Colors.ENDC}")
        if simulador.caso_seleccionado:
            caso_prueba = simulador.casos_prueba[simulador.caso_seleccionado]
            direcciones = sorted(caso_prueba['memoria'].keys())
            
            memoria_texto = ""
            for direccion in direcciones:
                valor = simulador.memoria[direccion]
                
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
                
                memoria_texto += f"{Colors.BOLD}0x{direccion:03X}:{Colors.ENDC} {Colors.OKCYAN}{valor_str}{Colors.ENDC} ({tipo})\n"
            
            dibujar_caja(memoria_texto.strip())
        
        # Mostrar mensaje actual
        print(f"\n{Colors.BOLD}{Colors.OKBLUE}MENSAJE ACTUAL:{Colors.ENDC}")
        mensaje = simulador.obtener_mensaje_actual()
        color_mensaje = Colors.OKGREEN if "completada" in mensaje.lower() else Colors.OKCYAN
        dibujar_caja(f"{color_mensaje}{mensaje}{Colors.ENDC}")
        
        # Verificar si la simulación ha terminado
        if simulador.paso_actual > len(simulador.casos_prueba[simulador.caso_seleccionado]['pasos']):
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}¡Simulación completada!{Colors.ENDC}")
            input(f"\n{Colors.OKCYAN}Presione Enter para continuar...{Colors.ENDC}")
            break
        
        # Esperar entrada del usuario
        print(f"\n{Colors.WARNING}{'-'*60}{Colors.ENDC}")
        entrada = input(f"{Colors.OKCYAN}Presione Enter para continuar (o 'salir'/'reiniciar'): {Colors.ENDC}").strip().lower()
        
        if entrada == 'salir':
            break
        elif entrada == 'reiniciar':
            simulador.cargar_caso_prueba(simulador.caso_seleccionado)
            limpiar_consola()
            print(f"{Colors.BOLD}{Colors.HEADER}SIMULACIÓN DE MÁQUINA HIPOTÉTICA (REINICIADA){Colors.ENDC}")
            print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
            continue
        
        # Ejecutar siguiente paso
        if not simulador.ejecutar_paso():
            print(f"\n{Colors.OKGREEN}{Colors.BOLD}¡Simulación completada!{Colors.ENDC}")
            input(f"\n{Colors.OKCYAN}Presione Enter para continuar...{Colors.ENDC}")
            break
        
        # Limpiar consola para el siguiente paso
        limpiar_consola()
        print(f"{Colors.BOLD}{Colors.HEADER}SIMULACIÓN DE MÁQUINA HIPOTÉTICA{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}Instrucciones:{Colors.ENDC}")
        print(f"- Presione {Colors.OKGREEN}Enter{Colors.ENDC} para avanzar al siguiente paso")
        print(f"- Escriba {Colors.WARNING}'salir'{Colors.ENDC} para terminar la simulación")
        print(f"- Escriba {Colors.WARNING}'reiniciar'{Colors.ENDC} para reiniciar la simulación")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")

def main():
    """Función principal del programa"""
    while True:
        mostrar_menu()
        opcion = input(f"{Colors.OKCYAN}Seleccione una opción: {Colors.ENDC}")
        
        if opcion == '1':
            # Máquina Hipotética
            simulador = SimuladorMaquinaHipotetica()
            mostrar_casos_prueba(simulador)
            
            caso = input(f"\n{Colors.OKCYAN}Seleccione un caso de prueba (1-3): {Colors.ENDC}")
            try:
                caso = int(caso)
                if 1 <= caso <= 3:
                    simulador.cargar_caso_prueba(caso)
                    ejecutar_simulacion(simulador)
                else:
                    print(f"{Colors.FAIL}Opción inválida. Intente de nuevo.{Colors.ENDC}")
                    input(f"{Colors.OKCYAN}Presione Enter para continuar...{Colors.ENDC}")
            except ValueError:
                print(f"{Colors.FAIL}Entrada inválida. Intente de nuevo.{Colors.ENDC}")
                input(f"{Colors.OKCYAN}Presione Enter para continuar...{Colors.ENDC}")
        
        elif opcion == '2':
            print(f"{Colors.OKGREEN}¡Hasta luego!{Colors.ENDC}")
            break
        
        else:
            print(f"{Colors.FAIL}Opción inválida. Intente de nuevo.{Colors.ENDC}")
            input(f"{Colors.OKCYAN}Presione Enter para continuar...{Colors.ENDC}")

if __name__ == "__main__":
    main()