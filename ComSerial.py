import serial,time
from tkinter import filedialog, messagebox
ser = serial.Serial('COM2', 9600)



def set_bits(shape):
    if shape == 'x':
        return "HIGH","LOW"
    elif shape == 'o':
        return "LOW", "HIGH"
    elif shape == 'triangulo':
        return "HIGH","HIGH"
    elif shape == 'estrella':
        return "estrella"
    else:
        return "LOW","LOW"
    
def serial(lista):
    contador = 7
    for print in lista:
        for data in print.instructions:
            bit1,bit2 = set_bits(data.shape)


            arduino_input = f'{contador} {bit1}\n'
            ser.write(arduino_input.encode()) 
            contador -=1
            messagebox.showerror("Error", arduino_input)
            arduino_input = f'{contador} {bit2}\n'
            ser.write(arduino_input.encode()) 
            contador -=1
            messagebox.showerror("Error", arduino_input)
          
            
            if contador<2:
                if data.row == 1:
                    ser.write(b"9 HIGH\n") 
                    ser.write(b"8 LOW\n") 
                    ser.write(b"10 HIGH\n") 
                    time.sleep(5)
                    ser.write(b"9 LOW\n") 
                    ser.write(b"10 LOW\n") 
                    
                if data.row == 2:
                    ser.write(b"9 LOW\n") 
                    ser.write(b"8 HIGH\n") 
                    ser.write(b"10 HIGH\n") 
                    time.sleep(5)
                    ser.write(b"10 LOW\n") 
                if data.row == 3:
                    ser.write(b"8 HIGH\n") 
                    ser.write(b"9 HIGH\n") 
                    ser.write(b"10 HIGH\n") 
                    time.sleep(5)
                    ser.write(b"10 LOW\n") 
                    
                contador = 7

                
    ser.close()