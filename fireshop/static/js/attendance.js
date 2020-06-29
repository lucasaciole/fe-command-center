$(function(){

	$("#submitAttendances").click(function(){
		data = {}
		$("tr.member-data").each(function(){
			var userId = $($(this).children("td")[0]).data("userId");
			var categoryId = $(this).children("td").children("input:checked")[0].value
			data[userId] = categoryId
		});
		$.ajax({
			url: "attendance/confirm",
			type: "GET",
			data: ({'attendances': JSON.stringify(data)}),
			success: function(resp) {
				console.log(resp);
			}
		})
	});
});