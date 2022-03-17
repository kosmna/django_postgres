var Select2Cascade = ( function(window, $) {

    function Select2Cascade(parent, child, url, requestData) {
        var afterActions = [];
        var requestData = requestData || {};

        // Register functions to be called after cascading data loading done
        this.then = function(callback) {
            afterActions.push(callback);
            return this;
        };

        parent.select2().on("change", function (e) {

            requestData.parent_id = $(this).val();
            child.prop("disabled", true);

            var _this = this;
            $.getJSON(url, requestData, function(items) {
                var newOptions = '<option value="">-- Select --</option>';
                var sorted = items.sort(function(a, b) {
                  return a[1] > b[1];
                });
                for(var id in sorted) {
                    var el = sorted[id];
                    newOptions += '<option value="'+ el[0] +'">'+ el[1] +'</option>';
                }

                child.select2('destroy').html(newOptions).prop("disabled", false)
                    .select2({ width: 'resolve', placeholder: "-- Select --" });

                afterActions.forEach(function (callback) {
                    callback(parent, child, items);
                });
            });
        });
    }

    return Select2Cascade;

})( window, $);
