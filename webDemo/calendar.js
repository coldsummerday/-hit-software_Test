function submitDate()
{
        postdata = {
            "year": $('#year').val(),
            "month": $('#month').val(),
            "day": $('#day').val(),
        };

        $.post('/cgi-bin/main.py', postdata, function (returnData, status) {
            document.getElementById("nextday").innerHTML = returnData;
        })


}