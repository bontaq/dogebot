module.exports = function(grunt) {
    grunt.initConfig({
      watch: {
        scripts: {
          files: [],
          tasks: []
        },
        css : {
          files: ['**/*.scss'],
          tasks: ['compass']
        }
      },
      compass: {                  // Task
        dist: {                   // Target
          options: {              // Target options
            sassDir: 'dogebote/sass',
            cssDir: 'dogebote/static/stylesheets',
            environment: 'production'
          }
        }
      }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass');

    grunt.registerTask('default', []);
};
