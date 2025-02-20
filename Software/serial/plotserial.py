import matplotlib.pyplot as plt
import serial
import time

def read_serial_data(ser):
    temp = []
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                temp.append(float(line))
            except ValueError:
                continue  # Skip lines that cannot be converted to float
        yield temp

def plot_data(temp_gen, ser):
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot([], [])
    ax.set_ylim(27, 50)
    # ax.set_ylim(0, 100)
    last_send_time = time.time()
    send_data = 30  # Initial data to send
    increase = True  # Flag to alternate between increasing and decreasing
    count = 0
    while True:
        temp = next(temp_gen)
        line.set_xdata(range(len(temp)))
        line.set_ydata(temp)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)

        # Send data every 5 seconds
        current_time = time.time()
        if current_time - last_send_time >= 10:
            if increase:
                send_data += 2
                if send_data > 36:
                    increase = False  # Toggle the flag
            else:
                send_data -= 2
                if send_data <= 28:
                    increase = True  # Toggle the flag
                    count += 1
            ser.write(f"{send_data}\n".encode('utf-8'))
            last_send_time = current_time

        # Close the program when count reaches 5
        if count >= 2:
            print("Test complete!, closing program.")
            plt.savefig('plot.png')  # Save the figure to a file
            break

if __name__ == "__main__":
    port = 'COM4'  # Change this to your serial port
    baudrate = 9600
    timeout = 1
    ser = serial.Serial(port, baudrate, timeout=timeout)
    temp_gen = read_serial_data(ser)
    plot_data(temp_gen, ser)
    ser.close()  # Close the serial port when the program ends