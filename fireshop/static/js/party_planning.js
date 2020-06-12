$( function() {
  var sortableCount = 0;
  var sortables = []
  var opts = {
    group: 'shared',
    handle: '.handle',
    animation: 150,
    onEnd: function(e) {
      var openList = $("#openParties");

      if ($(e.to).hasClass("empty-group")) {
        $(e.to).removeClass("empty-group");
      }

      if ( e.from.children.length == 0) {
        $(e.from).addClass("empty-group");
      }

      openList.empty();
      sortables.forEach(function(sortable){
        if (sortable.children.length < 5) {
          var warning = $("<p>" +
            $(sortable).prev().text()
            + " tem " + (5 - sortable.children.length) + " vaga(s) livres</p>")
          openList.append(warning);
        }
      });
    }
  };
  Sortable.create(playerList, opts);

  $("#addParty").click(function(e){
    var row = $("#partyPlanner");
    var col = $("<div class='col-sm-4'></div>")
    row.append(col);

    var uheader = $("<h6>PT #"+ ++sortableCount + "</h6>");
    var ulist = $("<ul id='sortable" + sortableCount + "' class='list-group empty-group'></ul>")
    col.append(uheader, ulist);
    Sortable.create(ulist[0], opts);
    sortables.push(ulist[0]);
  })
});