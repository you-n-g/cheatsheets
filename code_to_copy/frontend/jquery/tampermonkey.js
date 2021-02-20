


(function() {
    // Your code here...
    $(document).keydown(function(e){
        //e.which is set by jQuery for those browsers that do not normally support e.keyCode.
        var keyCode = e.keyCode || e.which;

        /*
        if (keyCode == 38)
        {
           alert( "Up arrow key hit." );
           return false;
        }

        if (keyCode == 40)
        {
           alert( "Down arrow key hit." );
           return false;
        }
        */

        if (keyCode == 37)
        {
           $('a[title="上一页"]').click();
           return false;
        }

        if (keyCode == 39)
        {
           $('a[title="下一页"]').click();
           return false;
        }

    });
})();
