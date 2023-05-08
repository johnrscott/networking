# Hypertext Transfer Protocol (HTTP)

HTTP is an application-layer protocol for allowing clients to make requests of servers. Requests are text-based, and have the following format (CRLF means carriage-return line-feed, i.e. `\r\n`):

```txt
method request_uri http_version CRLF
header0: value0 CRLF
header1: value1 CRLF
...
headerN: valueN CRLF
CRLF
message CRLF
CRLF
```

The header and message lines are optional (although the Host header is required for HTTP/1.1). An example of an HTTP request is:

```text
GET / HTTP/1.1
Host: localhost
```

Response have the following format:

```txt
http_version status_code reason_phrase
header0: value0 CRLF
header1: value1 CRLF
...
headerN: valueN CRLF
CRLF
message CRLF
CRLF
```

An example response is

```txt
HTTP/1.1 200 OK
Content-Type: text/http

Hello World!

```

