package main

import (
    "bytes"
    "errors"
    "fmt"
    "github.com/google/uuid"
    "github.com/nfnt/resize"
    "image"
    "image/draw"
    "image/jpeg"
    _ "image/jpeg"
    "image/png"
    _ "image/png"
    "io/ioutil"
    "log"
    "mime"
    "net/http"
    "os"
    "strconv"
)

const uploadDir = "./uploads"
const thumbNailDir = uploadDir + "/thumb"

var legalContentTypes = map[string]bool {
    "image/png": true,
    "image/jpeg": true,
    "image/svg+xml": true,
}
func main() {
    fmt.Println("Starting fileserver...")
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

    img, _, err := image.Decode(bytes.NewReader(bs))
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

    thumbImg := createThumbNail(img)
    saveThumb(thumbImg, -1, fileUUID.String(), fileExts[0])
    saveThumb(thumbImg, 256, fileUUID.String(), fileExts[0])
    saveThumb(thumbImg, 512, fileUUID.String(), fileExts[0])
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

// Center images in their square bound
func createThumbNail(img image.Image) image.Image {
    imgWidth := img.Bounds().Max.X
    imgHeight := img.Bounds().Max.Y

    horizontal := imgWidth >= imgHeight
    thumbNailSize := max(imgWidth, imgHeight)

    var offsetX, offsetY int
    if horizontal {
        offsetX = 0
        offsetY = (imgWidth - imgHeight) / 2
    } else {
        offsetX = (imgHeight - imgWidth) / 2
        offsetY = 0
    }

    thumbImg := image.NewRGBA(image.Rectangle{Min: image.Point{X: 0, Y: 0}, Max: image.Point{X: thumbNailSize, Y: thumbNailSize}})
    draw.Draw(
        thumbImg,
        image.Rectangle{
            Min: image.Point{X: img.Bounds().Min.X + offsetX, Y: img.Bounds().Min.Y + offsetY},
            Max: image.Point{X: img.Bounds().Max.X + offsetX, Y: img.Bounds().Max.Y + offsetY}},
        img,
        image.Point{X: 0, Y: 0},
        draw.Src)

    return thumbImg
}

// Save the thumbnail image
// Scale it to match size and save in /thumb/[size]/ if size is anything but -1
func saveThumb(img image.Image, size int, fileName, fileExt string) error {
    sizeDir := ""
    resizedImg := img
    if size != -1 {
        sizeDir = "/" + strconv.Itoa(size)
        resizedImg = resize.Resize(uint(size), 0, img, resize.Lanczos3)
    }

    err := os.MkdirAll(thumbNailDir + sizeDir, 0666)
    if err != nil {
        return err
    }

    file, err := os.Create(thumbNailDir + sizeDir + "/" + fileName + fileExt)
    if err != nil {
        return err
    }
    defer file.Close()

    if fileExt == ".png" {
        err = png.Encode(file, resizedImg)
    } else if fileExt == ".jpg" || fileExt == ".jpeg" {
        err = jpeg.Encode(file, resizedImg, nil)
    } else {
        err = errors.New("bad file extension")
    }
    return err
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

func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}
