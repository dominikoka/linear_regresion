import time
from turtle import onclick

import cursor as cursor
import requests
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import tkinter as tk
from tkinter import ttk
import seaborn as sns
import mplcursors


from matplotlib.backend_bases import MouseEvent
from matplotlib.widgets import Cursor

res = requests.get('https://robyg.pl/warszawa/wyszukiwarka/wyniki/investment_id=760,572,714,705,689,614/view=table')
soup = BeautifulSoup(res.content, 'html.parser')
# print(soup.prettify()) formularz ktory dodaje naszą kropeczke i podaje o niej informacje ktore mieszkania są nad nią a ktore pod nią

prices = []
squareMeters = []
content = soup.find_all('div', class_='price-pln')
if content:
    for para in content:
        price = para.text.strip()
        priceWithoutCurrency = price[:-6]
        priceWithoutSpace = priceWithoutCurrency.replace(' ', '')
        priceWithoutSpace = priceWithoutSpace.replace(',', '.')
        # print(price)
        priceInt = int(priceWithoutSpace)
        prices.append(priceInt)

content = soup.find_all('div', class_='area-usable')
if content:
    for para in content:
        price = para.text.strip()
        priceWithoutCurrency = price[:-3]
        # priceWithoutSpace = priceWithoutCurrency.replace(' ','')
        # priceWithoutSpace = priceWithoutSpace.replace(',','.')
        # print(price)
        priceInt = float(priceWithoutCurrency)
        squareMeters.append(priceInt)

np.random.seed(0)
X = np.array(prices).reshape(-1, 1)
y = np.array(squareMeters)

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
a = model.coef_
b = model.intercept_

fig = Figure()
axes = fig.add_subplot(111)

mouseText = axes.text(0, 0, 'GeeksforGeeks', style='italic',
                      fontsize=10, color="black")

addedEl = 0
totalLoadedEl = 50
# sc = axes.scatter(X, y, color='blue', label='Prices')
oldSc = axes.scatter(X[:totalLoadedEl], y[:totalLoadedEl], picker=1, color='blue', label='Prices')
newSc = axes.scatter(X[0: 0], y[0: 0], picker=1, color='green')

# newSc = axes.scatter(0)
axes.plot(X, y_pred, color='red', linewidth=2, label='regresja liniowa')
axes.set_xlabel('prices')
axes.set_ylabel('square meters')
axes.legend()

# plt.show()
allSc = [oldSc, newSc]
cursorMain = mplcursors.cursor(allSc, hover=True)


# cursorMain = mplcursors.cursor()

@cursorMain.connect("add")
def on_add(sel):
    ann = sel.annotation
    art = sel.artist
    if sel.artist is oldSc:
        ann.set_text(labelsAll[sel.index])
    else:
        ann.set_text(labelsAll[sel.index + totalLoadedEl])

root = tk.Tk()

# thinker
frame = tk.Frame(root)
label = tk.Label(frame, text='regresja liniowa')
label.config(font=("Courier", 32))
# canvas
figure_canvas = FigureCanvasTkAgg(fig, master=frame)
axes.ticklabel_format(axis='x', style='plain', useOffset=False)


def format_coord(x, y):
    return "(x,y)  = (%.0f, %.1f)" % (x, y)
axes.format_coord = format_coord
vline = axes.axvline(X[0], linewidth=1,
                     color='red')
hline = axes.axhline(y[0], linewidth=1,
                     color='red')
switchLine = False


def moveLines(e):
    global switchLine
    newX = e.xdata
    newY = e.ydata
    print(newX)
    vline.set_visible(True)
    hline.set_visible(True)
    vline.set_xdata([newX, newX])
    hline.set_ydata([newY, newY])
    figure_canvas.draw_idle()

    if e.inaxes !=axes:
        mouseText.set_visible(False)
        return
    mouseText.set_text(f"price: {newX:.0f} squareM: {newY:.0f}")
    mouseText.set_position((newX, newY))
    mouseText.set_visible(True)


figure_canvas.mpl_connect("motion_notify_event", moveLines)

figure_canvas.draw()
NavigationToolbar2Tk(figure_canvas, frame)
label.pack()

figure_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
frame.pack(fill=tk.BOTH, expand=True)


def button_form():
    # tk.filedialog.askfloat("Input", "podaj cene")
    # tk.filedialog.askfloat("Input", "podaj metraz")

    window = tk.Toplevel(root)
    window.title("Add Data")
    window.geometry('400x200')

    ttk.Label(window, text="price :",
              font=("Times New Roman", 15)).grid(
        column=0, row=0, padx=10, pady=25)

    t = tk.Text(window, width=20, height=1)

    ttk.Label(window, text="meters :",
              font=("Times New Roman", 15)).grid(
        column=0, row=1, padx=10, pady=25)

    t2 = tk.Text(window, width=20, height=1)
    t.grid(column=1, row=0)
    t2.grid(column=1, row=1)
    button2 = tk.Button(window, text="add house", command=lambda: add_house(t, t2, window))

    button2.grid(column=0, row=2, padx=30)


# def getLabelsForNewData(addedEl):
#     print('pokazytwanie cen!!!!!!!!!!noewe')
#     res = []
#     counterEl = -addedEl
#     while (counterEl < 0):
#         actualElPrice = prices[counterEl]
#         counter = 0
#         higher = []
#         lower = []
#         higher.append('higher: \n')
#         lower.append('lower: \n')
#         for price in prices:
#             if actualElPrice < price:
#                 higher.append('meters: ' + str(squareMeters[counter]) + ' price: ' + str(price) + '\n')
#             else:
#                 lower.append('meters: ' + str(squareMeters[counter]) + ' price: ' + str(price) + '\n')
#             counter += 1
#         counterEl += 1
#         res.append("".join(higher) + "".join(lower))
#     return res


def getLabelsAll(addedEl):
    res = []
    sizeElements = len(prices)
    counterMain = 0
    while (counterMain < sizeElements):
        # print(sel)
        actualElPrice = prices[counterMain]
        counter = 0
        higher = []
        lower = []
        higher.append('higher: \n')
        lower.append('lower: \n')
        for price in prices:
            if counter != counterMain:
                if actualElPrice < price:
                    higher.append('meters: ' + str(squareMeters[counter]) + ' price: ' + str(price) + '\n')
                else:
                    lower.append('meters: ' + str(squareMeters[counter]) + ' price: ' + str(price) + '\n')
            counter += 1
        counterMain += 1
        res.append("".join(higher) + "".join(lower))
    return res


labelsAll = getLabelsAll(addedEl)


def add_house(t, t2, window):
    # global cursorMain
    # cursorMain.remove()
    priceValue = t.get("1.0", "end-1c")
    squareMeter = t2.get("1.0", "end-1c")
    global addedEl
    addedEl += 1
    # labels = getLabelsForNewData(addedEl)
    global totalLoadedEl

    prices.append(float(priceValue))
    squareMeters.append(float(squareMeter))

    X = np.array(prices).reshape(-1, 1)
    y = np.array(squareMeters)

    new_X = X[50:, 0]
    new_y = y[50:]

    newDataStackColumn = np.column_stack((new_X, new_y))
    newSc.set_offsets(newDataStackColumn)

    global labelsAll
    labelsAll.clear()
    labelsAll.extend(getLabelsAll(addedEl))

    axes.relim()
    axes.autoscale_view()

    figure_canvas.draw_idle()
    window.destroy()


# def add_house(t, t2, window):
#     global cursorMain
#     cursorMain.remove()
#     print('added')
#     priceValue = t.get("1.0", "end-1c")
#     squareMeter = t2.get("1.0", "end-1c")
#
#     # print(priceValue + 'price')
#     # print(squareMeters+'square_meters')
#
#     global addedEl
#     addedEl += 1
#     print(addedEl)
#     labels = getLabelsForNewData(addedEl)
#
#     prices.append(float(priceValue))
#     squareMeters.append(float(squareMeter))
#
#     # axes.clear()
#     X = np.array(prices).reshape(-1, 1)
#     y = np.array(squareMeters)
#     model = LinearRegression()
#     model.fit(X, y)
#     y_pred = model.predict(X)
#
#     # oldSc = axes.scatter(X[:-addedEl], y[:-addedEl], picker=1, color='blue', label='Prices')
#     oldSc = axes.scatter(X[:-addedEl], y[:-addedEl], picker=1, color='blue')
#     i = 1
#     # extraData = []
#     # while i <= addedEl:
#     #     sc = axes.scatter(X[-i], y[-i], picker=5, color='green')
#     #     i += 1
#     #     extraData.append(sc)
#     newSc = axes.scatter(X[-addedEl:, 0], y[-addedEl:], picker=1, color='green')
#
#     # cursorOld = mplcursors.cursor(oldSc, hover=True)
#     # cursor.annotation_kwargs = dict()
#     # cursor.keep_alive = False
#
#     # cursor = mplcursors.cursor(newSc, hover=True)
#     # cursor.connect(
#     #     "add", lambda sel: sel.annotation.set_text(labels[sel.index]))
#     #
#     # # cursorOld.connect(
#     # #     "add", lambda sel: sel.annotation.set_text(labelsOld[sel.index]))
#     # cursor.connect(
#     #     "remove", lambda sel: sel.annotation.remove())
#     axes.plot(X, y_pred, color='red', linewidth=2, label='regresja liniowa')
#     # axes.set_xlabel('prices')
#     # axes.set_ylabel('square meters')
#     # axes.legend()
#     axes.ticklabel_format(axis='x', style='plain', useOffset=False)
#
#     # vline = axes.axvline(X[0], linewidth=1,
#     #                      color='red')
#     # hline = axes.axhline(y[0], linewidth=1,
#     #                      color='red')
#
#     def moveLines2(e):
#         newX = e.xdata
#         newY = e.ydata
#         print('aa')
#         vline.set_visible(True)
#         hline.set_visible(True)
#         vline.set_xdata([newX, newX])
#         hline.set_ydata([newY, newY])
#         figure_canvas.draw()
#
#     axes.format_coord = format_coord
#     # figure_canvas.mpl_connect("motion_notify_event", moveLines2)
#
#     figure_canvas.draw()
#     window.destroy()


button = tk.Button(frame, text='add new house', command=button_form,
                   activebackground="blue",
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="lightgray",
                   cursor="hand2",
                   disabledforeground="gray",
                   fg="black",
                   font=("Arial", 12),
                   height=2,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=10,
                   pady=5,
                   width=15,
                   wraplength=100)

button.pack(padx=20, pady=20)

root.mainloop()
