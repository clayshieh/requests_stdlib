# Requests Standard Libary
A dependency free drop-in replacement for requests and requests-unixsocket for the common functions implemented using only Python 2 and 3 standard libraries.

### Should I use this?

* I have a project where I use requests because that's what everyone on stackoverflow tells me to do but I really only use simple GET/POST/PUT/DELETE functions.

* I want to communicate with my Docker daemon but I think it's ridiculous that I have to install requests AND requests-unixsocket just to send HTTP requests to a unix socket file.

* I have a project where the only dependency is requests and/or requests-unixsocket and I don't want to have to require users to install those just to use my project.


Well, if you find yourself thinking any of these when writing a project using request and/or requests-unixsocket then you should consider using this!


### Prerequisites
None, that's the point.

### Getting Started
Just drop `requests.py` into your project directory!

### Usage
Features and usage are the same as requests [quickstart](http://docs.python-requests.org/en/master/user/quickstart/) for the following:

* Make a Request [link](http://docs.python-requests.org/en/master/user/quickstart/#make-a-request)
* Passing Parameters In URLs [link](http://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls)
* Response Content (except the encoding bit) [link](http://docs.python-requests.org/en/master/user/quickstart/#response-content)
* JSON Response Content [link](http://docs.python-requests.org/en/master/user/quickstart/#json-response-content)
* Custom Headers [link](http://docs.python-requests.org/en/master/user/quickstart/#custom-headers)
* More complicated POST requests [link](http://docs.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests)
* Response Status Codes (only the r.status_code bit) [link](http://docs.python-requests.org/en/master/user/quickstart/#response-status-codes)
* Response Headers [link](http://docs.python-requests.org/en/master/user/quickstart/#response-headers)
* Redirection and History (except the history bit) [link](http://docs.python-requests.org/en/master/user/quickstart/#redirection-and-history)

Unix socket usage is the same as requests-unixsocket [documentation](https://github.com/docker/docker-py/blob/master/docker/transport/unixconn.py) in regards to the scheme.

For example to send an HTTP request to `/var/run/docker.sock` you would use:

`r = requests.get("http+unix://%2Fvar%2Frun%2Fdocker.sock/info")`


### TODO
I only implemented a subset of the features in requests which I found myself most commonly using. If there is interest for more of requests features I will implement them or feel free to make a PR if you want to add it yourself!

* Binary Response Content [link](http://docs.python-requests.org/en/master/user/quickstart/#binary-response-content)
* Raw Response Content [link](http://docs.python-requests.org/en/master/user/quickstart/#raw-response-content)
* POST a Multipart-Encoded File [link](http://docs.python-requests.org/en/master/user/quickstart/#post-a-multipart-encoded-file)
* Cookies [link](http://docs.python-requests.org/en/master/user/quickstart/#cookies)
* Timeouts [link](http://docs.python-requests.org/en/master/user/quickstart/#timeouts)

### Acknowledgements
Referenced https://github.com/docker/docker-py/blob/master/docker/transport/unixconn.py for Docker's socket HTTPConnection code.

### Contributing
Pull requests and contributions are welcomed!

### Support
For any questions or concerns, please create an issue or contact me.
