===========
metallum_scraper
===========

Scrapes pertinent details for bands/albums/songs from https://www.metal-archives.com/

    #!/usr/bin/env python

    from towelstuff import location
    from towelstuff import utils

    if utils.has_towel():
        print "Your towel is located:", location.where_is_my_towel()

