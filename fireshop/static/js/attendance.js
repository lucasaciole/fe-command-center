$(function(){

	$("#submitAttendances").click(function(){
		$("tr.member-data").each(function(){
			var userId = $($(this).children("td")[0]).data("userId");
			var categoryId = $(this).children("td").children("input:checked")[0].value
			console.log("attendance/" + userId + "/" + categoryId);
		});
	});
});