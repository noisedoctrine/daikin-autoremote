#include <stdio.h>
#include <stdlib.h>
#include <pigpio.h>
#include <unistd.h>
#include "daikin_arc480.h"

#define IR_GPIO 17

void add_byte_to_wave(int gpio, uint8_t byte, gpioPulse_t *pulses, int *count) {
    for (int i = 0; i < 8; i++) {
        int bit = (byte >> i) & 1;
        // Pulse
        pulses[*count].gpioOn = (1 << gpio);
        pulses[*count].gpioOff = 0;
        pulses[*count].usDelay = PULSE;
        (*count)++;
        // Space
        pulses[*count].gpioOn = 0;
        pulses[*count].gpioOff = (1 << gpio);
        pulses[*count].usDelay = bit ? ONE_GAP : ZERO_GAP;
        (*count)++;
    }
}

void send_frames(int gpio, uint8_t *f1, uint8_t *f2) {
    // Max pulses: Header(2) + 11*16 + Stop(1) + Gap(1) + Header(2) + 19*16 + Stop(1) = ~500
    gpioPulse_t pulses[1000];
    int count = 0;

    // --- Frame 1 ---
    pulses[count++] = (gpioPulse_t){1<<gpio, 0, HEADER_PULSE};
    pulses[count++] = (gpioPulse_t){0, 1<<gpio, HEADER_GAP};
    for(int i=0; i<FRAME1_LEN; i++) add_byte_to_wave(gpio, f1[i], pulses, &count);
    pulses[count++] = (gpioPulse_t){1<<gpio, 0, PULSE}; // Stop
    pulses[count++] = (gpioPulse_t){0, 1<<gpio, GAP_BETWEEN_FRAMES}; // Inter-frame gap

    // --- Frame 2 ---
    pulses[count++] = (gpioPulse_t){1<<gpio, 0, HEADER_PULSE};
    pulses[count++] = (gpioPulse_t){0, 1<<gpio, HEADER_GAP};
    for(int i=0; i<FRAME2_LEN; i++) add_byte_to_wave(gpio, f2[i], pulses, &count);
    pulses[count++] = (gpioPulse_t){1<<gpio, 0, PULSE}; // Stop

    gpioWaveClear();
    gpioWaveAddGeneric(count, pulses);
    int wave_id = gpioWaveCreate();

    if (wave_id >= 0) {
        gpioWaveTxSend(wave_id, PI_WAVE_MODE_ONE_SHOT);
        while (gpioWaveTxBusy()) time_sleep(0.1);
        gpioWaveDelete(wave_id);
    } else {
        fprintf(stderr, "Failed to create wave: %d\n", wave_id);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Usage: %s <power 0/1> <temp 16-32> <mode 0-6>\n", argv[0]);
        return 1;
    }

    if (gpioInitialise() < 0) return 1;
    gpioSetMode(IR_GPIO, PI_OUTPUT);

    daikin_state_t state = {
        .power = atoi(argv[1]),
        .temp = atoi(argv[2]),
        .mode = atoi(argv[3]),
        .fan = 0, // Auto
        .swing = 0
    };

    uint8_t f1[FRAME1_LEN], f2[FRAME2_LEN];
    daikin_encode_state(&state, f1, f2);

    printf("Sending Daikin IR Command: Power=%d, Temp=%d, Mode=%d\n", state.power, state.temp, state.mode);
    send_frames(IR_GPIO, f1, f2);

    gpioTerminate();
    return 0;
}
