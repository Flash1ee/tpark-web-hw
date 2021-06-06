$('.form-check-input').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        qid = $this.data('qid'),
        aid = $this.data('aid');
    $.ajax('/choice/', {
        method: 'POST',
        data: {
            aid: aid,
            qid: qid,
            url: this.baseURI

        }
    }).done(function (data) {
        if (data.redirect) {
            window.location.href = data.redirect
        } else {
            console.log("RESPONSE: " + data);

            var checkbox_id = "answer-correct-" + aid;
            var checkbox = $("#" + checkbox_id);
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });

    console.log('CLIENT: correct checkbox click   ' + qid + '   ' + aid);
});
