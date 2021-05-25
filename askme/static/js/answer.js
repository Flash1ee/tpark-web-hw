$('.form-check-input').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        qid = $this.data('qid'),
        aid = $this.data('aid');
    $.ajax('/choice/', {
        method: 'POST',
        data: {
            aid: aid,
            qid: qid
        }
    }).done(function (data) {
        console.log("RESPONSE: " + data);

        var checkbox_id = "answer-correct-" + aid;
        var checkbox = $("#" + checkbox_id);
        checkbox.prop('checked', !checkbox.prop('checked'));
    });

    console.log('CLIENT: correct checkbox click   ' + qid + '   ' + aid);
});
        // console.log("RESPONSE: " + data);
        // var likes = $('.like_' + data.qid).contents()[0].textContent;
        // console.log("LIKES: " + likes);
        //
        // var bef = parseInt(likes, 10);
        // bef = bef + 1;
        // if (bef === 0)
        //     bef = 1;
        // $('.like_'+data.qid).contents().last()[0].textContent=bef.toString(10);


    // console.log("Click: " + action + " " + qid);
// });