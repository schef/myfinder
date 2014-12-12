#!/usr/bin/env python

from colorama import Fore, Back, Style
from subprocess import call
from imdbpie import Imdb
imdb = Imdb()
imdb = Imdb({'anonymize' : True}) # to proxy requests


print (Fore.BLUE + "Connecting to IMDb and reading from database..." + Fore.RESET)

# Creating an instance with caching enabled
# Note that the cached responses expire every 2 hours or so.
# The API response itself dictates the expiry time)
imdb = Imdb({'cache': True})
# Specify optional cache directory, the default is '/tmp/imdbpiecache'
imdb = Imdb({'cache': True, 'cache_dir': '/tmp/imdbpie-cache-here'})

lines = [line.strip() for line in open("list.txt", 'r')]
watchlist = [line.strip() for line in open("watchlist.txt", 'r')]
blacklist = [line.strip() for line in open("blacklist.txt", 'r')]

try:
  if (lines[0] not in blacklist) and (lines[0] not in watchlist):
    searchlist = imdb.find_by_title(lines[0])
    first_match = searchlist[0]['imdb_id']
    movie = imdb.find_movie_by_id(first_match)
    print ( Fore.YELLOW + movie.title + Fore.RESET, Fore.GREEN + movie.rating + Fore.RESET, Fore.BLUE + movie.genres + Fore.RESET)
    print (movie.plot_outline)
    call(["feh", movie.cover_url])

    #TODO:questin if it is a movie of episode.
    anwser = input('What should i do?([n]ext, [p]ilot, [b]lacklist, [w]atchlist): ')
    if ( anwser == 'n'):
      print ("next")
      lines.pop(0)
    elif ( anwser == 'p'):
      print (movie.title + " s01e01")
      lines.pop(0)
      #TODO:torrent download
    elif ( anwser == 'b'):
      if (movie.title not in blacklist):
        print ("adding " + movie.title + " to the blacklist")
        blacklist.append(movie.title)
      lines.pop(0)
    elif ( anwser == 'w'):
      if (movie.title not in watchlist):
        print ("adding " + movie.title + " to the watchlist")
        blacklist.append(movie.title)
      lines.pop(0)
  else:
    lines.pop(0)
except: 
  print("Exiting and saving!")
  f = open('list.txt', "w")
  f.write('\n'.join(lines))
  f.close()
  f = open('blacklist.txt', "w")
  f.write('\n'.join(blacklist))
  f.close()
  f = open('watchlist.txt', "w")
  f.write('\n'.join(blacklist))
  f.close()
  
#find a torrent search engine and download pilot
