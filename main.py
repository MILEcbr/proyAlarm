from kivy.config import Config

Config.set('graphics', 'width', '350')  # ancho de la ventana
Config.set('graphics', 'height', '600')  # altura de la ventana


from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
import json
import os

# pantallas
class LoginScreen(Screen):
    def verify_credentials(self, username, password):
        if username == username and password == password:
            self.manager.current = "menu"
        else:
            self.ids.login_message.text = "Usuario o contraseña inválidos"
            self.ids.login_message.color = (0, 0, 0, 1)  # RGBA para negro
class RegisterScreen(Screen):
    def register_user(self, username, password, email):
        users = self.load_users()
        if username in users:
            self.ids.register_message.text = "Usuario ya existe"
            self.ids.register_message.color = (0, 0, 0, 1)  # RGBA para negro
        else:
            users[username] = {'password': password, 'email': email}
            self.save_users(users)
            self.ids.register_message.text = "Registro exitoso"
            self.ids.register_message.color = (0, 0, 0, 1)  # RGBA para negro
    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as file:
                return json.load(file)
        return {}

    def save_users(self, users):
        with open('users.json', 'w') as file:
            json.dump(users, file)

class HomeScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class ProfileScreen(Screen):
    def save_profile(self, nombre, apellido, direccion, contactos):
        profile_data = {
            'nombre': nombre,
            'apellido': apellido,
            'direccion': direccion,
            'contactos': contactos
        }
        with open('profile.json', 'w') as file:
            json.dump(profile_data, file)
        self.ids.profile_message.text = "Perfil guardado exitosamente"
        self.ids.profile_message.color = (0, 0, 0, 1)  # RGBA para negro
        self.disable_editing()

    def load_profile(self):
        if os.path.exists('profile.json'):
            with open('profile.json', 'r') as file:
                profile_data = json.load(file)
                self.ids.nombre.text = profile_data.get('nombre', '')
                self.ids.apellido.text = profile_data.get('apellido', '')
                self.ids.direccion.text = profile_data.get('direccion', '')
                self.ids.contactos.text = profile_data.get('contactos', '')

    def enable_editing(self):
        self.ids.nombre.disabled = False
        self.ids.apellido.disabled = False
        self.ids.direccion.disabled = False
        self.ids.contactos.disabled = False
        self.ids.save_button.disabled = False

    def disable_editing(self):
        self.ids.nombre.disabled = True
        self.ids.apellido.disabled = True
        self.ids.direccion.disabled = True
        self.ids.contactos.disabled = True
        self.ids.save_button.disabled = True

class AlarmsScreen(Screen):
    def load_alarms(self):
        self.ids.alarms_list.clear_widgets()
        if os.path.exists('alarms.json'):
            with open('alarms.json', 'r') as file:
                alarms = json.load(file)
                for i, alarm in enumerate(alarms):
                    alarm_text = f"{alarm['medicamento']} - {alarm['hora']} - {alarm['frecuencia']} - {alarm['dosis']}"
                    
                    alarm_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    
                    # Etiqueta con letras en azul
                    label = Label(text=alarm_text, font_size=20, size_hint_y=None, height=40, color=(0, 0, 1, 1))
                    
                    # Botón para activar/desactivar con letras en blanco y fondo azul
                    toggle_button = Button(text='Activar', size_hint_x=None, width=100, color=(1, 1, 1, 1),
                                           background_color=(0, 0, 1, 1), background_normal='')
                    toggle_button.bind(on_press=self.toggle_alarm)
                    
                    # Botón para eliminar con letras en negro y fondo azul
                    delete_button = Button(text='X', size_hint_x=None, width=50, color=(0, 0, 0, 1),
                                           background_color=(1, 0, 0, 1), background_normal='')
                    delete_button.bind(on_press=lambda btn, idx=i: self.delete_alarm(idx))
                    
                    alarm_box.add_widget(label)
                    alarm_box.add_widget(toggle_button)
                    alarm_box.add_widget(delete_button)
                    
                    self.ids.alarms_list.add_widget(alarm_box)

    def toggle_alarm(self, instance):
        if instance.text == 'Activar':
            instance.text = 'Desactivar'
            instance.background_color = (1, 0, 0, 1)  # Rojo para desactivado
        else:
            instance.text = 'Activar'
            instance.background_color = (0, 0, 1, 1)  # Azul para activado

    def delete_alarm(self, index):
        # Cargo alarmas
        if os.path.exists('alarms.json'):
            with open('alarms.json', 'r') as file:
                alarms = json.load(file)
            
            # Elimino alarma
            if 0 <= index < len(alarms):
                alarms.pop(index)
        
            with open('alarms.json', 'w') as file:
                json.dump(alarms, file)
            
            # Recarga alarmas
            self.load_alarms()


class AddAlarmScreen(Screen):
    def save_alarm(self, medicamento, hora, frecuencia, dosis):
        alarm = {
            'medicamento': medicamento,
            'hora': hora,
            'frecuencia': frecuencia,
            'dosis': dosis,
            'active': False 
        }
        alarms = self.load_alarms()
        alarms.append(alarm)
        self.save_alarms(alarms)
        self.manager.current = "alarms"
        self.update_alarm_label(alarm)

    def load_alarms(self):
        if os.path.exists('alarms.json'):
            with open('alarms.json', 'r') as file:
                return json.load(file)
        return []

    def save_alarms(self, alarms):
        with open('alarms.json', 'w') as file:
            json.dump(alarms, file)

    def update_alarm_label(self, alarm):
        alarm_text = f"{alarm['medicamento']} - {alarm['hora']} - {alarm['frecuencia']} - {alarm['dosis']}"
        
        alarm_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40) #activa
        label = Label(text=alarm_text, font_size=20, size_hint_y=None, height=40)
        
        toggle_button = Button(text='Activar', size_hint_x=None, width=100) #desactiva
        toggle_button.bind(on_press=self.toggle_alarm)
        
        delete_button = Button(text='Eliminar', size_hint_x=None, width=100) #elimina
        delete_button.bind(on_press=self.delete_alarm)
        
        alarm_box.add_widget(label)
        alarm_box.add_widget(toggle_button)
        alarm_box.add_widget(delete_button)
        
        self.manager.get_screen('alarms').ids.alarms_list.add_widget(alarm_box)

    def toggle_alarm(self, instance):
        if instance.text == 'Activar':
            instance.text = 'Desactivar'
            instance.background_color = (1, 0, 0, 1)  # Rojo para desactivado
            
        else:
            instance.text = 'Activar'
            instance.background_color = (0, 1, 0, 1)  # Verde para activado
            

    def delete_alarm(self, instance):
        box = instance.parent
        index = self.manager.get_screen('alarms').ids.alarms_list.children.index(box)
        
        #elimina la alarma
        self.manager.get_screen('alarms').delete_alarm(index)




class TurnsScreen(Screen):
    def load_turns(self):
        self.ids.turns_list.clear_widgets()
        if os.path.exists('turns.json'):
            with open('turns.json', 'r') as file:
                turns = json.load(file)
                for i, turn in enumerate(turns):
                    turn_text = f"{turn['fecha']} - {turn['hora']} - {turn['especialidad']}"
                    
                    turn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    
                    # cuadro del texto
                    text_box = BoxLayout(orientation='horizontal', size_hint=(0.6, None), width=200)
                    with text_box.canvas.before:
                        Color(0.678, 0.847, 0.902, 1)
                        Rectangle(pos=text_box.pos, size=text_box.size)
                    label = Label(text=turn_text, font_size=20, size_hint_y=None, height=40)
                    label.color = (0, 0, 1, 1)  #azul
                    text_box.add_widget(label)
                    
                    # Boton reprogramar
                    reprogram_button = Button(text='Reprogramar', size_hint_x=None, width=100, height=50)
                    reprogram_button.bind(on_press=lambda btn, idx=i: self.reprogram_turn(idx))
                    reprogram_button.background_color = (0, 0, 1, 1)
                    # Boton eliminar
                    delete_button = Button(text='X', size_hint_x=None, width=40, height=50)
                    delete_button.bind(on_press=lambda btn, idx=i: self.delete_turn(idx))
                    delete_button.background_color = (1, 0.3, 0.3, 1)  # Rojo
                    
                    turn_box.add_widget(text_box)
                    turn_box.add_widget(reprogram_button)
                    turn_box.add_widget(delete_button)
                    
                    self.ids.turns_list.add_widget(turn_box)

    def reprogram_turn(self, index):
        turn = self.load_turns()[index]
        self.manager.get_screen('edit_turn').load_turn(turn, index)
        self.manager.current = 'edit_turn'

    def delete_turn(self, index):
        if os.path.exists('turns.json'):
            with open('turns.json', 'r') as file:
                turns = json.load(file)
            
            if 0 <= index < len(turns):
                turns.pop(index)
            
            with open('turns.json', 'w') as file:
                json.dump(turns, file)
            
            self.load_turns()

class AddTurnScreen(Screen):
    def save_turn(self, fecha, hora, especialidad):
        turn = {
            'fecha': fecha,
            'hora': hora,
            'especialidad': especialidad
        }
        turns = self.load_turns()
        turns.append(turn)
        self.save_turns(turns)
        self.manager.current = "turns"
        self.manager.get_screen('turns').load_turns()

    def load_turns(self):
        if os.path.exists('turns.json'):
            with open('turns.json', 'r') as file:
                return json.load(file)
        return []

    def save_turns(self, turns):
        with open('turns.json', 'w') as file:
            json.dump(turns, file)


class MyDoctorScreen(Screen):
    def load_doctors(self):
        self.ids.doctors_list.clear_widgets()
        if os.path.exists('doctors.json'):
            with open('doctors.json', 'r') as file:
                doctors = json.load(file)
                for i, doctor in enumerate(doctors):
                    doctor_text = f"{doctor['nombre']} - {doctor['especialidad']} - {doctor['contacto']}"
                    
                    doctor_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
                    
                    # cuadro del texto
                    text_box = BoxLayout(orientation='horizontal', size_hint=(0.6, None), width=200)
                    with text_box.canvas.before:
                        Color(0.678, 0.847, 0.902, 1)  # Color azul claro
                        Rectangle(pos=text_box.pos, size=text_box.size)
                    label = Label(text=doctor_text, font_size=20, size_hint_y=None, height=40)
                    label.color = (0, 0, 1, 1)  # Azul
                    text_box.add_widget(label)
                    
                    # Botón editar
                    edit_button = Button(text='Editar', size_hint_x=None, width=100, height=50)
                    edit_button.bind(on_press=lambda btn, idx=i: self.edit_doctor(idx))
                    edit_button.background_color = (0, 0, 1, 1)  # Azul
                    
                    # Botón eliminar
                    delete_button = Button(text='X', size_hint_x=None, width=40, height=50)
                    delete_button.bind(on_press=lambda btn, idx=i: self.delete_doctor(idx))
                    delete_button.background_color = (1, 0.3, 0.3, 1)  # Rojo
                    
                    doctor_box.add_widget(text_box)
                    doctor_box.add_widget(edit_button)
                    doctor_box.add_widget(delete_button)
                    
                    self.ids.doctors_list.add_widget(doctor_box)

    def edit_doctor(self, index):
        doctor = self.load_doctors_data()[index]
        self.manager.get_screen('add_doctor').load_doctor(doctor, index)
        self.manager.current = 'add_doctor'

    def delete_doctor(self, index):
        if os.path.exists('doctors.json'):
            with open('doctors.json', 'r') as file:
                doctors = json.load(file)
            
            if 0 <= index < len(doctors):
                doctors.pop(index)
            
            with open('doctors.json', 'w') as file:
                json.dump(doctors, file)
            
            self.load_doctors()

    def load_doctors_data(self):
        if os.path.exists('doctors.json'):
            with open('doctors.json', 'r') as file:
                return json.load(file)
        return []


class AddDoctorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_doctor_index = None  # Inicializa con None

    def save_doctor(self):
        doctor = {
            'nombre': self.ids.name_input.text,
            'especialidad': self.ids.specialty_input.text,
            'contacto': self.ids.contact_input.text
        }

        doctors = self.load_doctors()
        if self.current_doctor_index is not None:
            doctors[self.current_doctor_index] = doctor  # Editar doctor existente
        else:
            doctors.append(doctor)  # Añadir nuevo doctor

        self.save_doctors(doctors)
        self.manager.current = "my_doctor"
        self.manager.get_screen('my_doctor').load_doctors()

        # Limpia los campos de entrada después de guardar
        self.ids.name_input.text = ''
        self.ids.specialty_input.text = ''
        self.ids.contact_input.text = ''
        self.current_doctor_index = None  # Restablece el índice

    def load_doctor(self, doctor, index):
        self.ids.name_input.text = doctor['nombre']
        self.ids.specialty_input.text = doctor['especialidad']
        self.ids.contact_input.text = doctor['contacto']
        self.current_doctor_index = index

    def load_doctors(self):
        if os.path.exists('doctors.json'):
            with open('doctors.json', 'r') as file:
                return json.load(file)
        return []

    def save_doctors(self, doctors):
        with open('doctors.json', 'w') as file:
            json.dump(doctors, file)




class ScreenManagement(ScreenManager):
    pass


kv = Builder.load_file("login.kv")

class LoginApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    LoginApp().run()
