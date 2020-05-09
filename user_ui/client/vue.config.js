module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
      ? '/human-datascience/'
      : '/',
      devServer: {
        proxy: `${process.env.VUE_APP_PYTHON_BACKEND}`
      },
  }