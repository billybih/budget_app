import pickle
import datetime
import tkinter as tk
from tkinter import ttk
import tkinter.font as TkFont


class Budget:
    total_expense = 0

    def __init__(self, name, budget, expense = 0, remaining_budget = 0):
        self.name = name
        self.budget = budget
        self.expense = expense
        self.remaining_budget = budget - expense

    def __repr__(self):
        return('{} budget with {}$ remaining'.format(self.name, self.budget))

    @classmethod
    def update(cls, value):
        cls.total_expense += value

class NegativeError(Exception):
    pass

class App(tk.Frame):

    #list entries for budget categories
    def list_budgets(self):

        self.window = tk.Toplevel()
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        self.window.geometry("+%d+%d" % (x + 1045, y + 300))
        self.window.resizable(False, False)

        self.window.config(bg='#DBEAFE')

        ent_housing = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_housing.grid(row=1, column=1)
        tk.Label(master=self.window, text='Housing', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=1, column=2, sticky='w')

        ent_transportation = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_transportation.grid(row=2, column=1)
        tk.Label(master=self.window, text='Transportation', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=2, column=2, sticky='w')

        ent_food = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_food.grid(row=3, column=1)
        tk.Label(master=self.window, text='Food', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=3, column=2, sticky='w')

        ent_clothing = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_clothing.grid(row=4, column=1)
        tk.Label(master=self.window, text='Clothing', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=4, column=2, sticky='w')

        ent_utilities = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_utilities.grid(row=5, column=1)
        tk.Label(master=self.window, text='Utilities', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=5, column=2, sticky='w')

        ent_household_supplies = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_household_supplies.grid(row=6, column=1)
        tk.Label(master=self.window, text='Household supplies', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=6, column=2, sticky='w')

        ent_savings = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_savings.grid(row=7, column=1)
        tk.Label(master=self.window, text='Savings', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=7, column=2, sticky='w')

        ent_leisure = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_leisure.grid(row=8, column=1)
        tk.Label(master=self.window, text='Leisure', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=8, column=2, sticky='w')

        ent_other = tk.Entry(master=self.window, width=9, font=self.ent_font)
        ent_other.grid(row=9, column=1)
        tk.Label(master=self.window, text='Other', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=9, column=2, sticky='w')

        self.entries = [ent_housing, ent_transportation, ent_food,
                        ent_clothing, ent_utilities, ent_household_supplies,
                        ent_savings, ent_leisure, ent_other]

    def submit(self, function):
        self.data_btn = tk.Button(master=self.window, text='submit', font=self.ent_font, bg=self.btn_color, fg=self.btn_text, command = function)
        self.data_btn.grid(row=10, column=1, sticky='w')

    #save remaining budgets for future use
    def save_and_exit(self):

        budgets =  {'housing': [self.housing.budget, self.housing.expense],
                    'transportation': [self.transportation.budget, self.transportation.expense],
                    'food': [self.food.budget, self.food.expense],
                    'clothing': [self.clothing.budget, self.clothing.expense],
                    'utilities': [self.utilities.budget, self.utilities.expense],
                    'household_supplies': [self.household_supplies.budget, self.household_supplies.expense],
                    'savings': [self.savings.budget, self.savings.expense],
                    'leisure': [self.leisure.budget, self.savings.expense],
                    'other': [self.other.budget, self.other.expense],
                    'total_expense': Budget.total_expense,}
        pickle.dump(budgets, open('budgets.dat', 'wb'))

        reset_data = pickle.load(open('budget_reset.dat', 'rb'))
        budget_reset = {'reset': self.reset_date,
                        'day': reset_data['day']}
        pickle.dump(budget_reset, open('budget_reset.dat', 'wb'))

        main.destroy()

    #add expense
    def expense(self):

        self.list_budgets()

        lbl_title = tk.Label(master=self.window, text='Enter expense', font=('Calibri', 15, 'bold'), bg=self.background, fg=self.text)
        lbl_title.grid(row=0, column=1, columnspan=2, sticky='w')

        def add_expense():
            try:
                for ent in range(len(self.entries)):
                    if self.entries[ent].get() == '':
                        continue
                    if float(self.entries[ent].get()):
                        pass
                    if float(self.entries[ent].get()) < 0:
                        raise NegativeError('Input must be positive!')
                for ent in range(len(self.entries)):
                    if self.entries[ent].get() == '':
                        continue
                    self.budgets[ent].remaining_budget = self.budgets[ent].remaining_budget - float(self.entries[ent].get())
                    self.budgets[ent].expense = self.budgets[ent].expense + float(self.entries[ent].get())
                    Budget.update(float(self.entries[ent].get()))

                self.lbl_remaining_budget.config(text=str(sum([x.remaining_budget for x in self.budgets])))
                self.window.destroy()

            except ValueError as err:
                lbl_error = tk.Label(master=self.window, text = 'Check inputs!', font=self.lbl_font, bg=self.background, fg='red').grid(row=10, column=2, sticky='w')
            except NegativeError as err:
                lbl_error = tk.Label(master=self.window, text = str(err), font=('Calibri', 13), bg=self.background, fg='red').grid(row=10, column=2, sticky='w')
            except Exception as err:
                lbl_error = tk.Label(master=self.window, text = repr(err), font=self.lbl_font, bg=self.background, fg='red').grid(row=10, column=2, sticky='w')

        self.submit(add_expense)

    #change default budget per category
    def budget_change(self):

        self.list_budgets()

        lbl_title = tk.Label(master=self.window, text='Budget change (+/- amount)', font=('Calibri', 15, 'bold'), bg=self.background, fg=self.text)
        lbl_title.grid(row=0, column=1, columnspan=2, sticky='w')

        def inc_dcr():
            try:
                for ent in range(len(self.entries)):
                    if self.entries[ent].get() == '':
                        continue
                    if float(self.entries[ent].get()):
                        pass
                for ent in range(len(self.budgets)):
                    if self.entries[ent].get() == '':
                        continue
                    self.budgets[ent].budget = self.budgets[ent].budget + float(self.entries[ent].get())
                    self.budgets[ent].remaining_budget = self.budgets[ent].remaining_budget + float(self.entries[ent].get())

                self.lbl_remaining_budget.config(text=str(sum([x.remaining_budget for x in self.budgets])))
                self.window.destroy()

            except ValueError as err2:
                lbl_error = tk.Label(master=self.window, text = 'Check inputs!', font=self.lbl_font, bg=self.background, fg='red').grid(row=10, column=2, sticky='w')
            except NegativeError as err3:
                lbl_error = tk.Label(master=self.window, text = str(err3), font=self.lbl_font, bg=self.background, fg='red').grid(row=10, column=2, sticky='w')
            except Exception as err:
                lbl_error = tk.Label(master=self.window, text = repr(err), font=self.lbl_font, bg=self.background, fg='red').grid(row=10, column=2, sticky='w')

        self.submit(inc_dcr)

    def show_stats(self):

        self.window = tk.Toplevel()
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        self.window.geometry("+%d+%d" % (x + 1045, y + 300))
        self.window.resizable(False, False)

        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
              elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style(self.window)
        style.map('Treeview', foreground=fixed_map('foreground'),
                    background=fixed_map('background'))
        cols = ('Category', 'Remaining Budget', 'Total Expense', "Total perc spent", 'Default Budget')
        table = ttk.Treeview(self.window, columns=cols, show='headings')
        for col in cols:
            table.heading(col, text=col)
        table.grid(row=0, column=0)

        style.theme_use("default")
        style.configure('Treeview', font = ('Calibri', 12), background=self.background, foreground=self.text)
        style.configure("Treeview.Heading", font = ('Calibri', 12), background=self.btn_color, foreground=self.btn_text)
        style.map('Treeview.Heading', background = [('selected', self.btn_color)])
        style.map('Treeview', background = [('selected', '#60A5FA')], foreground = [('selected', 'black')])

        budgets = [self.housing, self.transportation, self.food,
                    self.clothing, self.utilities, self.household_supplies,
                    self.savings, self.leisure, self.other]

        data = []
        total_data = ['',
                    sum([x.remaining_budget for x in self.budgets]),
                    sum([x.expense for x in self.budgets]),
                    '',
                    sum([x.budget for x in self.budgets])]

        for i in budgets:
            if Budget.total_expense == 0:
                data.append([i.name, i.remaining_budget, i.expense, "/", i.budget])
            else:
                data.append([i.name, i.remaining_budget, i.expense, "{:.1f}".format((i.expense / Budget.total_expense) * 100) + '%', i.budget])
        for (cat, rem, defa, tot, perc) in data:
            table.insert("", 'end', values = (cat, rem, defa, tot, perc), tags = ('rows', ))
        table.insert("", 'end', values = (total_data[0], total_data[1], total_data[2], total_data[3], total_data[4]), tags = ('total',))
        table.tag_configure('total', font = ("Calibri", 14, 'bold'), foreground=self.text, background=self.background)
        # table.tag_configure('rows', font = ('Calibri', 12), foreground=self.text, background=self.background)
        for col in cols:
            table.column(col, width=120, anchor='center')
        table.column('Category', width=140, anchor='w')

    #main screen initialization
    def __init__(self, parent):

        self.parent=parent
        tk.Frame.__init__(self, parent)
        self.pack(padx = 5, pady = 5)
        x = self.parent.winfo_x()
        y = self.parent.winfo_y()
        self.parent.geometry("+%d+%d" % (x + 500, y + 200))
        self.parent.resizable(False, False)
        self.parent.config(bg='#DBEAFE')
        self.default_font = TkFont.nametofont("TkDefaultFont")
        self.default_font.configure(family = 'Calibri', size=20)
        self.btn_color = '#3B82F6'
        self.btn_text = 'white'
        self.background = '#DBEAFE'
        self.text = '#1E3A8A'
        self.lbl_font = ('Calibri', 15)
        self.ent_font = ('Calibri', 12)

        #try to load user data for data files
        try:
            data = pickle.load(open('budgets.dat', 'rb'))
            reset_data = pickle.load(open('budget_reset.dat', 'rb'))

            if datetime.datetime.now().date() >= reset_data['reset']:
                self.housing = Budget('housing', data['housing'][0])
                self.transportation = Budget('transportation', data['transportation'][0])
                self.clothing = Budget('clothing', data['clothing'][0])
                self.food = Budget('food', data['food'][0])
                self.utilities = Budget('utilities', data['utilities'][0])
                self.household_supplies = Budget('household supplies', data['household_supplies'][0])
                self.savings = Budget('savings', data['savings'][0])
                self.leisure = Budget('leisure', data['leisure'][0])
                self.other = Budget('other', data['other'][0])
                self.reset_date = (datetime.datetime.now().date().replace(day=1) + datetime.timedelta(days=32)).replace(day=int(reset_data['day']))

                self.budgets = [self.housing, self.transportation, self.food,
                                self.clothing, self.utilities, self.household_supplies,
                                self.savings, self.leisure, self.other]

            else:
                self.housing = Budget('housing', data['housing'][0], expense = data['housing'][1])
                self.transportation = Budget('transportation', data['transportation'][0], expense = data['transportation'][1])
                self.clothing = Budget('clothing', data['clothing'][0], expense = data['clothing'][1])
                self.food = Budget('food', data['food'][0], expense = data['food'][1])
                self.utilities = Budget('utilities', data['utilities'][0], expense = data['utilities'][1])
                self.household_supplies = Budget('household supplies', data['household_supplies'][0], expense = data['household_supplies'][1])
                self.savings = Budget('savings', data['savings'][0], expense = data['savings'][1])
                self.leisure = Budget('leisure', data['leisure'][0], expense = data['leisure'][1])
                self.other = Budget('other', data['other'][0], expense = data['other'][1])
                Budget.total_expense = data['total_expense']
                self.reset_date = reset_data['reset']

                self.budgets = [self.housing, self.transportation, self.food,
                                self.clothing, self.utilities, self.household_supplies,
                                self.savings, self.leisure, self.other]

        #if no user data found ==> enter defaults budgets for the first time
        except:

            #initial budget entry
            self.list_budgets()
            lbl_title = tk.Label(master=self.window, text='  Enter budgets:', font=('Calibri', 18), bg=self.background, fg=self.text)
            lbl_title.grid(row=0, column=1, columnspan=2, sticky='w')

            self.ent_reset = tk.Entry(master=self.window, width=9, font=self.ent_font)
            self.ent_reset.grid(row=10, column=1)
            tk.Label(master=self.window, text='Day of reset (1-28)', font=self.lbl_font, bg=self.background, fg=self.text).grid(row=10, column=2, sticky = 'w')

            def get_data():
                try:
                    self.housing = Budget('housing', float(self.entries[0].get()))
                    self.transportation = Budget('transportation', float(self.entries[1].get()))
                    self.clothing = Budget('clothing', float(self.entries[2].get()))
                    self.food = Budget('food', float(self.entries[3].get()))
                    self.utilities = Budget('utilities', float(self.entries[4].get()))
                    self.household_supplies = Budget('household_supplies', float(self.entries[5].get()))
                    self.savings = Budget('savings', float(self.entries[6].get()))
                    self.leisure = Budget('leisure', float(self.entries[7].get()))
                    self.other = Budget('other', float(self.entries[8].get()))

                    self.reset_day = (float(self.ent_reset.get()))
                    self.reset_date = (datetime.datetime.now().date().replace(day=1) + datetime.timedelta(days=32)).replace(day=int(self.reset_day))
                    budget_reset = {'reset': self.reset_date,
                                    'day': self.reset_day}
                    pickle.dump(budget_reset, open('budget_reset.dat', 'wb'))

                    self.budgets = [self.housing, self.transportation, self.food,
                                    self.clothing, self.utilities, self.household_supplies,
                                    self.savings, self.leisure, self.other]

                    self.lbl_remaining_budget.config(text=str(sum([x.remaining_budget for x in self.budgets])))
                    self.window.destroy()

                except ValueError as err2:
                    lbl_error = tk.Label(master=self.window, text = 'Check inputs!', font=self.lbl_font, bg=self.background, fg='red').grid(row=11, column=2, sticky='w')
                except NegativeError as err3:
                    lbl_error = tk.Label(master=self.window, text = str(err3), font=self.lbl_font, bg=self.background, fg='red').grid(row=11, column=2, sticky='w')
                except Exception as err:
                    lbl_error = tk.Label(master=self.window, text = repr(err), font=self.lbl_font, bg=self.background, fg='red').grid(row=11, column=2, sticky='w')

            self.submit(get_data)
            self.data_btn.grid(row=11, column=1, sticky='w')

        #main screen labels and buttons
        self.lbl_balance = tk.Label(master=parent, text = 'Balance:', bg = self.background, fg = self.text)
        self.lbl_balance.configure(font = ('Calibri', 20))
        self.lbl_balance.pack()

        try:
            self.lbl_remaining_budget = tk.Label(master=parent, text = str(sum([x.remaining_budget for x in self.budgets])), bg = self.background, fg = self.text)
            self.lbl_remaining_budget.configure(font = ('Calibri', 55))
            self.lbl_remaining_budget.pack()
        except:
            self.lbl_remaining_budget = tk.Label(master=parent, text = '0', bg = self.background, fg = self.text)
            self.lbl_remaining_budget.configure(font = ('Calibri', 55))
            self.lbl_remaining_budget.pack()

        self.btn_expense = tk.Button(master=parent, text='add expense', bg = self.btn_color, fg = self.btn_text, width=30, command = self.expense)
        self.btn_expense.pack()

        self.btn_icr_dcr = tk.Button(master=parent, text='increase/decrease budget', bg = self.btn_color, fg = self.btn_text, width=30, command = self.budget_change)
        self.btn_icr_dcr.pack()

        self.budget_stats = tk.Button(master=parent, text = 'show budget stats', bg = self.btn_color, fg = self.btn_text, width=30, command = self.show_stats)
        self.budget_stats.pack()

        self.save = tk.Button(master=parent, text='save and exit', width=30, bg = self.btn_color, fg = self.btn_text, command  = self.save_and_exit)
        self.save.pack()

#app initalization
if __name__ == "__main__":
    main = tk.Tk()
    try:
        main.iconbitmap('icon.ico')
    except:
        pass
    App(main)
    main.title('Budget App')
    main.mainloop()
