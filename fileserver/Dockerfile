FROM golang:1.11.2 as builder
RUN mkdir -p /go/src/fileserver
WORKDIR /go/src/fileserver
COPY main.go  .
RUN go get -u github.com/golang/dep/...
RUN dep init
RUN dep ensure 
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /go/src/fileserver/main .
