'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  VUE_APP_API_HOST: `${window.location.href}:8000`, //'"http://127.0.0.1:8000"',
  VUE_APP_FILESERVER_HOST: `${window.location.href}:9000` //'"http://127.0.0.1:9000"'
})
