import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.HashMap;
import java.util.Map;

public class ComputerSimulationGUI {

    // Clase base para las simulaciones
    static abstract class ComputerSimulationBase {
        protected Map<String, Integer> registers;
        protected int[] memory;
        protected Map<String, String> controlUnits;
        protected int currentStep;
        protected boolean isRunning;
        protected String[] steps;
        protected Map<String, String> instructionSet;
        protected SimulationGUI gui;

        public ComputerSimulationBase() {
            registers = new HashMap<>();
            controlUnits = new HashMap<>();
            currentStep = 0;
            isRunning = false;
            initialize(); // Inicializar en el constructor
        }

        public abstract void initialize();
        public abstract void executeStep();
        public abstract String[] getTestCases();
        public abstract String getSimulationName();

        public void setGUI(SimulationGUI gui) {
            this.gui = gui;
        }

        protected abstract void loadTestCase(int testCaseIndex);

        public void nextStep() {
            if (currentStep < steps.length) {
                executeStep();
                currentStep++;
                gui.updateDisplay();

                if (currentStep >= steps.length) {
                    gui.simulationCompleted();
                }
            }
        }

        public void reset() {
            currentStep = 0;
            isRunning = false;
            initialize();
            gui.updateDisplay();
        }

        public String getCurrentStepDescription() {
            if (currentStep < steps.length) {
                return steps[currentStep];
            }
            return "Simulación completada";
        }

        public int getTotalSteps() {
            return steps != null ? steps.length : 0;
        }

        public int getCurrentStep() {
            return currentStep;
        }

        // Método público para obtener el conjunto de instrucciones
        public Map<String, String> getInstructionSet() {
            return instructionSet;
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
        public String getSimulationName() {
            return "Máquina Hipotética";
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

            // Inicializar steps con un array vacío para evitar NullPointerException
            steps = new String[0];
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

            // Cargar caso de prueba - corregir el índice (comienza en 0)
            switch (testCaseIndex) {
                case 0: // Suma Básica (5 + 10)
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

                case 1: // Resta Básica (20 - 8)
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

                case 2: // Suma Triple (4 + 7 + 9)
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
                            "Ciclo de ejecución - Incrementar PC",
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
                    // Inicializar steps con un array vacío para evitar NullPointerException
                    steps = new String[0];
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
            instructionSet.put("00001010", "M(X)");
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
        public String getSimulationName() {
            return "Computador IAS";
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

            // Inicializar steps con un array vacío para evitar NullPointerException
            steps = new String[0];
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

            // Cargar caso de prueba - corregir el índice (comienza en 0)
            switch (testCaseIndex) {
                case 0: // Cargar AC desde memoria, sumar otro valor y almacenar resultado
                    // CORRECCIÓN: Almacenar la instrucción de 20 bits directamente (sin << 20)
                    // Usar las direcciones correctas (ej: 0x00A para 10)
                    memory[0] = 0x0100A; // LOAD M(10)
                    memory[1] = 0x0A00B; // ADD M(11)
                    memory[2] = 0x0500C; // STOR M(12)
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

                case 1: // Multiplicación y división
                    // CORRECCIÓN: Almacenar la instrucción de 20 bits directamente (sin << 20)
                    memory[0] = 0x0100A; // LOAD M(10)
                    memory[1] = 0x0E00B; // MUL M(11)
                    memory[2] = 0x0500C; // STOR M(12)
                    memory[3] = 0x0100A; // LOAD M(10)
                    memory[4] = 0x0F00B; // DIV M(11)
                    memory[5] = 0x0500D; // STOR M(13)
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
                    // Inicializar steps con un array vacío para evitar NullPointerException
                    steps = new String[0];
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
                // CORRECCIÓN: El MBR ya contiene la única instrucción (simplificación de 32 bits)
                registers.put("IR", registers.get("MBR"));
            } else if (step.contains("Transferir instrucción derecha de MBR a IBR")) {
                // CORRECCIÓN: No hay instrucción derecha en esta simulación simplificada
                registers.put("IBR", 0);
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
        public String[] getTestCases() {
            return new String[] {
                    "1. Suma Básica (5 + 10)",
                    "2. Multiplicación y División (20 * 4, 20 / 4)"
            };
        }
    }

    // Clase para la interfaz gráfica
    static class SimulationGUI extends JFrame {
        private ComputerSimulationBase simulation;
        private JLabel titleLabel;
        private JLabel stepLabel;
        private JLabel actionLabel;
        private JProgressBar progressBar;
        private JTable registersTable;
        private JTable controlUnitsTable;
        private JTable memoryTable;
        private JButton nextButton;
        private JButton resetButton;
        private JComboBox<String> simulationComboBox;
        private JComboBox<String> testCaseComboBox;
        private JButton startButton;

        public SimulationGUI() {
            setTitle("Simulación de Arquitectura de Computadoras");
            setSize(1000, 700);
            setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            setLocationRelativeTo(null);

            initComponents();
            layoutComponents();
        }

        private void initComponents() {
            // Panel superior con selección de simulación
            JPanel topPanel = new JPanel(new FlowLayout());
            topPanel.setBorder(new EmptyBorder(10, 10, 10, 10));

            simulationComboBox = new JComboBox<>(new String[]{"Máquina Hipotética", "Computador IAS"});
            testCaseComboBox = new JComboBox<>();
            startButton = new JButton("Iniciar Simulación");

            simulationComboBox.addActionListener(e -> updateTestCases());
            startButton.addActionListener(e -> startSimulation());

            topPanel.add(new JLabel("Tipo de Simulación:"));
            topPanel.add(simulationComboBox);
            topPanel.add(new JLabel("Caso de Prueba:"));
            topPanel.add(testCaseComboBox);
            topPanel.add(startButton);

            // Panel principal
            JPanel mainPanel = new JPanel(new BorderLayout());

            // Panel de información
            JPanel infoPanel = new JPanel(new GridLayout(3, 1));
            infoPanel.setBorder(new EmptyBorder(10, 10, 10, 10));

            titleLabel = new JLabel("Seleccione una simulación para comenzar", JLabel.CENTER);
            titleLabel.setFont(new Font("Arial", Font.BOLD, 16));

            stepLabel = new JLabel("Paso: 0/0", JLabel.CENTER);
            stepLabel.setFont(new Font("Arial", Font.PLAIN, 14));

            actionLabel = new JLabel("Acción: Esperando inicio", JLabel.CENTER);
            actionLabel.setFont(new Font("Arial", Font.ITALIC, 12));

            infoPanel.add(titleLabel);
            infoPanel.add(stepLabel);
            infoPanel.add(actionLabel);

            // Barra de progreso
            progressBar = new JProgressBar(0, 100);
            progressBar.setStringPainted(true);
            progressBar.setString("0%");

            // Panel de tablas
            JPanel tablesPanel = new JPanel(new GridLayout(1, 3));

            // Tabla de registros
            JPanel registersPanel = new JPanel(new BorderLayout());
            registersPanel.setBorder(new TitledBorder("Registros"));

            String[] registersColumns = {"Registro", "Valor", "Bits"};
            DefaultTableModel registersModel = new DefaultTableModel(registersColumns, 0);
            registersTable = new JTable(registersModel);
            registersTable.getTableHeader().setReorderingAllowed(false);
            registersPanel.add(new JScrollPane(registersTable), BorderLayout.CENTER);

            // Tabla de unidades de control
            JPanel controlPanel = new JPanel(new BorderLayout());
            controlPanel.setBorder(new TitledBorder("Unidades de Control"));

            String[] controlColumns = {"Unidad", "Estado"};
            DefaultTableModel controlModel = new DefaultTableModel(controlColumns, 0);
            controlUnitsTable = new JTable(controlModel);
            controlUnitsTable.getTableHeader().setReorderingAllowed(false);
            controlPanel.add(new JScrollPane(controlUnitsTable), BorderLayout.CENTER);

            // Tabla de memoria
            JPanel memoryPanel = new JPanel(new BorderLayout());
            memoryPanel.setBorder(new TitledBorder("Memoria Relevante"));

            String[] memoryColumns = {"Dirección", "Valor", "Contenido"};
            DefaultTableModel memoryModel = new DefaultTableModel(memoryColumns, 0);
            memoryTable = new JTable(memoryModel);
            memoryTable.getTableHeader().setReorderingAllowed(false);
            memoryPanel.add(new JScrollPane(memoryTable), BorderLayout.CENTER);

            tablesPanel.add(registersPanel);
            tablesPanel.add(controlPanel);
            tablesPanel.add(memoryPanel);

            // Panel de botones
            JPanel buttonPanel = new JPanel(new FlowLayout());
            buttonPanel.setBorder(new EmptyBorder(10, 10, 10, 10));

            nextButton = new JButton("Siguiente Paso");
            resetButton = new JButton("Reiniciar");

            nextButton.addActionListener(e -> {
                if (simulation != null) {
                    simulation.nextStep();
                }
            });

            resetButton.addActionListener(e -> {
                if (simulation != null) {
                    simulation.reset();
                }
            });

            nextButton.setEnabled(false);
            resetButton.setEnabled(false);

            buttonPanel.add(nextButton);
            buttonPanel.add(resetButton);

            // Ensamblar la ventana
            mainPanel.add(infoPanel, BorderLayout.NORTH);
            mainPanel.add(progressBar, BorderLayout.CENTER);
            mainPanel.add(tablesPanel, BorderLayout.SOUTH);

            add(topPanel, BorderLayout.NORTH);
            add(mainPanel, BorderLayout.CENTER);
            add(buttonPanel, BorderLayout.SOUTH);

            updateTestCases();
        }

        private void layoutComponents() {
            // El layout ya se configuró en initComponents
        }

        private void updateTestCases() {
            testCaseComboBox.removeAllItems();

            String selectedSimulation = (String) simulationComboBox.getSelectedItem();
            if (selectedSimulation != null) {
                ComputerSimulationBase tempSimulation;
                if (selectedSimulation.equals("Máquina Hipotética")) {
                    tempSimulation = new HypotheticalMachineSimulation();
                } else {
                    tempSimulation = new IASSimulation();
                }

                String[] testCases = tempSimulation.getTestCases();
                for (String testCase : testCases) {
                    testCaseComboBox.addItem(testCase);
                }
            }
        }

        private void startSimulation() {
            String selectedSimulation = (String) simulationComboBox.getSelectedItem();
            int selectedTestCase = testCaseComboBox.getSelectedIndex();

            if (selectedSimulation != null && selectedTestCase >= 0) {
                if (selectedSimulation.equals("Máquina Hipotética")) {
                    simulation = new HypotheticalMachineSimulation();
                } else {
                    simulation = new IASSimulation();
                }

                simulation.setGUI(this);
                simulation.loadTestCase(selectedTestCase);

                titleLabel.setText(simulation.getSimulationName());
                updateDisplay();

                nextButton.setEnabled(true);
                resetButton.setEnabled(true);
            }
        }

        public void updateDisplay() {
            if (simulation == null) return;

            // Actualizar etiquetas
            stepLabel.setText("Paso: " + (simulation.getCurrentStep() + 1) + "/" + simulation.getTotalSteps());
            actionLabel.setText("Acción: " + simulation.getCurrentStepDescription());

            // Actualizar barra de progreso
            int totalSteps = simulation.getTotalSteps();
            int progress = totalSteps > 0 ? (int) ((double) simulation.getCurrentStep() / totalSteps * 100) : 0;
            progressBar.setValue(progress);
            progressBar.setString(progress + "%");

            // Actualizar tabla de registros
            DefaultTableModel registersModel = (DefaultTableModel) registersTable.getModel();
            registersModel.setRowCount(0);

            for (Map.Entry<String, Integer> entry : simulation.registers.entrySet()) {
                String register = entry.getKey();
                int value = entry.getValue();
                String bits = "";

                if (simulation instanceof HypotheticalMachineSimulation) {
                    if (register.equals("PC") || register.equals("MAR")) {
                        bits = "12 bits";
                        registersModel.addRow(new Object[]{register, String.format("0x%03X", value), bits});
                    } else {
                        bits = "16 bits";
                        registersModel.addRow(new Object[]{register, String.format("0x%04X", value), bits});
                    }
                } else { // IAS
                    if (register.equals("PC") || register.equals("MAR")) {
                        bits = "12 bits";
                        registersModel.addRow(new Object[]{register, String.format("0x%03X", value), bits});
                    } else if (register.equals("IR") || register.equals("IBR")) {
                        bits = "20 bits";
                        registersModel.addRow(new Object[]{register, String.format("0x%05X", value), bits});
                    } else {
                        bits = "40 bits";
                        registersModel.addRow(new Object[]{register, String.format("0x%010X", value), bits});
                    }
                }
            }

            // Actualizar tabla de unidades de control
            DefaultTableModel controlModel = (DefaultTableModel) controlUnitsTable.getModel();
            controlModel.setRowCount(0);

            for (Map.Entry<String, String> entry : simulation.controlUnits.entrySet()) {
                String unit = entry.getKey();
                String state = entry.getValue();
                controlModel.addRow(new Object[]{unit, state});
            }

            // Actualizar tabla de memoria
            DefaultTableModel memoryModel = (DefaultTableModel) memoryTable.getModel();
            memoryModel.setRowCount(0);

            if (simulation instanceof HypotheticalMachineSimulation) {
                // Mostrar instrucciones
                for (int i = 0x100; i <= 0x123; i++) {
                    if (simulation.memory[i] != 0) {
                        int value = simulation.memory[i];
                        String content = "";

                        if (i < 0x200) { // Es una instrucción
                            // Extraer opcode (4 bits) y dirección (12 bits)
                            int opcode = (value >> 12) & 0xF;
                            int address = value & 0xFFF;

                            // Convertir opcode a binario de 4 bits
                            String opcodeBinary = String.format("%4s", Integer.toBinaryString(opcode)).replace(' ', '0');

                            // Buscar la instrucción en el conjunto de instrucciones
                            Map<String, String> instructionSet = simulation.getInstructionSet();
                            String instructionName = instructionSet.get(opcodeBinary);
                            if (instructionName == null) {
                                instructionName = "???";
                            }

                            content = instructionName + " M(0x" + Integer.toHexString(address).toUpperCase() + ")";
                        } else { // Es un dato
                            content = Integer.toString(value);
                        }

                        memoryModel.addRow(new Object[]{
                                String.format("0x%03X", i),
                                String.format("0x%04X", value),
                                content
                        });
                    }
                }

                // Mostrar datos
                for (int i = 0x200; i <= 0x223; i++) {
                    if (simulation.memory[i] != 0) {
                        memoryModel.addRow(new Object[]{
                                String.format("0x%03X", i),
                                String.format("0x%04X", simulation.memory[i]),
                                Integer.toString(simulation.memory[i])
                        });
                    }
                }
            } else { // IAS
                // Mostrar instrucciones
                for (int i = 0; i <= 5; i++) {
                    if (simulation.memory[i] != 0) {
                        int value = simulation.memory[i];
                        String content = "";

                        // Extraer instrucción izquierda (20 bits)
                        int leftInstr = value;
                        int opcode = leftInstr >> 12;
                        int address = leftInstr & 0xFFF;

                        // Convertir opcode a binario de 8 bits
                        String opcodeStr = String.format("%8s", Integer.toBinaryString(opcode)).replace(' ', '0');

                        // Buscar la instrucción en el conjunto de instrucciones
                        Map<String, String> instructionSet = simulation.getInstructionSet();
                        String instructionName = instructionSet.get(opcodeStr);
                        if (instructionName == null) {
                            instructionName = "???";
                        }

                        // Corregir aquí: cambiar la forma de construir la cadena de contenido
                        content = ((IASSimulation) simulation).instructionSet.getOrDefault(opcodeStr, "???") +
                                " M(" + address + ")";

                        memoryModel.addRow(new Object[]{
                                String.format("0x%03X", i),
                                String.format("0x%010X", value),
                                content
                        });
                    }
                }

                // Mostrar datos
                for (int i = 10; i <= 13; i++) {

                    memoryModel.addRow(new Object[]{
                            String.format("0x%03X", i),
                            String.format("0x%010X", simulation.memory[i]),
                            Integer.toString(simulation.memory[i])
                    });


                }
            }
        }

        public void simulationCompleted() {
            JOptionPane.showMessageDialog(this,
                    "Simulación completada con éxito",
                    "Completado",
                    JOptionPane.INFORMATION_MESSAGE);
        }
    }

    public static void main(String[] args) {
        // Establecer look and feel del sistema
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Crear y mostrar la GUI
        SwingUtilities.invokeLater(() -> {
            SimulationGUI gui = new SimulationGUI();
            gui.setVisible(true);
        });
    }
}