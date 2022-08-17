import tkinter as tk
import tkinter.filedialog as fd


class Menu:

    params = list()

    def __init__(self, gui):
        self.gui = gui
        self.parent = gui.root
        # print("Hello", type(self.gui), dir(self.gui))
        self.menu_bar = tk.Menu()

        self.file_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_dir)
        self.open_recent_menu = self.file_menu.add_command(label="Open recents ...", command=self.open_recent)
        self.file_menu.add_command(label="Add files", command=self.open_dir)

        self.file_menu.add_command(label="Settings", command=self.settings)
        # file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.parent.quit)

        self.help_menu = tk.Menu(master=self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Logs", command=self.show_logs)
        self.help_menu.add_command(label="About", command=self.alert("Under construction"))

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.parent.config(menu=self.menu_bar)


    def alert(self, msg):
        print(msg)


    def open_dir(self):
        """ 
        Open dir browser in local computer, then call Gui.add_item(filepath)

        Return 
        ------
        A path to the targeted folder
        """

        filepath = fd.askdirectory(title="Open directory")
        print("path returned :", filepath)
        # self.params.append(filepath)
        # self.gui.create_main_canvas(parent=self.gui.main_container)
        self.gui.add_items(file_path=filepath)


    def open_recent(self):
        """ 
        Open files in local computer and return a list of path to the targeted files
        """
        # filepath = fd.askopenfilename(title="Open directory", filetypes=[('png files','.png'), ('all files','.*')])
        # photo = tk.PhotoImage(file=filepath)  # sélectionner une image
        # canvas = tk.Canvas(self.root,
        #                    width=600, height=200, 
        #                 #    width=photo.width(), height=photo.height(), 
        #                    bg="#aaa") # Créer un canva à la bonne dimension
        # canvas.create_image(0, 0, anchor=tk.NW, image=photo)  # afficher l'image dans le canva
        # canvas.pack()
        # print("open_dir")
        pass


    def settings(self):
        print("settings")


    def show_logs(self):
        print("show_logs")