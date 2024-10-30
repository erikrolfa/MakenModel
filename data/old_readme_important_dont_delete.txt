<!-- Html Pages -->
All html pages are extended from base.html
    - Call {% extends "base.html" %} on EVERY page to ensure all links are imported
    - If something is present on every page, add it to base.html


<!-- Comment Legend -->
TODO: This means this is a key feature that needs to be implemented

REVIEW: This means we need to decide if this looks good or needs to be changed



<!-- GENERAL REVIEW -->
Does font look good like this or should I go back to normal?
    - Comparison Screenshots in WEBSITE_STYLE_TESTS Folder


<!-- IDEAS -->

    Possibly add section that tells how many:
        - Paints we cover
        - Models we have in our index
        - Models we search for your personal recommendations

    Possibly add "leaderboard" section
        - How many paints you have in your inventory
            - How your paint count ranks against other users
        - How many models you've completed
            - How this ranks against others

    Add social section where users can post pictures of their models
        - Allow comments and likes from other users
        - Users can set their profile public or private

    Add Forum section where modelers can converse about techniques and such
        - We can do some text processing and retrieval stuff here

    Add tab where you can choose a color on a color wheel, and the program returns colors similar to that from brands you want


<!-- TODO: Website HTML/Javascript -->
    Index.html:
        - Fix modal pop-up styling for when a user is not signed in

    Create Account Page:
        - Fix profile pic upload input (DONE)
        - Fix profile pic upload not showing up in uploads directory
            - When you create an account an upload a profile pic it should show up in var/uploads folder but it is not for some reason
        - Add sign in with google
        - Sliding welcome screen for when a user signs up or logs in

    Sign In page:
        - Username for login (DONE)
        - Login logic (DONE)
        - Forgot username button
        - Email person password reset stuff
            -https://medium.com/@stevenrmonaghan/password-reset-with-flask-mail-protocol-ddcdfc190968
        - Forgot username/password pages

    Toolbox Page:
        - Paints searchbar
            - Autofill when users start to type
            - Have filters for adding lots of paints at once
                - Filter by brand
            - Fix null showing up in autofill when paint_type is null

        - Style add paints page

        - Add tracker for paints that are getting low
            - Have these paints appear in a seperate section on the page

        - Add favorite's selection bar
            - Displays favorite paint brand

        - Add total paints in collection section
            - You should be able to see the number of paints in your collection
            - Should also see



<!--  TODO: Scraping -->

    Paint Scraper (DONE)
        - Scrape all paint data off scalemates and turn it into a json dump (DONE)
        - Import json dump into sql database (DONE)

    Model Scraper