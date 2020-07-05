from tkinter import *
from tkinter import filedialog
import reconociento
from datetime import datetime
from PIL import ImageTk
from PIL import Image  

rostros_existentes=[] 
top = Tk() 
indice_general = 0
class Rostro():
  def __init__(self, fecha_registro, direccion_imagen, rostros_reconocidos):
    self.fecha_registro = fecha_registro
    self.direccion_imagen = direccion_imagen
    self.rostros_reconocidos = rostros_reconocidos




def hello():  
    print("hello!") 
#Esta definicion lo que hace es abrir traer el archivo(imagen) 
def cargar_archivo():
    top.filename =  filedialog.askopenfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files",".jpg"),("all files",".*")))
#Esta definicion lo que hace es guardar el archivo(imagen)   
def salvar_archivo():
    top.filename =  filedialog.asksaveasfile(initialdir = "/",title = "Select file",filetypes = (("jpeg files",".jpg"),("all files",".*")))
#Esta definición lo que hace es guardar la fecha/hora, la URL del archivo y la mica.
def reconocer_rostro():
    cargar_archivo()
    caras = reconociento.reconocer_caras(top.filename.name)
    ahora = datetime.now()
    rostros_existentes.append(Rostro(ahora,top.filename.name,caras))
    mostrar_foto(rostros_existentes[-1])
#Esta funcion lo que hace es avanzar foto por foto
def avanzar():
    global indice_general
    indice_general = indice_general + 1
    mostrar_foto(rostros_existentes[indice_general])
#Esta funcion lo que hace es retroceder foto por foto
def retroceder():
    global indice_general
    indice_general = indice_general - 1
    mostrar_foto(rostros_existentes[indice_general])

    
#Esta definicion lo que hace es limpiar el lienzo y abre una nueva imagen y la muestra en el lienzo
def mostrar_foto(rostro):
    canvas.delete("all")
    canvas.update()
    width = canvas.winfo_width()
    height = canvas.winfo_height()    
    scrollbary.config( command = canvas.yview )
    scrollbarx.config( command = canvas.xview )
    img = ImageTk.PhotoImage(Image.open(rostro.direccion_imagen))
    label = Label(image=img)
    label.image = img
    canvas.create_image(width/2, height/2 ,anchor=CENTER, image=img)
    #Tengo que hacer que esto no se duplique cada vez que abro una imagen y tratar de sacar las face_expressions de la mica
    label_2.configure(text=rostro.rostros_reconocidos[0]["vertices"])
    label_2.pack()

    
    
def etiquetar_rostro():
    #Esto obliga a que el indice siempre inicie en la primera foto
    indice_general=0
    #Aqui se va a mostrar la primer foto / Cada vez que se llama a mostrar foto, el canvas se limpia
    mostrar_foto(rostros_existentes[indice_general])
    #Estas dos lineas muestran los 2 botones en la parte de abajo. 
    Button(top, text="Avanzar",command=avanzar).pack(side=RIGHT)
    Button(top, text="Retroceder",command=retroceder).pack(side=RIGHT)
    
    
   
    
# crea el cuadro blaco (lienzo)
scrollbary = Scrollbar(top)
scrollbary.pack( side = RIGHT, fill = Y )
scrollbarx = Scrollbar(top,orient=HORIZONTAL)
scrollbarx.pack( side = BOTTOM, fill = X )
canvas = Canvas(width=500, height=500, bg='white', xscrollcommand = scrollbarx.set, yscrollcommand = scrollbary.set)
canvas.pack(expand=YES, fill=BOTH)
canvas.update()
label_2 =  Label(top, text="")
# Menu de acciones
menubar = Menu(top)
menuaccion = Menu(menubar, tearoff=0) 
menuaccion.add_command(label="Reconocer Rostros", command=reconocer_rostro)
menuaccion.add_command(label="Etiquetado de personas", command=etiquetar_rostro)
menuaccion.add_command(label="Visualización de Etiquetas", command=hello)
menuaccion.add_command(label="Imágenes por persona", command=hello)
menuaccion.add_command(label="Abrir Archivo", command=cargar_archivo)
menuaccion.add_command(label="Salvar Archivo", command=salvar_archivo)  
menuaccion.add_separator()
#Para salir
menuaccion.add_command(label="Salir!", command=top.quit)
menubar.add_cascade(label="Accion", menu=menuaccion)
  
top.config(menu=menubar)

top.mainloop()
