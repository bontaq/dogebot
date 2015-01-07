module.exports = function(grunt) {
    grunt.initConfig({
        watch: {
            scripts: {
                files: [],
                tasks: []
            }
        }
    });
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-compass')

    grunt.registerTask('default', []);
};
