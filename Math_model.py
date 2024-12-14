import matplotlib.pyplot as plt
import numpy as np


#Функция плотности атмосферы (по таблице)
def q_f(h):
    if h < 2500:
        return 1.225
    elif h < 5000:
        return 0.898
    elif h < 7500:
        return 0.642
    elif h < 10000:
        return 0.446
    elif h < 15000:
        return 0.288
    elif h < 20000:
        return 0.108
    elif h < 25000:
        return 0.04
    elif h < 30000:
        return 0.015
    elif h < 40000:
        return 0.006
    elif h < 50000:
        return 0.001
    else:
        return 0
    
#Функция силы гравитации
def F_gr(m, h):
    G = 6.6743*10**-11
    M = 5.2915158*10**22
    R = 600000
    Fgr = G*((M*m)/((R+h)**2))
    return Fgr

#Функция силы сопротивления
def F_s(q, v):
    c = 0.47
    r = 2
    S = 3.1415*r**2
    Fs = c*S*q*v**2/2
    return Fs

#Функция ускорения
def a_f(t, h, q, v, power, m):
    Fgr = F_gr(m, h)
    Fs = F_s(q, v)
    Ft_max = 1428000
    a = (power*Ft_max/100 - Fgr  - Fs)/m
    return a

#Функция скорости
def v_f(t, power, h, v, m):
    q = q_f(h)
    a = a_f(t, h, q, v, power, m)
    v = v + a
    return v

#Начальные параметры 
h = 750 
v = 0
m = 52408
power = 100
t = 0

#Массивы для вывода графиков
speed_data = []
high_data = []
mass_data = []
time_data = []

while t <= 88:
    if t > 36:
        power = 55 #Снижение тяги ракеты до 55%

    v = v_f(t, power, h, v, m)
    n = 430 * power/100
    h += v
    m = m - n

    time_data.append(int(t))
    speed_data.append(int(v))
    high_data.append(int(h))
    mass_data.append(int(m))
    t += 1


# Построение графиков
x = np.linspace(0, time_data[-1], len(time_data))  # Общее значение X для всех графиков
y1 = mass_data  # Первый график: масса
y2 = speed_data  # Второй график: скорость
y3 = high_data  # Третий график: высота

# Создание фигуры и осей
fig, axs = plt.subplots(3, 1, figsize=(5, 12))

# Первый график
axs[0].plot(x, y1, color="blue", label="Масса", linewidth=2)
axs[0].set_title("График массы (кг)")
axs[0].set_xlabel("Время (сек)")
axs[0].set_ylabel("Масса (кг)")
axs[0].grid()
axs[0].legend()

# Второй график
axs[1].plot(x, y2, color="red", label="Скорость", linewidth=2)
axs[1].set_title("График скорости (м/c)") 
axs[1].set_xlabel("Время (сек)")
axs[1].set_ylabel("Скорость (м/c)")
axs[1].grid()
axs[1].legend()

# Третий график
axs[2].plot(x, y3, color="green", label="Высота", linewidth=2)
axs[2].set_title("График высоты (м)")
axs[2].set_xlabel("Время (сек)")
axs[2].set_ylabel("Высота (м)")
axs[2].grid()
axs[2].legend()

# Настройка общего расстояния между графиками
plt.tight_layout()


# Показ графиков
plt.show()