import sys
import queue
import threading
import time
import webbrowser
from tkinter import filedialog
import customtkinter as ctk
import serial
import serial.tools.list_ports
import requests
from packaging import version

CURRENT_VERSION = "1.0.1"
GITHUB_USER = "Paulina-Sanchez"
GITHUB_REPO = "Bioprinter_GUI"

CENTER_X = 82.50
CENTER_Y = 65.50

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLOR_BG_DARK = "#1E1F22"
COLOR_BG_CARD = "#2B2D30"
COLOR_PRIMARY = "#1976D2"
COLOR_PRIMARY_HOVER = "#1565C0"
COLOR_SUCCESS = "#2E7D32"
COLOR_SUCCESS_HOVER = "#1B5E20"
COLOR_RETRACT = "#8D5316"
COLOR_RETRACT_HOVER = "#A4621D"
COLOR_DANGER = "#D32F2F"
COLOR_DANGER_HOVER = "#B71C1C"

FONT_TITLE = ("SF Pro Display", 16, "bold")
FONT_SUBTITLE = ("SF Pro Text", 13, "bold")
FONT_BUTTON = ("SF Pro Text", 12, "bold")
FONT_REGULAR = ("SF Pro Text", 12)

USERS_DB = {
    "operator": "workshop2026",
    "admin": "bioprintAdmin"
}

TRANSLATIONS = {
    "EN": {
        "login_title": "Bioprinter Access Control",
        "operator_login": "Operator Login",
        "username": "Username",
        "password": "Password",
        "login_btn": "Authenticate",
        "invalid_credentials": "Invalid credentials. Access denied.",
        "app_title": "Bioprinter Controller — Multi-Board Host",
        "app_name": "BioPrinter Studio",
        "operator": "Operator",
        "port": "Port:",
        "firmware": "Firmware:",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "disconnected": "● Disconnected",
        "connected": "● Connected",
        "no_ports": "No ports found",
        "tab_prep": "🔬 Preparation & Calibration",
        "tab_print": "🖨️ Print Execution",
        "tab_terminal": "⚙️ Terminal & Diagnostics",
        "jog_title": "Motion Control (Jog XYZ)",
        "step_label": "Step Size:",
        "home_all": "⌂ Home All",
        "center_bed": "⌖ Center",
        "home_z": "⌂ Home Z",
        "axis_z": "Bed (Z-Axis)",
        "z_up": "▲ Bed Up",
        "z_down": "▼ Bed Down",
        "dispenser_title": "Bio-Dispenser / Syringe (E1)",
        "distance": "Distance:",
        "speed_unit": "Speed (mm/min):",
        "extrude": "💧 Purge / Extrude",
        "retract": "↩ Retract",
        "file_title": "G-code Job / Macro Execution",
        "load_file": "📁 Load G-code File",
        "no_file": "No file selected",
        "lines_progress": "Lines executed: {cur} / {tot} ({pct}%)",
        "start_print": "▶️ Start Bioprinting",
        "pause": "⏸ Pause",
        "resume": "▶️ Resume",
        "cancel": "⏹ Cancel",
        "overrides_title": "Real-time Process Overrides",
        "speed_override": "Print Speed: {val}%",
        "flow_override": "Dispense Flow: {val}%",
        "apply": "Apply",
        "terminal_title": "System Telemetry & G-code Console",
        "cmd_placeholder": "Send G-code command (e.g. M114, G28, M105)...",
        "send": "Send",
        "emergency_stop": "🚨 IMMEDIATE EMERGENCY STOP (M112)",
        "file_loaded_msg": "File loaded: {name} ({count} active commands)",
        "not_connected_warning": "WARNING: Machine is not connected.",
        "need_file_warning": "WARNING: Please load a valid G-code file first.",
        "job_started": "Starting execution: {name}...",
        "job_cancelled": "Job execution cancelled by operator.",
        "job_completed": "Macro execution completed successfully.",
        "estop_sent": "CRITICAL >> M112 Emergency Stop Triggered!",
        "update_title": "Update Available",
        "update_heading": "🚀 New Version Available",
        "update_msg": "Current version: v{cur}\nLatest available: v{latest}\n\nUpdating is recommended for stability.",
        "update_download": "Go to Download",
        "update_later": "Remind Me Later"
    },
    "ES": {
        "login_title": "Control de Acceso — Bioimpresora",
        "operator_login": "Autenticación de Operador",
        "username": "Usuario",
        "password": "Contraseña",
        "login_btn": "Iniciar Sesión",
        "invalid_credentials": "Credenciales no válidas. Acceso denegado.",
        "app_title": "Controlador de Bioimpresora — Multi-Placa",
        "app_name": "BioPrinter Studio",
        "operator": "Operador",
        "port": "Puerto:",
        "firmware": "Firmware:",
        "connect": "Conectar",
        "disconnect": "Desconectar",
        "disconnected": "● Desconectado",
        "connected": "● Conectado",
        "no_ports": "No se detectaron puertos",
        "tab_prep": "🔬 Preparación & Calibración",
        "tab_print": "🖨️ Ejecución de Impresión",
        "tab_terminal": "⚙️ Terminal & Diagnóstico",
        "jog_title": "Control de Movimiento (Jog XYZ)",
        "step_label": "Paso:",
        "home_all": "⌂ Calibrar Todo (Home)",
        "center_bed": "⌖ Centrar",
        "home_z": "⌂ Home Z",
        "axis_z": "Plato (Eje Z)",
        "z_up": "▲ Subir Plato",
        "z_down": "▼ Bajar Plato",
        "dispenser_title": "Bio-Dispensador / Jeringa (E1)",
        "distance": "Distancia:",
        "speed_unit": "Velocidad (mm/min):",
        "extrude": "💧 Purgar / Dosificar",
        "retract": "↩ Retracción",
        "file_title": "Archivo de Bioimpresión / Macro",
        "load_file": "📁 Cargar Archivo G-code",
        "no_file": "Ningún archivo seleccionado",
        "lines_progress": "Líneas ejecutadas: {cur} / {tot} ({pct}%)",
        "start_print": "▶️ Iniciar Bioimpresión",
        "pause": "⏸ Pausar",
        "resume": "▶️ Reanudar",
        "cancel": "⏹ Cancelar",
        "overrides_title": "Ajustes de Proceso en Vivo (Overrides)",
        "speed_override": "Velocidad: {val}%",
        "flow_override": "Flujo de Dosificación: {val}%",
        "apply": "Aplicar",
        "terminal_title": "Consola de Telemetría & Depuración G-code",
        "cmd_placeholder": "Escribir comando G-code manual (ej. M114, G28, M105)...",
        "send": "Enviar",
        "emergency_stop": "🚨 PARADA DE EMERGENCIA INMEDIATA (M112)",
        "file_loaded_msg": "Archivo cargado: {name} ({count} comandos activos)",
        "not_connected_warning": "AVISO: Máquina desconectada.",
        "need_file_warning": "AVISO: Cargue un archivo G-code primero.",
        "job_started": "Iniciando ejecución: {name}...",
        "job_cancelled": "Trabajo cancelado por el operador.",
        "job_completed": "Ejecución completada con éxito.",
        "estop_sent": "CRÍTICO >> ¡M112 Parada de Emergencia Activada!",
        "update_title": "Actualización Disponible",
        "update_heading": "🚀 Nueva Versión Disponible",
        "update_msg": "Tu versión actual: v{cur}\nÚltima versión disponible: v{latest}\n\nSe recomienda actualizar para mejoras de estabilidad.",
        "update_download": "Ir a Descargar",
        "update_later": "Recordar más tarde"
    }
}


class UpdateDialog(ctk.CTkToplevel):
    def __init__(self, parent, latest_ver, release_url, lang="EN"):
        super().__init__(parent)
        self.t = TRANSLATIONS[lang]
        self.title(self.t["update_title"])
        self.geometry("440x250")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.lift()

        lbl_title = ctk.CTkLabel(self, text=self.t["update_heading"], font=FONT_TITLE)
        lbl_title.pack(pady=(20, 10))

        lbl_msg = ctk.CTkLabel(self, text=self.t["update_msg"].format(cur=CURRENT_VERSION, latest=latest_ver), font=FONT_REGULAR, justify="center")
        lbl_msg.pack(pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15)

        btn_download = ctk.CTkButton(btn_frame, text=self.t["update_download"], fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, command=lambda: [webbrowser.open(release_url), self.destroy()])
        btn_download.pack(side="left", padx=8)

        btn_later = ctk.CTkButton(btn_frame, text=self.t["update_later"], fg_color="#45484E", hover_color="#5A5D65", command=self.destroy)
        btn_later.pack(side="left", padx=8)


class BioprinterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "EN"
        self.t = TRANSLATIONS[self.current_lang]

        self.title(self.t["login_title"])
        self.geometry("420x450")
        self.resizable(False, False)

        self.serial_conn = None
        self.is_connected = False
        self.current_user = None

        self.cmd_queue = queue.Queue()
        self.worker_thread = None

        self.loaded_gcode_lines = []
        self.loaded_file_name = ""
        self.is_printing = False
        self.is_paused = False
        self.cancel_print_flag = False
        self.print_index = 0

        self.controlled_buttons = []

        self.build_login_screen()

        self.update_idletasks()
        self.lift()
        self.focus_force()

    def build_login_screen(self):
        self.login_frame = ctk.CTkFrame(self, fg_color=COLOR_BG_CARD, corner_radius=12)
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=20)

        lang_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        lang_frame.pack(anchor="ne", padx=12, pady=(12, 0))
        self.lang_switch = ctk.CTkSegmentedButton(lang_frame, values=["EN", "ES"], width=70, height=24, command=self.change_login_language)
        self.lang_switch.set(self.current_lang)
        self.lang_switch.pack()

        self.lbl_login_title = ctk.CTkLabel(self.login_frame, text=self.t["operator_login"], font=FONT_TITLE)
        self.lbl_login_title.pack(pady=(10, 16))

        self.entry_user = ctk.CTkEntry(self.login_frame, placeholder_text=self.t["username"], width=280, height=36)
        self.entry_user.pack(pady=8)

        self.entry_pass = ctk.CTkEntry(self.login_frame, placeholder_text=self.t["password"], show="•", width=280, height=36)
        self.entry_pass.pack(pady=8)
        self.entry_pass.bind("<Return>", lambda event: self.attempt_login())

        self.lbl_login_error = ctk.CTkLabel(self.login_frame, text="", text_color="#EF5350", font=FONT_REGULAR)
        self.lbl_login_error.pack(pady=4)

        self.btn_login = ctk.CTkButton(
            self.login_frame, text=self.t["login_btn"], command=self.attempt_login,
            width=280, height=40, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=FONT_BUTTON
        )
        self.btn_login.pack(pady=(12, 16))

    def change_login_language(self, lang):
        self.current_lang = lang
        self.t = TRANSLATIONS[self.current_lang]
        self.title(self.t["login_title"])
        self.lbl_login_title.configure(text=self.t["operator_login"])
        self.entry_user.configure(placeholder_text=self.t["username"])
        self.entry_pass.configure(placeholder_text=self.t["password"])
        self.btn_login.configure(text=self.t["login_btn"])

    def attempt_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if username in USERS_DB and USERS_DB[username] == password:
            self.current_user = username
            self.login_frame.destroy()
            
            self.resizable(True, True)
            self.geometry("1160x860")
            self.minsize(1020, 740)
            
            self.build_ui()
            self.check_for_updates()
        else:
            self.lbl_login_error.configure(text=self.t["invalid_credentials"])

    def check_for_updates(self):
        def _worker():
            url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases/latest"
            try:
                response = requests.get(url, timeout=3.0)
                if response.status_code == 200:
                    data = response.json()
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    html_url = data.get("html_url", f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases")
                    if latest_tag and version.parse(latest_tag) > version.parse(CURRENT_VERSION):
                        self.after(0, lambda: UpdateDialog(self, latest_tag, html_url, lang=self.current_lang))
            except Exception:
                pass
        threading.Thread(target=_worker, daemon=True).start()

    def build_ui(self):
        self.build_header()
        self.build_connection_bar()

        self.tabs = ctk.CTkTabview(self, corner_radius=10, fg_color=COLOR_BG_CARD)
        self.tabs.pack(fill="both", expand=True, padx=16, pady=(6, 8))

        self.tab_prep = self.tabs.add("tab_prep")
        self.tab_print = self.tabs.add("tab_print")
        self.tab_terminal = self.tabs.add("tab_terminal")

        self.build_preparation_view(self.tab_prep)
        self.build_printing_view(self.tab_print)
        self.build_terminal_view(self.tab_terminal)

        self.build_sticky_footer()
        self.refresh_ui_texts()
        self.set_buttons_state("disabled")

    def build_header(self):
        self.header_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_BG_CARD, height=48)
        self.header_frame.pack(fill="x", padx=16, pady=(12, 6))

        self.lbl_app_name = ctk.CTkLabel(self.header_frame, text=self.t["app_name"], font=FONT_TITLE)
        self.lbl_app_name.pack(side="left", padx=16, pady=8)

        self.lang_selector = ctk.CTkSegmentedButton(self.header_frame, values=["EN", "ES"], width=80, height=28, command=self.switch_language)
        self.lang_selector.set(self.current_lang)
        self.lang_selector.pack(side="right", padx=16, pady=8)

        self.user_badge = ctk.CTkLabel(self.header_frame, text=f"{self.t['operator']}: {self.current_user}", font=FONT_REGULAR, text_color="#90CAF9")
        self.user_badge.pack(side="right", padx=12, pady=8)

    def build_connection_bar(self):
        self.conn_frame = ctk.CTkFrame(self, corner_radius=8, fg_color=COLOR_BG_CARD)
        self.conn_frame.pack(fill="x", padx=16, pady=4)

        self.lbl_port = ctk.CTkLabel(self.conn_frame, text=self.t["port"], font=FONT_REGULAR)
        self.lbl_port.pack(side="left", padx=(16, 6), pady=8)

        self.port_dropdown = ctk.CTkComboBox(self.conn_frame, values=self.get_serial_ports(), width=190)
        self.port_dropdown.pack(side="left", padx=4, pady=8)

        self.btn_refresh = ctk.CTkButton(self.conn_frame, text="↻", width=34, height=28, command=self.refresh_ports, fg_color="#45484E", hover_color="#5A5D65")
        self.btn_refresh.pack(side="left", padx=4, pady=8)

        self.baud_dropdown = ctk.CTkComboBox(self.conn_frame, values=["115200", "250000", "57600"], width=95)
        self.baud_dropdown.pack(side="left", padx=6, pady=8)
        self.baud_dropdown.set("115200")

        self.lbl_firmware = ctk.CTkLabel(self.conn_frame, text=self.t["firmware"], font=FONT_REGULAR)
        self.lbl_firmware.pack(side="left", padx=(8, 4), pady=8)

        self.firmware_dropdown = ctk.CTkComboBox(self.conn_frame, values=["Marlin", "Duet (RRF)"], width=115)
        self.firmware_dropdown.pack(side="left", padx=4, pady=8)
        self.firmware_dropdown.set("Marlin")

        self.btn_connect = ctk.CTkButton(self.conn_frame, text=self.t["connect"], command=self.toggle_connection, width=100, height=30, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=FONT_BUTTON)
        self.btn_connect.pack(side="left", padx=10, pady=8)

        self.status_pill = ctk.CTkLabel(self.conn_frame, text=self.t["disconnected"], text_color="#E57373", font=FONT_BUTTON)
        self.status_pill.pack(side="left", padx=10, pady=8)

    def center_carriage(self, target_x=CENTER_X, target_y=CENTER_Y):
        self.send_gcode(f"G90\nG1 X{target_x:.2f} Y{target_y:.2f} F1500")

    def build_preparation_view(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_rowconfigure(0, weight=1)

        card_jog = ctk.CTkFrame(container, corner_radius=10, fg_color="#232528")
        card_jog.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

        self.lbl_jog_title = ctk.CTkLabel(card_jog, text="", font=FONT_SUBTITLE)
        self.lbl_jog_title.pack(pady=(12, 6))

        step_box = ctk.CTkFrame(card_jog, fg_color="transparent")
        step_box.pack(pady=6)
        self.lbl_step = ctk.CTkLabel(step_box, text="", font=FONT_REGULAR)
        self.lbl_step.pack(side="left", padx=6)
        self.step_selector = ctk.CTkSegmentedButton(step_box, values=["0.1 mm", "1 mm", "10 mm", "50 mm"])
        self.step_selector.set("10 mm")
        self.step_selector.pack(side="left", padx=6)

        home_box = ctk.CTkFrame(card_jog, fg_color="transparent")
        home_box.pack(pady=6)

        self.btn_home_all = ctk.CTkButton(home_box, text="", width=110, height=32, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=FONT_BUTTON, command=lambda: self.send_gcode("G28"))
        self.btn_home_all.pack(side="left", padx=3)

        self.btn_center = ctk.CTkButton(home_box, text="", width=110, height=32, fg_color="#37474F", hover_color="#455A64", font=FONT_BUTTON, command=self.center_carriage)
        self.btn_center.pack(side="left", padx=3)

        self.btn_home_z = ctk.CTkButton(home_box, text="", width=85, height=32, fg_color="#45484E", hover_color="#5A5D65", font=FONT_BUTTON, command=lambda: self.send_gcode("G28 Z"))
        self.btn_home_z.pack(side="left", padx=3)

        self.controlled_buttons.extend([self.btn_home_all, self.btn_center, self.btn_home_z])

        dpad_container = ctk.CTkFrame(card_jog, fg_color="transparent")
        dpad_container.pack(pady=12)

        xy_frame = ctk.CTkFrame(dpad_container, fg_color="transparent")
        xy_frame.pack(side="left", padx=(10, 24))

        btn_y_pos = ctk.CTkButton(xy_frame, text="▲ Y+", width=75, height=40, font=FONT_BUTTON, command=lambda: self.jog_axis("Y", 1))
        btn_y_pos.grid(row=0, column=1, padx=4, pady=4)
        btn_x_neg = ctk.CTkButton(xy_frame, text="◄ X-", width=75, height=40, font=FONT_BUTTON, command=lambda: self.jog_axis("X", -1))
        btn_x_neg.grid(row=1, column=0, padx=4, pady=4)
        btn_x_pos = ctk.CTkButton(xy_frame, text="X+ ►", width=75, height=40, font=FONT_BUTTON, command=lambda: self.jog_axis("X", 1))
        btn_x_pos.grid(row=1, column=2, padx=4, pady=4)
        btn_y_neg = ctk.CTkButton(xy_frame, text="▼ Y-", width=75, height=40, font=FONT_BUTTON, command=lambda: self.jog_axis("Y", -1))
        btn_y_neg.grid(row=2, column=1, padx=4, pady=4)

        z_frame = ctk.CTkFrame(dpad_container, fg_color="transparent")
        z_frame.pack(side="left", padx=10)

        self.lbl_axis_z = ctk.CTkLabel(z_frame, text="", font=FONT_SUBTITLE)
        self.lbl_axis_z.pack(pady=(0, 4))
        
        # Inversión visual: '▲ Subir' envía -1 a Marlin (sube la cama) y '▼ Bajar' envía +1 (baja la cama)
        self.btn_z_pos = ctk.CTkButton(z_frame, text="", width=115, height=42, fg_color="#37474F", hover_color="#455A64", font=FONT_BUTTON, command=lambda: self.jog_axis("Z", -1))
        self.btn_z_pos.pack(pady=4)
        self.btn_z_neg = ctk.CTkButton(z_frame, text="", width=115, height=42, fg_color="#37474F", hover_color="#455A64", font=FONT_BUTTON, command=lambda: self.jog_axis("Z", 1))
        self.btn_z_neg.pack(pady=4)

        self.controlled_buttons.extend([btn_y_pos, btn_y_neg, btn_x_neg, btn_x_pos, self.btn_z_pos, self.btn_z_neg])

        card_dispenser = ctk.CTkFrame(container, corner_radius=10, fg_color="#232528")
        card_dispenser.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)

        self.lbl_dispenser_title = ctk.CTkLabel(card_dispenser, text="", font=FONT_SUBTITLE)
        self.lbl_dispenser_title.pack(pady=(12, 10))

        param_grid = ctk.CTkFrame(card_dispenser, fg_color="transparent")
        param_grid.pack(pady=10)

        self.lbl_dist = ctk.CTkLabel(param_grid, text="", font=FONT_REGULAR)
        self.lbl_dist.grid(row=0, column=0, padx=6, pady=8, sticky="e")
        self.ext_dist_combo = ctk.CTkComboBox(param_grid, values=["0.1 mm", "0.5 mm", "1.0 mm", "2.0 mm", "5.0 mm", "10.0 mm"], width=120)
        self.ext_dist_combo.set("1.0 mm")
        self.ext_dist_combo.grid(row=0, column=1, padx=6, pady=8)

        self.lbl_speed_unit = ctk.CTkLabel(param_grid, text="", font=FONT_REGULAR)
        self.lbl_speed_unit.grid(row=1, column=0, padx=6, pady=8, sticky="e")
        self.ext_speed_entry = ctk.CTkEntry(param_grid, width=120)
        self.ext_speed_entry.insert(0, "120")
        self.ext_speed_entry.grid(row=1, column=1, padx=6, pady=8)

        btn_box = ctk.CTkFrame(card_dispenser, fg_color="transparent")
        btn_box.pack(pady=16)

        self.btn_extrude = ctk.CTkButton(btn_box, text="", width=160, height=44, fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, text_color="#FFFFFF", font=FONT_BUTTON, command=lambda: self.dispense(direction=1))
        self.btn_extrude.pack(side="left", padx=8)

        self.btn_reverse = ctk.CTkButton(btn_box, text="", width=150, height=44, fg_color=COLOR_RETRACT, hover_color=COLOR_RETRACT_HOVER, text_color="#FFFFFF", font=FONT_BUTTON, command=lambda: self.dispense(direction=-1))
        self.btn_reverse.pack(side="left", padx=8)

        self.controlled_buttons.extend([self.btn_extrude, self.btn_reverse])

    def build_printing_view(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=12, pady=12)

        card_file = ctk.CTkFrame(container, corner_radius=10, fg_color="#232528")
        card_file.pack(fill="x", pady=6)

        self.lbl_file_section = ctk.CTkLabel(card_file, text="", font=FONT_SUBTITLE)
        self.lbl_file_section.pack(pady=(12, 6))

        file_row = ctk.CTkFrame(card_file, fg_color="transparent")
        file_row.pack(fill="x", padx=16, pady=8)

        self.btn_load_file = ctk.CTkButton(file_row, text="", width=190, height=36, fg_color="#45484E", hover_color="#5A5D65", font=FONT_BUTTON, command=self.load_gcode_file)
        self.btn_load_file.pack(side="left", padx=4)

        self.lbl_loaded_file = ctk.CTkLabel(file_row, text="", font=FONT_REGULAR, text_color="#90A4AE")
        self.lbl_loaded_file.pack(side="left", padx=16)

        self.progress_bar = ctk.CTkProgressBar(card_file, progress_color=COLOR_PRIMARY, height=14)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=24, pady=(12, 4))

        self.lbl_progress = ctk.CTkLabel(card_file, text="", font=FONT_REGULAR, text_color="#B0BEC5")
        self.lbl_progress.pack(pady=(0, 10))

        macro_btn_row = ctk.CTkFrame(card_file, fg_color="transparent")
        macro_btn_row.pack(pady=(4, 16))

        self.btn_start_print = ctk.CTkButton(macro_btn_row, text="", width=180, height=40, fg_color=COLOR_SUCCESS, hover_color=COLOR_SUCCESS_HOVER, font=FONT_BUTTON, command=self.start_print_job)
        self.btn_start_print.pack(side="left", padx=8)

        self.btn_pause_print = ctk.CTkButton(macro_btn_row, text="", width=120, height=40, fg_color="#37474F", hover_color="#455A64", font=FONT_BUTTON, command=self.toggle_pause_job)
        self.btn_pause_print.pack(side="left", padx=8)

        self.btn_cancel_print = ctk.CTkButton(macro_btn_row, text="", width=120, height=40, fg_color="#45484E", hover_color="#5A5D65", font=FONT_BUTTON, command=self.cancel_print_job)
        self.btn_cancel_print.pack(side="left", padx=8)

        self.controlled_buttons.extend([self.btn_start_print, self.btn_pause_print, self.btn_cancel_print])

        card_overrides = ctk.CTkFrame(container, corner_radius=10, fg_color="#232528")
        card_overrides.pack(fill="x", pady=10)

        self.lbl_overrides_title = ctk.CTkLabel(card_overrides, text="", font=FONT_SUBTITLE)
        self.lbl_overrides_title.pack(pady=(12, 6))

        speed_row = ctk.CTkFrame(card_overrides, fg_color="transparent")
        speed_row.pack(fill="x", padx=20, pady=8)
        self.lbl_speed_val = ctk.CTkLabel(speed_row, text="", width=160, anchor="w", font=FONT_REGULAR)
        self.lbl_speed_val.pack(side="left")
        self.slider_speed = ctk.CTkSlider(speed_row, from_=10, to=250, number_of_steps=48, command=self.on_speed_slide)
        self.slider_speed.set(100)
        self.slider_speed.pack(side="left", fill="x", expand=True, padx=12)
        self.btn_apply_speed = ctk.CTkButton(speed_row, text="", width=80, height=30, fg_color="#45484E", hover_color="#5A5D65", command=self.apply_speed)
        self.btn_apply_speed.pack(side="left")

        flow_row = ctk.CTkFrame(card_overrides, fg_color="transparent")
        flow_row.pack(fill="x", padx=20, pady=(8, 16))
        self.lbl_flow_val = ctk.CTkLabel(flow_row, text="", width=180, anchor="w", font=FONT_REGULAR)
        self.lbl_flow_val.pack(side="left")
        self.slider_flow = ctk.CTkSlider(flow_row, from_=10, to=250, number_of_steps=48, command=self.on_flow_slide)
        self.slider_flow.set(100)
        self.slider_flow.pack(side="left", fill="x", expand=True, padx=12)
        self.btn_apply_flow = ctk.CTkButton(flow_row, text="", width=80, height=30, fg_color="#45484E", hover_color="#5A5D65", command=self.apply_flow)
        self.btn_apply_flow.pack(side="left")

        self.controlled_buttons.extend([self.btn_apply_speed, self.btn_apply_flow])

    def build_terminal_view(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        self.lbl_term_title = ctk.CTkLabel(container, text="", font=FONT_SUBTITLE)
        self.lbl_term_title.pack(pady=(6, 4))

        self.txt_log = ctk.CTkTextbox(container, state="disabled", wrap="word", font=("Menlo", 12), fg_color="#18191B")
        self.txt_log.pack(fill="both", expand=True, padx=8, pady=(4, 8))

        cmd_bar = ctk.CTkFrame(container, fg_color="transparent")
        cmd_bar.pack(fill="x", padx=8, pady=(0, 6))

        self.entry_cmd = ctk.CTkEntry(cmd_bar, placeholder_text="")
        self.entry_cmd.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_cmd.bind("<Return>", lambda event: self.send_manual_command())

        self.btn_send_cmd = ctk.CTkButton(cmd_bar, text="", width=90, height=32, command=self.send_manual_command, fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER, font=FONT_BUTTON)
        self.btn_send_cmd.pack(side="left")
        self.controlled_buttons.append(self.btn_send_cmd)

    def build_sticky_footer(self):
        footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#18191B", height=60)
        footer_frame.pack(fill="x", side="bottom")

        self.btn_estop = ctk.CTkButton(footer_frame, text="", command=self.emergency_stop, fg_color=COLOR_DANGER, hover_color=COLOR_DANGER_HOVER, font=FONT_TITLE, height=44)
        self.btn_estop.pack(fill="x", padx=16, pady=8)
        self.controlled_buttons.append(self.btn_estop)

    def refresh_ui_texts(self):
        self.t = TRANSLATIONS[self.current_lang]
        self.title(self.t["app_title"])

        self.lbl_app_name.configure(text=self.t["app_name"])
        self.user_badge.configure(text=f"{self.t['operator']}: {self.current_user}")
        self.lbl_port.configure(text=self.t["port"])
        self.lbl_firmware.configure(text=self.t["firmware"])
        self.btn_connect.configure(text=self.t["disconnect"] if self.is_connected else self.t["connect"])
        if not self.is_connected:
            self.status_pill.configure(text=self.t["disconnected"])
        else:
            self.status_pill.configure(text=f"{self.t['connected']} ({self.serial_conn.port})")

        try:
            tab_buttons = self.tabs._segmented_button._buttons_dict
            tab_buttons["tab_prep"].configure(text=self.t["tab_prep"])
            tab_buttons["tab_print"].configure(text=self.t["tab_print"])
            tab_buttons["tab_terminal"].configure(text=self.t["tab_terminal"])
        except Exception:
            pass

        self.lbl_jog_title.configure(text=self.t["jog_title"])
        self.lbl_step.configure(text=self.t["step_label"])
        self.btn_home_all.configure(text=self.t["home_all"])
        self.btn_center.configure(text=self.t["center_bed"])
        self.btn_home_z.configure(text=self.t["home_z"])
        self.lbl_axis_z.configure(text=self.t["axis_z"])
        self.btn_z_pos.configure(text=self.t["z_up"])
        self.btn_z_neg.configure(text=self.t["z_down"])

        self.lbl_dispenser_title.configure(text=self.t["dispenser_title"])
        self.lbl_dist.configure(text=self.t["distance"])
        self.lbl_speed_unit.configure(text=self.t["speed_unit"])
        self.btn_extrude.configure(text=self.t["extrude"])
        self.btn_reverse.configure(text=self.t["retract"])

        self.lbl_file_section.configure(text=self.t["file_title"])
        self.btn_load_file.configure(text=self.t["load_file"])
        if not self.loaded_file_name:
            self.lbl_loaded_file.configure(text=self.t["no_file"])
        self.btn_start_print.configure(text=self.t["start_print"])
        self.btn_pause_print.configure(text=self.t["resume"] if self.is_paused else self.t["pause"])
        self.btn_cancel_print.configure(text=self.t["cancel"])

        self.lbl_overrides_title.configure(text=self.t["overrides_title"])
        self.lbl_speed_val.configure(text=self.t["speed_override"].format(val=int(self.slider_speed.get())))
        self.lbl_flow_val.configure(text=self.t["flow_override"].format(val=int(self.slider_flow.get())))
        self.btn_apply_speed.configure(text=self.t["apply"])
        self.btn_apply_flow.configure(text=self.t["apply"])

        total_lines = len(self.loaded_gcode_lines)
        if total_lines > 0:
            current_progress = int(self.progress_bar.get() * total_lines)
            pct = int(self.progress_bar.get() * 100)
            self.lbl_progress.configure(text=self.t["lines_progress"].format(cur=current_progress, tot=total_lines, pct=pct))
        else:
            self.lbl_progress.configure(text=self.t["lines_progress"].format(cur=0, tot=0, pct=0))

        self.lbl_term_title.configure(text=self.t["terminal_title"])
        self.entry_cmd.configure(placeholder_text=self.t["cmd_placeholder"])
        self.btn_send_cmd.configure(text=self.t["send"])
        self.btn_estop.configure(text=self.t["emergency_stop"])

    def switch_language(self, lang):
        self.current_lang = lang
        self.refresh_ui_texts()

    def get_serial_ports(self):
        ports = [p.device for p in serial.tools.list_ports.comports()]
        return ports if ports else [self.t["no_ports"]]

    def refresh_ports(self):
        ports = self.get_serial_ports()
        self.port_dropdown.configure(values=ports)
        self.port_dropdown.set(ports[0])

    def toggle_connection(self):
        if not self.is_connected:
            port = self.port_dropdown.get()
            baud = int(self.baud_dropdown.get())
            if port == self.t["no_ports"] or "No ports" in port or "No se detectaron" in port:
                self.log("ERROR: No valid serial port selected.")
                return
            try:
                self.serial_conn = serial.Serial(port, baud, timeout=0.01)
                self.serial_conn.dtr = True
                self.serial_conn.rts = True
                time.sleep(1.2)

                self.serial_conn.reset_input_buffer()

                self.is_connected = True
                self.btn_connect.configure(text=self.t["disconnect"], fg_color="#555A60", hover_color="#666C73")
                self.status_pill.configure(text=f"{self.t['connected']} ({port})", text_color="#81C784")
                self.set_buttons_state("normal")
                self.log(f"Connected to {port} @ {baud} baud.")

                self.worker_thread = threading.Thread(target=self._serial_worker_loop, daemon=True)
                self.worker_thread.start()

                self.send_gcode("M110 N0")
                self.send_gcode("M999")
                target_fw = self.firmware_dropdown.get()
                init_ext = "M302 S0" if "Marlin" in target_fw else "M302 P1"
                self.send_gcode(init_ext)
                self.send_gcode("G90")
            except Exception as ex:
                self.log(f"Connection error: {str(ex)}")
        else:
            self.disconnect()

    def disconnect(self):
        self.is_connected = False
        self.is_printing = False
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except Exception:
                pass
        self.btn_connect.configure(text=self.t["connect"], fg_color=COLOR_PRIMARY, hover_color=COLOR_PRIMARY_HOVER)
        self.status_pill.configure(text=self.t["disconnected"], text_color="#E57373")
        self.set_buttons_state("disabled")
        self.log("Serial port disconnected.")

    def set_buttons_state(self, state: str):
        for btn in self.controlled_buttons:
            try:
                btn.configure(state=state)
            except Exception:
                pass

    def send_gcode(self, commands: str):
        if not self.is_connected:
            self.log(self.t["not_connected_warning"])
            return
        for line in commands.strip().split("\n"):
            clean_cmd = line.strip()
            if clean_cmd:
                self.cmd_queue.put(clean_cmd)

    def send_manual_command(self):
        cmd = self.entry_cmd.get().strip()
        if cmd:
            self.send_gcode(cmd)
            self.entry_cmd.delete(0, "end")

    def _serial_worker_loop(self):
        while self.is_connected and self.serial_conn and self.serial_conn.is_open:
            try:
                cmd = self.cmd_queue.get_nowait()
                self._send_and_wait_ack(cmd)
                self.cmd_queue.task_done()
                continue
            except queue.Empty:
                pass

            if self.is_printing and not self.is_paused and not self.cancel_print_flag:
                if self.print_index < len(self.loaded_gcode_lines):
                    cmd = self.loaded_gcode_lines[self.print_index]
                    self._send_and_wait_ack(cmd)
                    self.print_index += 1

                    total = len(self.loaded_gcode_lines)
                    if self.print_index % 10 == 0 or self.print_index == total:
                        prog = self.print_index / total
                        self.after(0, self._update_progress_ui, self.print_index, total, prog)
                else:
                    self.is_printing = False
                    self.log(self.t["job_completed"])
                    self.after(0, self._reset_print_controls)
                continue

            time.sleep(0.002)

    def _send_and_wait_ack(self, cmd: str):
        try:
            clean = cmd.strip()
            if not clean:
                return

            msg = (clean + "\n").encode("ascii", errors="replace")
            self.serial_conn.write(msg)
            self.serial_conn.flush()

            self.log(f"TX >> {clean}")

            while self.is_connected and not self.cancel_print_flag:
                line = self.serial_conn.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    if "echo:busy" in line:
                        continue
                    if not line.startswith("ok"):
                        self.log(f"RX << {line}")
                    if line.startswith("ok") or line == "ok":
                        break
        except Exception as ex:
            self.log(f"TX Error: {str(ex)}")

    def load_gcode_file(self):
        file_path = filedialog.askopenfilename(
            title="Select G-code File",
            filetypes=[("G-code Files", ".gcode *.gco *.nc"), ("All Files", ".*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_lines = f.readlines()

            target_fw = self.firmware_dropdown.get()
            clean_lines = []

            for line in raw_lines:
                stmt = line.split(";")[0].strip()
                if not stmt:
                    continue

                stmt_upper = stmt.upper()

                # Se omiten comandos térmicos/ventiladores no aplicables en bioprinting
                if any(stmt_upper.startswith(skip_cmd) for skip_cmd in ["M109", "M190", "M104", "M140", "M106", "M107"]):
                    continue

                if stmt_upper == "T0":
                    continue

                # Se preservan todos los G92 (incluidos offsets y resets de dispensador)
                if stmt_upper.startswith("M302"):
                    stmt = "M302 S0" if "Marlin" in target_fw else "M302 P1"

                clean_lines.append(stmt)

            self.loaded_gcode_lines = clean_lines
            self.loaded_file_name = file_path.split("/")[-1].split("\\")[-1]
            self.lbl_loaded_file.configure(
                text=f"{self.loaded_file_name} ({len(clean_lines)} cmd)", text_color="#E0E0E0"
            )
            self.progress_bar.set(0)
            self.lbl_progress.configure(
                text=self.t["lines_progress"].format(cur=0, tot=len(clean_lines), pct=0)
            )
            self.log(self.t["file_loaded_msg"].format(name=self.loaded_file_name, count=len(clean_lines)))
        except Exception as e:
            self.log(f"File load error: {str(e)}")

    def start_print_job(self):
        if not self.is_connected:
            self.log(self.t["not_connected_warning"])
            return

        if not self.loaded_gcode_lines:
            self.log(self.t["need_file_warning"])
            return

        # Sincronización explícita para evitar que la macro arranque en coordenadas relativas
        self.send_gcode("G90\nM82")

        self.print_index = 0
        self.is_printing = True
        self.is_paused = False
        self.cancel_print_flag = False

        self.btn_start_print.configure(state="disabled")
        self.btn_pause_print.configure(state="normal", text=self.t["pause"])
        self.btn_cancel_print.configure(state="normal")
        self.log(self.t["job_started"].format(name=self.loaded_file_name))

    def _reset_print_controls(self):
        self.btn_start_print.configure(state="normal")
        self.btn_pause_print.configure(state="disabled")
        self.btn_cancel_print.configure(state="disabled")

    def _update_progress_ui(self, current_line, total_lines, progress):
        self.progress_bar.set(progress)
        self.lbl_progress.configure(
            text=self.t["lines_progress"].format(cur=current_line, tot=total_lines, pct=int(progress * 100))
        )

    def toggle_pause_job(self):
        if not self.is_printing:
            return
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause_print.configure(text=self.t["resume"])
            self.log("Job paused.")
        else:
            self.btn_pause_print.configure(text=self.t["pause"])
            self.log("Job resumed.")

    def cancel_print_job(self):
        if self.is_printing:
            self.cancel_print_flag = True
            self.is_printing = False
            self.log(self.t["job_cancelled"])
            self._reset_print_controls()

    def jog_axis(self, axis: str, sign: int):
        try:
            raw_step = self.step_selector.get()
            cleaned_step = raw_step.lower().replace("mm", "").replace("m", "").strip()
            step = float(cleaned_step) * sign
            feedrate = 1200 if axis in ["X", "Y"] else 300
            self.send_gcode(f"G91\nG1 {axis}{step:.2f} F{feedrate}\nG90")
        except ValueError:
            self.log("Invalid step size value.")

    def dispense(self, direction: int):
        try:
            raw_dist = self.ext_dist_combo.get()
            cleaned_dist = raw_dist.lower().replace("mm", "").replace("m", "").strip()
            distance = float(cleaned_dist) * direction

            raw_speed = self.ext_speed_entry.get()
            cleaned_speed = raw_speed.lower().replace("mm/min", "").replace("mm", "").strip()
            speed = float(cleaned_speed)

            self.send_gcode(f"M83\nG1 E{distance:.2f} F{speed:.0f}\nM82")
        except ValueError:
            self.log("Invalid distance or speed values.")

    def on_speed_slide(self, val):
        self.lbl_speed_val.configure(text=self.t["speed_override"].format(val=int(val)))

    def apply_speed(self):
        val = int(self.slider_speed.get())
        self.send_gcode(f"M220 S{val}")
        self.log(f"Print speed override set to {val}%")

    def on_flow_slide(self, val):
        self.lbl_flow_val.configure(text=self.t["flow_override"].format(val=int(val)))

    def apply_flow(self):
        val = int(self.slider_flow.get())
        self.send_gcode(f"M221 S{val}")
        self.log(f"Flow rate override set to {val}%")

    def emergency_stop(self):
        if self.is_printing:
            self.cancel_print_job()
        while not self.cmd_queue.empty():
            try:
                self.cmd_queue.get_nowait()
            except queue.Empty:
                break
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(b"M112\n")
                self.serial_conn.flush()
                self.log(self.t["estop_sent"])
            except Exception as ex:
                self.log(f"Emergency stop error: {str(ex)}")

    def log(self, message: str):
        def _append():
            try:
                self.txt_log.configure(state="normal")
                self.txt_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
                self.txt_log.see("end")
                self.txt_log.configure(state="disabled")
            except Exception:
                pass
        self.after(0, _append)


if __name__ == "__main__":
    app = BioprinterApp()
    app.mainloop()