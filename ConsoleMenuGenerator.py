""" Project: Web/Html Scraper, Coder: Hakan Etik, Date:18.08.2016 """
"""Code source http://stackoverflow.com/questions/15083900/console-menu-generator-in-python"""
import sys
import os
import time

#Item class function definitions
class Item:
    def __init__(self, name, function, parent=None):
        self.name = name
        self.item_number = 0
        self.function = function
        self.parent = parent
        if parent:
            parent.add_item(self) 

    def draw(self):
        print self.item_number,
        print(" " + self.name)

    def set_item_number(self, number):
        self.item_number = number

    def run_item(self):
        self.function()

#Menu class function definitions        
class Menu:
    def __init__(self, name, items=None):
        self.name = name
        self.items = items or []

    def add_item(self, item):
        self.items.append(item)
        if item.parent != self:
            item.parent = self

    def remove_item(self, item):
        self.items.remove(item)
        if item.parent == self:
            item.parent = None

    def draw(self):
        print(self.name)
        item_number = 1
        for item in self.items:
            item.set_item_number(item_number)
            item.draw()
            item_number = item_number + 1

    def run(self, item_num):
        self.items[item_num].run_item()

    def terminate(self):
        print "bye"
        time.sleep(1) # delays for 1 seconds
        sys.exit(0)

    def cls(self):
        os.system('cls' if os.name=='nt' else 'clear')

#Item example specific functions
def openFile():
    print("OPEN FILE")

def closeFile():
    print("CLOSE FILE")	

#Main
def main():
    main_menu = Menu("***Vestel Nightbot***")
    # automatically calls main.AddItem(item1)
    open = Item("Open", openFile, main_menu)

    # automatically sets parent to main
    main_menu.add_item(Item("Close", closeFile))
    main_menu.add_item(Item("Exit", main_menu.terminate))

    main_menu.cls() # clear console before drawing

    while(True):
	    try:
		    main_menu.draw()
		    n=input("choice>")
		    main_menu.run(n-1)
	    except Exception as e:
		    print("Undefined option please select defined option\n\n")
		    time.sleep(1) # delays for 1 seconds
		    main_menu.cls()

if __name__=='__main__':
    main()