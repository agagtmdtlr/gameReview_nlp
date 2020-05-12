from pyy.crawling.game_review.크롤링.gameSuper import Crawl

crawls = Crawl()
cnt = 0
while True:
    cnt += 1
    crawls.cycleScroll()
    end = crawls.checkHeight()
    if end:
        crawls.savefile()
        break
    else:
        if cnt == 10 :
            crawls.savefile()
            crawls.deleteElement()
            cnt = 0

