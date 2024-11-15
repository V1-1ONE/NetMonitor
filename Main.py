from tkinter import *
from tkinter import ttk
import tkinter as tk
import define
import mainSQL
import subprocess
import platform

device_listbox = None

def ping(host):
        """Проверяет доступность устройства по IP-адресу и возвращает время пинга."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
    
        try:
            
            output = subprocess.check_output(command, universal_newlines=True)
            
            for line in output.splitlines():
                if "time=" in line:
                    time = line.split("time=")[1].split(" ")[0]
                    return True, time  
        except subprocess.CalledProcessError:
            return False, None  
    

def click():
    ip_address = txt.get()
    print(ip_address)
    ping_per = define.PingReq(ip_address)
    print(ping_per, 'для окна вывода')
    Ping_output.configure(text=f'{round(ping_per)} ms')

def ApplyAddBd(deviceName, addressIP):
    try:
        mainSQL.insertBD(deviceName, addressIP)
        print(f'Устройство {deviceName} с IP {addressIP} успешно добавлено.')
    except Exception as e:
        print(f'Ошибка при добавлении устройства: {e}')

def NewWindowDevice():
    window = Toplevel()
    window.title('Добавить устройсто')
    window.geometry("300x300")
    
    InputNameDevice = Entry(window, width=20)
    InputNameDevice.grid(column=1, row=0)
    
    InputNameDevicetext = ttk.Label(window, text='имя устройства -')
    InputNameDevicetext.grid(column=0, row=0)
    
    InputIPDevice = Entry(window, width=20)
    InputIPDevice.grid(column=1, row=1)
    
    InputIPDeviceText = ttk.Label(window, text='Адрес устройства -')
    InputIPDeviceText.grid(column=0, row=1)
    
    def add_device():
        deviceName = InputNameDevice.get()
        addressIP = InputIPDevice.get()
        print('Были отправлены -', deviceName, ', ', addressIP)
        mainSQL.insertBD(deviceName, addressIP)
        window.destroy()  
    AddDeviceBdButton = ttk.Button(window, text='Добавить', command=add_device)
    AddDeviceBdButton.grid(column=0, row=2, columnspan=2, pady=10)
   
    
def ViewDevices():
    window = Toplevel()
    window.title('Список устройств')
    window.geometry("300x400")
    devices = mainSQL.getDevices()
    device_listbox = Listbox(window, width=40, bd=1)
    device_listbox.pack(pady=20)
    print('Переменая девайсес ', Listbox)
    

    for device in devices:
        ip = device['ip']
        name = device['name']
        # Форматируем строку для отображения
        device_listbox.insert(tk.END, f"{name} - {ip}")

    def select_device():
        selected_device = device_listbox.curselection()
        if selected_device:
            device_info = device_listbox.get(selected_device)
            print(f'Выбрано устройство: {device_info}')
            window.destroy()
    def delete_device():
        selected_device = device_listbox.curselection()
        if selected_device:
            device_info = device_listbox.get(selected_device)
            print(f'Устройство удалено: {device_info}')
            mainSQL.deleteRecord(device_info.split("-")[1].strip())
            device_listbox.delete(0, tk.END)
            devices = mainSQL.getDevices()
            for device in devices:
                ip = device['ip']
                name = device['name']
                availability = ''
                device_listbox.insert(tk.END, f"{name} - {ip} ")
    def monit_status_device():
        devices = mainSQL.getDevices()
        device_listbox.delete(0, tk.END)  # Очищаем список перед обновлением
        for device in devices:
            ip = device['ip']
            name = device['name']
            ping_per = define.PingReq(ip)
            ping_status = round(ping_per)
            
            if ping_status > 0:
                status = f"{ping_status} ms"  # Время пинга
            else:
                status = "✖"  # Значок недоступности
            device_listbox.insert(tk.END, f"{name} - {ip} - {status}")
    
    select_button = ttk.Button(window, text='Выбрать', command=select_device)
    select_button.pack(pady=10)
    device_delet_button = ttk.Button(window, text='удалить устройство', command=delete_device)
    device_delet_button.pack(pady=10)
    Monitor_device_button = ttk.Button(window, text='следить', command=monit_status_device)
    Monitor_device_button.pack(pady=10)
    

window = Tk()
window.title("Володя продакшен")
window.geometry("500x400") 

txt = Entry(window, width=15)
txt.grid(column=0, row=0)

button_ping = ttk.Button(text='Пинг', command=click) 
button_ping.grid(column=0, row=1)

Ping_output = Label(window, text='XX')
Ping_output.grid(column=1, row=0)

new_device_window = ttk.Button(text='Добавить устройсто', command=NewWindowDevice)
new_device_window.grid(column=0, row=2)

view_devices_window = ttk.Button(text='Просмотреть устройства', command=ViewDevices)
view_devices_window.grid(column=0, row=3)

window.mainloop()
