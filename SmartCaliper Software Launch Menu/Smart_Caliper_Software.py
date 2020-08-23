import subprocess
import serial
from pynput.keyboard import Key, Controller
import multiprocessing


def take_serial_type_measurement():
    try:
        esp32 = serial.Serial('COM5', 115200)
        keyboard = Controller()
        while True:
            try:
                measured_value = float(esp32.readline())/100
                string_value = str(measured_value)
                #print(str(measured_value))
                for i in string_value:
                    keyboard.press(i)
                    keyboard.release(i)
            except:
                pass
    except:
        print("Serial not found")



def run_blender():
    subprocess.call(r'C:\Program Files\Blender Foundation\Blender\blender.exe')

def run_solidworks():
    subprocess.call(r'C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe')



if __name__ == "__main__":
    print("-----Welcome to Smart Caliper-----")
    print("Press 1 to select Create Mode")
    print("Press 2 to select Annotate/Tolerance Checking Mode")
    flag = True

    while flag:
        mode_select = input("Enter here: ")
        if mode_select == "1" or mode_select == "2":
            flag = False
    

    if mode_select == "1":
        p1 = multiprocessing.Process(target=take_serial_type_measurement)
        p2 = multiprocessing.Process(target=run_solidworks)
        p1.start()
        p2.start()
    elif mode_select == "2":
        p1 = multiprocessing.Process(target=take_serial_type_measurement)
        p2 = multiprocessing.Process(target=run_blender)
        p1.start()
        p2.start()
        

            


    
                        

