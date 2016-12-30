Backline provides a simple HTML-based display for use on a server during testing.

It's implemented as a Python http server which can serve:
   - any files in the current directory (as with SimpleHTTPServer)
   - a single string, at /line/, which can be altered with POST

The string at /line/ should be used as the class of the root HTML element.

A call to /line/blocking will block until the line is updated.

The example shipped with Backline displays three lightbulbs,
labelled "red", "green", and "blue". You can display them
by running Backline and launching

  http://localhost:8080/lights.html

in your browser. Then you can turn the lightbulbs on and off thus:

wget --post-data 'line=blue' http://localhost:8080/line/ -O -

wget --post-data 'line=red green' http://localhost:8080/line/ -O -

wget --post-data 'line=none' http://localhost:8080/line/ -O -

The example depends on JQuery, which it fetches from Google's CDN.
