const path = require("path");

module.exports = {
  mode: "development",
  entry: "./assets/index.js",
  output: {
    path: path.resolve(__dirname, "static"),
    filename: "index-bundle.js",
    clean: false,
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: { loader: "babel-loader", options: { presets: ["@babel/preset-env", "@babel/preset-react"] } },
      },
    ],
  },
  resolve: { extensions: [".js", ".jsx"] },
  devtool: "source-map",
};
