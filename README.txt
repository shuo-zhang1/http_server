This is a simplified version of a HTTP client and server using TCP sockets. The client program will
use the HTTP protocol to fetch a web page (stored in a file) from the server using the HTTP GET method,
cache it, and then subsequently use conditional GET operations to fetch the file only if it has been
modified. 

The HTTP client will perform the following functions:
1. Take in a single command line argument that specifies a web url containing the hostname and port
where the server is running, as well as the name of the file to be fetched, in the appropriate format.
Example: localhost:12000/filename.html
2. If the file is not yet cached, use a HTTP GET operation to fetch the file named in the URL
a. Print out the contents of the file
b. Cache the file
3. If the file is cached, use a Conditional GET operation for the file named in the URL
a. If the server indicates the file has not been modified since last downloaded, print output saying so (no need to print file contents in this case)
b. Otherwise, indicate that the file has been modified, and print and cache new contents

The HTTP server will perform the following functions:
1. Read a command-line argument specifying IP address and port server is to listen on e.g. 127.0.0.1
12000
2. Open a TCP socket and listen for incoming HTTP Get and Conditional GET requests from one or more
HTTP Clients at above address and port
3. In the case of a HTTP Get request:
a. Read the named file and return a HTTP GET Response, including the Last-Modified header field
4. In the case of a HTTP Conditional Get Request:
a. If the file has not been modified since that indicated by If-Modified-Since, return the
appropriate Not Modified response (return code 304)
b. If the file has been modified, return the file contents as in step 2
5. In the case that the named file does not exist, return the appropriate “Not Found” error (return code 404)
