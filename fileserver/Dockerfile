FROM golang:1.19 AS builder
RUN mkdir -p /go/src/fileserver
WORKDIR /go/src/fileserver
COPY main.go go.mod go.sum ./
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /go/src/fileserver/main .
