# 아두이노 체온 센서
import MySQLdb
import time
import board
import busio as io
import adafruit_mlx90614
import pymysql

# 데이터 베이스 연동 
conn = pymysql.connect(host="", user="min",passwd="",db="smartmirror")
i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

try:
    with conn.cursor() as cur:
        sql="insert into smartmirror_sensor values(%s, %s, %s, %s);"
        
        while True:
            ambientString = "{:.1f}".format(mlx.ambient_temperature-5)
            objectString = "{:.1f}".format(mlx.object_temperature+5)

            
            print("주변 온도:", ambientString, "°C")
            print("체온:", objectString, "°C")
    
            cur.execute(sql,(None, ambientString, objectString,time.strftime("%Y-%m-%d %H:%M",time.localtime())))
            conn.commit()  
            
            time.sleep(5)
            
except KeyboardInterrupt :
    exit()
finally:
    conn.close()