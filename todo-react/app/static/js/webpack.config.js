module.exports = {
    entry: {
        index: "./index.js"
    },
    output: {
        path: "./build",
        filename: "bundle.js"
    },
    modules: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel'
            }
        ]
    }
};