import sys
import math
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class ConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Converter Pro v2.1 | by Smith Lozano")
        self.setGeometry(100, 100, 1000, 700)

        # Variable para almacenar último resultado eléctrico
        self.last_electric_result = None

        # Establecer estilo oscuro profesional
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0f172a;
            }
            QGroupBox {
                font-weight: bold;
                color: #ffffff;
                border: 1px solid #334155;
                border-radius: 8px;
                margin-top: 5px;
                padding-top: 10px;
                background-color: #1e293b;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 6px 12px 6px 12px;
                color: #ffffff;
                background-color: #3b82f6;
                font-size: 13px;
                font-weight: bold;
                border-radius: 4px;
                border: 1px solid #2563eb;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #0f172a;
                color: #f1f5f9;
                font-size: 14px;
                selection-background-color: #3b82f6;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #60a5fa;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #64748b;
                font-style: italic;
            }
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                border: none;
                padding: 12px 28px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton#clear_button {
                background-color: #64748b;
            }
            QPushButton#clear_button:hover {
                background-color: #475569;
            }
            QPushButton#clear_button:pressed {
                background-color: #334155;
            }
            QLabel {
                font-size: 13px;
                color: #cbd5e1;
                font-weight: 500;
                margin-bottom: 4px;
            }
            QTextEdit {
                border: 1px solid #475569;
                border-radius: 6px;
                background-color: #0f172a;
                color: #f1f5f9;
                font-size: 14px;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                padding: 12px;
                selection-background-color: #3b82f6;
            }
            QRadioButton {
                color: #cbd5e1;
                font-size: 13px;
                font-weight: 500;
                padding: 6px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid #64748b;
            }
            QRadioButton::indicator:checked {
                background-color: #3b82f6;
                border-color: #3b82f6;
            }
            QRadioButton::indicator:hover {
                border-color: #60a5fa;
            }
            QScrollBar:vertical {
                background-color: #1e293b;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #475569;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #64748b;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }

            /* Estilos para diálogos personalizados */
            QDialog {
                background-color: #0f172a;
            }
            QDialog QLabel {
                color: #cbd5e1;
            }
            QDialog QPushButton {
                background-color: #3b82f6;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: 500;
            }
            QDialog QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        self.initUI()

    def initUI(self):
        # Widget central con scroll
        scroll_widget = QScrollArea()
        scroll_widget.setWidgetResizable(True)
        scroll_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setCentralWidget(scroll_widget)

        # Widget contenido
        central_widget = QWidget()
        scroll_widget.setWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # Título principal
        title_label = QLabel("🧮 Universal Converter Pro v2.1 | Convierte, Calcula, ¡Sorpréndete!")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                margin-bottom: 10px;
                padding: 15px;
                background-color: #1e293b;
                border-radius: 8px;
                border: 1px solid #334155;
            }
        """)
        main_layout.addWidget(title_label)

        # Selector de categoría
        category_group = QGroupBox("📁 CATEGORÍA DE CONVERSIÓN")
        category_layout = QVBoxLayout()
        category_layout.setSpacing(10)
        category_layout.setContentsMargins(15, 25, 15, 15)

        # Categorías organizadas en grid
        categories_grid = QGridLayout()

        self.category_buttons = {}
        categories = [
            ("⏰ TIEMPO", "time"),
            ("📏 LONGITUD", "length"),
            ("⚖️ MASA/PESO", "mass"),
            ("🌡️ TEMPERATURA", "temperature"),
            ("🔋 ENERGÍA", "energy"),
            ("⚡ POTENCIA", "power"),
            ("🔌 ELECTRICIDAD", "electricity"),
            ("💾 ALMACENAMIENTO", "storage"),
            ("🚀 VELOCIDAD DATOS", "data_speed"),
            ("🚗 VELOCIDAD", "speed"),
            ("📐 GEOMETRÍA", "geometry"),
        ]

        row, col = 0, 0
        for name, key in categories:
            btn = QRadioButton(name)
            btn.setObjectName(key)
            self.category_buttons[key] = btn
            categories_grid.addWidget(btn, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

        self.category_buttons["time"].setChecked(True)

        category_layout.addLayout(categories_grid)
        category_group.setLayout(category_layout)
        main_layout.addWidget(category_group)

        # Conectar señales para cambiar entre categorías
        for btn in self.category_buttons.values():
            btn.toggled.connect(self.update_conversion_units)

        # Widget para entrada y salida
        io_widget = QWidget()
        io_layout = QHBoxLayout(io_widget)
        io_layout.setSpacing(25)
        io_layout.setContentsMargins(0, 0, 0, 0)

        # Panel de entrada
        input_group = QGroupBox("📥 ENTRADA")
        input_layout = QVBoxLayout()
        input_layout.setSpacing(8)
        input_layout.setContentsMargins(15, 25, 15, 15)

        self.input_value = QLineEdit()
        self.input_value.setPlaceholderText("Ingrese valor numérico (ej: 2.25 o 2,25)...")

        # Configurar validador
        locale = QLocale(QLocale.Language.Spanish, QLocale.Country.UnitedStates)
        validator = QDoubleValidator()
        validator.setLocale(locale)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.input_value.setValidator(validator)

        self.input_unit = QComboBox()

        input_layout.addWidget(QLabel("Valor:"))
        input_layout.addWidget(self.input_value)
        input_layout.addWidget(QLabel("Unidad de origen:"))
        input_layout.addWidget(self.input_unit)

        input_group.setLayout(input_layout)
        io_layout.addWidget(input_group)

        # Panel de salida
        output_group = QGroupBox("📤 SALIDA")
        output_layout = QVBoxLayout()
        output_layout.setSpacing(8)
        output_layout.setContentsMargins(15, 25, 15, 15)

        self.output_unit = QComboBox()

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMaximumHeight(150)

        output_layout.addWidget(QLabel("Unidad de destino:"))
        output_layout.addWidget(self.output_unit)
        output_layout.addWidget(QLabel("Resultado:"))
        output_layout.addWidget(self.result_display)

        output_group.setLayout(output_layout)
        io_layout.addWidget(output_group)

        main_layout.addWidget(io_widget)

        # Botones de acción
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 10, 0, 0)

        self.convert_button = QPushButton("🔄 CONVERTIR")
        self.convert_button.clicked.connect(self.convert)

        self.clear_button = QPushButton("🗑️ LIMPIAR")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.clicked.connect(self.clear_fields)

        button_layout.addStretch()
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Panel de historial
        history_group = QGroupBox("📜 HISTORIAL DE CONVERSIONES")
        history_layout = QVBoxLayout()
        history_layout.setContentsMargins(15, 25, 15, 15)

        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setMaximumHeight(150)

        history_layout.addWidget(self.history_display)
        history_group.setLayout(history_layout)

        main_layout.addWidget(history_group)

        # Inicializar unidades
        self.update_conversion_units()

        # Historial
        self.conversion_history = []

    def update_conversion_units(self):
        """Actualiza las unidades disponibles según la categoría seleccionada"""
        self.input_unit.clear()
        self.output_unit.clear()

        # Actualizar unidades según categoría
        category = self.get_selected_category()
        units = self.get_units_for_category(category)
        self.input_unit.addItems(units)
        self.output_unit.addItems(units)

        # Establecer valores por defecto
        if category == "time":
            self.input_unit.setCurrentIndex(6)  # Días
            self.output_unit.setCurrentIndex(9)  # Años
        elif category == "temperature":
            self.input_unit.setCurrentIndex(0)  # Celsius
            self.output_unit.setCurrentIndex(1)  # Fahrenheit
        elif category == "electricity":
            self.input_unit.setCurrentIndex(0)  # Voltios (V)
            self.output_unit.setCurrentIndex(3)  # Ohmios (Ω)
        else:
            self.input_unit.setCurrentIndex(0)
            self.output_unit.setCurrentIndex(1)

    def get_selected_category(self):
        """Obtiene la categoría seleccionada"""
        for key, btn in self.category_buttons.items():
            if btn.isChecked():
                return key
        return "time"

    def get_units_for_category(self, category):
        """Devuelve las unidades para una categoría específica"""
        units_dict = {
            "time": [
                "Nanosegundos", "Microsegundos", "Milisegundos",
                "Segundos", "Minutos", "Horas", "Días",
                "Semanas", "Meses", "Años", "Décadas", "Siglos"
            ],
            "length": [
                "Milímetros", "Centímetros", "Metros", "Kilómetros",
                "Pulgadas", "Pies", "Yardas", "Millas",
                "Millas náuticas"
            ],
            "mass": [
                "Miligramos", "Gramos", "Kilogramos", "Toneladas",
                "Onzas", "Libras", "Stone", "Quintal"
            ],
            "temperature": [
                "Celsius", "Fahrenheit", "Kelvin"
            ],
            "energy": [
                "Julios", "Kilojulios", "Calorías", "Kilocalorías",
                "Kilovatios-hora", "Electronvoltios", "BTU"
            ],
            "power": [
                "Vatios (W)", "Kilovatios (kW)", "Megavatios (MW)",
                "Caballos de fuerza (HP)", "PS (caballos métricos)"
            ],
            "electricity": [
                "Voltios (V)", "Amperios (A)", "Ohmios (Ω)",
                "Vatios (W)", "Kilovatios (kW)"
            ],
            "storage": [
                "Bits", "Bytes", "Kilobytes (KB)", "Megabytes (MB)",
                "Gigabytes (GB)", "Terabytes (TB)", "Petabytes (PB)",
                "Kibibytes (KiB)", "Mebibytes (MiB)", "Gibibytes (GiB)"
            ],
            "data_speed": [
                "Bits/seg", "Kilobits/seg", "Megabits/seg", "Gigabits/seg",
                "Bytes/seg", "Kilobytes/seg", "Megabytes/seg"
            ],
            "speed": [
                "Metros/seg", "Kilómetros/hora", "Millas/hora",
                "Nudos", "Mach", "Pies/seg"
            ],
            "geometry": [
                "Metros²", "Centímetros²", "Kilómetros²", "Hectáreas",
                "Acres", "Pies²", "Pulgadas²", "Millas²",
                "Litros", "Mililitros", "Metros³", "Galones (US)", "Galones (UK)"
            ]
        }

        return units_dict.get(category, ["Unidad 1", "Unidad 2"])

    def parse_number(self, text):
        """Convierte texto con coma o punto a float"""
        if not text:
            return None

        normalized = text.strip().replace(',', '.').replace(' ', '')

        if 'e' in normalized.lower():
            parts = normalized.lower().split('e')
            if len(parts) == 2:
                mantisa = parts[0].replace(',', '.')
                exponente = parts[1]
                try:
                    return float(mantisa) * (10 ** float(exponente))
                except:
                    return None

        try:
            return float(normalized)
        except ValueError:
            return None

    def format_number(self, num):
        """Formatea un número de manera óptima"""
        if abs(num - round(num)) < 1e-10:
            return str(int(round(num)))

        if abs(num) >= 1e9 or (abs(num) <= 1e-9 and num != 0):
            formatted = f"{num:.4e}"
            if 'e' in formatted:
                parts = formatted.split('e')
                mantisa = parts[0].rstrip('0').rstrip('.')
                exponent = parts[1].lstrip('+').lstrip('0')
                if exponent == '':
                    exponent = '0'
                return f"{mantisa} × 10^{exponent}"

        str_num = f"{num:.15f}".rstrip('0').rstrip('.')

        if len(str_num.split('.')[-1]) > 6:
            str_num = f"{num:.6f}".rstrip('0').rstrip('.')

        return str_num

    def convert(self):
        """Realiza la conversión de unidades"""
        try:
            value_text = self.input_value.text().strip()
            if not value_text:
                self.show_message("Advertencia", "Por favor ingrese un valor para convertir")
                return

            category = self.get_selected_category()
            from_unit = self.input_unit.currentText()
            to_unit = self.output_unit.currentText()

            # Parsear número
            value = self.parse_number(value_text)
            if value is None:
                self.show_message("Error",
                                  f"No se pudo interpretar '{value_text}' como número.\n\n"
                                  "Use formato como: 2.25 o 2,25")
                return

            if from_unit == to_unit:
                formatted_input = self.format_input(value_text)
                self.result_display.setPlainText(
                    f"{formatted_input} {from_unit} = {formatted_input} {to_unit} (misma unidad)")
                self.result_display.setStyleSheet("""
                    QTextEdit {
                        border: 1px solid #64748b;
                        background-color: #1e293b;
                        color: #cbd5e1;
                        font-size: 15px;
                        font-weight: 500;
                    }
                """)
                return

            # Realizar conversión según categoría
            result = self.perform_conversion(value, from_unit, to_unit, category)

            if result is None:
                # Para electricidad, mostrar mensaje especial
                if category == "electricity" and self.is_complex_electric_conversion(from_unit, to_unit):
                    self.show_electricity_calculator(value, from_unit, to_unit)
                    return
                else:
                    self.show_message("Error", f"No se puede convertir de {from_unit} a {to_unit}")
                    return

            # Formatear y mostrar resultado
            formatted_input = self.format_input(value_text)
            formatted_result = self.format_number(result)

            result_text = f"{formatted_input} {from_unit} = {formatted_result} {to_unit}"
            self.result_display.setPlainText(result_text)

            self.result_display.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #3b82f6;
                    background-color: #1e293b;
                    color: #60a5fa;
                    font-size: 15px;
                    font-weight: 500;
                }
            """)

            # Agregar al historial
            history_entry = f"{formatted_input} {from_unit} → {formatted_result} {to_unit}"
            self.conversion_history.append(history_entry)

            # Actualizar historial
            self.update_history()

        except Exception as e:
            self.show_message("Error", f"Error en la conversión: {str(e)}")

    def perform_conversion(self, value, from_unit, to_unit, category):
        """Realiza la conversión según la categoría"""
        if category == "time":
            return self.convert_time(value, from_unit, to_unit)
        elif category == "length":
            return self.convert_length(value, from_unit, to_unit)
        elif category == "mass":
            return self.convert_mass(value, from_unit, to_unit)
        elif category == "temperature":
            return self.convert_temperature(value, from_unit, to_unit)
        elif category == "energy":
            return self.convert_energy(value, from_unit, to_unit)
        elif category == "power":
            return self.convert_power(value, from_unit, to_unit)
        elif category == "electricity":
            return self.convert_electricity(value, from_unit, to_unit)
        elif category == "storage":
            return self.convert_storage(value, from_unit, to_unit)
        elif category == "data_speed":
            return self.convert_data_speed(value, from_unit, to_unit)
        elif category == "speed":
            return self.convert_speed(value, from_unit, to_unit)
        elif category == "geometry":
            return self.convert_geometry(value, from_unit, to_unit)
        return None

    def convert_time(self, value, from_unit, to_unit):
        """Conversión de tiempo"""
        to_seconds = {
            "Nanosegundos": 1e-9,
            "Microsegundos": 1e-6,
            "Milisegundos": 0.001,
            "Segundos": 1,
            "Minutos": 60,
            "Horas": 3600,
            "Días": 86400,
            "Semanas": 604800,
            "Meses": 30.4375 * 86400,
            "Años": 365.25 * 86400,
            "Décadas": 10 * 365.25 * 86400,
            "Siglos": 100 * 365.25 * 86400
        }

        if from_unit == "Años" and to_unit == "Meses":
            return value * 12
        if from_unit == "Meses" and to_unit == "Años":
            return value / 12
        if from_unit == "Décadas" and to_unit == "Años":
            return value * 10
        if from_unit == "Años" and to_unit == "Décadas":
            return value / 10
        if from_unit == "Siglos" and to_unit == "Años":
            return value * 100
        if from_unit == "Años" and to_unit == "Siglos":
            return value / 100

        if from_unit in to_seconds and to_unit in to_seconds:
            return value * to_seconds[from_unit] / to_seconds[to_unit]

        return None

    def convert_length(self, value, from_unit, to_unit):
        """Conversión de longitud"""
        to_meters = {
            "Milímetros": 0.001,
            "Centímetros": 0.01,
            "Metros": 1,
            "Kilómetros": 1000,
            "Pulgadas": 0.0254,
            "Pies": 0.3048,
            "Yardas": 0.9144,
            "Millas": 1609.344,
            "Millas náuticas": 1852.0
        }

        if from_unit in to_meters and to_unit in to_meters:
            value_in_meters = value * to_meters[from_unit]
            return value_in_meters / to_meters[to_unit]

        return None

    def convert_mass(self, value, from_unit, to_unit):
        """Conversión de masa/peso"""
        to_kilograms = {
            "Miligramos": 0.000001,
            "Gramos": 0.001,
            "Kilogramos": 1,
            "Toneladas": 1000,
            "Onzas": 0.0283495,
            "Libras": 0.453592,
            "Stone": 6.35029,
            "Quintal": 100
        }

        if from_unit in to_kilograms and to_unit in to_kilograms:
            value_in_kg = value * to_kilograms[from_unit]
            return value_in_kg / to_kilograms[to_unit]

        return None

    def convert_temperature(self, value, from_unit, to_unit):
        """Conversión de temperatura"""
        if from_unit == to_unit:
            return value

        # Convertir a Celsius primero
        if from_unit == "Celsius":
            celsius = value
        elif from_unit == "Fahrenheit":
            celsius = (value - 32) * 5 / 9
        elif from_unit == "Kelvin":
            celsius = value - 273.15
        else:
            return None

        # Convertir de Celsius a la unidad destino
        if to_unit == "Celsius":
            return celsius
        elif to_unit == "Fahrenheit":
            return (celsius * 9 / 5) + 32
        elif to_unit == "Kelvin":
            return celsius + 273.15

        return None

    def convert_energy(self, value, from_unit, to_unit):
        """Conversión de energía"""
        to_joules = {
            "Julios": 1,
            "Kilojulios": 1000,
            "Calorías": 4.184,
            "Kilocalorías": 4184,
            "Kilovatios-hora": 3.6e6,
            "Electronvoltios": 1.602176634e-19,
            "BTU": 1055.06
        }

        if from_unit in to_joules and to_unit in to_joules:
            value_in_j = value * to_joules[from_unit]
            return value_in_j / to_joules[to_unit]

        return None

    def convert_power(self, value, from_unit, to_unit):
        """Conversión de potencia"""
        to_watts = {
            "Vatios (W)": 1,
            "Kilovatios (kW)": 1000,
            "Megavatios (MW)": 1e6,
            "Caballos de fuerza (HP)": 745.7,
            "PS (caballos métricos)": 735.5
        }

        if from_unit in to_watts and to_unit in to_watts:
            value_in_w = value * to_watts[from_unit]
            return value_in_w / to_watts[to_unit]

        return None

    def convert_electricity(self, value, from_unit, to_unit):
        """Conversión de electricidad - VERSIÓN MEJORADA E INTUITIVA"""

        # CASO 1: Mismas unidades
        if from_unit == to_unit:
            return value

        # CASO 2: Conversiones lineales simples
        simple_conversions = {
            # Prefijos de potencia
            ("Vatios (W)", "Kilovatios (kW)"): lambda x: x / 1000,
            ("Kilovatios (kW)", "Vatios (W)"): lambda x: x * 1000,

            # Potencia de Vatios (ya está en categoría power, pero la mantenemos por compatibilidad)
            ("Vatios (W)", "Kilovatios (kW)"): lambda x: x / 1000,
            ("Kilovatios (kW)", "Vatios (W)"): lambda x: x * 1000,
        }

        # Verificar si es una conversión simple
        key = (from_unit, to_unit)
        if key in simple_conversions:
            return simple_conversions[key](value)

        # CASO 3: Son diferentes magnitudes eléctricas (V, A, Ω, W)
        # Estas necesitan información adicional
        electric_units = ["Voltios (V)", "Amperios (A)", "Ohmios (Ω)", "Vatios (W)", "Kilovatios (kW)"]

        if from_unit in electric_units and to_unit in electric_units:
            # No podemos convertir directamente, retornar None para activar la calculadora
            return None

        # CASO 4: No se puede convertir
        return None

    def is_complex_electric_conversion(self, from_unit, to_unit):
        """Determina si es una conversión compleja que necesita calculadora"""
        electric_units = ["Voltios (V)", "Amperios (A)", "Ohmios (Ω)", "Vatios (W)", "Kilovatios (kW)"]
        return from_unit in electric_units and to_unit in electric_units and from_unit != to_unit

    def show_electricity_calculator(self, value, from_unit, to_unit):
        """Muestra una calculadora INTUITIVA para conversiones eléctricas"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"🔌 Calculadora Eléctrica Inteligente")
        dialog.setFixedSize(700, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
            }
            QLabel {
                color: #cbd5e1;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                background-color: #1e293b;
                color: #f1f5f9;
                border: 1px solid #475569;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #3b82f6;
            }
            QGroupBox {
                border: 1px solid #334155;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #1e293b;
            }
            QGroupBox::title {
                color: #60a5fa;
                font-weight: bold;
                padding-left: 10px;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        title = QLabel(f"<h2 style='color: #60a5fa;'>🔌 CALCULADORA DE LEY DE OHM</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Descripción clara
        desc = QLabel(f"""
        <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #3b82f6;'>
        <b style='color: #60a5fa;'>Conversión solicitada:</b> <span style='color: #fbbf24;'>{value} {from_unit} → {to_unit}</span><br>
        <span style='color: #cbd5e1;'>Para convertir entre <b>{from_unit}</b> y <b>{to_unit}</b> necesitamos conocer una tercera variable eléctrica.</span>
        </div>
        """)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Grupo de entrada de datos
        input_group = QGroupBox("📊 INGRESE LOS DATOS CONOCIDOS")
        input_layout = QGridLayout()
        input_layout.setSpacing(15)
        input_layout.setContentsMargins(15, 20, 15, 15)

        # Crear diccionario para almacenar los widgets de entrada
        self.input_widgets = {}

        # Definir todas las unidades eléctricas
        electric_units_list = ["Voltios (V)", "Amperios (A)", "Ohmios (Ω)", "Vatios (W)", "Kilovatios (kW)"]

        # Ya tenemos un valor conocido (el de la conversión)
        row = 0
        for unit in electric_units_list:
            if unit == from_unit:
                # Esta es la unidad que ya conocemos
                label = QLabel(f"<b>{unit}</b> (valor conocido):")
                value_edit = QLineEdit(str(value))
                value_edit.setReadOnly(True)
                value_edit.setStyleSheet("background-color: #334155;")
                self.input_widgets[unit] = value_edit
            else:
                label = QLabel(f"<b>{unit}</b>:")
                value_edit = QLineEdit()
                value_edit.setPlaceholderText(f"Ingrese valor en {unit}...")
                self.input_widgets[unit] = value_edit

            input_layout.addWidget(label, row, 0)
            input_layout.addWidget(value_edit, row, 1)
            row += 1

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Instrucción
        instruction = QLabel("""
        <div style='background-color: #1e293b; padding: 10px; border-radius: 5px;'>
        <b>💡 Instrucción:</b> Ingrese al menos <b>2 valores</b> en total (incluyendo el que ya tiene). 
        La calculadora calculará automáticamente todos los valores faltantes.
        </div>
        """)
        instruction.setWordWrap(True)
        layout.addWidget(instruction)

        # Botón calcular
        calculate_btn = QPushButton("🔮 CALCULAR VALORES FALTANTES")
        calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                font-weight: bold;
                padding: 15px;
                border-radius: 8px;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)

        # Área de resultados
        results_group = QGroupBox("📈 RESULTADOS")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(10)
        results_layout.setContentsMargins(15, 20, 15, 15)

        self.results_label = QLabel(
            "<div style='text-align: center; color: #94a3b8;'>Los resultados aparecerán aquí...</div>")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tabla de resultados
        self.results_table = QTextEdit()
        self.results_table.setReadOnly(True)
        self.results_table.setMaximumHeight(120)
        self.results_table.setStyleSheet("""
            QTextEdit {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }
        """)

        results_layout.addWidget(self.results_label)
        results_layout.addWidget(self.results_table)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Conectar botón calcular
        calculate_btn.clicked.connect(lambda: self.calculate_ohm_law(self.input_widgets, dialog))
        layout.addWidget(calculate_btn)

        # Ejemplos comunes
        examples = QLabel("""
        <div style='background-color: #1e293b; padding: 15px; border-radius: 8px; margin-top: 10px;'>
        <b style='color: #60a5fa;'>💡 Ejemplos comunes:</b><br>
        • <b>Bombilla casera:</b> 60W, 120V → 0.5A, 240Ω<hr style='border-color: #475569;'>
        • <b>Tomacorriente residencial:</b> 220V, 10A → 2200W, 22Ω<hr style='border-color: #475569;'>
        • <b>Batería de auto:</b> 12V, 50A → 600W, 0.24Ω<hr style='border-color: #475569;'>
        • <b>Resistencia típica:</b> 100Ω, 0.5A → 50V, 25W
        </div>
        """)
        examples.setWordWrap(True)
        layout.addWidget(examples)

        # Ejecutar diálogo
        dialog.exec()

    def calculate_ohm_law(self, input_widgets, dialog):
        """Calcula todos los valores eléctricos usando Ley de Ohm"""
        try:
            # Obtener valores de los widgets
            values = {}
            units = ["Voltios (V)", "Amperios (A)", "Ohmios (Ω)", "Vatios (W)", "Kilovatios (kW)"]

            for unit in units:
                text = input_widgets[unit].text().strip()
                if text:
                    value = self.parse_number(text)
                    if value is not None:
                        values[unit] = value
                    else:
                        QMessageBox.warning(dialog, "Error", f"Valor inválido en {unit}")
                        return
                else:
                    values[unit] = None

            # Convertir kW a W para cálculos
            if values["Kilovatios (kW)"] is not None:
                if values["Vatios (W)"] is None:
                    values["Vatios (W)"] = values["Kilovatios (kW)"] * 1000
                values["Kilovatios (kW)"] = None  # Ya lo convertimos

            # Contar valores conocidos
            known_count = sum(1 for v in values.values() if v is not None)

            if known_count < 2:
                QMessageBox.warning(dialog, "Error", "Se necesitan al menos 2 valores conocidos")
                return

            # Calcular valores faltantes
            # Intentar calcular Voltaje (V)
            if values["Voltios (V)"] is None:
                if values["Amperios (A)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Voltios (V)"] = values["Amperios (A)"] * values["Ohmios (Ω)"]
                elif values["Vatios (W)"] is not None and values["Amperios (A)"] is not None:
                    values["Voltios (V)"] = values["Vatios (W)"] / values["Amperios (A)"]
                elif values["Vatios (W)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Voltios (V)"] = math.sqrt(values["Vatios (W)"] * values["Ohmios (Ω)"])

            # Intentar calcular Corriente (A)
            if values["Amperios (A)"] is None:
                if values["Voltios (V)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Amperios (A)"] = values["Voltios (V)"] / values["Ohmios (Ω)"]
                elif values["Vatios (W)"] is not None and values["Voltios (V)"] is not None:
                    values["Amperios (A)"] = values["Vatios (W)"] / values["Voltios (V)"]
                elif values["Vatios (W)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Amperios (A)"] = math.sqrt(values["Vatios (W)"] / values["Ohmios (Ω)"])

            # Intentar calcular Resistencia (Ω)
            if values["Ohmios (Ω)"] is None:
                if values["Voltios (V)"] is not None and values["Amperios (A)"] is not None:
                    values["Ohmios (Ω)"] = values["Voltios (V)"] / values["Amperios (A)"]
                elif values["Voltios (V)"] is not None and values["Vatios (W)"] is not None:
                    values["Ohmios (Ω)"] = (values["Voltios (V)"] ** 2) / values["Vatios (W)"]
                elif values["Vatios (W)"] is not None and values["Amperios (A)"] is not None:
                    values["Ohmios (Ω)"] = values["Vatios (W)"] / (values["Amperios (A)"] ** 2)

            # Intentar calcular Potencia (W)
            if values["Vatios (W)"] is None:
                if values["Voltios (V)"] is not None and values["Amperios (A)"] is not None:
                    values["Vatios (W)"] = values["Voltios (V)"] * values["Amperios (A)"]
                elif values["Voltios (V)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Vatios (W)"] = (values["Voltios (V)"] ** 2) / values["Ohmios (Ω)"]
                elif values["Amperios (A)"] is not None and values["Ohmios (Ω)"] is not None:
                    values["Vatios (W)"] = (values["Amperios (A)"] ** 2) * values["Ohmios (Ω)"]

            # Calcular kW
            if values["Vatios (W)"] is not None:
                values["Kilovatios (kW)"] = values["Vatios (W)"] / 1000

            # Verificar si se pudieron calcular todos
            all_calculated = all(v is not None for v in [values["Voltios (V)"], values["Amperios (A)"],
                                                         values["Ohmios (Ω)"], values["Vatios (W)"]])

            # Actualizar tabla de resultados
            result_text = ""
            result_text += "╔══════════════════════╦══════════════════════╗\n"
            result_text += "║       PARÁMETRO      ║        VALOR         ║\n"
            result_text += "╠══════════════════════╬══════════════════════╣\n"

            for unit in ["Voltios (V)", "Amperios (A)", "Ohmios (Ω)", "Vatios (W)", "Kilovatios (kW)"]:
                if values[unit] is not None:
                    if unit in ["Voltios (V)", "Amperios (A)"]:
                        formatted = f"{values[unit]:.4f}"
                    elif unit == "Ohmios (Ω)":
                        formatted = f"{values[unit]:.4f}"
                    elif unit == "Vatios (W)":
                        formatted = f"{values[unit]:.2f}"
                    else:
                        formatted = f"{values[unit]:.6f}"

                    result_text += f"║ {unit:<20} ║ {formatted:>20} ║\n"
                else:
                    result_text += f"║ {unit:<20} ║ {'NO CALCULADO':>20} ║\n"

            result_text += "╚══════════════════════╩══════════════════════╝"

            self.results_table.setPlainText(result_text)

            # Actualizar mensaje
            if all_calculated:
                self.results_label.setText("""
                <div style='background-color: #064e3b; padding: 10px; border-radius: 5px; color: #a7f3d0;'>
                <b>✅ TODOS LOS VALORES CALCULADOS</b><br>
                Fórmulas usadas: V = I × R, P = V × I, R = V / I, I = P / V
                </div>
                """)
            else:
                self.results_label.setText("""
                <div style='background-color: #7c2d12; padding: 10px; border-radius: 5px; color: #fde68a;'>
                <b>⚠️ VALORES PARCIALMENTE CALCULADOS</b><br>
                Ingrese más valores para calcular todos los parámetros.
                </div>
                """)

            # Actualizar widgets con valores calculados
            for unit, widget in input_widgets.items():
                if values[unit] is not None and not widget.isReadOnly():
                    widget.setText(f"{values[unit]:.6f}".rstrip('0').rstrip('.'))

        except ZeroDivisionError:
            QMessageBox.warning(dialog, "Error", "División por cero. Verifique los valores ingresados.")
        except Exception as e:
            QMessageBox.warning(dialog, "Error", f"Error en el cálculo: {str(e)}")

    def convert_storage(self, value, from_unit, to_unit):
        """Conversión de almacenamiento digital"""
        # Unidades decimales (base 10)
        decimal_units = {
            "Bits": 1 / 8,
            "Bytes": 1,
            "Kilobytes (KB)": 1000,
            "Megabytes (MB)": 1e6,
            "Gigabytes (GB)": 1e9,
            "Terabytes (TB)": 1e12,
            "Petabytes (PB)": 1e15
        }

        # Unidades binarias (base 2)
        binary_units = {
            "Kibibytes (KiB)": 1024,
            "Mebibytes (MiB)": 1024 ** 2,
            "Gibibytes (GiB)": 1024 ** 3
        }

        # Combinar diccionarios
        all_units = {**decimal_units, **binary_units}

        if from_unit in all_units and to_unit in all_units:
            # Convertir a bytes primero
            value_in_bytes = value * all_units[from_unit]
            return value_in_bytes / all_units[to_unit]

        return None

    def convert_data_speed(self, value, from_unit, to_unit):
        """Conversión de velocidad de datos"""
        conversions = {
            "Bits/seg": 1,
            "Kilobits/seg": 1000,
            "Megabits/seg": 1e6,
            "Gigabits/seg": 1e9,
            "Bytes/seg": 8,
            "Kilobytes/seg": 8000,
            "Megabytes/seg": 8e6
        }

        if from_unit in conversions and to_unit in conversions:
            value_in_bps = value * conversions[from_unit]
            return value_in_bps / conversions[to_unit]

        return None

    def convert_speed(self, value, from_unit, to_unit):
        """Conversión de velocidad"""
        to_mps = {
            "Metros/seg": 1,
            "Kilómetros/hora": 1000 / 3600,
            "Millas/hora": 1609.344 / 3600,
            "Nudos": 1852 / 3600,
            "Mach": 343,  # Mach 1 ≈ 343 m/s
            "Pies/seg": 0.3048
        }

        if from_unit in to_mps and to_unit in to_mps:
            value_in_mps = value * to_mps[from_unit]
            return value_in_mps / to_mps[to_unit]

        return None

    def convert_geometry(self, value, from_unit, to_unit):
        """Conversión de unidades geométricas (área y volumen)"""
        # Unidades de área
        area_units = {
            "Metros²": 1,
            "Centímetros²": 0.0001,
            "Kilómetros²": 1e6,
            "Hectáreas": 10000,
            "Acres": 4046.86,
            "Pies²": 0.092903,
            "Pulgadas²": 0.00064516,
            "Millas²": 2.58999e6
        }

        # Unidades de volumen
        volume_units = {
            "Litros": 1,
            "Mililitros": 0.001,
            "Metros³": 1000,
            "Galones (US)": 3.78541,
            "Galones (UK)": 4.54609
        }

        # Verificar si son unidades de área
        if from_unit in area_units and to_unit in area_units:
            value_in_m2 = value * area_units[from_unit]
            return value_in_m2 / area_units[to_unit]

        # Verificar si son unidades de volumen
        if from_unit in volume_units and to_unit in volume_units:
            value_in_liters = value * volume_units[from_unit]
            return value_in_liters / volume_units[to_unit]

        return None

    def format_input(self, value):
        """Formatea el valor de entrada"""
        try:
            num = float(value.replace(',', '.'))
            if num.is_integer():
                return str(int(num))

            str_value = str(value).rstrip('0').rstrip('.')
            if '.' in str_value:
                decimal_part = str_value.split('.')[1]
                if len(decimal_part) > 4:
                    str_value = f"{num:.4f}".rstrip('0').rstrip('.')

            return str_value
        except:
            return str(value)

    def update_history(self):
        """Actualiza el historial"""
        self.history_display.clear()
        if self.conversion_history:
            self.history_display.append("Historial reciente:")
            self.history_display.append("")
            for entry in self.conversion_history[-8:]:
                self.history_display.append(f"• {entry}")
        else:
            self.history_display.setPlainText("No hay conversiones en el historial.")

    def clear_fields(self):
        """Limpia todos los campos"""
        self.input_value.clear()
        self.result_display.clear()
        self.result_display.setStyleSheet("""
            QTextEdit {
                border: 1px solid #475569;
                background-color: #0f172a;
                color: #f1f5f9;
                font-size: 14px;
            }
        """)
        self.history_display.clear()
        self.history_display.setPlainText("Historial limpio. Realice nuevas conversiones.")

    def show_message(self, title, message):
        """Muestra un mensaje de diálogo"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #1e293b;
            }
            QLabel {
                color: #cbd5e1;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: 500;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)

        msg_box.exec()


def main():
    app = QApplication(sys.argv)

    # Establecer estilo
    app.setStyle("Fusion")

    # Configurar paleta oscura
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(15, 23, 42))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(241, 245, 249))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 41, 59))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(15, 23, 42))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 41, 59))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(241, 245, 249))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(241, 245, 249))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(30, 41, 59))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(241, 245, 249))
    dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(59, 130, 246))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    app.setPalette(dark_palette)

    # Crear y mostrar ventana
    converter = ConverterApp()
    converter.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()