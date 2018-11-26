package main

import (
    "bytes"
    "github.com/google/uuid"
    "image"
    _ "image/jpeg"
    _ "image/png"
    "io/ioutil"
    "log"
    "mime"
    "net/http"
)

const uploadDir = "./uploads"

var legalContentTypes = map[string]bool {
    "image/png": true,
    "image/jpeg": true,
    "image/svg+xml": true,
}

func main() {
    http.HandleFunc("/upload/image", uploadHandler)
    fs := http.FileServer(http.Dir(uploadDir))
    http.Handle("/", fs)
    log.Fatal(http.ListenAndServe("0.0.0.0:9000", nil))
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
    addCORSHeader(w)
    if r.Method == http.MethodOptions {
        return
    }
    if r.Method != http.MethodPost {
        log.Printf("Rejected request with illegal method %s\n", r.Method)
        httpError(w, http.StatusMethodNotAllowed)
        return
    }
    file, header, err := r.FormFile("file")
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }
    defer file.Close()

    contentType := header.Header.Get("Content-Type")
    log.Printf("Content-Type: %s\n", contentType)

    if !legalContentTypes[contentType] {
        log.Printf("File with illegal content type uploaded: %s\n", contentType)
        httpError(w, http.StatusBadRequest)
        return
    }

    bs, err := ioutil.ReadAll(file)
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }

    _, _, err = image.Decode(bytes.NewReader(bs))
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }

    fileUUID, err := uuid.NewRandom()
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }

    fileExts, err := mime.ExtensionsByType(contentType)
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }

    fileURI := fileUUID.String() + fileExts[0]
    err = ioutil.WriteFile(uploadDir + "/" + fileURI, bs, 0644)
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusOK)
    _, err = w.Write([]byte(fileURI))
    if err != nil {
        log.Println(err)
        httpError(w, http.StatusInternalServerError)
        return
    }
}

func httpError(w http.ResponseWriter, errorCode int) {
    http.Error(w, http.StatusText(errorCode), errorCode)
}

func addCORSHeader(w http.ResponseWriter)  {
    w.Header().Set("Access-Control-Allow-Origin", "*")
    w.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS")
    w.Header().Set("Access-Control-Allow-Headers",
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
}
