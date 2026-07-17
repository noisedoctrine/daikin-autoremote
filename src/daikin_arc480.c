#include "daikin_arc480.h"
#include <string.h>

uint8_t daikin_calculate_checksum(uint8_t *data, size_t len) {
    uint32_t sum = 0;
    for (size_t i = 0; i < len - 1; i++) {
        sum += data[i];
    }
    return (uint8_t)(sum & 0xFF);
}

void daikin_encode_state(daikin_state_t *state, uint8_t *frame1, uint8_t *frame2) {
    // Default Preamble Frame 1
    static uint8_t f1_template[FRAME1_LEN] = {
        0x11, 0xda, 0x27, 0x00, 0xc5, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00
    };
    memcpy(frame1, f1_template, FRAME1_LEN);
    frame1[FRAME1_LEN-1] = daikin_calculate_checksum(frame1, FRAME1_LEN);

    // State Frame 2
    memset(frame2, 0, FRAME2_LEN);
    frame2[0] = 0x11;
    frame2[1] = 0xda;
    frame2[2] = 0x27;
    frame2[3] = 0x00;
    frame2[4] = 0x42; // ARC480 State frame ID

    // Power & Mode
    // Byte 5: Power bit (bit 0), Mode (bits 4-6)
    frame2[5] = (state->mode << 4) | (state->power & 0x01);

    // Temperature
    // Byte 6: Temp * 2
    frame2[6] = state->temp << 1;

    // Fan & Swing
    // Byte 8: Fan speed (bits 4-7), Swing (bits 0-3)
    frame2[8] = (state->fan << 4) | (state->swing & 0x0F);

    // Final Checksum
    frame2[FRAME2_LEN-1] = daikin_calculate_checksum(frame2, FRAME2_LEN);
}
