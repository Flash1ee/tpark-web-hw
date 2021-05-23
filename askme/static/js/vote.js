$('.js-vote-like').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid');
    $.ajax('.', {
        method: 'POST',
        data: {
            action: action,
            qid: qid
        }
    }).done(function (data) {
        console.log("RESPONSE: " + data);
        var likes = $('.like_' + data.qid).contents()[0].textContent;
        console.log("LIKES: " + likes);

        var bef = parseInt(likes, 10);
        bef = bef + 1;
        $('.like_'+data.qid).contents().last()[0].textContent=bef.toString(10);

    });

    // console.log("Click: " + action + " " + qid);
});
$('.js-vote-dislike').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid');
    $.ajax('.', {
        method: 'POST',
        data: {
            action: action,
            qid: qid
        }
    }).done(function (data) {
        console.log("RESPONSE: " + data);
        var likes = $('.like_' + data.qid).contents()[0].textContent;
        console.log("LIKES: " + likes);

        var bef = parseInt(likes, 10);
        bef = bef - 1;
        $('.like_'+data.qid).contents().last()[0].textContent=bef.toString(10);

    });

    // console.log("Click: " + action + " " + qid);
});