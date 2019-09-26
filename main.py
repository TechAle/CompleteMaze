## inspired from https://www.youtube.com/watch?v=uuUbdluqSiE ##
## it works but it's bad optimized
## TODO make it better
from tkinter import *
import time
Lista = []
rows = 0
distance = 0
option = 0
n_spawn = 1
n_end = 1
cell = {'spawn': 0, 'end': 0}
num = 0
x_start = x_finish = y_start = y_finish = 0
## class main
class main():
    ## first
    def __init__(self):
        self.height, self.width, self.delay = 500,500,250
        self.start()
    ## start all
    def start(self):
        ## create window root
        self.root = Tk()
        ## event
        self.root.bind("<ButtonPress-1>", lambda event:  # Thanks stackoverflow
        self.onMouseLeftPress(event))
        self.root.bind("<KeyRelease>", lambda event:  # Thanks stackoverflow
        self.onKeyboardPress(event))
        self.root.bind("<Return>", lambda event:  # Thanks stackoverflow
        self.enter(event))
        ## root to canvas
        self.canvas = Canvas(self.root, width = self.width, height=self.height, highlightthickness=0)
        ## setup widgets
        self.canvas.pack()
        self.screen()


    # The defualt Grid When no file is present




    ## start screen
    def screen(self):
        global rows
        rows = 10
        global Lista
        self.canvas.create_rectangle(-1,-1,self.width,self.height,fill = "white")
        instructions = """\nq: quit\nz: add spawn\nx: add end\nc: clear\nclick to modify \n(light = wall, gray = empty)\n(blue = spawn, yellow = end)"""
        self.canvas.create_text(self.width/2, self.height/10, text="Maze Create",
                                font="Arial 60 bold")
        self.canvas.create_text(self.width / 2 / 1.5, self.height/3-self.height/20,
                                text=instructions, font="Arial 15 bold")
        self.canvas.create_text(self.width-self.width/2 + self.width/4, self.height/3-self.height/20, text="inserti number\n+enter for\nresize maze\np: complete maze\nw-a-s-d = move",font="Arial 15 bold")
        ## start create box
        global x_start, x_finish, y_start, y_finish
        y_start = self.height/2-self.height/20
        y_finish = self.height-self.height/20
        D_y = y_finish - y_start
        x_start = self.width / 2 - D_y/2
        x_finish = self.width / 2 + D_y/2
        ## draw grid
        self.create_grid()
        self.draw_grid()
        self.root.mainloop()

    def draw_grid(self):
        ## drawn grid
        global Lista
        global rows
        global distance
        for i in range(rows):
            for j in range(rows):
                self.canvas.create_rectangle(Lista[i * rows + j]['x_in'], Lista[i * rows + j]['y_in'],
                                     Lista[i * rows + j]['x_fin'], Lista[i*rows+j]['y_fin'],
                                     fill=Lista[i*rows+j]['color'], outline="black")


    def create_grid(self):
        ## create grid (dependence by rows)
        global Lista
        global rows
        global distance, x_start, x_finish, y_start, y_finish
        ## grid:
        D = x_finish - x_start
        distance = D / rows
        print(rows)
        Lista = []
        for i in range(rows):
            for j in range(rows):
                ## create wall
                if i == 0 or j == 0 or i == rows - 1 or j == rows - 1:
                    color = 'gray'
                else:
                    color = 'white'
                ## put everything in a Lista of directory
                Lista.append({'x_in': x_start + j * distance, 'y_in': y_start + i * distance,
                             'x_fin': x_start + j * distance + distance, 'y_fin': y_start + i * distance + distance,
                             'color': color})
        ## set spawn and end
        Lista[rows*rows-rows*3+2]['color'] = 'blue'
        cell['spawn'] = rows*rows-rows*3+2
        Lista[rows*3-3]['color'] = 'yellow'
        cell['end'] = rows*3-3


    def onMouseLeftPress(self, event):
        (mouseX, mouseY) = (event.x, event.y)
        global Lista
        global rows
        global n_spawn
        global n_end
        global cell
        ## controll if the mouse is in the table
        if mouseX > Lista[0]['x_in'] and mouseX < Lista[rows-1]['x_fin'] and mouseY > Lista[0]['y_in'] and mouseY < Lista[rows*rows-1]['y_fin']:
            ## settings for search
            a = []
            a.append([Lista[i]['x_in'] for i in range(rows)])
            a[0].append(Lista[rows-1]['x_fin'])
            a.append([Lista[i * rows]['y_in'] for i in range(rows)])
            a[1].append(Lista[rows-1]['y_fin'])
            ## searching the cell that been clicked by the mouse
            cell_x = self.search(a[0],mouseX)
            cell_y = self.search(a[1],mouseY)
            ## coloring cell
            global option
            if option == 0:
                if Lista[cell_y*rows+cell_x]['color'] == 'gray':
                    Lista[cell_y * rows + cell_x]['color'] = 'white'
                elif Lista[cell_y*rows+cell_x]['color'] == 'white':
                    Lista[cell_y * rows + cell_x]['color'] = 'gray'
                elif Lista[cell_y*rows+cell_x]['color'] == 'blue':
                    print('b')
                    Lista[cell_y * rows + cell_x]['color'] = 'white'
                    n_spawn = 0
                else:
                    Lista[cell_y * rows + cell_x]['color'] = 'white'
                    n_end = 0
            else:
                print('a')
                if option == 1:
                    if n_spawn == 0:
                        Lista[cell_y * rows + cell_x]['color'] = 'blue'
                        n_spawn += 1
                        cell['spawn'] = cell_y * rows + cell_x
                else:
                    if n_end == 0:
                        Lista[cell_y * rows + cell_x]['color'] = 'yellow'
                        n_end += 1
                        cell['end'] = cell_y * rows + cell_x
                option = 0
            self.draw_grid()

    def onKeyboardPress(self, event):
        global option
        ## clear spawn / end
        if event.char == 'z':
            if option != 1:
                option = 1
        elif event.char == 'x':
            if option != -1:
                option = -1
        ## moving button
        elif event.char == 'w':
            self.movement(-rows)
        elif event.char == 's':
            self.movement(rows)
        elif event.char == 'a':
            self.movement(-1)
        elif event.char == 'd':
            self.movement(1)
        elif event.char == 'c':
            self.create_grid();
        elif event.char == 'p':
            self.complete()

        ## check if is a number for resize
        elif event.char.isdigit():
            global num
            max = 30
            event.char = int(event.char)
            if num == 0:
                num = event.char
            else:
                if num < 10:
                    if num*10+event.char:
                        num = num*10+event.char
                else:
                    num = round(num%10)*10+event.char
                print(num)

    def enter(self,event):
        print('a')
        global num
        if num > 5:
            global rows
            rows = num
            self.create_grid()
            self.draw_grid()


    def movement(self,mov):
        global rows
        global Lista
        global cell
        ## controll if the player can
        if Lista[cell['spawn'] + mov]['color'] == 'white':
            Lista[cell['spawn'] + mov]['color'] = 'blue'
            Lista[cell['spawn']]['color'] = 'white'
            cell['spawn'] = cell['spawn'] + mov
            self.draw_grid()
        elif Lista[cell['spawn']+mov]['color'] == 'yellow':
            print('hai vinto')

    def search(self,array_,target):
        ## simple custom dichotomic search
        xIn = 0
        xFin = rows
        found = False
        while not xIn+1 == xFin:
            x2 = round((xIn + xFin) / 2)
            if array_[x2] < target:
                xIn = x2
            elif array_[x2] > target:
                xFin = x2

        return xIn
    def complete(self):
        ## global variable
        global rows, Lista, cell
        ## Lista of all moves
        mov_ = [rows,1,-rows,-1]
        ## prev index array
        prev = 0
        ## create a "repistory" where add all the mouvement
        Lista_check = [{"cell": cell['spawn']}]
        ## loop begin from the last cell that check his mouvement
        i = 0
        fin = True
        limit = len(Lista_check)
        while i < limit and fin:
            for j in mov_:
                if Lista[Lista_check[i]["cell"] + j]["color"] != "yellow":
                    if Lista[Lista_check[i]["cell"] + j]["color"] == "white":
                        Lista[Lista_check[i]["cell"] + j]['color'] = 'green'
                        Lista_check.append({"cell": Lista_check[i]["cell"] + j, "prev": Lista_check[i]["cell"]})
                        self.draw_grid()
                        self.canvas.update_idletasks()

                else:
                    print("fine")
                    fin = False
                    ## print soluction
                    Lista_check.append({"cell": Lista_check[i]["cell"] + j, "prev": Lista_check[i]["cell"]})
                    n_list = [list(i.values()) for i in Lista_check]
                    now = n_list[-1][1]
                    while now != cell["spawn"]:
                        Lista[now]['color'] = "red"
                        ok = True
                        j = 1
                        print(n_list)
                        while ok:
                            if n_list[j][0] == now:
                                ok = not ok
                                now = n_list[j][1]
                            else:
                                j += 1
                        self.draw_grid()
                        self.canvas.update_idletasks()
            i += 1
            limit = len(Lista_check)
















## start
main()