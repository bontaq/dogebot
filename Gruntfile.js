module.exports = function(grunt) {
    grunt.initConfig({
        elm: {
            compile: {
                files: {
                    'dogebote/static/js/main.js': 'elm/Main.elm'
                }
            }
        },
        watch: {
            scripts: {
                files: ['elm/Main.elm'],
                tasks: ['elm']
            }
        }
    });
    grunt.loadNpmTasks('grunt-elm');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass')

    grunt.registerTask('default', ['elm']);
};
