import tkinter as tk
from tkinter import ttk
import menu

class Gui:
    color_light = '#eeeeff'
    color_vlight = '#ffffff'

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Audio')
        self.window_width = 1080
        self.window_height = 700
        self.canvas_height = 1200
        self.fig_width = 700
        self.fig_height = 280
        # self.root.geometry(str(self.window_width) + 'x' + str(self.window_height))
        # self.root.config(width=self.window_width, height=self.window_height)

        main_container = tk.Frame(master=self.root, bg='#aaaaee')
        main_container.grid(row=0, column=0)
        
        scroller = ttk.Scrollbar(master=main_container, orient="vertical")
        scroller.grid(row=0, column=1, sticky='ns')
        
        self.main_canvas = tk.Canvas(master=main_container, 
                                    width=(self.window_width - scroller.winfo_width()), height=self.window_height,
                                    bg="blue",
                                    scrollregion=(0, 0, self.window_width, self.window_height),
                                    yscrollcommand=scroller.set)
        self.main_canvas.grid(row=0, column=0)
        
        scroller.config(command=self.main_canvas.yview)

        self.content_wrapper = tk.Frame(master=self.main_canvas, bg=self.color_vlight)
        self.main_canvas.create_window(0, 0,
                                        width=(self.window_width - scroller.winfo_width()), height=self.window_height,
                                        anchor='nw',
                                        window=self.content_wrapper)
        self.content_wrapper.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.default_label = self.create_default_label(self.content_wrapper)

        print("gui created")
        menu.Menu(gui=self)
        self.root.mainloop()  # Lancement de la «boucle principale»


    def create_default_label(self, parent):
        label = tk.Label(master=parent, 
                         text='Open a directory to start the analysis.', 
                         font=('Helvetica', 28, 'bold'), 
                         fg='#aaaaaa', bg=self.color_vlight)
        label.pack(expand=True)
        return label


    def add_items(self, file_path):
        """
        Create a widget for the analysis of a file and place it into the root container.
        Called by menu > File > add directory
        Return
        ------ 
        Null
        """
        # TODO change self.content_wrapper dimension to fit the itmes size
        
        self.default_label.destroy()

        for nb in range(3):
            container = tk.Frame(master=self.content_wrapper, bg=self.color_light, padx=10, pady=10)
            # container.grid(row=nb, column=0, sticky='N')
            container.pack(side='top')
            
            label = tk.Label(master=container, text=file_path+str(nb), 
                             bg=self.color_light, justify='center')
            label.grid(row=0, column=0, columnspan=2)

            canvas = tk.Canvas(master=container,
                               width=self.fig_width, height=self.fig_height, 
                               bg="blue")
            # canvas.pack(side='right', fill='y')
            canvas.grid(row=1, column=0)

            right_side = tk.Frame(master=container, bg="yellow", width=100, padx=10)
            right_side.grid(row=1, column=1)
            tk.Button(master=right_side, text="atachou", padx=5, pady=5).grid(row=0, column=0)
            tk.Button(master=right_side, text="bfdsfb ", padx=5, pady=5).grid(row=1, column=0)
            
            line = tk.Label(master=container, justify='center', 
                            bg=self.color_light,
                            text="________________________________________________________________________________")
            # line = ttk.Separator(master=container, orient='horizontal')
            line.grid(row=2, column=0, columnspan=2)
        
        # self.main_canvas.config(height=container.winfo_height()*nb)
        self.content_wrapper.config(height=container.winfo_height()*3)
        
        print("container height :", container.winfo_height())
        print("wrapper height :", self.content_wrapper.winfo_height())
        print("main_canvas height :", self.main_canvas.winfo_height())

