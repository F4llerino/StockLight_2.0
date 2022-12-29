import tkinter as tk
import data_operations


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.mainframe = tk.Frame(self.master)
        self.mainframe.pack()

        # Widgets-Mainframe
        # StringVar
        self.company_var = tk.StringVar()
        self.roi_result_var = tk.StringVar()
        self.eigenkapitalquote_result_var = tk.StringVar()
        self.liquiditaet_result_var = tk.StringVar()

        self.company_var.set("")
        self.roi_result_var.set("")
        self.eigenkapitalquote_result_var.set("")
        self.liquiditaet_result_var.set("")

        # Widgets
        self.header = tk.Label(self.mainframe, text="Enter a ticker", font="Verdana 14 bold")
        self.ticker_entry = tk.Entry(self.mainframe)
        self.submit_button = tk.Button(self.mainframe, text="Submit", font="Verdana 10 bold", bg="magenta2",
                                       command=self.analyse)

        # Name_&_Numbers
        self.company_label = tk.Label(self.mainframe, textvariable=self.company_var, font="Verdana 14 underline bold",
                                      fg="blue")
        self.roi_label = tk.Label(self.mainframe, text="Return on Investment:", font="Verdana 12 bold")
        self.eigenkapitalquote_label = tk.Label(self.mainframe, text="Eigenkapitalquote:", font="Verdana 12 bold")
        self.liquiditaet_2_label = tk.Label(self.mainframe, text="Liquidität 2. Grades:", font="Verdana 12 bold")

        self.roi_result_label = tk.Label(self.mainframe, textvariable=self.roi_result_var, font="Verdana 12 bold")
        self.eigenkapitalquote_result_label = tk.Label(self.mainframe, textvariable=self.eigenkapitalquote_result_var,
                                                       font="Verdana 12 bold")
        self.liquiditaet_2_result_label = tk.Label(self.mainframe, textvariable=self.liquiditaet_result_var,
                                                   font="Verdana 12 bold")

        # Layout
        self.header.grid(column=1, row=1, columnspan=2, pady=25)
        self.ticker_entry.grid(column=1, row=2, columnspan=2, ipady=5)
        self.submit_button.grid(column=1, row=3, columnspan=2, pady=20)

        # Name_&_Numbers
        self.company_label.grid(column=1, row=5, columnspan=2)
        self.roi_label.grid(column=1, row=6)
        self.eigenkapitalquote_label.grid(column=1, row=7)
        self.liquiditaet_2_label.grid(column=1, row=8)

        self.roi_result_label.grid(column=2, row=6)
        self.eigenkapitalquote_result_label.grid(column=2, row=7)
        self.liquiditaet_2_result_label.grid(column=2, row=8)

    def get_ticker(self):
        ticker = self.ticker_entry.get()
        self.ticker_entry.delete(0, "end")

        return ticker

    def show_red(self):
        global red_img
        red_img = tk.PhotoImage(file="images\\Ampel_rot.png")
        red_label = tk.Label(self.mainframe, image=red_img)
        red_label.grid(column=1, row=4, columnspan=2)

    def show_yellow(self):
        global yellow_img
        yellow_img = tk.PhotoImage(file="images\\Ampel_Gelb.png")
        yellow_label = tk.Label(self.mainframe, image=yellow_img)
        yellow_label.grid(column=1, row=4, columnspan=2)

    def show_green(self):
        global green_img
        green_img = tk.PhotoImage(file="images\\Ampel_gruen.png")
        green_label = tk.Label(self.mainframe, image=green_img)
        green_label.grid(column=1, row=4, columnspan=2)

    def show_red_yellow(self):
        global red_yellow_img
        red_yellow_img = tk.PhotoImage(file="images\\Ampel_gelb_rot.png")
        red_yellow_label = tk.Label(self.mainframe, image=red_yellow_img)
        red_yellow_label.grid(column=1, row=4, columnspan=2)

    def show_green_yellow(self):
        global green_yellow_img
        green_yellow_img = tk.PhotoImage(file="images\\Ampel_gruen_gelb.png")
        green_yellow_label = tk.Label(self.mainframe, image=green_yellow_img)
        green_yellow_label.grid(column=1, row=4, columnspan=2)

    def change_label(self, r, eig, liq, ticker):
        self.company_var.set("")
        self.roi_result_var.set("")
        self.eigenkapitalquote_result_var.set("")
        self.liquiditaet_result_var.set("")
        self.master.update()
        self.company_var.set(ticker)
        self.roi_result_var.set(str(round(r, 2)) + "%")
        self.eigenkapitalquote_result_var.set(str(round(eig, 2)) + "%")
        self.liquiditaet_result_var.set(str(round(liq, 2)) + "%")

    def analyse(self):
        ticker = self.get_ticker()
        ratios = data_operations.query(ticker, data_operations.headers)
        counter_red = 0
        counter_yellow = 0
        counter_green = 0

        # IF-Conditions to get the base of the recommendation
        if ratios[0] < 5:
            counter_red += 1
        elif 5 <= ratios[0] <= 7.5:
            counter_yellow += 1
        elif ratios[0] > 7.5:
            counter_green += 1

        if ratios[2] < 50:
            counter_red += 1
        elif 50 <= ratios[2] <= 65:
            counter_yellow += 1
        elif ratios[2] > 65:
            counter_green += 1

        if ratios[1] < 80:
            counter_red += 1
        elif 80 <= ratios[1] < 100:
            counter_yellow += 1
        elif ratios[1] >= 100:
            counter_green += 1
        # If-Conditions with counter
        if counter_red == 3:
            self.show_red()
        elif counter_yellow == 3 or counter_yellow == 2:
            self.show_yellow()
        elif counter_green == 3:
            self.show_green()
        elif counter_red == 2:
            if counter_yellow == 1:
                self.show_red_yellow()
            else:
                self.show_yellow()
        elif counter_green == 2:
            if counter_yellow == 1:
                self.show_green_yellow()
            else:
                self.show_yellow()

        # End of Function
        self.change_label(ratios[0], ratios[2], ratios[1], ticker)
        counter_red = 0
        counter_yellow = 0
        counter_green = 0


def main():
    root = tk.Tk()
    root.title("StockLight 2.0")
    root.geometry("500x750")
    app = MainWindow(root)
    root.mainloop()
