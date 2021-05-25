$('.js-vote-like').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        qid = $this.data('qid'),
        aid = $this.data('aid');
    data = {};
    if (type == "answer")
        data = {
            action: action,
            aid: aid,
            type: type
        }
    else
        data = {
            action: action,
            qid: qid,
            type: type
        }
    $.ajax('/vote/', {
        method: 'POST',
        data: data
    }).done(function (data) {
        console.log("RESPONSE: " + data);
        id = 0
        if (type == "answer")
            id = data.aid
        else
            id = data.qid
        var likes = $('.like_' + id).contents()[0].textContent;
        console.log("LIKES: " + likes);

        var bef = parseInt(likes, 10);
        bef = bef + 1;
        if (bef === 0)
            bef = 1;
        $('.like_' + id).contents().last()[0].textContent = bef.toString(10);

    });
});
$('.js-vote-dislike').click(function (ev) {
    ev.preventDefault();
    const $this = $(this),
        action = $this.data('action'),
        type = $this.data('type'),
        qid = $this.data('qid'),
        aid = $this.data('aid');
    data = {};
    if (type == "answer")
        data = {
            action: action,
            aid: aid,
            type: type
        }
    else
        data = {
            action: action,
            qid: qid,
            type: type
        }

    $.ajax('/vote/', {
        method: 'POST',
        data: data
    }).done(function (data) {
        console.log("RESPONSE: " + data);
        id = 0
        if (type == "answer")
            id = data.aid
        else
            id = data.qid
        var likes = $('.like_' + id).contents()[0].textContent;
        console.log("LIKES: " + likes);

        var bef = parseInt(likes, 10);
        bef = bef - 1;
        if (bef === 0)
            bef -= 1;
        $('.like_' + id).contents().last()[0].textContent = bef.toString(10);

    });

    // console.log("Click: " + action + " " + qid);
});