
from cProfile import label
from faulthandler import disable
from sqlite3 import Cursor
import subprocess, os, re, subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.colorchooser import Chooser
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from turtle import width
import pandas as pd
from tkinter.messagebox import showerror, showinfo

class seekwindow:
    
        def __init__(self,root):
            self.ventana=root
            self.ventana.title("File_seeker")
            self.ventana.geometry("700x500")

            style = ttk.Style()
            style.configure('W.TButton', font =
               ('Comic Sans Ms', 10 ),
                foreground = 'blue',background='green')
            
            barramenu=Menu(self.ventana)
            menuopciones=Menu(barramenu,tearoff=0)
            menuArchivo=Menu(barramenu,tearoff=0)
            barramenu.add_cascade(label="Archivo",menu=menuArchivo)
            barramenu.add_cascade(label="Buscar",menu=menuopciones)
            menuopciones.add_command(label='Documento',command=self.seekfile)
            menuopciones.add_command(label='Cadena',command=self.seekstring)
            menuArchivo.add_command(label="Salir",command=root.destroy)

            self.ventana.config(menu=barramenu)
            self.seekstring()

        def seekstring(self):
            
            try:
                self.ventana_file.pack_forget()
            except:
                pass
            self.window_string=tk.Frame(self.ventana,width=500,height=700)
            self.window_string.pack(fill="both",expand="yes")

            self.labeldefinition=tk.LabelFrame(self.window_string,text="Define cadena",foreground='grey') 
            self.labeldefinition.place(in_=self.window_string,x=10,  y=40)
            Labeltitlestring=Label(self.window_string,text="Busqueda por cadena")
            Labeltitlestring.config(foreground='Red',font=('Comic Sans Ms',15))
            Labeltitlestring.place(in_=self.window_string,x=240,  y=0)

            label_string=Label(self.labeldefinition,text="Ingresa cadena de texto a buscar  ")
            label_string.grid(row=1,column=0,pady=2)
            lblbtnexp=Label(self.labeldefinition,text='Selecciona ruta de inicio de busqueda')
            lblbtnexp.grid(row=2,column=0,pady=2)
            
            self.string_Entry=Entry(self.labeldefinition)
            self.string_Entry.grid(row=1,column=1,padx=10)
            self.string_Entry.focus()

            ttk.Button(self.window_string,text="Buscar",command=self.seek_instrucction,style = 'W.TButton',cursor='hand2').place(in_=self.window_string,x=240,  y=170)
            
            ttk.Button(self.window_string,text="Cerrar",command=self.window_string.destroy,style='W.TButton',cursor='hand2').place(in_=self.window_string,x=570,  y=465)
            ttk.Button(self.labeldefinition, text='Explorar',command=self.browsedirectory,style = 'W.TButton',cursor='hand2').grid(row=3,column=0,pady=5,sticky='w')
            ttk.Button(self.window_string,text="Nueva Busqueda",command=self.cleartable,
                                        style='W.TButton',cursor='hand2').place(in_=self.window_string,x=350,  y=170)


            labelformat=tk.LabelFrame(self.window_string,text="tipo Archivo",foreground='grey')
            labelformat.place(in_=self.window_string,x=410,  y=40)
            #labelformat.grid(row=0,column=2)
            self.varformat=  StringVar()   
            combofiles = ttk.Combobox(labelformat,textvariable=self.varformat,
                            values=[
                                    ".Html", 
                                    ".txt",
                                    ".csv",
                                    ".py"])
            combofiles.set("Desplegar")  
            combofiles.grid(row=1,column=3,pady=2,padx=3)

            labeltreevstring=tk.LabelFrame(self.window_string,text="Cadenas",foreground='grey')
            labeltreevstring.place(in_=self.window_string,x=10,  y=200,  relx=0.01,  rely=0.01)
            #labeltreevstring.grid(row=6,column=0,columnspan=1)
            tree_scroll = Scrollbar(labeltreevstring)
            tree_scroll.pack(side=RIGHT, fill=Y)
            columns=('ruta','documento','linea')
            self.tree = ttk.Treeview(labeltreevstring, columns=columns, show='headings',yscrollcommand=tree_scroll.set,selectmode="extended")
            self.tree = ttk.Treeview(labeltreevstring, columns=columns, show='headings')
            self.tree.heading('ruta', text='Ruta')
            self.tree.heading('documento', text='Documento')
            self.tree.heading('linea', text='Linea')
            self.tree.column("# 3",width=260)
            self.tree.tag_configure('oddrow', background="white")
            self.tree.tag_configure('evenrow', background="lightblue")
            self.tree.pack()
            tree_scroll.config(command=self.tree.yview)
           
        def seekfile(self):
            if self.window_string:
                self.window_string.pack_forget()
            
            self.ventana_file=tk.Frame(self.ventana,width=500,height=700)
            self.ventana_file.pack(fill="both",expand="yes")
            Labeltitlefile=Label(self.ventana_file,text="Busqueda por Archivo")
            Labeltitlefile.config(foreground='Red',font=('Comic Sans Ms',15))
            Labeltitlefile.place(in_=self.ventana_file,x=240,  y=0)
            
            labeldefinition=tk.LabelFrame(self.ventana_file,text="Define cadena",foreground='grey')
            labeldefinition.place(in_=self.ventana_file,x=5,y=30)
            label_file=Label(labeldefinition,text="Nombre o caracteres de documento  ")
            label_file.grid(row=1,column=0,pady=2)
            self.entryFile=Entry(labeldefinition)
            self.entryFile.grid(row=2,column=0,pady=4,padx=2,sticky='w')
            ttk.Button(labeldefinition,text="Explorar",command=self.browsedirectory,cursor='hand2',style='W.TButton').grid(row=3,column=0,sticky='w',pady=5)
            
            labelcaract=tk.LabelFrame(self.ventana_file,text="Definición Caracteres",foreground='grey')
            labelcaract.place(in_=self.ventana_file,x=380,y=30)
            self.choosecaract=IntVar()
            self.strempieza=tk.Radiobutton(labelcaract,text='Empieza',variable=self.choosecaract,value=1)
            self.strempieza.grid(row=1,column=2,pady=2,sticky='w')
            self.strtermina=tk.Radiobutton(labelcaract,text="Termina",variable=self.choosecaract,value=2)
            self.strtermina.grid(row=3,column=2,pady=2,sticky='w')
            self.strentre=tk.Radiobutton(labelcaract,text='Entre',variable=self.choosecaract,value=3)
            self.strentre.grid(row=2,column=2,pady=2,sticky='w')
            self.strall=tk.Radiobutton(labelcaract,text='Todos los archivos',variable=self.choosecaract,value=4)
            self.strall.grid(row=4,column=2,pady=2,sticky='w')
            
            labelformat=tk.LabelFrame(self.ventana_file,text='Formato',foreground='grey')
            labelformat.place(in_=self.ventana_file,x=225,y=30)
            self.choseformat=IntVar()
            self.anyformat=tk.Radiobutton(labelformat,text='Todos los formatos',value=1,variable=self.choseformat)
            self.anyformat.grid(row=6,column=2,pady=2,sticky='w')
            self.specificformat=tk.Radiobutton(labelformat,text='Especificar',value=2,variable=self.choseformat,command=self.enableentry)
            self.specificformat.grid(row=7,column=2,pady=2,sticky='w')
            self.entrystringfile=Entry(labelformat)
            self.entrystringfile.grid(row=8, column=2,padx=4)
            self.entrystringfile.config(state="disable")

            ttk.Button(self.ventana_file,text='Buscar',command=self.seek_file,style='W.TButton',cursor='hand2').place(in_=self.ventana_file,x=240,  y=175)
            ttk.Button(self.ventana_file,text='Cerrar',command=self.ventana_file.destroy,style='W.TButton',cursor='hand2').place(in_=self.ventana_file,x=570,  y=465)
            ttk.Button(self.ventana_file,text="Nueva Busqueda",command=self.cleartablefile,
                                        style='W.TButton',cursor='hand2').place(in_=self.ventana_file,x=350,  y=175)

            labeltreevfile=tk.LabelFrame(self.ventana_file,text="Archivos",foreground='grey')
            labeltreevfile.place(in_=self.ventana_file,x=10,  y=200,  relx=0.01,  rely=0.01)
            tree_scrollfile = Scrollbar(labeltreevfile)
            tree_scrollfile.pack(side=RIGHT, fill=Y)
            columns=('fRuta','fDocumento')
            self.treef = ttk.Treeview(labeltreevfile, columns=columns, show='headings',yscrollcommand=tree_scrollfile.set,selectmode="extended")
                #self.treef = ttk.Treeview(labeltreevfile, columns=columns, show='headings')
            self.treef.heading('fRuta', text='Ruta',anchor=CENTER)
            self.treef.column("fRuta",width=300)
            self.treef.heading('fDocumento', text='Documento',anchor=CENTER)
            self.treef.column("# 2",width=300)
            self.treef.column("# 1",width=340)
            self.treef.tag_configure('oddrow', background="white")
            self.treef.tag_configure('evenrow', background="lightblue")
            self.treef.pack()
            tree_scrollfile.config(command=self.treef.yview)

        def seek_instrucction(self):
            if len(self.string_Entry.get()) ==0:
                tk.messagebox.showinfo(title='Atencion!', message='Ingrese cadena de texto')
            varstr=self.string_Entry.get()
            varpath=self.filename
            varformato=self.varformat.get()
            os.chdir(varpath)
            subprocess.run(f"findstr /s /i {varstr} *{varformato} > resultado.txt", shell=True)
            labelfile_result=Label(self.labeldefinition, text="Archivo generado!!", foreground="blue")
            labelfile_result.grid(row=3,column=1,pady=2)
            separador=varformato + ':'
            strframe = pd.read_table("resultado.txt", sep=separador,engine ='python', names=["Path","string"])
            strframe.insert(0,'NPath', strframe.Path + varformato )
            strframe.insert(1,'documento', strframe.NPath)
            strframe.insert(2,'pasoPath', strframe.NPath)
            for itera in strframe.NPath:
                conviertestr=str(itera)
                eliminastr=re.sub(r'.*?\\',"",conviertestr)
                strframe.loc[strframe.NPath==itera,'documento']=eliminastr
                  
            for itera in strframe.pasoPath:
                find_index=0
                tup_string=[]
                final_string=()
                convierte=str(itera)
                convierte=varpath + '\\' + convierte
                p = convierte.find("\\",find_index)
                while p != -1:
                    p=convierte.find("\\",find_index)
                    if p != -1:
                        find_index= p + 1
                tup_string.append(convierte[:find_index])
                final_string=''.join(tup_string)
                strframe.loc[strframe.pasoPath==itera,'NPath']=final_string
            strframe.drop(['Path','pasoPath'],axis=1,inplace=True)

            count=2
            for index,row  in strframe.iterrows():
                if count % 2 != 0:
                    self.tree.insert('', "end",text=index, values=list(row),tags=('oddrow'))
                    count += 1
                else:
                    self.tree.insert('', "end",text=index, values=list(row),tags=('evenrow'))
                    count += 1
                

        def seek_file(self):
            varPth=self.filename
            varPth=varPth.replace('/','\\')

            if self.choosecaract.get()==1 and self.choseformat.get()==2:
                seekfileipart1=(f'where /R {varPth} {self.entryFile.get()}*.{self.entrystringfile.get()} > paso.txt')

            if self.choosecaract.get()==1 and self.choseformat.get() == 1:
                seekfileipart1=(f'where /R {varPth} {self.entryFile.get()}* > paso.txt')

            if self.choosecaract.get()==2 and self.choseformat.get()==2:
                seekfileipart1=(f'where /R {varPth} *{self.entryFile.get()}*.{self.entrystringfile.get()} > paso.txt')
            
            if self.choosecaract.get()==2 and self.choseformat.get() == 1:
                seekfileipart1=(f'where /R {varPth} *{self.entryFile.get()}* > paso.txt')
            
            if self.choosecaract.get()==3 and self.choseformat.get()==2:
                seekfileipart1=(f'where /R {varPth} *{self.entryFile.get()}.{self.entrystringfile.get()} > paso.txt')
           
            if self.choosecaract.get()==3 and self.choseformat.get() == 1:
                seekfileipart1=(f'where /R {varPth} *{self.entryFile.get()} > paso.txt')

            if self.choseformat.get() == 1 and self.choosecaract.get()==4:
                seekfileipart1=(f'where /R {varPth} {self.entryFile.get()}.* > paso.txt')
            
            if self.choseformat.get() == 2 and self.choosecaract.get()==4:
                seekfileipart1=(f'where /R {varPth} {self.entryFile.get()}.{self.entrystringfile.get()} > paso.txt')

            notfound='no se pudo encontrar'
            proc=subprocess.Popen(seekfileipart1,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
            (err,out) = proc.communicate()
            outstring=str(out)

            if notfound in outstring:
                messagebox.showerror(title='Error!!',message='Patron no encontrado')
            else:

                fileframe = pd.read_table("paso.txt",engine ='python', names=["Path"])
                fileframe.insert(1,'Documento', fileframe.Path)
                fileframe.insert(0,'pasoPath', fileframe.Path)
                for itera in fileframe.Path:
                    conviertestr=str(itera)
                    eliminastr=re.sub(r'.*?\\',"",conviertestr)
                    fileframe.loc[fileframe.Path==itera,'Documento']=eliminastr

                for itera in fileframe.pasoPath:
                    find_index=0
                    tup_string=[]
                    final_string=()
                    convierte=str(itera)
                    convierte=varPth + '\\' + convierte
                    p = convierte.find("\\",find_index)
                    while p != -1:
                        p=convierte.find("\\",find_index)
                        if p != -1:
                            find_index= p + 1
                    tup_string.append(convierte[:find_index])
                    final_string=''.join(tup_string)
                    fileframe.loc[fileframe.pasoPath==itera,'Path']=final_string
                fileframe.drop(['pasoPath'],axis=1,inplace=True)

            count=1
            for index,row  in fileframe.iterrows():
                if count % 2 != 0:
                    self.treef.insert('', "end",text=index, values=list(row),tags=('oddrow'))
                    count += 1
                else:
                    self.treef.insert('', "end",text=index, values=list(row),tags=('evenrow'))
                    count += 1
            
            self.ventana_file.destroy


        def result_string_format(self):
            f=open('resultado.txt' "w")
            
        
        def browsedirectory(self): 
            self.filename = tk.filedialog.askdirectory()
        
        def cleartable(self):
                if self.tree.focus():
                    records=self.tree.get_children()
                    for elements in records:
                        self.tree.delete(elements)
                else:
                    tk.messagebox.showinfo(title='Atencion!', message='Realizar busqueda primero')


        def cleartablefile(self):
                if self.treef.focus():
                    records=self.treef.get_children()
                    for elements in records:
                        self.treef.delete(elements)
                else:
                    tk.messagebox.showinfo(title='Atencion!', message='Realizar busqueda primero')

        def openfile(self):
            if self.tree.focus():
                selected=self.tree.focus()
                temp = self.tree.item(selected, 'values')
                pathconcat=temp[0] + temp[1]
                pathconcat=str(pathconcat)
                print(type(pathconcat))
                print(pathconcat)
                subprocess.run(pathconcat,shell=True)
            else:
                tk.messagebox.showinfo(title='Atencion!', message='Debe seleccionar un registro primero')
        
        def enableentry(self):
                self.entrystringfile.config(state="enabled")
                self.entrystringfile.update()
        

if __name__==('__main__'):
    root=Tk()
    apllication=seekwindow(root)
    root.mainloop()