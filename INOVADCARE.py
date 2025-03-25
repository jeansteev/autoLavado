import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from rut_chile import rut_chile

import sqlite3

import serial
s=serial.Serial('COM4')
import time

def procesador():

    conexion=sqlite3.connect('db.sqlite3')
    print(conexion)
    cur=conexion.cursor()
    lavado = lavado_entry.get()
    codigo=codigo_entry.get()
    #tomo el rut recibido le di formato con punto y gion 
    rut = rut_entry.get()
    rut_format=rut_chile.format_rut_with_dots(rut=rut)
    q="""SELECT * FROM core_fichaspagados WHERE codigo = ? AND tipolavado=? AND rut=?"""
    cur.execute(q,(codigo, lavado,rut_format,))
          
    rows=cur.fetchall()
   

    print("ok")
    
    if rows!=[]:
       
       for row in rows:
        rut_ficha=row[1]
        lavado_ficha=row[4]
        codigo_ficha=row[6]
        print(rut_ficha, lavado_ficha,codigo_ficha)
        tiempo=row[5]*30000
        print(tiempo)
        
        ventana=tk.Toplevel()
        ventana.title("Temprorizador")
        ventana.config(width=300, height=200)
        ventana.resizable(0,0)
        ventana.overrideredirect(True)
       
        ventana.focus()
        ventana.grab_set()
        titulo=tk.Label(ventana, text="Temporizador" ,font=('Arial',15))
        titulo.place(x=100, y=10)
        text_timer=tk.Label(ventana, text="yop" ,font=("helvetica", 40), fg='darkgreen')

        text_timer.place(x=50 , y=80)

        duracion =tiempo

        while duracion >=0:
        
           text_timer['text']=str(duracion) 
          
           ventana.update()
          
           
           if duracion==0:    
              ventana.destroy()
           

           duracion -=1
           s.write("a".encode())
        
           s.write("b".encode())
          
          

        sql = '''INSERT INTO core_historial(id,fecha,rut,correo,cantidadficha,tipolavado,crono,codigo,Totalpagar,user_id)
        VALUES(?,?,?,?,?,?,?,?,?,?) '''
        data_tuple =(row[0],row[8],row[1],row[2],row[3],row[4],row[5],row[6],row[9],row[7])
        cur.execute(sql,data_tuple)
        conexion.commit()
        cur.execute("DELETE FROM 'core_fichaspagados' WHERE codigo = ? ",(codigo_ficha,))
        conexion.commit()


         
        messagebox.showinfo("Exito", "¡ Se agoto su tiempo ! ¡ Gracias por su visita !")

 
      
    if rows==[]:

        messagebox.showerror("Hubo un error", "¡Porfavor, ingrese los datos correctamente!")
       



    
        

          

 
 




####################################################################################################################

 
 












screen=tk.Tk()
screen.config(width=600, height=300)
screen.title("Inovadcare")
screen.resizable(0,0)
#screen.configure(background='#51d1f6')
img= (Image.open("card.png"))
resized_image= img.resize((240,300))
new_image= ImageTk.PhotoImage(resized_image)
label = ttk.Label(image=new_image,width=100)
label.place(x=0)


lavado_label=tk.Label(text="Lavado",font=('Arial',12))
lavado_label.place(x=250, y=50)

lavado_entry = ttk.Combobox(screen, values=['Exterior','Interior'])
lavado_entry.place(x=320, y=50 , width=200 , height=30)

rut_label = tk.Label(text="Rut", font=('Arial',12))
rut_label.place(x=270, y=100)


rut_entry = tk.Entry(screen)
rut_entry.place(x=320, y=100, width=200 , height=30)
info_label = tk.Label(text="Rut-ejemlo: 11.000.111-k",font=('Arial',8), fg='red')
info_label.place(x=350, y=130)

codigo_label = tk.Label(text="Codigo",font=('Arial',12))
codigo_label.place(x=250, y=160)

codigo_entry = tk.Entry(screen)
codigo_entry.place(x=320, y=160, width=200 , height=30)

proc_button = tk.Button(screen, text="Aceptar", font=('Arial',12) , background='#51d1f6', command=procesador)
proc_button.place(x=450,y=250)



screen.mainloop()



#ventana 2-###############################################################################################
