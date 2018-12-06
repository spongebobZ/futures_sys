import random, time, threading, tkinter as tk
from tkinter import *

current_location = 4500
day = 1


# 定义指数随机走势
def go_line():
    global current_location, day
    while True:
        current_location += random.randint(-200, 200)
        print('第%s天：指数价位为【%s】' % (day, current_location))
        time.sleep(3)
        day += 1


# 计算赚取金额
def cacl_money(current_location, location, money, times):
    r=0
    try:
        percent = (current_location - location) / location
        r = int(money * percent * times)
    except ZeroDivisionError:
        pass
    return r


# 定义玩家类
class player():
    # 初始化玩家的名字、资金
    def __init__(self, name, money):
        self.name = name
        self.total_money = money
        self.orders = {'long': {'location': 0, 'money': 0, 'times': 0},
                       'short': {'location': 0, 'money': 0, 'times': 0}}


    def test(self):
        print('123')

    def buying_long(self, buy_money, location, times=20):
        try:
            buy_money = int(buy_money)
            location = int(location)
        except:
            buy_money = 0
            location = current_location
        if buy_money > self.total_money:
            print('操作失败：没有足够剩余金额')
        else:
            print('%s在价位【%s】%s倍做多了%s元...' % (self.name, location, times, buy_money))
            self.orders['long']['location'] = location
            self.orders['long']['money'] = buy_money
            self.orders['long']['times'] = times

    def short_selling(self, sell_money, location, times=20):
        try:
            sell_money = int(sell_money)
            location = int(location)
        except:
            sell_money = 0
            location = current_location
        if sell_money > self.total_money:
            print('操作失败：没有足够剩余金额')
        else:
            print('%s在价位【%s】%s倍做空了%s元...' % (self.name, location, times, sell_money))
            self.orders['short']['location'] = location
            self.orders['short']['money'] = sell_money
            self.orders['short']['times'] = times

    def selling_long(self, sell_money, current_location):
        try:
            sell_money = int(sell_money)
        except:
            sell_money = 0
        if sell_money > self.orders['long']['money']:
            print('操作失败：超过开单金额')
        else:
            r = cacl_money(current_location, self.orders['long']['location'], self.orders['long']['money'],
                           self.orders['long']['times'])
            self.orders['long']['location'] += r
            if r >= 0:
                print('%s在价位【%s】平多了%s元，赚取了%s元...' % (self.name, current_location, sell_money, r))
            else:
                print('%s在价位【%s】平多了%s元，亏损了%s元...' % (self.name, current_location, sell_money, -r))
            self.total_money += r

    def selling_short(self, sell_money, current_location):
        try:
            sell_money = int(sell_money)
        except:
            sell_money = 0
        if sell_money > self.orders['short']['money']:
            print('操作失败：超过开单金额')
        else:
            r = cacl_money(current_location, self.orders['long']['location'], self.orders['long']['money'],
                           self.orders['long']['times'])
            self.orders['short']['location'] -= r
            if r >= 0:
                print('%s在价位【%s】平空了%s元，赚取了%s元...' % (self.name, current_location, sell_money, -r))
            else:
                print('%s在价位【%s】平空了%s元，亏损了%s元...' % (self.name, current_location, sell_money, r))


def player_client(player):
    # 新建tk对象
    root = tk.Tk()
    root.title('%s的客户端' % player.name)

    # 新建frame子类f1
    f1 = tk.Frame(root)
    # 新建logo对象
    logo = tk.PhotoImage(file='src/hrr.png')
    logoLabel = tk.Label(f1, image=logo)
    logoLabel.pack(anchor=NW, side=LEFT)
    # 新建变量存储余额
    var_total_money = StringVar()
    var_total_money.set('您的余额：%s' % player.total_money)
    # 新建label显示余额
    total_money_label = tk.Label(f1, textvariable=var_total_money, compound=LEFT)
    total_money_label.pack(anchor=NE, side=RIGHT)
    # 刷新余额显示方法
    def flesh_total_money():
        var_total_money.set('您的余额：%s' % player.total_money)
    # 新建刷新余额显示按钮
    flesh_total_money_btn = tk.Button(f1, text='刷新', command=flesh_total_money)
    flesh_total_money_btn.pack(anchor=E, side=RIGHT)
    # 把f1装载进root容器
    f1.grid(row=0)


    # 新建frame子类f2
    f2 = tk.Frame(root)
    #新建开单金额提示label
    label_order_money = tk.Label(f2,text='开单金额：')
    label_order_money.grid(row=0)
    # 新建开单金额输入框
    def valid_order_money():
        if not re.match(u'^[0-9]+$',order_money_entry.get()):
            order_money_entry.delete(0,END)
            return False
    order_money_entry = tk.Entry(f2,validate='focusout', validatecommand=valid_order_money)
    order_money_entry.grid(row=0,column=1)
    order_money_entry.insert(0,'请输入您要开的金额...')
    # 新建变量存储倍数
    var_times = IntVar()
    var_times.set(1)
    #设置倍数变量
    times=10
    # 设置倍数方法
    def set_times(t):
        global times
        times = t
    # 新建10倍、20倍单选按钮组
    radiobtn_10 = Radiobutton(f2, variable=var_times, value=1, text='10X',command=lambda :set_times(10))
    radiobtn_10.grid(row=1)
    radiobtn_20 = Radiobutton(f2, variable=var_times, value=2, text='20X',command=lambda :set_times(20))
    radiobtn_20.grid(row=1,column=1)
    # 新建开多按钮
    buy_long_btn = tk.Button(f2, text='开多', command=lambda :player.buying_long(order_money_entry.get(),current_location,times))
    buy_long_btn.grid(row=2)
    # 新建开空按钮
    sell_short_btn = tk.Button(f2, text='开空',
                               command=lambda :player.short_selling(order_money_entry.get(), current_location, times))
    sell_short_btn.grid(row=2,column=1)
    f2.grid(row=1)


    # 新建frame子类f3
    f3 = tk.Frame(root)
    # 新建平仓金额提示label
    label_order_money = tk.Label(f3, text='平仓金额：')
    label_order_money.grid(row=0)
    def valid_sell_money():
        if not re.match(u'^[0-9]+$', sell_money_entry.get()):
            sell_money_entry.delete(0, END)
            return False
    sell_money_entry = tk.Entry(f3,validate='focusout', validatecommand=valid_sell_money)
    sell_money_entry.grid(row=0,column=1)
    # 新建平仓金额输入框

    # 新建平多按钮
    sell_long_btn = tk.Button(f3, text='平多', command=lambda :player.selling_long(sell_money_entry.get(), current_location))
    sell_long_btn.grid(row=1)
    # 新建平空按钮
    sell_short_btn = tk.Button(f3, text='平空', command=lambda :player.selling_short(sell_money_entry.get(), current_location))
    sell_short_btn.grid(row=1,column=1)
    f3.grid(row=2)

    root.mainloop()



t_line = threading.Thread(target=go_line, name='line_thead')
t_client = threading.Thread(target=player_client, name='client_thread', args=(player('白肉肉', 10000),))
t_line.start()
t_client.start()
t_line.join()
t_client.join()
