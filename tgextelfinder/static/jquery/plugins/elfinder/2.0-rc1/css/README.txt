
Note:
=======

There are two immediate problems which are noticeable using the
combination of  bootstrap, jquery ui and the elfinder widget (with its
own css)

    1. the button sizes (in fact the <divs> which contain the <spans>)
       which hold the icon/image, are incorrect.  Whilst they're
       specified explicitly in elfinder.min.css as height & width = 16px
       for some reason, this results in an incorrectly computed icon
       size --  I see nothing apparent which would cause this.

       Solution:  simply take out the height/width settings from
                  .elfinder-button

    2. The upload button conflicts with the buttons to the
       left of it.  On closer inspection (and unlike the other buttons)
       <div... title="Upload Files"> contains a <form> with an
       <input type="file"> (which makes perfect sense so far).
       Problem is that this <form> isn't explicitly styles and so its
       width is being computed at 238px (starting from the left, and
       hence covering the four buttons which precede it. This almost
       certainly has something to do with the bootstrap columns etc.

       Solution:  explicitly set the width of the <form> to 24px

       [original] .elfinder-button form{position:absolute ...
       [amended]  .elfinder-button form{width:24px;position:absolute ...

