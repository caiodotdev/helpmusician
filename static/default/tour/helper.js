var tour = null;
var typingOut;

var template = '<div class="popover tour" role="tooltip"> <div class="arrow"></div>' +
    ' <h3 class="popover-title"></h3> <div class="popover-content"></div> <div class="popover-navigation"> ' +
    '<div class="btn-group"> ' +
    '<button class="btn btn-sm btn-default" data-role="prev" style="padding: 5px 10px;">« Anterior' +
    '</button> ' +
    '<button class="btn btn-sm btn-default" data-role="next" ' +
    'style="padding: 5px 10px;">Proximo »' + ' </button></div> ' +
    '<button class="btn btn-sm btn-default" data-role="end" style="padding: 5px 10px;' +
    ' margin-left: 10px;">Terminar' + '</button> </div> </div>';

function init_tour(name, array) {
    tour = new Tour({
        name: name,
        debug: true,
        steps: array,
        framework: 'bootstrap4',
    });
    tour.start();
}

function clearTour(name) {
    localStorage.removeItem(name + '_current_step');
    localStorage.removeItem(name + '_end');
    if (typeof tour !== 'undefined') {
        tour.restart();
    }
}
