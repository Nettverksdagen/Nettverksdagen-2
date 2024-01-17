'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"testing"',
  VUE_APP_API_HOST: '"http://34.88.95.69/"',
  VUE_APP_FILESERVER_HOST: '"http://34.88.95.69/"'
})
