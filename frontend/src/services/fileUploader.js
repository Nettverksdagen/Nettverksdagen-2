import axios from 'axios'
async function uploadImage (imageFile) {
  let formData = new FormData()
  formData.append('file', imageFile)
  return axios.post('http://127.0.0.1:9000/upload/image', formData).then((response) => {
    return response.data
  })
}

export const fileUploader = {
  uploadImage
}
