import requests
import json
import time
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import threading
import webbrowser
import pystray
import json
import sys
import traceback
import winsound

class ConfigManager:
    def __init__(self):
        self.config_file = "config.json"
        self.load_config()
        
    def load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "user_id": "",
                "osCsid": "",
                "update_interval": 60
            }
            self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def show_config_window(self):
        # Crear ventana de configuración
        config_window = tk.Toplevel()
        config_window.title("Configuración - IMVU Notify")
        config_window.geometry("450x380")
        config_window.resizable(False, False)
        config_window.configure(bg='#1e1e1e')
        
        # Estilo personalizado
        style = ttk.Style()
        style.configure('Config.TFrame', background='#1e1e1e')
        style.configure('Config.TLabel', 
                       background='#1e1e1e',
                       foreground='#ffffff',
                       font=('Segoe UI', 10))
        style.configure('Config.TEntry',
                       fieldbackground='#2d2d2d',
                       foreground='#ffffff',
                       insertcolor='#ffffff',
                       borderwidth=0)
        style.configure('Config.TButton',
                       background='#007acc',
                       foreground='#ffffff',
                       padding=10,
                       font=('Segoe UI', 10))
        
        # Frame principal con padding
        main_frame = ttk.Frame(config_window, style='Config.TFrame', padding="30 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame, style='Config.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame,
                             text="Configuración de IMVU Notify",
                             font=('Segoe UI', 16, 'bold'),
                             fg='#007acc',
                             bg='#1e1e1e')
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                text="Configura tus credenciales para comenzar",
                                font=('Segoe UI', 9),
                                fg='#cccccc',
                                bg='#1e1e1e')
        subtitle_label.pack()
        
        # Frame para entradas
        entries_frame = ttk.Frame(main_frame, style='Config.TFrame')
        entries_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Estilo para los campos de entrada
        class CustomEntry(tk.Entry):
            def __init__(self, master, placeholder, **kwargs):
                super().__init__(master, **kwargs)
                self.placeholder = placeholder
                self.placeholder_color = '#666666'
                self.default_fg_color = '#ffffff'
                
                self.bind("<FocusIn>", self._on_focus_in)
                self.bind("<FocusOut>", self._on_focus_out)
            
            def _on_focus_in(self, event):
                if self.get() == self.placeholder:
                    self.delete(0, tk.END)
                    self.config(fg=self.default_fg_color)
            
            def _on_focus_out(self, event):
                if not self.get():
                    self.insert(0, self.placeholder)
                    self.config(fg=self.placeholder_color)

            def insert_with_placeholder(self, index, text):
                if text:  # Si hay texto (datos del config)
                    self.config(fg=self.default_fg_color)
                    super().insert(index, text)
                else:  # Si no hay texto, mostrar placeholder
                    self.config(fg=self.placeholder_color)
                    super().insert(index, self.placeholder)
        
        # Frame para ID de Usuario
        user_frame = ttk.Frame(entries_frame, style='Config.TFrame')
        user_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(user_frame, 
                 text="ID de Usuario",
                 style='Config.TLabel').pack(anchor='w', pady=(0, 5))
        
        user_id_entry = CustomEntry(user_frame,
                                  placeholder="Ingresa tu ID de usuario de IMVU",
                                  font=('Segoe UI', 10),
                                  bg='#2d2d2d',
                                  fg='#ffffff',
                                  insertbackground='#ffffff',
                                  relief=tk.FLAT,
                                  width=40)
        user_id_entry.pack(fill=tk.X, ipady=8)
        user_id_entry.insert_with_placeholder(0, self.config.get("user_id", ""))
        
        # Frame para Cookie
        cookie_frame = ttk.Frame(entries_frame, style='Config.TFrame')
        cookie_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(cookie_frame,
                 text="Cookie osCsid",
                 style='Config.TLabel').pack(anchor='w', pady=(0, 5))
        
        oscid_entry = CustomEntry(cookie_frame,
                                placeholder="Ingresa tu cookie osCsid",
                                font=('Segoe UI', 10),
                                bg='#2d2d2d',
                                fg='#ffffff',
                                insertbackground='#ffffff',
                                relief=tk.FLAT,
                                width=40)
        oscid_entry.pack(fill=tk.X, ipady=8)
        oscid_entry.insert_with_placeholder(0, self.config.get("osCsid", ""))
        
        # Frame para intervalo de actualización
        interval_frame = ttk.Frame(entries_frame, style='Config.TFrame')
        interval_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(interval_frame,
                 text="Intervalo de Actualización (segundos)",
                 style='Config.TLabel').pack(anchor='w', pady=(0, 5))
        
        interval_entry = CustomEntry(interval_frame,
                                  placeholder="60",
                                  font=('Segoe UI', 10),
                                  bg='#2d2d2d',
                                  fg='#ffffff',
                                  insertbackground='#ffffff',
                                  relief=tk.FLAT,
                                  width=40)
        interval_entry.pack(fill=tk.X, ipady=8)
        interval_entry.insert_with_placeholder(0, str(self.config.get("update_interval", "60")))
        
        def validate_interval(event=None):
            try:
                value = interval_entry.get()
                if value == interval_entry.placeholder:
                    return True
                    
                interval = int(value)
                if interval < 10:  
                    interval_entry.config(fg='#ff6b6b')
                    return False
                interval_entry.config(fg=interval_entry.default_fg_color)
                return True
            except ValueError:
                interval_entry.config(fg='#ff6b6b')
                return False
        
        interval_entry.bind('<KeyRelease>', validate_interval)
        
        # Frame para botones con efecto hover
        button_frame = ttk.Frame(main_frame, style='Config.TFrame')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        class HoverButton(tk.Label):
            def __init__(self, master, text, command=None, primary=False, **kwargs):
                super().__init__(master, text=text, **kwargs)
                self.primary = primary
                self.normal_bg = '#007acc' if primary else '#2d2d2d'
                self.hover_bg = '#0098ff' if primary else '#3d3d3d'
                self.configure(
                    bg=self.normal_bg,
                    fg='#ffffff',
                    font=('Segoe UI', 10),
                    cursor='hand2',
                    pady=10
                )
                self.bind('<Enter>', self._on_enter)
                self.bind('<Leave>', self._on_leave)
                self.bind('<Button-1>', lambda e: command() if command else None)
            
            def _on_enter(self, e):
                self['background'] = self.hover_bg
            
            def _on_leave(self, e):
                self['background'] = self.normal_bg
        
        def save_and_close():
            if not validate_interval():
                return
                
            self.config["user_id"] = user_id_entry.get()
            self.config["osCsid"] = oscid_entry.get()
            
            interval = interval_entry.get()
            if interval and interval != interval_entry.placeholder:
                self.config["update_interval"] = int(interval)
            else:
                self.config["update_interval"] = 60
                
            self.save_config()
            config_window.destroy()
        
        def cancel():
            config_window.destroy()
        
        # Botones
        save_button = HoverButton(button_frame,
                                text=" Guardar Cambios",
                                command=save_and_close,
                                primary=True)
        save_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        cancel_button = HoverButton(button_frame,
                                  text=" Cancelar",
                                  command=cancel)
        cancel_button.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Centrar la ventana
        config_window.update_idletasks()
        width = config_window.winfo_width()
        height = config_window.winfo_height()
        x = (config_window.winfo_screenwidth() // 2) - (width // 2)
        y = (config_window.winfo_screenheight() // 2) - (height // 2)
        config_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Hacer la ventana modal
        config_window.transient(self.config_window if hasattr(self, 'config_window') else None)
        config_window.grab_set()

class SystemTrayIcon:
    def __init__(self, config_manager, monitor):
        self.config_manager = config_manager
        self.monitor = monitor
        self.create_icon()
    
    def create_icon(self):
        # Crear un ícono simple
        image = Image.new('RGB', (64, 64), color='red')
        menu = pystray.Menu(
            pystray.MenuItem("Ver Usuarios en Línea", self.show_online_users),
            pystray.MenuItem("Configuración", self.show_config),
            pystray.MenuItem("Salir", self.quit_application)
        )
        self.icon = pystray.Icon("Vu_Notificacion", image, "Vu_Notificacion", menu)
    
    def show_online_users(self, icon, item):
        OnlineUsersWindow(self.monitor)
    
    def show_config(self, icon, item):
        self.config_manager.show_config_window()
    
    def quit_application(self, icon, item):
        self.icon.stop()
        sys.exit()
    
    def run(self):
        self.icon.run()

class NotificationManager:
    _instance = None
    _notifications = []
    _offset = 0
    _root = None
    _panel = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            # Crear la ventana raíz oculta
            cls._root = tk.Tk()
            cls._root.withdraw()  # Ocultar la ventana raíz
            
            # Crear el panel de notificaciones
            cls._panel = tk.Toplevel(cls._root)
            cls._panel.overrideredirect(True)
            cls._panel.attributes('-alpha', 0.0)  # Invisible inicialmente
            cls._panel.attributes('-transparentcolor', '#1a1a1a')  # Hacer transparente el fondo
            cls._panel.configure(bg='#1a1a1a')
            
            # Configurar el panel
            screen_width = cls._root.winfo_screenwidth()
            screen_height = cls._root.winfo_screenheight()
            panel_width = 320  # Un poco más ancho que las notificaciones
            panel_height = 600  # Altura máxima para el panel
            
            # Posicionar en la esquina inferior derecha
            x = screen_width - panel_width - 20
            y = screen_height - panel_height - 60
            cls._panel.geometry(f'{panel_width}x{panel_height}+{x}+{y}')
            
            # Frame principal con efecto de vidrio
            main_frame = tk.Frame(cls._panel, bg='#1a1a1a')
            main_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Canvas con efecto de vidrio
            canvas = tk.Canvas(main_frame, 
                             bg='#1a1a1a',
                             highlightthickness=0,
                             bd=0)
            canvas.pack(side='left', fill='both', expand=True)
            
            # Scrollbar personalizado
            scrollbar = tk.Scrollbar(main_frame,
                                   orient='vertical',
                                   command=canvas.yview,
                                   width=10)
            scrollbar.pack(side='right', fill='y', padx=(2, 0))
            
            # Configurar el scrollbar
            scrollbar.configure(bg='#2d2d2d',
                              activebackground='#3d3d3d',
                              troughcolor='#1a1a1a',
                              bd=0,
                              relief='flat')
            
            # Frame contenedor para las notificaciones
            cls._scroll_frame = tk.Frame(canvas, bg='#1a1a1a')
            cls._scroll_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            # Crear ventana en el canvas
            canvas.create_window((0, 0), 
                               window=cls._scroll_frame,
                               anchor="nw",
                               width=panel_width-25)
            
            # Configurar el scroll del canvas
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Hacer el panel invisible al mouse cuando no hay notificaciones
            cls._panel.bind('<Enter>', cls._on_panel_enter)
            cls._panel.bind('<Leave>', cls._on_panel_leave)
            
            # Configurar el scroll con el mouse
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            cls._panel.bind_all("<MouseWheel>", _on_mousewheel)
            
        return cls._instance
    
    @classmethod
    def _on_panel_enter(cls, event):
        # Cuando el mouse entra al panel, detener todos los temporizadores
        for notif in cls._notifications:
            notif.stop_timer()
    
    @classmethod
    def _on_panel_leave(cls, event):
        # Cuando el mouse sale del panel, reiniciar los temporizadores
        for notif in cls._notifications:
            notif.start_timer()
    
    def add_notification(self, notification):
        self._notifications.append(notification)
        notification.window.pack(in_=self._scroll_frame, fill=tk.X, padx=5, pady=5)
        self._update_panel_visibility()
    
    def remove_notification(self, notification):
        if notification in self._notifications:
            self._notifications.remove(notification)
            self._update_panel_visibility()
    
    def _update_panel_visibility(self):
        if self._notifications:
            self._panel.attributes('-alpha', 1.0)
        else:
            self._panel.attributes('-alpha', 0.0)
    
    @property
    def root(self):
        return self._root

    def show_notifications(self, online_users):
        if not online_users:
            return
            
        # Reproducir sonido una sola vez para todas las notificaciones
        self.play_notification_sound()
        
        for username, user_data in online_users.items():
            self.show_custom_notification(
                "Usuario En Línea",
                username,
                user_data.get('display_name', username),
                user_data.get('thumbnail_url', '')
            )
        
        self.update_position()
        self.is_showing = True
    
    def play_notification_sound(self):
        """Reproduce el sonido de notificación una sola vez"""
        try:
            if os.path.exists("notification.mp3"):
                try:
                    import pygame
                    pygame.mixer.init()
                    pygame.mixer.music.load("notification.mp3")
                    pygame.mixer.music.play()
                except ImportError:
                    print("Pygame no está instalado. No se reproducirá el sonido.")
                except Exception as e:
                    print(f"Error reproduciendo sonido: {e}")
        except Exception as e:
            print(f"Error con el archivo de sonido: {e}")

    def show_custom_notification(self, title, username, display_name, image_url):
        CustomNotification(
            title=title,
            username=username,
            display_name=display_name,
            image_url=image_url
        )

class CustomNotification:
    def __init__(self, title, username, display_name, image_url):
        self.manager = NotificationManager.get_instance()
        self.fade_steps = 20
        self.fade_interval = 50
        self.display_time = 7000
        self.current_alpha = 1.0
        self.is_fading = False
        
        # Frame principal con borde elegante y gradiente
        self.window = tk.Frame(self.manager._scroll_frame)
        self.window.pack(fill='x', padx=10, pady=5)
        
        # Frame interno con efecto de vidrio y sombra
        self.inner_frame = tk.Frame(self.window, 
                                  bg='#2d2d2d',
                                  highlightbackground='#4a4a4a',
                                  highlightthickness=1)
        self.inner_frame.pack(fill='x', padx=1, pady=1)
        
        # Agregar indicador de estado (punto verde)
        status_frame = tk.Frame(self.inner_frame, bg='#2d2d2d')
        status_frame.pack(fill='x', padx=10, pady=(5,0))
        
        status_dot = tk.Canvas(status_frame, width=8, height=8, bg='#2d2d2d', highlightthickness=0)
        status_dot.create_oval(0, 0, 8, 8, fill='#00ff00', outline='#00cc00')
        status_dot.pack(side='left')
        
        status_text = tk.Label(status_frame, 
                             text="En línea ahora",
                             font=('Segoe UI', 8),
                             fg='#00ff00',
                             bg='#2d2d2d')
        status_text.pack(side='left', padx=(5,0))
        
        # Tiempo transcurrido
        self.time_label = tk.Label(status_frame,
                                 text="ahora",
                                 font=('Segoe UI', 8),
                                 fg='#888888',
                                 bg='#2d2d2d')
        self.time_label.pack(side='right')
        self.update_time()
        
        # Frame para contenido
        content_frame = tk.Frame(self.inner_frame, bg='#2d2d2d')
        content_frame.pack(fill='x', padx=10, pady=10)
        
        # Frame para imagen con borde redondeado
        image_frame = tk.Frame(content_frame, 
                             bg='#2d2d2d',
                             highlightbackground='#4a4a4a',
                             highlightthickness=1)
        image_frame.pack(side='left', padx=(0,10))
        
        # Cargar y redimensionar la imagen
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            image = image.resize((45, 45), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            image_label = tk.Label(image_frame, 
                                 image=photo,
                                 bg='#2d2d2d',
                                 bd=0)
            image_label.image = photo
            image_label.pack(padx=2, pady=2)
        except Exception as e:
            print(f"Error cargando imagen: {e}")
        
        # Frame para texto
        text_frame = tk.Frame(content_frame, bg='#2d2d2d')
        text_frame.pack(side='left', fill='both', expand=True)
        
        # Título con efecto de brillo
        title_label = tk.Label(text_frame,
                             text=title,
                             font=('Segoe UI', 11, 'bold'),
                             fg='#ffffff',
                             bg='#2d2d2d')
        title_label.pack(anchor='w')
        
        # Nombre de usuario con estilo
        name_label = tk.Label(text_frame,
                            text=display_name,
                            font=('Segoe UI', 10),
                            fg='#e0e0e0',
                            bg='#2d2d2d')
        name_label.pack(anchor='w')
        
        username_label = tk.Label(text_frame,
                                text=f"@{username}",
                                font=('Segoe UI', 9),
                                fg='#aaaaaa',
                                bg='#2d2d2d')
        username_label.pack(anchor='w')
        
        # Frame para botones
        button_frame = tk.Frame(self.inner_frame, bg='#2d2d2d')
        button_frame.pack(fill='x', padx=10, pady=(5,10))
        
        # Estilo para botones
        class HoverButton(tk.Label):
            def __init__(self, master, text, command=None, **kwargs):
                super().__init__(master, text=text, **kwargs)
                self.default_bg = kwargs.get('bg', '#2d2d2d')
                self.hover_bg = '#454545'
                self.bind('<Enter>', self._on_enter)
                self.bind('<Leave>', self._on_leave)
                self.bind('<Button-1>', lambda e: command() if command else None)
                
            def _on_enter(self, e):
                self['background'] = self.hover_bg
            
            def _on_leave(self, e):
                self['background'] = self.default_bg
        
        # Función para visitar perfil
        def visit_profile():
            url = f"https://es.imvu.com/next/av/{username}/"
            print(f"Abriendo perfil: {url}")
            webbrowser.open(url)
        
        # Función para ocultar notificación
        def hide_notification():
            self.window.destroy()
            if self.timer:
                self.timer.cancel()
        
        # Botones con iconos
        visit_btn = HoverButton(button_frame,
                              text=" Visitar Perfil",
                              command=visit_profile,
                              font=('Segoe UI', 9),
                              fg='#ffffff',
                              bg='#2d2d2d',
                              cursor='hand2',
                              padx=10,
                              pady=5)
        visit_btn.pack(side='left', padx=(0,5))
        
        hide_btn = HoverButton(button_frame,
                             text=" Ocultar",
                             command=hide_notification,
                             font=('Segoe UI', 9),
                             fg='#ffffff',
                             bg='#2d2d2d',
                             cursor='hand2',
                             padx=10,
                             pady=5)
        hide_btn.pack(side='left')
        
        # Variables para el temporizador
        self.timer = None
        self.fade_timer = None
        self.start_timer()
        
        # Eventos de mouse
        self.window.bind('<Enter>', self._on_enter)
        self.window.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        self.stop_fade()
        self.restore_visibility()
    
    def _on_leave(self, event):
        self.start_timer()
    
    def stop_fade(self):
        self.is_fading = False
        if self.fade_timer:
            self.window.after_cancel(self.fade_timer)
            self.fade_timer = None
    
    def restore_visibility(self):
        self.current_alpha = 1.0
        root = self.window.winfo_toplevel()
        if root:
            root.attributes('-alpha', 1.0)
    
    def start_timer(self):
        # Cancelar temporizadores existentes
        self.stop_fade()
        if self.timer:
            self.timer.cancel()
        
        # Restaurar visibilidad
        self.restore_visibility()
        
        # Iniciar nuevo temporizador
        self.timer = threading.Timer(self.display_time / 1000, self.start_fade)
        self.timer.start()
    
    def start_fade(self):
        if not self.is_fading:
            self.is_fading = True
            self.fade_step()
    
    def fade_step(self):
        if not self.is_fading:
            return
        
        root = self.window.winfo_toplevel()
        if root and self.current_alpha > 0:
            self.current_alpha -= 1.0 / self.fade_steps
            root.attributes('-alpha', max(self.current_alpha, 0))
            self.fade_timer = self.window.after(self.fade_interval, self.fade_step)
        else:
            self.window.destroy()
    
    def close(self):
        self.stop_fade()
        if self.timer:
            self.timer.cancel()
        self.window.destroy()
    
    def update_time(self):
        """Actualizar el tiempo transcurrido"""
        if not hasattr(self, 'start_time'):
            self.start_time = time.time()
        
        elapsed = int(time.time() - self.start_time)
        if elapsed < 60:
            text = "ahora"
        elif elapsed < 3600:
            minutes = elapsed // 60
            text = f"hace {minutes}m"
        else:
            hours = elapsed // 3600
            text = f"hace {hours}h"
        
        self.time_label.config(text=text)
        if not self.is_fading:
            self.window.after(60000, self.update_time)  # Actualizar cada minuto

class ConfigNotification(CustomNotification):
    def __init__(self, config_manager):
        self.window = tk.Frame(NotificationManager.get_instance()._scroll_frame, bg='#2b2b2b')
        self.window.pack(fill=tk.BOTH, expand=True)
        
        # Frame principal con borde redondeado
        main_frame = tk.Frame(self.window, bg='#2b2b2b', padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para el texto
        text_frame = tk.Frame(main_frame, bg='#2b2b2b')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 20))
        
        # Mensaje de configuración
        tk.Label(text_frame, 
                text="¡Configuración Necesaria!", 
                fg='#ff6b6b', 
                bg='#2b2b2b', 
                font=('Arial', 12, 'bold')).pack()
        
        tk.Label(text_frame, 
                text="Por favor configura tu ID de usuario\ny cookie osCsid para continuar.", 
                fg='white', 
                bg='#2b2b2b', 
                font=('Arial', 10),
                justify=tk.CENTER).pack(pady=5)
        
        # Frame para botones
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Estilo para botones
        style = ttk.Style()
        style.configure('Config.TButton', padding=5)
        
        def open_config():
            config_manager.show_config_window()
        
        # Botón de configuración
        ttk.Button(button_frame, 
                  text="Abrir Configuración", 
                  style='Config.TButton',
                  command=open_config).pack(expand=True)
        
        # Registrar en el administrador de notificaciones
        NotificationManager.get_instance().add_notification(self)
        
        # Configurar la opacidad inicial
        self.opacity = 0.0
        self.window.pack_forget()  # Ocultar inicialmente
        self.animate_in()
        
        # Temporizador para cerrar después de 20 segundos
        self.window.after(20000, self.animate_out)
    
    def animate_in(self):
        if self.opacity < 1.0:
            self.opacity += 0.1
            self.window.pack(fill=tk.BOTH, expand=True)
            self.window.update()
            self.window.after(50, self.animate_in)
    
    def animate_out(self):
        if self.opacity > 0.0:
            self.opacity -= 0.1
            if self.opacity <= 0:
                self.window.pack_forget()
            else:
                self.window.update()
                self.window.after(50, self.animate_out)
        else:
            self.close()
    
    def close(self):
        NotificationManager.get_instance().remove_notification(self)
        self.window.destroy()
    
    def reposition(self, new_y):
        self.window.geometry(f'{self.window_width}x{self.window_height}+{self.x}+{new_y}')

class IMVUFriendsMonitor:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.base_url = "https://api.imvu.com/user/user-"
        self.headers = {
            'Accept': 'application/json; charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Origin': 'imvunext://client'
        }
        self.params = {
            'status': 'online',
            'online': 'true',
            'limit': '50',
            'sortby': 'name'
        }
        self.online_users = {}
        self.last_check = {}
        self.online_users_file = "online_users.json"
        self.load_online_users()
    
    def load_online_users(self):
        try:
            with open(self.online_users_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()  # Eliminar espacios en blanco
                if content:  # Si hay contenido
                    self.online_users = json.loads(content)
                else:
                    self.online_users = {}
        except (FileNotFoundError, json.JSONDecodeError):
            self.online_users = {}
            self.save_online_users()  # Crear archivo vacío
    
    def save_online_users(self):
        with open(self.online_users_file, 'w', encoding='utf-8') as f:
            json.dump(self.online_users, f, indent=4, ensure_ascii=False)
    
    def get_friends_list(self):
        config = self.config_manager.config
        if not config["user_id"] or not config["osCsid"]:
            print("Error: Configuración incompleta. Por favor configure su ID de usuario y cookie osCsid.")
            return []
        
        url = f"https://api.imvu.com/user/user-{config['user_id']}/friends?status=online&online=true&limit=50&sortby=name"
        headers = {
            'Cookie': f'osCsid={config["osCsid"]}'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error obteniendo lista de amigos: {e}")
            return []

    def get_online_friends(self):
        try:
            print("Intentando obtener amigos en línea...")
            friends_list = self.get_friends_list()
            if friends_list and 'denormalized' in friends_list:
                online_users = {}
                denormalized = friends_list['denormalized']
                
                # Obtener la lista de amigos en línea
                friends_data = next(
                    (v for k, v in denormalized.items() 
                     if k.endswith('/friends?status=online&online=true&limit=50&sortby=name')),
                    None
                )
                
                if friends_data and 'data' in friends_data and 'items' in friends_data['data']:
                    print(f"Número de usuarios en línea encontrados: {len(friends_data['data']['items'])}")
                    
                    for friend_url in friends_data['data']['items']:
                        # Extraer el ID del usuario del URL
                        user_id = friend_url.split('user-')[-1]
                        # Construir la URL completa del usuario
                        user_url = f"https://api.imvu.com/user/user-{user_id}"
                        
                        if user_url in denormalized:
                            user_info = denormalized[user_url]
                            if 'data' in user_info:
                                user_data = user_info['data']
                                username = user_data.get('username', '')
                                thumbnail_url = user_data.get('thumbnail_url', '')
                                display_name = user_data.get('display_name', username)
                                
                                # Solo agregar usuarios con datos válidos
                                if username and thumbnail_url and display_name:
                                    online_users[username] = {
                                        'username': username,
                                        'thumbnail_url': thumbnail_url,
                                        'display_name': display_name
                                    }
                                    print(f"Usuario en línea encontrado: {username}")
                
                return online_users
            return {}
        except Exception as e:
            print(f"Error obteniendo datos: {e}")
            traceback.print_exc()
            return None
    
    def show_notification(self, title, message, image_url=None, username=None, display_name=None):
        # No mostrar notificación si falta algún dato importante
        if not all([username, image_url, display_name]):
            print(f"Saltando notificación para {username}: datos incompletos")
            return
            
        try:
            print(f"Intentando mostrar notificación: {title} - {message}")
            
            def show_custom_notification():
                CustomNotification(
                    title=title,
                    username=username,
                    display_name=display_name,
                    image_url=image_url
                )
            
            # Iniciar la notificación en un hilo separado
            threading.Thread(target=show_custom_notification, daemon=True).start()
            
            print("Notificación mostrada con éxito")
        except Exception as e:
            print(f"Error mostrando notificación: {e}")
            print(f"Tipo de error: {type(e)}")
    
    def save_current_state(self):
        try:
            # Asegurarse de que el archivo se cierre correctamente usando with
            with open('online_users.json', 'w', encoding='utf-8') as f:
                json.dump(self.online_users, f, ensure_ascii=False)
            print("Estado guardado exitosamente")
        except PermissionError as e:
            print(f"Error de permisos al guardar el estado: {e}")
            print("Intenta ejecutar el script como administrador")
        except Exception as e:
            print(f"Error al guardar el estado: {e}")
    
    def load_previous_state(self):
        try:
            # Asegurarse de que el archivo se cierre correctamente usando with
            with open('online_users.json', 'r', encoding='utf-8') as f:
                content = f.read()
                if not content:  # Si el archivo está vacío
                    return {}
                return json.loads(content)
        except PermissionError as e:
            print(f"Error de permisos al cargar el estado: {e}")
            print("Intenta ejecutar el script como administrador")
            return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        except Exception as e:
            print(f"Error al cargar el estado: {e}")
            return {}
    
    def monitor_friends(self):
        while True:
            try:
                print("\nVerificando amigos en línea...")
                current_online = self.get_online_friends()
                
                if current_online is not None:
                    print(f"Usuarios actualmente en línea: {len(current_online)}")
                    
                    # Crear una copia temporal del estado actual
                    try:
                        # Revisar usuarios nuevos en línea
                        for username, user_data in current_online.items():
                            if username not in self.online_users:
                                print(f"Nuevo usuario en línea detectado: {username}")
                                self.show_notification(
                                    "Amigo en Línea",
                                    f"{username} se ha conectado!",
                                    user_data['thumbnail_url'],
                                    username,
                                    user_data['display_name']
                                )
                        
                        # Revisar usuarios que se desconectaron
                        for username, user_data in self.online_users.items():
                            if username not in current_online:
                                print(f"Usuario desconectado detectado: {username}")
                                self.show_notification(
                                    "Amigo Desconectado",
                                    f"{username} se ha desconectado",
                                    user_data['thumbnail_url'],
                                    username,
                                    user_data['display_name']
                                )
                        
                        # Actualizar estado actual
                        self.online_users = current_online.copy()
                        self.save_online_users()
                    except Exception as e:
                        print(f"Error al procesar cambios de usuarios: {e}")
                else:
                    print("No se pudo obtener la lista de amigos en esta verificación")
                
                interval = self.config_manager.config.get("update_interval", 60)
                print(f"Esperando {interval} segundos para la próxima verificación...")
                time.sleep(interval)
            except Exception as e:
                print(f"Error en el bucle principal: {e}")
                print(f"Tipo de error: {type(e)}")
                traceback.print_exc()
                time.sleep(60)  # En caso de error, esperar 1 minuto

class OnlineUsersWindow:
    def __init__(self, monitor):
        self.monitor = monitor
        self.window = tk.Toplevel()
        self.window.title("Usuarios en Línea - IMVU Notify")
        self.window.geometry("800x600")
        self.window.configure(bg='#1e1e1e')
        
        # Frame principal
        main_frame = ttk.Frame(self.window, style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configurar estilo
        style = ttk.Style()
        style.configure('Main.TFrame', background='#1e1e1e')
        
        # Canvas y Scrollbar
        self.canvas = tk.Canvas(main_frame, bg='#1e1e1e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid para usuarios
        self.grid_frame = ttk.Frame(self.scrollable_frame, style='Main.TFrame')
        self.grid_frame.pack(fill=tk.BOTH, expand=True)
        
        # Empaquetar elementos
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Actualizar la vista
        self.update_users()
        
        # Actualización periódica
        self.window.after(5000, self.periodic_update)
        
        # Centrar la ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_user_card(self, username, user_data, grid_pos):
        row, col = grid_pos
        
        # Frame para la tarjeta
        card = tk.Frame(self.grid_frame, bg='#2d2d2d', relief=tk.RAISED, bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        try:
            # Cargar y mostrar la imagen
            response = requests.get(user_data['thumbnail_url'])
            image = Image.open(BytesIO(response.content))
            image = image.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            img_label = tk.Label(card, image=photo, bg='#2d2d2d')
            img_label.image = photo
            img_label.pack(pady=(10,5))
        except Exception as e:
            print(f"Error cargando imagen para {username}: {e}")
        
        # Nombre de usuario
        name_label = tk.Label(card,
                            text=user_data['display_name'],
                            font=('Segoe UI', 11, 'bold'),
                            fg='#ffffff',
                            bg='#2d2d2d',
                            wraplength=150)
        name_label.pack()
        
        # Username
        username_label = tk.Label(card,
                                text=f"@{username}",
                                font=('Segoe UI', 9),
                                fg='#aaaaaa',
                                bg='#2d2d2d')
        username_label.pack()
        
        # Estado (visible/oculto)
        status_text = "🔒 Oculto" if not user_data.get('online', True) else "👁 Visible"
        status_color = '#ff6b6b' if not user_data.get('online', True) else '#00ff00'
        
        status_label = tk.Label(card,
                              text=status_text,
                              font=('Segoe UI', 9),
                              fg=status_color,
                              bg='#2d2d2d')
        status_label.pack(pady=(5,10))
        
        # Botón para visitar perfil
        visit_btn = tk.Label(card,
                           text="Visitar Perfil",
                           font=('Segoe UI', 9),
                           fg='#ffffff',
                           bg='#007acc',
                           cursor='hand2',
                           pady=5,
                           padx=10)
        visit_btn.pack(pady=(0,10))
        
        def on_enter(e):
            visit_btn.configure(bg='#0098ff')
        
        def on_leave(e):
            visit_btn.configure(bg='#007acc')
        
        def visit_profile(e):
            url = f"https://es.imvu.com/next/av/{username}/"
            webbrowser.open(url)
        
        visit_btn.bind('<Enter>', on_enter)
        visit_btn.bind('<Leave>', on_leave)
        visit_btn.bind('<Button-1>', visit_profile)
    
    def update_users(self):
        # Limpiar grid actual
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # Configurar el grid
        current_row = 0
        current_col = 0
        max_cols = 4  # Número de tarjetas por fila
        
        # Crear tarjetas para cada usuario
        for username, user_data in self.monitor.online_users.items():
            self.create_user_card(username, user_data, (current_row, current_col))
            
            current_col += 1
            if current_col >= max_cols:
                current_col = 0
                current_row += 1
    
    def periodic_update(self):
        self.update_users()
        self.window.after(5000, self.periodic_update)

if __name__ == "__main__":
    # Inicializar el administrador de configuración
    config_manager = ConfigManager()
    
    # Crear y ejecutar el ícono del system tray en un hilo separado
    monitor = IMVUFriendsMonitor(config_manager)
    tray_icon = SystemTrayIcon(config_manager, monitor)
    tray_thread = threading.Thread(target=tray_icon.run, daemon=True)
    tray_thread.start()
    
    # Mostrar notificación de configuración si es necesario
    if not config_manager.config["user_id"] or not config_manager.config["osCsid"]:
        ConfigNotification(config_manager)
    
    # Iniciar el monitoreo en un hilo separado
    monitor_thread = threading.Thread(target=monitor.monitor_friends, daemon=True)
    monitor_thread.start()
    
    # Iniciar el mainloop de tkinter
    NotificationManager.get_instance().root.mainloop()
