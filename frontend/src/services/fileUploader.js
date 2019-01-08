import axios from 'axios'
async function uploadImage (imageFile) {
  let formData = new FormData()
  formData.append('file', imageFile)
  return axios.post(process.env.VUE_APP_FILESERVER_HOST + '/upload/image', formData).then((response) => {
    return response.data
  })
}

export const fileUploader = {
  uploadImage
}
