import matplotlib.pyplot as plt
import serial
import time
import csv

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
    line_temp, = ax.plot([], [], label='actual temperature')
    line_send, = ax.plot([], [], label='Set temperature')
    ax.set_ylim(27, 50)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title('Temperature vs Time')
    ax.legend()
    start_time = time.time()
    last_send_time = start_time
    send_data = 30  # Initial data to send
    increase = True  # Flag to alternate between increasing and decreasing
    count = 0
    send_data_list = []
    time_list = []

    # Open CSV file for writing
    with open('On_hand.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Temperature (°C)', 'Send Data'])

        while True:
            temp = next(temp_gen)
            elapsed_time = time.time() - start_time
            time_list.append(elapsed_time)
            
            # Ensure the lengths of time_list and temp are the same
            if len(time_list) > len(temp):
                time_list.pop(0)
            
            line_temp.set_xdata(time_list)
            line_temp.set_ydata(temp)

            # Update send_data_list for plotting
            send_data_list.append(send_data)
            if len(send_data_list) > len(temp):
                send_data_list.pop(0)
            
            # Ensure the lengths of time_list and send_data_list are the same
            if len(time_list) > len(send_data_list):
                time_list.pop(0)
            
            line_send.set_xdata(time_list)
            line_send.set_ydata(send_data_list)

            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.005)

            if len(temp) > 0:
                try:
                    # Write data to CSV file
                    writer.writerow([elapsed_time, temp[-1], send_data])
                except IndexError:
                    continue  # Skip empty temp list

            # Send data every 5 seconds
            current_time = time.time()
            if current_time - last_send_time >= 25:
                if increase:
                    send_data += 2
                    if send_data >= 40:
                        increase = False  # Toggle the flag
                else:
                    send_data -= 2
                    if send_data <= 30:
                        increase = True  # Toggle the flag
                        count += 1
                ser.write(f"{send_data}\n".encode('utf-8'))
                last_send_time = current_time

            # Close the program when count reaches 5
            if count >= 5:
                print("Test complete!, closing program.")
                plt.savefig('On_hand.png')  # Save the figure to a file
                break

if __name__ == "__main__":
    port = 'COM4'  # Change this to your serial port
    baudrate = 9600
    timeout = 1
    ser = serial.Serial(port, baudrate, timeout=timeout)
    temp_gen = read_serial_data(ser)
    plot_data(temp_gen, ser)
    ser.close()  # Close the serial port when the program ends