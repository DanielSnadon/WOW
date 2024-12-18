import matplotlib.pyplot as plt
import krpc
import time

conn = krpc.connect(name="My project")

# Получение доступа к важным объектам и функциям
vessel = conn.space_center.active_vessel
ap = vessel.auto_pilot
control = vessel.control

# Создание полезных переменных потока
altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
periapsis = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")
surface_velocity_stream = conn.add_stream(
    getattr, vessel.flight(vessel.orbit.body.reference_frame), "velocity"
)

# Получение объекта топливного бака
fuel_tank = vessel.parts.with_tag("rk-7")[0]

# Получение объекта ресурса LiquidFuel
liquid_fuel_resource = fuel_tank.resources.with_resource("LiquidFuel")[0]

# Получение текущего количества топлива
current_fuel = liquid_fuel_resource.amount


# Функция вывода информации в терминал
def print_logs(mass, curr_speed):
    print(f"*Данные на {seconds} секунде*")
    print(f"Текущая скорость ступенчатой ракеты: {curr_speed} м/с")
    print("Расстояние от Земли:", round(altitude(), 3), "м")
    print(f"Масса ракеты: {mass} кг\n")


# Активация двигателя
control.throttle = 1
control.sas = True

print("Запуск двигателей прошел успешно, полет через:")
time.sleep(1)
print("3...")
time.sleep(1)
print("2...")
time.sleep(1)
print("1...")
control.activate_next_stage()
timing = time.time()

# Данные на первую секунду полета
print("\n*Данные на 0 секунде*")
print(f"Текущая скорость ступенчатой ракеты: {0} м/с")
print("Расстояние от Земли:", round(altitude(), 3), "м")
print(f"Масса ракеты на момент старта составляет: {vessel.mass} кг\n")

# Вспомогательные переменные необходимые для корректной работы программы
times = 0
changed = 0

while True:
    seconds = round(time.time() - timing)
    # Скорость ракеты
    surface_velocity = surface_velocity_stream()
    surface_speed = (
        surface_velocity[0] ** 2 + surface_velocity[1] ** 2 + surface_velocity[2] ** 2
    )
    surface_speed = surface_speed**0.5
    if 13 <= seconds <= 17:
        if times == 0:
            times += 1
            print_logs(vessel.mass, surface_speed)

    if 500 <= surface_speed <= 550:
        if times == 1 and (30 <= seconds <= 38):
            times += 1
            print_logs(vessel.mass, surface_speed)
            print("*уменьшение тяги до 55%*\n")
        control.throttle = 0.55

    elif 30000 <= altitude() <= 50000 and changed < 1:
        print("*достижение высоты в 30.000 метров*")
        print("*изменение угла наклона*\n")
        vessel.control.pitch = -1
        time.sleep(4.0)
        vessel.control.pitch = 0
        angle = vessel.flight().pitch
        print(f"Текущий угол наклона относительно горизонтальной оси: {angle}")
        changed += 1

    elif (times == 2) and (58 <= seconds <= 62):
        times += 1
        print_logs(vessel.mass, surface_speed)

    elif (times == 3) and (88 <= seconds <= 95):
        times += 1
        print_logs(vessel.mass, surface_speed)

    elif 50500 <= altitude() <= 60000:
        vessel.control.pitch = 0
        control.sas = True

    elif altitude() >= 60500 or current_fuel < 7:
        break

print("Выход в космос прошел успешно!")
print("*отделение первой ступени*")
control.activate_next_stage()

# Изменение тангажа ракеты к внутреннему радиальному вектору
print("*изменение угла наклона к внутреннему радиальному вектору*")
control.sas = True
vessel.control.pitch = -1
time.sleep(5.0)
vessel.control.pitch = 0
angle = vessel.flight().pitch
print(f"Текущий угол наклона относительно горизонтальной оси: {angle}")
print("\nРакета идет к орбите")


# Летим до определенных значений апогея и перегея
last = 0
while True:
    apoapsis_value = apoapsis()
    periapsis_value = periapsis()
    time.sleep(0.1)
    if (850000 <= apoapsis_value) and (90000 <= periapsis_value):
        # выключение двигателей
        print("*отключение двигателей*")
        control.sas = False
        vessel.control.pitch = 0.05
        time.sleep(0.5)
        vessel.control.pitch = 0
        control.sas = True
        control.throttle = 0
        break

print("*ракета вышла на орбиту*")
# Выпуск спутника на орбиту
time.sleep(5)
control.activate_next_stage()
print("*отделение спутника от ракетоносителя 1 ЭТАП*")
time.sleep(5)
control.activate_next_stage()
print("*вывод антенн*")
time.sleep(5)
control.antennas = True
print("Спутник успешно вышел на орбиту!")
