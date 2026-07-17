package daikin

import (
	"fmt"
)

// Timing constants in microseconds
const (
	Pulse            = 430
	ZeroGap          = 430
	OneGap           = 1290
	HeaderPulse      = 3440
	HeaderGap        = 1720
	GapBetweenFrames = 35000
)

type State struct {
	Power uint8 // 0: OFF, 1: ON
	Temp  uint8 // 16-32
	Mode  uint8 // 0: AUTO, 3: COOL, 2: DRY, 4: HEAT, 6: FAN
	Fan   uint8 // 0: AUTO, 1-5: Level, 10: QUIET
	Swing uint8 // 0: OFF, 1: ON
}

func CalculateChecksum(data []byte) byte {
	var sum uint32
	for i := 0; i < len(data)-1; i++ {
		sum += uint32(data[i])
	}
	return byte(sum & 0xFF)
}

func EncodeState(state State) ([][]byte, error) {
	// Frame 1: Preamble
	f1 := []byte{0x11, 0xda, 0x27, 0x00, 0xc5, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00}
	f1[len(f1)-1] = CalculateChecksum(f1)

	// Frame 2: State
	f2 := make([]byte, 19)
	f2[0] = 0x11
	f2[1] = 0xda
	f2[2] = 0x27
	f2[3] = 0x00
	f2[4] = 0x42

	// Byte 5: Mode (bits 4-6) | Power (bit 0)
	f2[5] = (state.Mode << 4) | (state.Power & 0x01)

	// Byte 6: Temp * 2
	f2[6] = state.Temp << 1

	// Byte 8: Fan (bits 4-7) | Swing (bits 0-3)
	f2[8] = (state.Fan << 4) | (state.Swing & 0x0F)

	f2[len(f2)-1] = CalculateChecksum(f2)

	return [][]byte{f1, f2}, nil
}
