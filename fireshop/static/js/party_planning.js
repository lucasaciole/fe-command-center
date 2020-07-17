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
  if (document.getElementById("playerList")) {
    Sortable.create(playerList, opts);
  }
  if (document.getElementById("goingList")) {
    Sortable.create(goingList, opts);
  }
  if (document.getElementById("maybeList")) {
    Sortable.create(maybeList, opts);
  }
  if (document.getElementById("notGoingList")) {
    Sortable.create(notGoingList, opts);
  }

  $(".select-character").click(function(e){
    var el = $(e.target);
    var char = el.parent().children(".char-class");
    var target = el.parent().parent().parent().parent().children(".user-name")
    target.text(target.data("name") + ":" + char.text())
  });

  $("#addParty").click(function(e){
    var row = $("#partyPlanner");
    var col = $("<div class='col-sm-3'></div>")
    row.append(col);

    var uheader = $("<h6>PT #"+ ++sortableCount + "</h6>");
    var ulist = $("<ul id='sortable" + sortableCount + "' class='list-group empty-group'></ul>")
    col.append(uheader, ulist);
    Sortable.create(ulist[0], opts);
    sortables.push(ulist[0]);
  })
});