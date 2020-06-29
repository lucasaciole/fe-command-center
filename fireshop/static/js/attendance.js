$(function(){
	$("#submitAttendances").click(function(e){
		e.preventDefault();
		data = {}
		$("tr.member-data").each(function(){
			var userId = $($(this).children("td")[0]).data("userId");
			var categoryId = $(this).children("td").children("input:checked")[0].value
			data[userId] = categoryId
		});

		$("#attendanceList").val(JSON.stringify(data))
		attendancesForm.submit();
	});
});