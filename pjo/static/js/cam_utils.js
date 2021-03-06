
/****************************************************************
 *  clear object
 ****************************************************************/
 function f_clear(obj) {
	obj.value = "";
 }


/****************************************************************
 *  number only
 ****************************************************************/
function f_numOnly(objId) {

	const regexp = /[^[0-9]/gi;

	if(regexp.test($('#' + objId).val())){
		alert('number only');
		$('#' + objId).val("");
		$('#' + objId).focus();
		return false;
	}
	return true;
}


/****************************************************************
 *  CSRF Token
 ****************************************************************/
function f_getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie != '') {
		let cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			let cookie = $.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}


/****************************************************************
 *  CSRF Token
 ****************************************************************/
function f_csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


/****************************************************************
 *  only English & number
 ****************************************************************/
function f_checkSpecial(objectId){

	const chkObject = $("#" + objectId);
	const str = chkObject.val();

	// special character
	const regExp = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi
	if(regExp.test(str)){
		const retStr = str.replace(regExp, "")
		chkObject.val(retStr);
		alert("Only Alphanumeric is allowed.");
		chkObject.focus();
		return false;
	}

	// space
	const blank_pattern = /[\s]/g;
	if (blank_pattern.test(str) == true) {
		const retStr = str.replace(blank_pattern, "")
		chkObject.val(retStr);
		alert("No space please.");
		chkObject.focus();
		return false;
	}

	return true;
}


/****************************************************************
 *  check number only
 ****************************************************************/
function f_checkNumOnly(objId) {

	const regexp = /^[0-9]+$/;

	if(!regexp.test($('#' + objId).val())){
		alert('number only');
		$('#' + objId).val("");
		$('#' + objId).focus();
		return false;
	}
	return true;
}


/****************************************************************
 *  float only
 ****************************************************************/
function f_checkFloatOnly(objId) {

	const regexp = /^\d+(?:[.]\d+)?$/;
	if(!regexp.test($('#' + objId).val())){
		alert('float only');
		$('#' + objId).val("");
		$('#' + objId).focus();
		return false;
	}
	return true;
}


/****************************************************************
 *  list only for ED
 *      ex)  1,2,3
 ****************************************************************/
function f_checkNumListOnly(objId) {

	const regexp = /^\d*(,\d+)*$/;
	if(!regexp.test($('#' + objId).val())){
		alert('Number list only');
		$('#' + objId).val("");
		$('#' + objId).focus();
		return false;
	}
	return true;
}




