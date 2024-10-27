from tkinter import *

root = Tk()

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)


root.add(frame1, text = "Window 1")
command = Label(root, text='Command')
command.grid(column=0, row=1)

command_field = Text(height=5, width=50)
command_field.grid(column=1, row=1)

motors_val = IntVar()
motors_val.set(1)
nums = [1,2]

root.add(frame2, text = "Window 2")
motors_chose = OptionMenu(root, motors_val, *nums)
motors_chose.grid(column=0, row=2)




def func():
    temp = command_field.get("1.0", "end-1c")
    if not temp:
        pass
    else:
        print("Runned ", temp)
    



submit_button = Button(root, text="OK", command=func)
submit_button.grid(column=1, row=4)
root.mainloop() 