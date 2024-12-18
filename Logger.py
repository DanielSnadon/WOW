import krpc
import math

# Создание файлов для записи данных
speed_file = open("speed_data.txt", "w")
altitude_file = open("altitude_data.txt", "w")
mass_file = open("mass_data.txt", "w")
speed_ox_file = open("speed_ox_data.txt", "w")
speed_oy_file = open("speed_oy_data.txt", "w")

# Создание полезных переменных потока
conn = krpc.connect(name="My project")
vessel = conn.space_center.active_vessel
engines = vessel.parts.engines
altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")
launch_time = conn.add_stream(getattr, engines[5], "active")
current_time = conn.add_stream(getattr, conn.space_center, "ut")

print("Ожидаем запуска ракеты")
while not launch_time():
    pass

mission_start_time = conn.space_center.ut
actual_time = mission_start_time
print("Данные начали запись")
while True:
    if current_time() - actual_time >= 0.01:
        actual_time = current_time()
        time_flight = actual_time - mission_start_time
        if time_flight >= 120:
            break

        angle = vessel.flight().pitch
        velocity = vessel.flight(vessel.orbit.body.reference_frame).speed

        speed_ox_file.write(
            f"{time_flight} {(math.cos(math.radians(angle))) * velocity}\n"
        )
        speed_ox_file.flush()

        speed_oy_file.write(
            f"{time_flight} {(math.sin(math.radians(angle))) * velocity}\n"
        )
        speed_oy_file.flush()

        speed_file.write(f"{time_flight} {velocity}\n")
        speed_file.flush()

        mass_file.write(f"{time_flight} {vessel.mass}\n")
        mass_file.flush()

        altitude_file.write(f"{time_flight} {round(altitude(), 3)}\n")
        altitude_file.flush()
print("Данные записаны в файлы, конец записи")
