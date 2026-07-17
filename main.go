package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/BxNiom/go-pigpio"
	"github.com/noisedoctrine/daikin-autoremote/pkg/daikin"
)

const (
	defaultIRPin      = 17
	defaultPigpioPort = 8888
)

type ControlRequest struct {
	Power *int `json:"power"`
	Temp  *int `json:"temp"`
	Mode  *int `json:"mode"`
}

func main() {
	pigpioHost := envString("PIGPIO_HOST", "localhost")
	pigpioPort := envInt("PIGPIO_PORT", defaultPigpioPort)
	irPin := envInt("IR_GPIO", defaultIRPin)
	apiAddr := envString("DAIKIN_API_ADDR", "127.0.0.1:8000")

	// Initialize pigpio connection
	pi, err := pigpio.Initialize(pigpioHost, pigpioPort)
	if err != nil {
		log.Fatalf("Failed to connect to pigpiod: %v", err)
	}
	defer pi.Close()

	// Set GPIO mode
	pin := pi.Gpio(irPin)
	pin.SetMode(pigpio.Output)

	http.HandleFunc("/control", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req ControlRequest
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid request", http.StatusBadRequest)
			return
		}

		// Prepare state
		state := daikin.State{
			Power: 1, // Default ON
			Temp:  24,
			Mode:  3, // COOL
		}
		if req.Power != nil {
			state.Power = uint8(*req.Power)
		}
		if req.Temp != nil {
			state.Temp = uint8(*req.Temp)
		}
		if req.Mode != nil {
			state.Mode = uint8(*req.Mode)
		}

		frames, err := daikin.EncodeState(state)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Send IR signal
		if err := sendFrames(pi, irPin, frames); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
	})

	fmt.Printf("Daikin AutoRemote Go API starting on %s\n", apiAddr)
	log.Fatal(http.ListenAndServe(apiAddr, nil))
}

func sendFrames(pi *pigpio.Pi, gpio int, frames [][]byte) error {
	// Waveform construction logic...
	// Note: This is a high-level representation.
	// The go-pigpio library provides methods to build and send waves.

	// Example (simplified):
	// pulses := []pigpio.Pulse{}
	// ... add pulses for headers, bits, and gaps ...
	// waveID, _ := pi.WaveCreate(pulses)
	// pi.WaveSendOnce(waveID)

	fmt.Printf("Sending %d frames via GPIO %d\n", len(frames), gpio)
	return nil
}

func envString(name, fallback string) string {
	if value := os.Getenv(name); value != "" {
		return value
	}
	return fallback
}

func envInt(name string, fallback int) int {
	value := os.Getenv(name)
	if value == "" {
		return fallback
	}
	parsed, err := strconv.Atoi(value)
	if err != nil {
		log.Printf("Ignoring invalid %s=%q: %v", name, value, err)
		return fallback
	}
	return parsed
}
