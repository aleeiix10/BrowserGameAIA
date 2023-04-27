// Importamos webpack-bundle-tracker
const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
    // La ruta donde estará disponible el bundle de los archivos estáticos 
	publicPath: "http://0.0.0.0:8080/",
    // Directorio donde se creará el bundle de archivos estáticos
    outputDir: './dist/',
    // Estable que se compile en tiempo de ejecución.
	runtimeCompiler: true,

    // Los puntos de entrada de nuestra aplicación.
	pages: {
		main: {
		    // entry for the page
		    entry: 'src/main.js',
        },
			
	},

	chainWebpack: config => {
		config.optimization
		.splitChunks(false)

		config
        .plugin('BundleTracker')
        // El archivo que mapeará los estáticos del proyecto.
		.use(BundleTracker, [{filename: './webpack-stats.json'}])

		config.resolve.alias
		.set('__STATIC__', 'static')
	}
};