const path = require("path");

module.exports = {
  entry: path.resolve(__dirname, "./llm_regex/apps/frontend/src/index.js"),
  output: {
    filename: "main.js",
    path: path.resolve(__dirname, "./llm_regex/apps/frontend/static/frontend"),
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/i,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
};
