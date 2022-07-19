from tkinter import * 
import tkinter as tk
import tkinter.ttk as ttk
import PIL
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from ImageToSpikes import ImageToSpikes
from Network import Network
from SpykeTorch import utils as ut
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

image_place = None
image_place2 = None
snn = None
figure1 = None
figure2 = None
diff_figures = []

def give_spikes(image,neurons,runtime,grid_x,grid_y,colspan = 1,fig = 1):
    global figure1,figure2
    if image == None or image == () or image == "":
        messagebox.showerror("Error", "You should choose an image to work on!")
    elif neurons.get() < 2:
        messagebox.showerror("Error", "You should give a positive number for the dimension of the input neural population greater than or equal to 2!")
    elif runtime.get() <= 0:
        messagebox.showerror("Error", "The runtime should be at least 1!")
    elif runtime.get() > neurons.get() * neurons.get():
        
        messagebox.showerror("Error", "The squate of the runtime should be less than the input neurons!")
        
    else:
        ret = ImageToSpikes(image)
        ret_spikes = ret.to_spikes(neurons.get(),runtime.get())
        figure = plt.Figure(figsize=(5,5), dpi=50)
        ax = figure.add_subplot(111)
        ret.plot_spikes(ax)
        if fig == 1:
            figure1 = FigureCanvasTkAgg(figure, frame)
            figure1.get_tk_widget().grid(row = grid_x,column = grid_y,columnspan = colspan,padx = (10,30), pady = 20)
        elif fig == 2:
            figure2 = FigureCanvasTkAgg(figure, frame)
            figure2.get_tk_widget().grid(row = grid_x,column = grid_y,columnspan = colspan,padx = (10,30), pady = 20)

def get_normal_page():
    menu = Menu(root)
    root.config(menu=menu)
    
    menu.add_command(label='Home', command=home_window,activebackground='#0BB5FF')
    menu.add_command(label='Get Spikes', command=spike_window,activebackground='#0BB5FF')
    menu.add_command(label='Compare images', command=compare_window,activebackground='#0BB5FF')
    menu.add_command(label='Observe path', command=path_window,activebackground='#0BB5FF')
    menu.add_command(label='Exit', command=root.quit,activebackground='#0BB5FF')
    
    root.title("Street attention application")
    root['background']='#0BB5FF'
    
def home_window():
    global frame
    frame.destroy()
    frame = tk.Frame(root)
    frame['bg'] = '#0BB5FF'
    frame.grid()
    
    Label(frame, text ="Street attention application",font=("Arial", 30),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 0)
    open_img(1,0,"network.jpg",resize = 300)
    
def remove_img(fig=1):
    global figure1, figure2, diff_figures
    if fig == 1:
        if figure1 != None and figure1 != '':
            figure1.get_tk_widget().destroy()
            figure1 = None
    elif fig == 2:
        if figure2 != None and figure2 != '':
            figure2.get_tk_widget().destroy()
            figure2 = None
    if diff_figures != []:
        diff_figures[0].get_tk_widget().destroy()
        diff_figures[1].get_tk_widget().destroy()
        diff_figures = []
        
def spike_window():
    global frame,image_place,figure1
    image_place = None
    frame.destroy()
    frame = tk.Frame(root)
    frame['bg'] = '#0BB5FF'
    frame.grid()
    
    Label(frame, text ="Create spikes from an image",font=("Arial", 25),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 0,column = 1,columnspan = 8, padx = 20,pady = 20)
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=1, columnspan=8, sticky='we', padx = 20, pady = (0,20))
    
    neurons = IntVar()
    neurons.set(16)
    runtime = IntVar()
    runtime.set(100)
    Label(frame, text ="Input Neurons",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=2,column = 1,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = neurons, from_ = 2, to = 32,width = 3).grid(row=2,column=2,padx = 7,pady = 20)
    Label(frame, text ="Runtime",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=2,column=4,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = runtime,from_ = 1, to = 500,width = 4).grid(row=2,column=5,padx = 7,pady = 20)
    Button(frame, text ='Choose image', command = lambda: filename(4,1,colspan = 2)).grid(row = 3, column = 1, columnspan = 2,padx = 40)
    neurons.trace("r", lambda a, b, c: remove_img())
    runtime.trace("r", lambda a, b, c: remove_img())
    
    Button(frame, text ="Spikes",bg = '#0BB5FF',relief="raised",fg ='white',font=("Arial", 15),command = lambda: give_spikes(image_place,neurons,runtime,4,4,colspan = 5)).grid(row=3,column = 4,columnspan = 5,padx = 30,pady = 20)
    
def path_window():
    global frame,image_place,snn,frame1
    snn = None
    image_place = None
    frame.destroy()
    frame = tk.Frame(root)
    frame['bg'] = '#0BB5FF'
    frame.grid()
    
    neurons = IntVar()
    neurons.set(16)
    runtime = IntVar()
    runtime.set(100)
    kernel_size = IntVar()
    kernel_size.set(5)
    horiz = IntVar()
    vert = IntVar()
    diag45 = IntVar()
    diag135 = IntVar()
    circle = IntVar()
    weights_to_v2 = IntVar()
    weights_to_v2.set(7)
    weights_to_v4_1 = IntVar()
    weights_to_v4_1.set(4)
    weights_to_v4_2 = IntVar()
    weights_to_v4_2.set(12)
    weights_to_lip = IntVar()
    weights_to_lip.set(12)
    weights_wta = IntVar()
    weights_wta.set(-10)
    
    Label(frame, text ="The spiking neural network and its components",font=("Arial", 25),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 0,column = 1,columnspan = 10, padx = 20, pady = 20)
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=1, columnspan=10, sticky='we', padx = 20, pady = (0,20))
    
    Label(frame, text ="Input parameters",font=("Arial", 20),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 2,column = 1,columnspan = 3, padx = 20, pady = 20)
    Label(frame, text ="Input Neurons",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=3,column = 1,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = neurons, from_ = 4, to = 32,width = 3).grid(row=3,column=2,padx = 7,pady = 20)
    Label(frame, text ="Runtime",bg = '#0BB5FF',bd = 2,relief="groove",fg ='white',font=("Arial", 15)).grid(row=4,column=1,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = runtime,from_ = 1, to = 500,width = 4).grid(row=4,column=2,padx = 7,pady = 20)
    Button(frame, text ='Choose image', command = lambda: filename(4,2,rowspan = 6,resize = 150)).grid(row = 5, column = 1,padx = 40)
    ttk.Separator(frame, orient=VERTICAL).grid(column=3, row=2, rowspan=7, sticky='ns', padx = 10, pady = (0,20))
    
    Label(frame, text ="Data filtering",font=("Arial", 20),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 2,column = 4, padx = (160,0), pady = 20)
    Label(frame, text ="Kernel size",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=3,column = 4,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = kernel_size, from_ = 3, to = 7,width = 3).grid(row=3,column=5,padx = (0,150),pady = 20)
    Label(frame, text ="Gaussian filters",bg = '#0BB5FF',bd = 2,relief="groove",fg ='white',font=("Arial", 15)).grid(row=4,column=4,padx = (160,0),pady = 20)
    Checkbutton(frame, text='Horizontal',bg = '#0BB5FF', variable=horiz).grid(row=5,column=4,padx = 7,pady = 20)
    Checkbutton(frame, text='Vertical',bg = '#0BB5FF', variable=vert).grid(row=5,column=5,padx = 7,pady = 20)
    Checkbutton(frame, text='Diagonal (45°)',bg = '#0BB5FF', variable=diag45).grid(row=6,column=4,padx = 7,pady = 20)
    Checkbutton(frame, text='Diagonal (135°)',bg = '#0BB5FF', variable=diag135).grid(row=6,column=5,padx = 7,pady = 20)
    Checkbutton(frame, text='Circle',bg = '#0BB5FF', variable=circle).grid(row=7,column=4,padx = 7,pady = 20)
    ttk.Separator(frame, orient=VERTICAL).grid(column=6, row=2, rowspan=7, sticky='ns', padx = 20, pady = (0,20))
    
    Label(frame, text ="Synapses weights",font=("Arial", 20),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 2,column = 7,columnspan = 9, padx = 20, pady = 20)
    Label(frame, text ="V1 => V2",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=3,column = 7,padx = 30,pady = 20)
    Entry(frame,textvariable = weights_to_v2,width = 3).grid(row=3,column = 8,padx = (30,0),pady = 20)
    Label(frame, text ="V2 => V4_1",bg = '#0BB5FF',bd = 2,relief="groove",fg ='white',font=("Arial", 15)).grid(row=4,column=7,padx = 30,pady = 20)
    Entry(frame,textvariable = weights_to_v4_1,width = 3).grid(row=4,column = 8,padx = (30,0),pady = 20)
    Label(frame, text ="V4_1 => V4_2",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=5,column = 7,padx = 30,pady = 20)
    Entry(frame,textvariable = weights_to_v4_2,width = 3).grid(row=5,column = 8,padx = (30,0),pady = 20)
    Label(frame, text ="V4_2 => LIP",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=6,column = 7,padx = 30,pady = 20)
    Entry(frame,textvariable = weights_to_lip,width = 3).grid(row=6,column = 8,padx = (30,0),pady = 20)
    Label(frame, text ="WTA",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=7,column = 7,padx = 30,pady = 20)
    Entry(frame,textvariable = weights_wta,width = 3).grid(row=7,column = 8,padx = (30,0),pady = 20)
    
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=8, columnspan=10, sticky='we', padx = 20, pady = 20)
    Label(frame, text ="Execute the network for visual observations",font=("Arial", 20),bd = 2,bg = '#0BB5FF',relief="flat",fg ='white').grid(row=9,column = 2,columnspan = 3,padx = (0,0),pady = 20)
    Button(frame, text ="Run Network",bg = '#0BB5FF',relief="raised",fg ='white',font=("Arial", 15),command = lambda: compute_network(image_place,neurons,runtime,kernel_size,[horiz,diag135,vert,diag45,circle],[weights_to_v2.get(),weights_to_v4_1.get(),weights_to_v4_2.get(),weights_to_lip.get(),weights_wta.get()])).grid(row=10,column = 2, columnspan = 3,padx = 30,pady = 20)
    
    neurons.trace("r", lambda a, b, c: remove_img())
    runtime.trace("r", lambda a, b, c: remove_img())
    kernel_size.trace("r", lambda a, b, c: remove_img())
    #horiz.trace("r", lambda a, b, c: remove_img())
    #vert.trace("r", lambda a, b, c: remove_img())
    #diag45.trace("r", lambda a, b, c: remove_img())
    #diag135.trace("r", lambda a, b, c: remove_img())
    #circle.trace("r", lambda a, b, c: remove_img())
    weights_to_v2.trace("r", lambda a, b, c: remove_img())
    weights_to_v4_1.trace("r", lambda a, b, c: remove_img())
    weights_to_v4_2.trace("r", lambda a, b, c: remove_img())
    weights_to_lip.trace("r", lambda a, b, c: remove_img())
    weights_wta.trace("r", lambda a, b, c: remove_img())
    
    Label(frame, text ="Choose layer to display",font=("Arial", 20),bd = 2,bg = '#0BB5FF',relief="flat",fg ='white').grid(row=9,column = 5,columnspan = 7,padx = (0,0),pady = 20)
    display = StringVar()
    display_spikes = ttk.Combobox(frame,width = 5,textvariable = display)
    display_spikes['values'] = ('v1','v2','v4_1','v4_2','lip')
    display_spikes.grid(row = 10, column = 7)
    
    display.trace("r", lambda a, b, c: remove_img())
    
    Button(frame, text ="Display",bg = '#0BB5FF',bd = 2,relief="raised",fg ='white',font=("Arial", 15),command = lambda: display_network(display)).grid(row = 10, column = 6)  #row=3,column=10,padx = (30,0),pady = 20)
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=11, columnspan=10, sticky='we', padx = 20, pady = 20)

def compute_network(img,neurons,runtime,kernel_size,gaussian_filters,weights):
    global snn
    filters = []
    if img == None or img == () or img == "":
        messagebox.showerror("Error", "You should choose an image to work on!")
    elif neurons.get() < 4:
        messagebox.showerror("Error", "You should give a positive number for the dimension of the input neural population greater than or equal to 4!")
    elif runtime.get() <= 0:
        messagebox.showerror("Error", "The runtime should be at least 1!")
    elif runtime.get() > neurons.get() * neurons.get():
        messagebox.showerror("Error", "The squate of the runtime should be less than the input neurons!")
    elif gaussian_filters[0].get() == 0 and gaussian_filters[1].get() == 0 and gaussian_filters[2].get() == 0 and gaussian_filters[3].get() == 0 and gaussian_filters[4].get() == 0:
        messagebox.showerror("Error", "You should choose at least 1 Gaussian filter!")
    elif neurons.get() - kernel_size.get() + 1 <= 4:
        messagebox.showerror("Error", "The filter is too big. You should choose bigger value for the input neurons or lower value for the kernel size!")
    else:
        for i in range(len(gaussian_filters)):
            if gaussian_filters[i].get() == 0:
                filters.append(None)
            else:
                if i == 0:
                    filters.append(0)
                elif i == 1:
                    filters.append(135)
                elif i == 2:
                    filters.append(90)
                elif i == 3:
                    filters.append(45)
                elif i == 4:
                    filters.append(1)
                else:
                    filters.append(None)
        snn = Network(neurons.get(),runtime.get(),img,kernel_size.get(),filters,weights)
        snn.create_network()
        messagebox.showinfo("Success", "The network was successfully executed. Now you can display and observe each layer.")
    
def display_network(layer):
    global snn,figure1
    if figure1 != None:
        figure1.get_tk_widget().destroy()
        figure1 = None
        
    if layer.get() != None and snn != None and layer.get() != "":
        figure = plt.Figure(figsize=(25,5), dpi=50)
        snn.display(layer.get(),figure)
        figure1 = FigureCanvasTkAgg(figure, frame)
        figure1.get_tk_widget().grid(row = 11,column = 2,columnspan = 6,pady = 20)
    elif snn == None:
        messagebox.showerror("Error", "You should run the network!")
    elif layer.get() == None or layer.get() == "":
        messagebox.showerror("Error", "Choose a layer to display!")
           
def compare_window():
    global frame,image_place,image_place2,figure1,figure2,diff_figures
    image_place = None
    image_place2 = None
    frame.destroy()
    frame = tk.Frame(root)
    frame['bg'] = '#0BB5FF'
    frame.grid()
    
    Label(frame, text ="Compare spikes of two images",font=("Arial", 25),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 0,column = 1,columnspan = 19,padx = 20,pady = 20)
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=1, columnspan=19, sticky='we', padx = 20, pady = (0,20))
    
    #First Picture
    neurons = IntVar()
    neurons.set(16)
    runtime = IntVar()
    runtime.set(100)
    
    Label(frame, text ="Input Neurons",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=2,column = 1,padx = (10,0),pady = 20)
    Spinbox(frame,textvariable = neurons, from_ = 2, to = 32,width = 3).grid(row=2,column=2,padx = 7,pady = 20)
    Label(frame, text ="Runtime",bg = '#0BB5FF',bd = 2,relief="groove",fg ='white',font=("Arial", 15)).grid(row=2,column=3,padx = (10,0),pady = 20)
    Spinbox(frame,textvariable = runtime,from_ = 1, to = 500,width = 4).grid(row=2,column=4,padx = 7,pady = 20)
    Button(frame, text ='Choose image', command = lambda: filename(4,1,colspan = 2)).grid(row = 3, column = 1, columnspan = 2,padx = 20)
    neurons.trace("r", lambda a, b, c: remove_img())
    runtime.trace("r", lambda a, b, c: remove_img())
    
    Button(frame, text ="Spikes",bg = '#0BB5FF',relief="raised",fg ='white',font=("Arial", 15),command = lambda: give_spikes(image_place,neurons,runtime,4,3,colspan = 4)).grid(row=3,column = 3,columnspan = 4,padx = 10,pady = 20)
    Label(frame,text ="  ",bg = '#0BB5FF').grid(row = 4, column = 5,columnspan = 7,padx = 40)
    # Second Picture
    neurons2 = IntVar()
    neurons2.set(16)
    runtime2 = IntVar()
    runtime2.set(100)
    Label(frame, text ="Input Neurons",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=2,column = 8,padx = (10,0),pady = 20)
    Spinbox(frame,textvariable = neurons2, from_ = 2, to = 32,width = 3).grid(row=2,column=9,padx = 7,pady = 20)
    Label(frame, text ="Runtime",bg = '#0BB5FF',bd = 2,relief="groove",fg ='white',font=("Arial", 15)).grid(row=2,column=15,padx = (30,0),pady = 20)
    Spinbox(frame,textvariable = runtime2,from_ = 1, to = 500,width = 4).grid(row=2,column=16,padx = 7,pady = 20)
    Button(frame, text ='Choose image', command = lambda: filename(4,7,image_number = 2,colspan = 8)).grid(row = 3, column = 8, columnspan = 2,padx = 40)
    
    Button(frame, text ="Spikes",bg = '#0BB5FF',relief="raised",fg ='white',font=("Arial", 15),command = lambda: give_spikes(image_place2,neurons2,runtime2,4,15,colspan = 16,fig = 2)).grid(row=3,column = 13,columnspan = 14,padx = 30,pady = 20)
    neurons2.trace("r", lambda a, b, c: remove_img(fig=2))
    runtime2.trace("r", lambda a, b, c: remove_img(fig=2))
    
    ttk.Separator(frame, orient=HORIZONTAL).grid(column=1, row=5, columnspan=19, sticky='we', padx = 20, pady = 20)
    #Execution
    Button(frame, text ='Compare', command = lambda: compare_spikes(image_place,image_place2,neurons,neurons2,runtime,runtime2)).grid(row = 6,column = 6) ######################Change
    
def compare_spikes(image,image2,neurons,neurons2,runtime,runtime2):
    global diff_figures
    if image == None or image == () or image == "" or image2 == None or image2 == () or image2 == "":
        messagebox.showerror("Error", "You should choose an images to work on!")
    elif neurons.get() <= 2 or neurons2.get() < 2:
        messagebox.showerror("Error", "You should give a positive number for the dimension of the input neural population greater than or equal to 2!")
    elif runtime.get() <= 0 or runtime2.get() <= 0:
        messagebox.showerror("Error", "The runtime should be at least 1!")
    elif runtime.get() > neurons.get() * neurons.get() or runtime2.get() > neurons2.get() * neurons2.get():
        messagebox.showerror("Error", "The squate of the runtime should be less than the input neurons!")
        
    else:
        #image 1
        retina = ImageToSpikes(image)
        retina.to_spikes(neurons.get(),runtime.get())
        
        #image 2
        retina2 = ImageToSpikes(image2)
        retina2.to_spikes(neurons2.get(),runtime2.get())
        
        figure = plt.Figure(figsize=(5,5), dpi=50)
        ax = figure.add_subplot(111)
        retina.display_difference(retina2,ax)
        
        fig2 = plt.Figure(figsize=(5,5), dpi=50)
        ax2 = fig2.add_subplot(111)
        retina.display_common(retina2,ax2)
        
        diff_figures = []
        
        Label(frame, text ="Difference",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=8,column = 3,padx = (10,0),pady = 20)
        spikes = FigureCanvasTkAgg(figure, frame)
        spikes.get_tk_widget().grid(row = 9, column = 3)#, columnspan = 4)
        diff_figures.append(spikes)
        filename
        Label(frame, text ="Common Spikes",font=("Arial", 15),bd = 2,bg = '#0BB5FF',relief="groove",fg ='white').grid(row=8,column = 7,columnspan = 8,padx = (10,0),pady = 20)
        spikes2 = FigureCanvasTkAgg(fig2, frame)
        spikes2.get_tk_widget().grid(row = 9, column = 7,columnspan = 8)    
        diff_figures.append(spikes2)
        
    
def open_img(grid_x,grid_y,img_path,rowspan = 0,colspan=0,resize = 250):
    #global frame
    img = Image.open(img_path)
    if resize == 300:
        img = img.resize((900, 300), Image.ANTIALIAS)
    else:
        img = img.resize((resize, resize), Image.ANTIALIAS)
        
    img = ImageTk.PhotoImage(img)
    panel = Label(frame, image = img)
    panel.image = img
    
    if rowspan == 0 and colspan == 0:
        panel.grid(row = grid_x, column = grid_y,padx = 40,pady=20)
    elif rowspan == 0:
        panel.grid(row = grid_x, column = grid_y,columnspan = colspan,padx = 40,pady=20)
    elif colspan == 0:
        panel.grid(row = grid_x, column = grid_y,rowspan = rowspan,padx = 40,pady=20)
    else:
        panel.grid(row = grid_x, column = grid_y,rowspan = rowspan,columnspan = colspan,padx = 40,pady=10)
    
def filename(grid_x, grid_y, image_number = 1,rowspan=0,colspan=0,resize=250):
    global image_place,image_place2
    valid_images = ['.jpg','.png']
    file = filedialog.askopenfilename(title ='choose image')
    if file[-4:] in valid_images:
        open_img(grid_x, grid_y,file,rowspan,colspan,resize=resize)
        if image_number == 1:
            image_place = None
            image_place = file
        else:
            image_place2 = None
            image_place2 = file
    else:
        #return None
        messagebox.showerror("Error", "You should choose a valid image file (jpg or png)!")
root = Tk()

root.resizable(width = True, height = True)
root.columnconfigure(0,weight=1,minsize=75)
root.rowconfigure(0,weight=1,minsize=55)
get_normal_page()
frame = tk.Frame(root)
frame['bg'] = '#0BB5FF'
frame.grid()

Label(frame, text ="Street attention application",font=("Arial", 30),bg = '#0BB5FF',relief="flat",fg ='white').grid(row = 0)
open_img(1,0,"network.jpg",resize = 300)

  
root.mainloop()