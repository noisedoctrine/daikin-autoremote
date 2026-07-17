#ifndef DAIKIN_ARC480_H
#define DAIKIN_ARC480_H

#include <stdint.h>
#include <stddef.h>

// ARC480 Timing Constants (in microseconds)
#define PULSE 430
#define ZERO_GAP 430
#define ONE_GAP 1290
#define HEADER_PULSE 3440
#define HEADER_GAP 1720
#define GAP_BETWEEN_FRAMES 35000
#define CARRIER_HZ 38000

typedef struct {
    uint8_t power;   // 0: OFF, 1: ON
    uint8_t temp;    // 16-32
    uint8_t mode;    // 0: AUTO, 3: COOL, 2: DRY, 4: HEAT, 6: FAN
    uint8_t fan;     // 0: AUTO, 1-5: Level, 10: QUIET
    uint8_t swing;   // 0: OFF, 1: ON
} daikin_state_t;

// Frame 1: Preamble (11 bytes)
// Frame 2: State (19 bytes)
#define FRAME1_LEN 11
#define FRAME2_LEN 19

void daikin_encode_state(daikin_state_t *state, uint8_t *frame1, uint8_t *frame2);
uint8_t daikin_calculate_checksum(uint8_t *data, size_t len);

#endif // DAIKIN_ARC480_H
