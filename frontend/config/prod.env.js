'use strict'
module.exports = {
  NODE_ENV: '"production"',
  VUE_APP_API_HOST: `"https://${process.env.VUE_APP_DOMAIN}"`,
  VUE_APP_FILESERVER_HOST: `"https://${process.env.VUE_APP_DOMAIN}/fileserver"`
}
