//regex used to capture header content
var re = /^[A-Za-z\-\/]+?\:\s?[A-Za-z0-9\-\/\=;,|\s]*$/mg,
    url = require('url'),
    spawn = require('child_process').spawn,
    hArray = [];
/* merge usage
 obj3 = merge(obj1,obj2)*/
var merge = function () {
    "use strict";
    var obj = {},
        i = 0,
        il = arguments.length,
        key;
    for (; i < il; i++) {
        for (key in arguments[i]) {
            if (arguments[i].hasOwnProperty(key)) {
                obj[key] = arguments[i][key];
            }
        }
    }
    return obj;
};

function spawnPerlCGI(script, req, env, callback) {
    var script_name = ''
        , returnStr = ''
        , returnErr = ''
        , scriptArr
        , auth
        , header
        , name
        , cp;

    if (script !== '') {
        scriptArr = process.platform === 'win32' ? script.split("\\") : script.split('/');
        script_name = scriptArr.pop();
    }
    if (!env && req) {
        env = merge(process.env,
            {
                GATEWAY_INTERFACE: "CGI/1.1",
                SCRIPT_NAME: script_name,
                SCRIPT_FILENAME: script,
                PATH_INFO: __dirname + '/cgi-bin/',
                SERVER_NAME: req.headers.host.split(':')[0],
                SERVER_PORT: req.headers.host.split(':')[1] || 80,
                SERVER_PROTOCOL: "HTTP/1.1",
                SERVER_SOFTWARE: "Node/" + process.version,
                REQUEST_METHOD: req.method,
            });
        //If GET Request than build QUERY_STRING
        if (req.method === 'GET') {
            env.QUERY_STRING = req.uri || url.parse(req.url).query;
        }
        // If POST Method than grab client content length and type
        if (req.method === 'POST') {
            //console.log('req.method = '+req.method);
            if ('content-length' in req.headers) {
                env.CONTENT_LENGTH = req.headers['content-length'];
            }
            if ('content-type' in req.headers) {
                env.CONTENT_TYPE = req.headers['content-type'];
            }
        }
        if ('authorization' in req.headers) {
            auth = req.headers.authorization.split(' ');
            env.AUTH_TYPE = auth[0];
        }

        // Transform all headers into a general looking env
        for (header in req.headers) {
            // Env looks like HTTP_HEADER_ALL_CAPS
            name = 'HTTP_' + header.toUpperCase().replace(/[^A-Z0-9_]/g, '_');
            env[name] = req.headers[header];
        }

    }

    // Childprocess.spawn
    cp = spawn('perl', [script], {env: env});

    // The request body is piped to 'stdin' of the CGI spawn
    req.pipe(cp.stdin);
    cp.stdout.on('data', function (data) {

        returnStr += data.toString();

    });
    //Any error the perl script returns will come through here
    cp.stderr.on("data", function (data) {
        returnErr += data.toString();
    });
    cp.on('exit', function (code) {
        // Remove the header that perl script might have written to stdout.
        var parts = returnStr.split('\n\n');
        if (parts.length && re.test(parts[0])) {
            hArray = parts.shift().match(re);
        }
        returnStr = parts.join('\n\n');
        return callback(returnErr, returnStr);
    });


}
// Converts the Array of header values and returns an Object
// to client for passing into res.header() in one pass
spawnPerlCGI.prototype.getHeader = function () {
    var objArray = Object.create(null),
        x,
        header;
    for (x in hArray) {
        if (hArray.hasOwnProperty(x) === false) continue;
        header = hArray[x].split(':');
        objArray[header[0]] = header[1].trim();
    }
    //console.log(objArray);
    return objArray;

}
exports.spawnPerlCGI = spawnPerlCGI;

