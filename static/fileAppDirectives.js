function dropzone() {

    return function(scope, element, attrs) {

        var config = {
            url: '/upload',
            maxFilesize: 100,
            paramName: "uploadfile",
            maxThumbnailFilesize: 10,
            parallelUploads: 1,
            autoProcessQueue: false
        };

        var eventHandlers = {
            'addedfile': function(file) {
                scope.file = file;
                if (this.files[1]!=null) {
                    this.removeFile(this.files[0]);
                }
                scope.$apply(function() {
                    scope.fileAdded = true;
                });
            },

            'success': function (file, response) {
                // angular.element(document.querySelector('#result')).html(response);
                document.open();
                document.write(response);
                document.close();
            }
        };

        dropzone = new Dropzone(element[0], config);

        angular.forEach(eventHandlers, function(handler, event) {
            dropzone.on(event, handler);
        });

        scope.processDropzone = function() {
            var tool = document.querySelector('input[name="tool"]:checked').value;
            var channel = document.querySelector('input[name="channel"]').value;
            dropzone.options.url = '/upload/' + channel + '/' + tool;
            dropzone.processQueue();
        };

    }
}

angular.module('fileApp').directive('dropzone', dropzone);
