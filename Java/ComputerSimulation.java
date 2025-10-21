import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class ComputerSimulation {

    // Clase base para las simulaciones
    static abstract class ComputerSimulationBase {
        protected Map<String, Integer> registers;
        protected int[] memory;
        protected Map<String, String> controlUnits;
        protected int currentStep;
        protected boolean isRunning;
        protected String[] steps;
        protected Map<String, String> instructionSet;
        protected Scanner scanner;

        public ComputerSimulationBase() {
            registers = new HashMap<>();
            controlUnits = new HashMap<>();
            currentStep = 0;
            isRunning = false;
            scanner = new Scanner(System.in);
        }

        public abstract void initialize();
        public abstract void executeStep();
        public abstract void displayState();
        public abstract String[] getTestCases();

        public void runSimulation(int testCaseIndex) {
            initialize();
            loadTestCase(testCaseIndex);
            isRunning = true;

            try {
                while (isRunning && currentStep < steps.length) {
                    System.out.print("\033[H\033[2J"); // Limpiar consola
                    System.out.flush();

                    displayState();

                    // Mostrar instrucciones para el usuario
                    System.out.println("===============================================");
                    System.out.println("Presione ENTER para continuar al siguiente paso");
                    System.out.println("Presione 'q' y ENTER para salir de la simulación");
                    System.out.println("===============================================");

                    // Esperar a que el usuario presione una tecla
                    String input = scanner.nextLine();
                    if (input.equalsIgnoreCase("q")) {
                        System.out.println("Simulación interrumpida por el usuario.");
                        break;
                    }

                    executeStep();
                    currentStep++;
                }

                if (currentStep >= steps.length) {
                    System.out.println("Simulación completada.");
                    System.out.println("Presione ENTER para continuar...");
                    scanner.nextLine();
                }
            } catch (Exception e) {
                System.out.println("Error en la simulación: " + e.getMessage());
                e.printStackTrace();
                System.out.println("Presione ENTER para continuar...");
                scanner.nextLine();
            }
        }

        protected abstract void loadTestCase(int testCaseIndex);

        public void closeScanner() {
            if (scanner != null) {
                scanner.close();
            }
        }
    }

    // Simulación de la Máquina Hipotética
    static class HypotheticalMachineSimulation extends ComputerSimulationBase {
        public HypotheticalMachineSimulation() {
            super();
            instructionSet = new HashMap<>();
            instructionSet.put("0001", "LOAD");
            instructionSet.put("0010", "STOR");
            instructionSet.put("0011", "LOADIO");
            instructionSet.put("0100", "STORIO");
            instructionSet.put("0101", "ADD");
            instructionSet.put("0110", "SUB");
            instructionSet.put("0111", "JUMP");
            instructionSet.put("1000", "JNEG");
            instructionSet.put("1001", "JPOS");
            instructionSet.put("1010", "JZERO");
        }

        @Override
        public void initialize() {
            memory = new int[4096];
            registers.put("PC", 0);
            registers.put("MAR", 0);
            registers.put("MBR", 0);
            registers.put("IR", 0);
            registers.put("AC", 0);

            controlUnits.put("ALU", "INACTIVA");
            controlUnits.put("Control", "INACTIVA");
        }

        @Override
        public void loadTestCase(int testCaseIndex) {
            // Reiniciar memoria y registros
            for (int i = 0; i < memory.length; i++) {
                memory[i] = 0;
            }

            registers.put("PC", 0);
            registers.put("MAR", 0);
            registers.put("MBR", 0);
            registers.put("IR", 0);
            registers.put("AC", 0);

            controlUnits.put("ALU", "INACTIVA");
            controlUnits.put("Control", "INACTIVA");

            // Cargar caso de prueba
            switch (testCaseIndex) {
                case 1: // Suma Básica (5 + 10)
                    memory[0x100] = 0x1200; // LOAD M(0x200)
                    memory[0x101] = 0x5201; // ADD M(0x201)
                    memory[0x102] = 0x2202; // STOR M(0x202)
                    memory[0x200] = 5;
                    memory[0x201] = 10;
                    memory[0x202] = 0;
                    registers.put("PC", 0x100);

                    steps = new String[] {
                            "Ciclo de captación - PC contiene la dirección de la instrucción",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(0x200)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x200) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción ADD M(0x201)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x201) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de suma",
                            "Ciclo de ejecución - Sumar MBR (10) a AC (5) = 15",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(0x202)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x202) y colocar en MAR",
                            "Ciclo de ejecución - Copiar AC (15) a MBR",
                            "Ciclo de ejecución - Escribir MBR (15) en memoria (0x202)"
                    };
                    break;

                case 2: // Resta Básica (20 - 8)
                    memory[0x110] = 0x1210; // LOAD M(0x210)
                    memory[0x111] = 0x6211; // SUB M(0x211)
                    memory[0x112] = 0x2212; // STOR M(0x212)
                    memory[0x210] = 20;
                    memory[0x211] = 8;
                    memory[0x212] = 0;
                    registers.put("PC", 0x110);

                    steps = new String[] {
                            "Ciclo de captación - PC contiene la dirección de la instrucción",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(0x210)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x210) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción SUB M(0x211)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x211) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de resta",
                            "Ciclo de ejecución - Restar MBR (8) de AC (20) = 12",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(0x212)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x212) y colocar en MAR",
                            "Ciclo de ejecución - Copiar AC (12) a MBR",
                            "Ciclo de ejecución - Escribir MBR (12) en memoria (0x212)"
                    };
                    break;

                case 3: // Suma Triple (4 + 7 + 9)
                    memory[0x120] = 0x1220; // LOAD M(0x220)
                    memory[0x121] = 0x5221; // ADD M(0x221)
                    memory[0x122] = 0x5222; // ADD M(0x222)
                    memory[0x123] = 0x2223; // STOR M(0x223)
                    memory[0x220] = 4;
                    memory[0x221] = 7;
                    memory[0x222] = 9;
                    memory[0x223] = 0;
                    registers.put("PC", 0x120);

                    steps = new String[] {
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(0x220)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x220) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción ADD M(0x221)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x221) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de suma",
                            "Ciclo de ejecución - Sumar MBR (7) a AC (4) = 11",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción ADD M(0x222)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x222) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de suma",
                            "Ciclo de ejecución - Sumar MBR (9) a AC (11) = 20",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer instrucción de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción de MBR a IR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(0x223)",
                            "Ciclo de ejecución - Extraer dirección del operando (0x223) y colocar en MAR",
                            "Ciclo de ejecución - Copiar AC (20) a MBR",
                            "Ciclo de ejecución - Escribir MBR (20) en memoria (0x223)"
                    };
                    break;

                default:
                    System.out.println("Caso de prueba no válido.");
                    isRunning = false;
                    break;
            }
        }

        @Override
        public void executeStep() {
            if (currentStep >= steps.length) {
                isRunning = false;
                return;
            }

            String step = steps[currentStep];

            // Ejecutar la acción correspondiente al paso actual
            if (step.contains("Copiar PC a MAR")) {
                registers.put("MAR", registers.get("PC"));
            } else if (step.contains("Leer instrucción de memoria a MBR")) {
                registers.put("MBR", memory[registers.get("MAR")]);
            } else if (step.contains("Incrementar PC")) {
                registers.put("PC", registers.get("PC") + 1);
            } else if (step.contains("Transferir instrucción de MBR a IR")) {
                registers.put("IR", registers.get("MBR"));
            } else if (step.contains("Decodificar instrucción")) {
                controlUnits.put("Control", "DECODIFICANDO");
            } else if (step.contains("Extraer dirección del operando")) {
                int address = registers.get("IR") & 0xFFF;
                registers.put("MAR", address);
            } else if (step.contains("Leer dato de memoria a MBR")) {
                registers.put("MBR", memory[registers.get("MAR")]);
            } else if (step.contains("Transferir dato de MBR a AC")) {
                registers.put("AC", registers.get("MBR"));
            } else if (step.contains("ALU realizando operación de suma")) {
                controlUnits.put("ALU", "SUMANDO");
            } else if (step.contains("ALU realizando operación de resta")) {
                controlUnits.put("ALU", "RESTANDO");
            } else if (step.contains("Sumar MBR")) {
                // Extraer valores de la descripción del paso
                int mbrValue = extractValue(step, "MBR");
                int acValue = extractValue(step, "AC");
                int result = extractResult(step);
                registers.put("AC", result);
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Restar MBR")) {
                // Extraer valores de la descripción del paso
                int mbrValue = extractValue(step, "MBR");
                int acValue = extractValue(step, "AC");
                int result = extractResult(step);
                registers.put("AC", result);
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Copiar AC")) {
                int acValue = extractValue(step, "AC");
                registers.put("MBR", acValue);
            } else if (step.contains("Escribir MBR")) {
                int mbrValue = extractValue(step, "MBR");
                int address = extractAddress(step);
                memory[address] = mbrValue;
            }

            // Restablecer unidades de control si es necesario
            if (currentStep < steps.length - 1 && !steps[currentStep + 1].contains("ALU") && !steps[currentStep + 1].contains("Decodificar")) {
                controlUnits.put("Control", "INACTIVA");
            }
        }

        // Método auxiliar para extraer valores numéricos de las descripciones de pasos
        private int extractValue(String step, String register) {
            try {
                int startIndex = step.indexOf(register) + register.length() + 2;
                int endIndex = step.indexOf(')', startIndex);
                String valueStr = step.substring(startIndex, endIndex);
                return Integer.parseInt(valueStr);
            } catch (Exception e) {
                // Si hay un error al extraer el valor, devolver 0
                return 0;
            }
        }

        // Método auxiliar para extraer el resultado de una operación
        private int extractResult(String step) {
            try {
                int startIndex = step.indexOf('=') + 2;
                return Integer.parseInt(step.substring(startIndex));
            } catch (Exception e) {
                // Si hay un error al extraer el resultado, devolver 0
                return 0;
            }
        }

        // Método auxiliar para extraer una dirección de memoria
        private int extractAddress(String step) {
            try {
                int startIndex = step.indexOf('(') + 1;
                int endIndex = step.indexOf(')', startIndex);
                String addressStr = step.substring(startIndex, endIndex);
                if (addressStr.startsWith("0x")) {
                    return Integer.parseInt(addressStr.substring(2), 16);
                } else {
                    return Integer.parseInt(addressStr);
                }
            } catch (Exception e) {
                // Si hay un error al extraer la dirección, devolver 0
                return 0;
            }
        }

        @Override
        public void displayState() {
            System.out.println("===============================================");
            System.out.println("         MÁQUINA HIPOTÉTICA");
            System.out.println("===============================================");
            System.out.println("Paso actual: " + (currentStep + 1) + "/" + steps.length);
            System.out.println("Acción: " + steps[currentStep]);
            System.out.println();

            // Mostrar registros
            System.out.println("REGISTROS:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-8s %-12s %-10s%n", "Registro", "Valor", "Bits");
            System.out.printf("%-8s 0x%03X        12 bits%n", "PC", registers.get("PC"));
            System.out.printf("%-8s 0x%03X        12 bits%n", "MAR", registers.get("MAR"));
            System.out.printf("%-8s 0x%04X       16 bits%n", "MBR", registers.get("MBR"));
            System.out.printf("%-8s 0x%04X       16 bits%n", "IR", registers.get("IR"));
            System.out.printf("%-8s 0x%04X       16 bits%n", "AC", registers.get("AC"));
            System.out.println();

            // Mostrar unidades de control
            System.out.println("UNIDADES DE CONTROL:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-15s %-15s%n", "Unidad", "Estado");
            System.out.printf("%-15s %-15s%n", "ALU", controlUnits.get("ALU"));
            System.out.printf("%-15s %-15s%n", "Control", controlUnits.get("Control"));
            System.out.println();

            // Mostrar memoria relevante
            System.out.println("MEMORIA RELEVANTE:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-8s %-12s %-15s%n", "Dirección", "Valor", "Contenido");

            // Mostrar instrucciones
            for (int i = 0x100; i <= 0x123; i++) {
                if (memory[i] != 0) {
                    int value = memory[i];
                    String content = "";

                    if (i < 0x200) { // Es una instrucción
                        int opcode = (value >> 12) & 0xF;
                        int address = value & 0xFFF;
                        String opcodeStr = String.format("%04X", opcode);
                        content = instructionSet.getOrDefault(opcodeStr, "???") + " M(0x" + Integer.toHexString(address).toUpperCase() + ")";
                    } else { // Es un dato
                        content = Integer.toString(value);
                    }

                    System.out.printf("0x%03X    0x%04X       %-15s%n", i, value, content);
                }
            }

            // Mostrar datos
            for (int i = 0x200; i <= 0x223; i++) {
                if (memory[i] != 0) {
                    System.out.printf("0x%03X    0x%04X       %-15s%n", i, memory[i], memory[i]);
                }
            }

            System.out.println();
        }

        @Override
        public String[] getTestCases() {
            return new String[] {
                    "1. Suma Básica (5 + 10)",
                    "2. Resta Básica (20 - 8)",
                    "3. Suma Triple (4 + 7 + 9)"
            };
        }
    }

    // Simulación del Computador IAS
    static class IASSimulation extends ComputerSimulationBase {
        public IASSimulation() {
            super();
            instructionSet = new HashMap<>();
            instructionSet.put("00000001", "LOAD M(X)");
            instructionSet.put("00000010", "LOAD -M(X)");
            instructionSet.put("00000011", "LOAD |M(X)|");
            instructionSet.put("00000100", "LOAD -|M(X)|");
            instructionSet.put("00000101", "STOR M(X)");
            instructionSet.put("00000110", "JUMP M(X,0:19)");
            instructionSet.put("00000111", "JUMP M(X,20:39)");
            instructionSet.put("00001000", "JUMP+ M(X,0:19)");
            instructionSet.put("00001001", "JUMP+ M(X,20:39)");
            instructionSet.put("00001010", "ADD M(X)");
            instructionSet.put("00001011", "ADD |M(X)|");
            instructionSet.put("00001100", "SUB M(X)");
            instructionSet.put("00001101", "SUB |M(X)|");
            instructionSet.put("00001110", "MUL M(X)");
            instructionSet.put("00001111", "DIV M(X)");
            instructionSet.put("00010000", "LSH");
            instructionSet.put("00010001", "RSH");
            instructionSet.put("00010010", "STOR M(X,8:19)");
        }

        @Override
        public void initialize() {
            memory = new int[1000];
            registers.put("PC", 0);
            registers.put("MAR", 0);
            registers.put("MBR", 0);
            registers.put("IR", 0);
            registers.put("IBR", 0);
            registers.put("AC", 0);
            registers.put("MQ", 0);

            controlUnits.put("ALU", "INACTIVA");
            controlUnits.put("Control", "INACTIVA");
        }

        @Override
        public void loadTestCase(int testCaseIndex) {
            // Reiniciar memoria y registros
            for (int i = 0; i < memory.length; i++) {
                memory[i] = 0;
            }

            registers.put("PC", 0);
            registers.put("MAR", 0);
            registers.put("MBR", 0);
            registers.put("IR", 0);
            registers.put("IBR", 0);
            registers.put("AC", 0);
            registers.put("MQ", 0);

            controlUnits.put("ALU", "INACTIVA");
            controlUnits.put("Control", "INACTIVA");

            // Cargar caso de prueba
            switch (testCaseIndex) {
                case 1: // Cargar AC desde memoria, sumar otro valor y almacenar resultado
                    // Instrucciones (formato: 8 bits opcode + 12 bits dirección)
                    memory[0] = 0x010A0; // LOAD M(10)
                    memory[1] = 0x0A0A1; // ADD M(11)
                    memory[2] = 0x050A2; // STOR M(12)
                    memory[10] = 5;
                    memory[11] = 10;
                    memory[12] = 0;
                    registers.put("PC", 0);

                    steps = new String[] {
                            "Ciclo de captación - PC contiene la dirección de la instrucción",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(10)",
                            "Ciclo de ejecución - Extraer dirección del operando (10) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción ADD M(11)",
                            "Ciclo de ejecución - Extraer dirección del operando (11) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de suma",
                            "Ciclo de ejecución - Sumar MBR (10) a AC (5) = 15",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(12)",
                            "Ciclo de ejecución - Extraer dirección del operando (12) y colocar en MAR",
                            "Ciclo de ejecución - Copiar AC (15) a MBR",
                            "Ciclo de ejecución - Escribir MBR (15) en memoria (12)"
                    };
                    break;

                case 2: // Multiplicación y división
                    memory[0] = 0x010A0; // LOAD M(10)
                    memory[1] = 0x0E0A1; // MUL M(11)
                    memory[2] = 0x050A2; // STOR M(12)
                    memory[3] = 0x010A0; // LOAD M(10)
                    memory[4] = 0x0F0A1; // DIV M(11)
                    memory[5] = 0x050A3; // STOR M(13)
                    memory[10] = 20;
                    memory[11] = 4;
                    memory[12] = 0;
                    memory[13] = 0;
                    registers.put("PC", 0);

                    steps = new String[] {
                            "Ciclo de captación - PC contiene la dirección de la instrucción",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(10)",
                            "Ciclo de ejecución - Extraer dirección del operando (10) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción MUL M(11)",
                            "Ciclo de ejecución - Extraer dirección del operando (11) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de multiplicación",
                            "Ciclo de ejecución - Multiplicar AC (20) por MBR (4) = 80",
                            "Ciclo de ejecución - Almacenar parte alta en AC y parte baja en MQ",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(12)",
                            "Ciclo de ejecución - Extraer dirección del operando (12) y colocar en MAR",
                            "Ciclo de ejecución - Copiar AC (80) a MBR",
                            "Ciclo de ejecución - Escribir MBR (80) en memoria (12)",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción LOAD M(10)",
                            "Ciclo de ejecución - Extraer dirección del operando (10) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - Transferir dato de MBR a AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción DIV M(11)",
                            "Ciclo de ejecución - Extraer dirección del operando (11) y colocar en MAR",
                            "Ciclo de ejecución - Leer dato de memoria a MBR",
                            "Ciclo de ejecución - ALU realizando operación de división",
                            "Ciclo de ejecución - Dividir AC (20) por MBR (4) = 5",
                            "Ciclo de ejecución - Almacenar cociente en MQ y resto en AC",
                            "Ciclo de captación - Copiar PC a MAR",
                            "Ciclo de captación - Leer palabra de memoria a MBR",
                            "Ciclo de captación - Incrementar PC",
                            "Ciclo de captación - Transferir instrucción izquierda de MBR a IR",
                            "Ciclo de captación - Transferir instrucción derecha de MBR a IBR",
                            "Ciclo de ejecución - Decodificar instrucción STOR M(13)",
                            "Ciclo de ejecución - Extraer dirección del operando (13) y colocar en MAR",
                            "Ciclo de ejecución - Copiar MQ (5) a MBR",
                            "Ciclo de ejecución - Escribir MBR (5) en memoria (13)"
                    };
                    break;

                default:
                    System.out.println("Caso de prueba no válido.");
                    isRunning = false;
                    break;
            }
        }

        @Override
        public void executeStep() {
            if (currentStep >= steps.length) {
                isRunning = false;
                return;
            }

            String step = steps[currentStep];

            // Ejecutar la acción correspondiente al paso actual
            if (step.contains("Copiar PC a MAR")) {
                registers.put("MAR", registers.get("PC"));
            } else if (step.contains("Leer palabra de memoria a MBR")) {
                registers.put("MBR", memory[registers.get("MAR")]);
            } else if (step.contains("Incrementar PC")) {
                registers.put("PC", registers.get("PC") + 1);
            } else if (step.contains("Transferir instrucción izquierda de MBR a IR")) {
                // Extraer los 20 bits izquierdos del MBR (instrucción izquierda)
                registers.put("IR", registers.get("MBR") >> 20);
            } else if (step.contains("Transferir instrucción derecha de MBR a IBR")) {
                // Extraer los 20 bits derechos del MBR (instrucción derecha)
                registers.put("IBR", registers.get("MBR") & 0xFFFFF);
            } else if (step.contains("Decodificar instrucción")) {
                controlUnits.put("Control", "DECODIFICANDO");
            } else if (step.contains("Extraer dirección del operando")) {
                // Extraer la dirección de 12 bits del IR
                int address = registers.get("IR") & 0xFFF;
                registers.put("MAR", address);
            } else if (step.contains("Leer dato de memoria a MBR")) {
                registers.put("MBR", memory[registers.get("MAR")]);
            } else if (step.contains("Transferir dato de MBR a AC")) {
                registers.put("AC", registers.get("MBR"));
            } else if (step.contains("ALU realizando operación de suma")) {
                controlUnits.put("ALU", "SUMANDO");
            } else if (step.contains("ALU realizando operación de resta")) {
                controlUnits.put("ALU", "RESTANDO");
            } else if (step.contains("ALU realizando operación de multiplicación")) {
                controlUnits.put("ALU", "MULTIPLICANDO");
            } else if (step.contains("ALU realizando operación de división")) {
                controlUnits.put("ALU", "DIVIDIENDO");
            } else if (step.contains("Sumar MBR")) {
                // Extraer valores de la descripción del paso
                int mbrValue = extractValue(step, "MBR");
                int acValue = extractValue(step, "AC");
                int result = extractResult(step);
                registers.put("AC", result);
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Restar MBR")) {
                // Extraer valores de la descripción del paso
                int mbrValue = extractValue(step, "MBR");
                int acValue = extractValue(step, "AC");
                int result = extractResult(step);
                registers.put("AC", result);
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Multiplicar AC")) {
                // Extraer valores de la descripción del paso
                int acValue = extractValue(step, "AC");
                int mbrValue = extractValue(step, "MBR");
                int result = extractResult(step);
                registers.put("AC", result);
                registers.put("MQ", 0); // Simplificación: en IAS real, MQ contendría la parte baja
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Dividir AC")) {
                // Extraer valores de la descripción del paso
                int acValue = extractValue(step, "AC");
                int mbrValue = extractValue(step, "MBR");
                int result = extractResult(step);
                registers.put("MQ", result);
                registers.put("AC", 0); // Simplificación: en IAS real, AC contendría el resto
                controlUnits.put("ALU", "INACTIVA");
            } else if (step.contains("Copiar AC")) {
                int acValue = extractValue(step, "AC");
                registers.put("MBR", acValue);
            } else if (step.contains("Copiar MQ")) {
                int mqValue = extractValue(step, "MQ");
                registers.put("MBR", mqValue);
            } else if (step.contains("Escribir MBR")) {
                int mbrValue = extractValue(step, "MBR");
                int address = extractAddress(step);
                memory[address] = mbrValue;
            }

            // Restablecer unidades de control si es necesario
            if (currentStep < steps.length - 1 && !steps[currentStep + 1].contains("ALU") && !steps[currentStep + 1].contains("Decodificar")) {
                controlUnits.put("Control", "INACTIVA");
            }
        }

        // Método auxiliar para extraer valores numéricos de las descripciones de pasos
        private int extractValue(String step, String register) {
            try {
                int startIndex = step.indexOf(register) + register.length() + 2;
                int endIndex = step.indexOf(')', startIndex);
                String valueStr = step.substring(startIndex, endIndex);
                return Integer.parseInt(valueStr);
            } catch (Exception e) {
                // Si hay un error al extraer el valor, devolver 0
                return 0;
            }
        }

        // Método auxiliar para extraer el resultado de una operación
        private int extractResult(String step) {
            try {
                int startIndex = step.indexOf('=') + 2;
                return Integer.parseInt(step.substring(startIndex));
            } catch (Exception e) {
                // Si hay un error al extraer el resultado, devolver 0
                return 0;
            }
        }

        // Método auxiliar para extraer una dirección de memoria
        private int extractAddress(String step) {
            try {
                int startIndex = step.indexOf('(') + 1;
                int endIndex = step.indexOf(')', startIndex);
                String addressStr = step.substring(startIndex, endIndex);
                if (addressStr.startsWith("0x")) {
                    return Integer.parseInt(addressStr.substring(2), 16);
                } else {
                    return Integer.parseInt(addressStr);
                }
            } catch (Exception e) {
                // Si hay un error al extraer la dirección, devolver 0
                return 0;
            }
        }

        @Override
        public void displayState() {
            System.out.println("===============================================");
            System.out.println("         COMPUTADOR IAS");
            System.out.println("===============================================");
            System.out.println("Paso actual: " + (currentStep + 1) + "/" + steps.length);
            System.out.println("Acción: " + steps[currentStep]);
            System.out.println();

            // Mostrar registros
            System.out.println("REGISTROS:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-8s %-12s %-10s%n", "Registro", "Valor", "Bits");
            System.out.printf("%-8s 0x%03X        12 bits%n", "PC", registers.get("PC"));
            System.out.printf("%-8s 0x%03X        12 bits%n", "MAR", registers.get("MAR"));
            System.out.printf("%-8s 0x%010X    40 bits%n", "MBR", registers.get("MBR"));
            System.out.printf("%-8s 0x%05X      20 bits%n", "IR", registers.get("IR"));
            System.out.printf("%-8s 0x%05X      20 bits%n", "IBR", registers.get("IBR"));
            System.out.printf("%-8s 0x%010X    40 bits%n", "AC", registers.get("AC"));
            System.out.printf("%-8s 0x%010X    40 bits%n", "MQ", registers.get("MQ"));
            System.out.println();

            // Mostrar unidades de control
            System.out.println("UNIDADES DE CONTROL:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-15s %-15s%n", "Unidad", "Estado");
            System.out.printf("%-15s %-15s%n", "ALU", controlUnits.get("ALU"));
            System.out.printf("%-15s %-15s%n", "Control", controlUnits.get("Control"));
            System.out.println();

            // Mostrar memoria relevante
            System.out.println("MEMORIA RELEVANTE:");
            System.out.println("-----------------------------------------------");
            System.out.printf("%-8s %-12s %-15s%n", "Dirección", "Valor", "Contenido");

            // Mostrar instrucciones
            for (int i = 0; i <= 5; i++) {
                if (memory[i] != 0) {
                    int value = memory[i];
                    String content = "";

                    // Extraer instrucción izquierda (20 bits)
                    int leftInstr = value >> 20;
                    int opcode = leftInstr >> 12;
                    int address = leftInstr & 0xFFF;
                    String opcodeStr = String.format("%08X", opcode);
                    content = instructionSet.getOrDefault(opcodeStr, "???") + " M(" + address + ")";

                    System.out.printf("0x%03X    0x%010X    %-15s%n", i, value, content);
                }
            }

            // Mostrar datos
            for (int i = 10; i <= 13; i++) {
                if (memory[i] != 0) {
                    System.out.printf("0x%03X    0x%010X    %-15s%n", i, memory[i], memory[i]);
                }
            }

            System.out.println();
        }

        @Override
        public String[] getTestCases() {
            return new String[] {
                    "1. Suma Básica (5 + 10)",
                    "2. Multiplicación y División (20 * 4, 20 / 4)"
            };
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("===============================================");
        System.out.println("    SIMULACIÓN DE ARQUITECTURA DE COMPUTADORAS");
        System.out.println("===============================================");
        System.out.println();
        System.out.println("Seleccione el tipo de simulación:");
        System.out.println("1. Máquina Hipotética");
        System.out.println("2. Computador IAS");
        System.out.print("Opción: ");

        int simulationType = scanner.nextInt();

        ComputerSimulationBase simulation;

        switch (simulationType) {
            case 1:
                simulation = new HypotheticalMachineSimulation();
                break;
            case 2:
                simulation = new IASSimulation();
                break;
            default:
                System.out.println("Opción no válida.");
                scanner.close();
                return;
        }

        System.out.println();
        System.out.println("Seleccione un caso de prueba:");
        String[] testCases = simulation.getTestCases();
        for (int i = 0; i < testCases.length; i++) {
            System.out.println(testCases[i]);
        }
        System.out.print("Opción: ");

        int testCase = scanner.nextInt();
        // Consumir el salto de línea después de leer el entero
        scanner.nextLine();

        System.out.println();
        System.out.println("Iniciando simulación...");
        System.out.println("Presione ENTER para comenzar...");
        scanner.nextLine();

        simulation.runSimulation(testCase);
        simulation.closeScanner();

        scanner.close();
    }
}