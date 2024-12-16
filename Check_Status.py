import krpc
conn = krpc.connect(name='My project')
print(conn.krpc.get_status().version)
print('Соединение установлено\nРакета готова к запуску')