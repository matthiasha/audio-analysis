function dropzone() {

    return function(scope, element, attrs) {

        var config = {
            url: '/upload',
            paramName: "uploadfile",
            parallelUploads: 1,
            autoProcessQueue: true
        };

        var uploaded = '';

        var eventHandlers = {
            'success': function (file, response) {
                uploaded += response + ',';
            },
            'queuecomplete': function (file, response) {
                window.location.replace('/wav/' + uploaded);
            }
        };

        dropzone = new Dropzone(element[0], config);

        angular.forEach(eventHandlers, function(handler, event) {
            dropzone.on(event, handler);
        });

        scope.processDropzone = function() {
            dropzone.processQueue();
        };

    }
}

angular.module('fileApp').directive('dropzone', dropzone);
