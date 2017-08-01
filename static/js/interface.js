function GetCookie(sName){
    var aCookie = document.cookie.split("; ");
    for (var i=0; i < aCookie.length; i++){
      var aCrumb = aCookie[i].split("=");
      if (sName == aCrumb[0])
        return unescape(aCrumb[1]);
    }
    return null;
}



jQuery(document).ready(function(){
   $("#welcomeuser").text("Welcome "+GetCookie("username")+" !");

      var editor = CodeMirror.fromTextArea(document.getElementById("myText"), {
        lineNumbers: true,
        styleActiveLine: true,
        matchBrackets: true
      });

      var input = document.getElementById("select");

      function selectTheme() {
        var theme = input.options[input.selectedIndex].textContent;
        editor.setOption("theme", theme);
        location.hash = "#" + theme;
      }
      var choice = (location.hash && location.hash.slice(1)) ||
                   (document.location.search &&
                    decodeURIComponent(document.location.search.slice(1)));

      if (choice) {
        input.value = choice;
        editor.setOption("theme", choice);
      }

      CodeMirror.on(window, "hashchange", function() {
        var theme = location.hash.slice(1);
        if (theme) { input.value = theme; selectTheme(); }
      });

      editor.setSize(900,400);

    $('body').on('click','#submitCode',function(){
        console.log("Submitted Code");
        console.log(editor);
        var post_data = new Object();
        post_data["code"] = editor.getValue();
        post_data["contest"] = "sampleContest";
        post_data["problem"] = "sampleProblem";
        post_data["language"] = "c++";
         $.ajax({
                url: "/rest/submit/",
                headers: {
                     'X-CSRFToken' : GetCookie('csrftoken')
                },
                dataType: "json",
                type: "POST",
                data : post_data,
                success: function(data){
                    console.log("submit sucess");
                    console.log(data);

                },
                error:function(){
                     console.log("submit failed");
                }
           });
    });
});
