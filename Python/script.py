import os
import sys
from tabulate import tabulate
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
            print(f"Error: El caso de prueba {caso} no existe.")
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
    
    def obtener_tabla_registros(self) -> List[List[str]]:
        """Genera una tabla con los valores actuales de los registros"""
        tabla = []
        for nombre, registro in self.registros.items():
            tabla.append([nombre, registro.obtener_valor_hex(), f"{registro.bits} bits"])
        return tabla
    
    def obtener_tabla_control(self) -> List[List[str]]:
        """Genera una tabla con los valores actuales de las unidades de control"""
        tabla = []
        for nombre, estado in self.control.items():
            tabla.append([nombre, estado])
        return tabla
    
    def obtener_tabla_memoria(self) -> List[List[str]]:
        """Genera una tabla con las posiciones de memoria relevantes"""
        if not self.caso_seleccionado:
            return [["No hay caso seleccionado", "", ""]]
        
        caso_prueba = self.casos_prueba[self.caso_seleccionado]
        direcciones = sorted(caso_prueba['memoria'].keys())
        
        tabla = []
        for direccion in direcciones:
            valor = self.memoria[direccion]
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
            else:
                valor_str = str(valor)
            
            tabla.append([f"0x{direccion:03X}", valor_str, "Instrucción" if direccion < 0x200 else "Dato"])
        
        return tabla
    
    def obtener_mensaje_actual(self) -> str:
        """Obtiene el mensaje del paso actual"""
        if not self.caso_seleccionado or self.paso_actual == 0:
            return "Esperando inicio de ejecución..."
        
        if self.paso_actual > len(self.casos_prueba[self.caso_seleccionado]['pasos']):
            return "Ejecución completada."
        
        paso = self.casos_prueba[self.caso_seleccionado]['pasos'][self.paso_actual - 1]
        return f"Paso {self.paso_actual}: {paso['mensaje']}"

class SimuladorIAS:
    """Simulador del computador IAS basado en el HTML y el resumen teórico"""
    
    def __init__(self):
        # Inicializar registros del IAS
        self.registros = {
            'PC': ComponenteCPU('PC', 12, 0),      # Program Counter
            'MAR': ComponenteCPU('MAR', 12, 0),    # Memory Address Register
            'MBR': ComponenteCPU('MBR', 40, 0),   # Memory Buffer Register
            'IR': ComponenteCPU('IR', 8, 0),       # Instruction Register (opcode)
            'IBR': ComponenteCPU('IBR', 20, 0),   # Instruction Buffer Register
            'AC': ComponenteCPU('AC', 40, 0),     # Accumulator
            'MQ': ComponenteCPU('MQ', 40, 0)      # Multiplier-Quotient
        }
        
        # Inicializar control
        self.control = {
            'ALU': 'INACTIVA',
            'Control': 'INACTIVA'
        }
        
        # Memoria (1000 palabras de 40 bits)
        self.memoria = [0] * 1000
        
        # Casos de prueba
        self.casos_prueba = {
            1: {
                'nombre': 'Suma Básica (5 + 10)',
                'memoria': {
                    0: 0x010FA210FB,  # LOAD M(0xFA), STOR M(0xFB)
                    1: 0x010FA0F08D,  # LOAD M(0xFA), JUMP+M(0x8D)
                    2: 0x020FA210FB,  # LOAD -M(0xFA), STOR M(0xFB)
                    0xFA: 5,
                    0xFB: 10
                },
                'PC_inicial': 0,
                'pasos': [
                    # Fetch instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x010FA210FB, 'mensaje': 'Ciclo de captación - Leer palabra de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 1, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x01, 'mensaje': 'Ciclo de captación - Extraer opcode izquierdo a IR'},
                    {'accion': 'actualizar', 'registro': 'IBR', 'valor': 0x0FA210FB, 'mensaje': 'Ciclo de captación - Extraer instrucción derecha a IBR'},
                    
                    # Decode and execute LOAD M(0xFA)
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción LOAD M(0xFA)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0xFA, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0xFA) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Transferir dato de MBR a AC'},
                    
                    # Execute right instruction (STOR M(0xFB))
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x02, 'mensaje': 'Ciclo de ejecución - Cargar opcode derecho a IR'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0xFB, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0xFB) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Copiar AC (5) a MBR'},
                    {'accion': 'memoria', 'direccion': 0xFB, 'valor': 5, 'mensaje': 'Ciclo de ejecución - Escribir MBR (5) en memoria (0xFB)'},
                    
                    # Fetch next instruction
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 1, 'mensaje': 'Ciclo de captación - Copiar PC a MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 0x010FA0F08D, 'mensaje': 'Ciclo de captación - Leer palabra de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 2, 'mensaje': 'Ciclo de captación - Incrementar PC'},
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x01, 'mensaje': 'Ciclo de captación - Extraer opcode izquierdo a IR'},
                    {'accion': 'actualizar', 'registro': 'IBR', 'valor': 0x0FA0F08D, 'mensaje': 'Ciclo de captación - Extraer instrucción derecha a IBR'},
                    
                    # Decode and execute LOAD M(0xFA)
                    {'accion': 'actualizar', 'control': 'Control', 'valor': 'DECODIFICANDO', 'mensaje': 'Ciclo de ejecución - Decodificar instrucción LOAD M(0xFA)'},
                    {'accion': 'actualizar', 'registro': 'MAR', 'valor': 0xFA, 'mensaje': 'Ciclo de ejecución - Extraer dirección del operando (0xFA) y colocar en MAR'},
                    {'accion': 'actualizar', 'registro': 'MBR', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Leer dato de memoria a MBR'},
                    {'accion': 'actualizar', 'registro': 'AC', 'valor': 5, 'mensaje': 'Ciclo de ejecución - Transferir dato de MBR a AC'},
                    
                    # Execute right instruction (JUMP+M(0x8D))
                    {'accion': 'actualizar', 'registro': 'IR', 'valor': 0x0F, 'mensaje': 'Ciclo de ejecución - Cargar opcode derecho a IR'},
                    {'accion': 'actualizar', 'registro': 'PC', 'valor': 0x8D, 'mensaje': 'Ciclo de ejecución - Saltar a dirección 0x8D si AC es positivo'}
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
        
        self.memoria = [0] * 1000
        self.paso_actual = 0
    
    def cargar_caso_prueba(self, caso: int):
        """Carga un caso de prueba en memoria y establece el PC inicial"""
        self.reiniciar()
        
        if caso not in self.casos_prueba:
            print(f"Error: El caso de prueba {caso} no existe.")
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
    
    def obtener_tabla_registros(self) -> List[List[str]]:
        """Genera una tabla con los valores actuales de los registros"""
        tabla = []
        for nombre, registro in self.registros.items():
            if nombre == 'IR':
                tabla.append([nombre, f"0x{registro.valor:02X}", f"{registro.bits} bits"])
            else:
                tabla.append([nombre, f"0x{registro.valor:010X}", f"{registro.bits} bits"])
        return tabla
    
    def obtener_tabla_control(self) -> List[List[str]]:
        """Genera una tabla con los valores actuales de las unidades de control"""
        tabla = []
        for nombre, estado in self.control.items():
            tabla.append([nombre, estado])
        return tabla
    
    def obtener_tabla_memoria(self) -> List[List[str]]:
        """Genera una tabla con las posiciones de memoria relevantes"""
        if not self.caso_seleccionado:
            return [["No hay caso seleccionado", "", ""]]
        
        caso_prueba = self.casos_prueba[self.caso_seleccionado]
        direcciones = sorted(caso_prueba['memoria'].keys())
        
        tabla = []
        for direccion in direcciones:
            valor = self.memoria[direccion]
            # Determinar si es una instrucción o un dato
            if direccion < 0x100:  # Heurística simple: las instrucciones están en direcciones bajas
                # Extraer instrucciones izquierda y derecha
                left_op = (valor >> 32) & 0xFF
                left_addr = (valor >> 20) & 0xFFF
                right_op = (valor >> 12) & 0xFF
                right_addr = valor & 0xFFF
                
                # Mapeo de códigos de operación a nombres
                opcodes = {
                    0x01: "LOAD",
                    0x02: "LOAD-",
                    0x03: "LOAD|",
                    0x04: "LOAD||",
                    0x05: "STOR",
                    0x06: "STOR-",
                    0x07: "JUMP",
                    0x08: "JUMP+",
                    0x09: "JUMP-",
                    0x0A: "ADD",
                    0x0B: "ADD|",
                    0x0C: "SUB",
                    0x0D: "SUB|",
                    0x0E: "MUL",
                    0x0F: "DIV",
                    0x10: "LSH",
                    0x11: "RSH",
                    0x12: "STOR M(X[8:19])"
                }
                
                left_op_name = opcodes.get(left_op, "???")
                right_op_name = opcodes.get(right_op, "???")
                
                valor_str = f"{left_op_name} M(0x{left_addr:03X}), {right_op_name} M(0x{right_addr:03X})"
            else:
                valor_str = str(valor)
            
            tabla.append([f"0x{direccion:03X}", valor_str, "Instrucción" if direccion < 0x100 else "Dato"])
        
        return tabla
    
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
    print("=" * 60)
    print("SIMULADOR DE ARQUITECTURA DE COMPUTADORES")
    print("=" * 60)
    print("1. Máquina Hipotética")
    print("2. Computador IAS")
    print("3. Salir")
    print("=" * 60)

def mostrar_casos_prueba(simulador, nombre_simulador):
    """Muestra los casos de prueba disponibles"""
    print(f"\nCasos de prueba disponibles para {nombre_simulador}:")
    print("-" * 40)
    for num, caso in simulador.casos_prueba.items():
        print(f"{num}. {caso['nombre']}")
    print("-" * 40)

def ejecutar_simulacion(simulador, nombre_simulador):
    """Ejecuta la simulación paso a paso con control del usuario"""
    limpiar_consola()
    print(f"SIMULACIÓN DE {nombre_simulador.upper()}")
    print("=" * 60)
    print("Instrucciones:")
    print("- Presione Enter para avanzar al siguiente paso")
    print("- Escriba 'salir' para terminar la simulación")
    print("- Escriba 'reiniciar' para reiniciar la simulación")
    print("=" * 60)
    
    while True:
        # Mostrar tablas
        print("\nREGISTROS:")
        print(tabulate(simulador.obtener_tabla_registros(), headers=["Registro", "Valor", "Bits"], tablefmt="grid"))
        
        print("\nUNIDADES DE CONTROL:")
        print(tabulate(simulador.obtener_tabla_control(), headers=["Unidad", "Estado"], tablefmt="grid"))
        
        print("\nMEMORIA RELEVANTE:")
        print(tabulate(simulador.obtener_tabla_memoria(), headers=["Dirección", "Valor", "Tipo"], tablefmt="grid"))
        
        print(f"\n{simulador.obtener_mensaje_actual()}")
        
        # Verificar si la simulación ha terminado
        if simulador.paso_actual > len(simulador.casos_prueba[simulador.caso_seleccionado]['pasos']):
            print("\n¡Simulación completada!")
            input("\nPresione Enter para continuar...")
            break
        
        # Esperar entrada del usuario
        print("\n" + "-" * 60)
        entrada = input("Presione Enter para continuar (o 'salir'/'reiniciar'): ").strip().lower()
        
        if entrada == 'salir':
            break
        elif entrada == 'reiniciar':
            simulador.cargar_caso_prueba(simulador.caso_seleccionado)
            limpiar_consola()
            print(f"SIMULACIÓN DE {nombre_simulador.upper()} (REINICIADA)")
            print("=" * 60)
            continue
        
        # Ejecutar siguiente paso
        if not simulador.ejecutar_paso():
            print("\n¡Simulación completada!")
            input("\nPresione Enter para continuar...")
            break
        
        # Limpiar consola para el siguiente paso
        limpiar_consola()
        print(f"SIMULACIÓN DE {nombre_simulador.upper()}")
        print("=" * 60)
        print("Instrucciones:")
        print("- Presione Enter para avanzar al siguiente paso")
        print("- Escriba 'salir' para terminar la simulación")
        print("- Escriba 'reiniciar' para reiniciar la simulación")
        print("=" * 60)

def main():
    """Función principal del programa"""
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            # Máquina Hipotética
            simulador = SimuladorMaquinaHipotetica()
            mostrar_casos_prueba(simulador, "Máquina Hipotética")
            
            caso = input("\nSeleccione un caso de prueba (1-3): ")
            try:
                caso = int(caso)
                if 1 <= caso <= 3:
                    simulador.cargar_caso_prueba(caso)
                    ejecutar_simulacion(simulador, "Máquina Hipotética")
                else:
                    print("Opción inválida. Intente de nuevo.")
                    input("Presione Enter para continuar...")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
                input("Presione Enter para continuar...")
        
        elif opcion == '2':
            # Computador IAS
            simulador = SimuladorIAS()
            mostrar_casos_prueba(simulador, "Computador IAS")
            
            caso = input("\nSeleccione un caso de prueba (1): ")
            try:
                caso = int(caso)
                if caso == 1:
                    simulador.cargar_caso_prueba(caso)
                    ejecutar_simulacion(simulador, "Computador IAS")
                else:
                    print("Opción inválida. Intente de nuevo.")
                    input("Presione Enter para continuar...")
            except ValueError:
                print("Entrada inválida. Intente de nuevo.")
                input("Presione Enter para continuar...")
        
        elif opcion == '3':
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción inválida. Intente de nuevo.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()