# Build Stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go.mod and install dependencies
COPY go.mod ./
# RUN go mod download

COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o daikin_remote main.go

# Production Stage
FROM alpine:latest

WORKDIR /root/

# Copy the binary from builder
COPY --from=builder /app/daikin_remote .

# Expose the API port
EXPOSE 8000

# Start the application
CMD ["./daikin_remote"]
