# Connectivity Research

## Local Discovery Status
- UDP Broadcast (30050): FAILED
- Subnet Scan (80, 8000, 8080): FAILED
- Conclusion: Local HTTP API is likely disabled in 2025 Malaysian firmware.

## Cloud API (Go Daikin Malaysia)
- App: Go Daikin (Daikin Malaysia).
- Known Endpoints: `https://api.daikin.com.my`.
- Auth: Requires Login -> Access Token.

## Alternative: IR Blaster
- RPi 4 GPIO + IR LED.
- Protocol: Daikin ARC480 or similar.
- Pros: 100% reliable local control.
- Cons: No feedback (state unknown).

## Next Step
- Try scanning port 8000 (WebSocket) and 8080.
- Ask user if they can provide a token or if we should attempt a login script.
