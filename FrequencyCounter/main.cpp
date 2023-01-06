#include <iostream>
#include <serialib.h>
#include <sys/time.h>
#include <chrono>
#include <thread>

int main() {

    using namespace std::chrono_literals; // ns, us, ms, s, h, ... suffixes i.e. 1ns
    using std::this_thread::sleep_for;

    // Create a serialib object
    serialib serial;

    // Connect to device
    if (serial.openDevice("COM3", 9600) != 1) return 1;

    // Set DTR and RTS. This is configured for the B&K Precision 1856D Frequency Counter.
    serial.DTR(true);
    serial.RTS(false);

    // Create a buffer array to write serial input to
    byte buffer[15];

    
    serial.writeString("D1\r");
    serial.readBytes(&buffer, 15);
    sleep_for(300ms);

    // Print buffer to cout
    for (int i=1; i < 15; i++) {
        // printf("%x", buffer[i]);
        std::cout << buffer[i];
    }
    // printf("\n");
    std::cout << "\n";

    serial.closeDevice();
    
    return 0;
}