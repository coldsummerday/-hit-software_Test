function loadUser() {
	var date = getYearMonth();
	var domain = document.URL;
	monthShow();
	var imageurl = domain.substring(0, find(domain, "/", 2)) + "/statistical/user";
	$.get(imageurl, function(result) {
		if(result.error == 0) {
			$('#page-container').empty();
			var imageElement = document.createElement('img');
			imageElement.setAttribute("id", "userimage");
			imageElement.setAttribute("src", "data:image/png;base64," + result.imagedata);
			$('#page-container').append(imageElement);
			$('#checkButton').attr("onclick","getUserTable()")
		} else {
			$('#pageTitle').text(result.errorReason);
		}
	})
}
function getUserTable() {
    var date = getYearMonth(true);
	var domain = document.URL;
    var tableurl = domain.substring(0, find(domain, "/", 2)) + "/statistical/table/passuser/" + date.year + "/" + date.month;
    var tableElement = document.createElement("div");
    tableElement.setAttribute("id", "tableRow");
    $('#page-container').append(tableElement);
    $('#tableRow').load(tableurl);
}
function loadPassUserHis() {
    $('#checkButton').attr("onclick","getPassUerHis()")
}

function getPassUerHis() {
    getDateAndLoad("/statistical/user/pass/",true)
}


function loadProductYearSales() {
	$('#page-container').empty();
    monthHide();
    $('#checkButton').attr("onclick","getProductYearSales()")

}

function getProductYearSales() {
    getDateAndLoad("/statistical/product/month/",false)

}
function loadProductLinePage() {
	$('#page-container').empty();
	monthHide();
	 $('#checkButton').attr("onclick","getProductLinePage()")

}

function getProductLinePage() {
    getDateAndLoad("/statistical/product/line/",false);

}

function loadProductTownMonthPage() {
	$('#page-container').empty();
	monthShow();
	loadButton("getTwonMonthPage", "")
}

function loadProductTownYearPage() {
	$('#page-container').empty();
	monthHide();
	loadButton("getTwonyearPage", "")
}

function loadUserCommissionHisYearPage() {
	$('#page-container').empty();
	monthHide();
	loadButton("getUserCommissionHisYearPage", "")
}

function getUserCommissionHisYearPage() {
    getDateAndLoad("/statistical/user/commission/histogram/",false)

}

function loadUsersalesCountPage() {
	$('#page-container').empty();
	loadButton("getUsersalesCountPage", "")
}

function getUsersalesCountPage() {
    getDateAndLoad("/statistical/user/sellcount/line/",false)

}

function loadUserCommissionHisMonthPage() {
	$('#page-container').empty();
	monthShow()
	loadButton("getUserCommissionHisMonthPage", "")
}

function getUserCommissionHisMonthPage() {
    getDateAndLoad("/statistical/user/commission/histogram/",true)
}

function loadUserCommissionLinePage() {
	$('#page-container').empty();
	monthHide();
	loadButton("getUserCommissionLinePage", "")
}

function getUserCommissionLinePage() {
    getDateAndLoad("/statistical/user/commission/line/",false)

}

function getTwonyearPage() {
    getDateAndLoad("/statistical/product/town/month/",false)

}

function getTwonMonthPage() {
    getDateAndLoad("/statistical/product/town/month/",true)
}

function loadProductMonthPage() {
	$('#page-container').empty();
	monthShow()
	loadButton("getProductMonthImage", "");
}

function getProductMonthImage() {
    getDateAndLoad("/statistical/product/month/",true)


}

function getYearMonth(flag) {

	var yearOptions = $("#selectyear option:selected");
	var year = yearOptions.val()
    if(flag==true)
    {
        var monthOptions = $("#selectmonth option:selected");
	    var month = monthOptions.val()
        return {
		"year": year,
		"month": month,
	    }
    }else {
	    return {
	        "year":year,
        }
    }

}

function getImage(url) {
	$('#myimage').remove();
	$.get(url, function(result) {
		if(result.error == 0) {
			var imageElement = document.createElement('img');
			imageElement.setAttribute("id", "myimage");
			imageElement.setAttribute("src", "data:image/png;base64," + result.imagedata);
			$('#pageTitle').text("");
			$('#page-container').append(imageElement);
		} else {
			$('#pageTitle').text(result.errorReason);
		}
	})
}
function getDateAndLoad(url,flag) {
    var date = getYearMonth(flag);
    var domain = document.URL;
    var url = domain.substring(0, find(domain, "/", 2)) + url + date.year+"/";
    if(flag==true){
        url+=date.month;
    }else {
        url+="0";
    }
	getImage(url)
}

function find(str, cha, num) {
	var x = str.indexOf(cha);
	for(var i = 0; i < num; i++) {
		x = str.indexOf(cha, x + 1);
	}
	return x;
}
function monthHide() {
    $('#monthHead').hide();
	$('#selectmonth').hide()
}
function monthShow() {
    $('#monthHead').show();
	$('#selectmonth').show()
}
function loadButton(func,param) {
    $('#checkButton').attr("onclick",func+"("+param+")");
}