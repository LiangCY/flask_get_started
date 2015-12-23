module.exports = {
    entry: {
        index: "./index.js"
    },
    output: {
        path: "./build",
        filename: "bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loader: 'babel',
                query: {
                    presets: ['react']
                }
            }
        ]
    }
};