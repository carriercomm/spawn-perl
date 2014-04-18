var perl = require('./spawn-perl').spawnPerlCGI;
var express = require('express')
  ,http = require('http')
  ,url = require('url')
  ,path = require('path');
var app = express();
var script_name = '/cgi-bin/guest.cgi';

var script = path.join(__dirname, '/cgi-bin/guest.cgi');

//var re = /\s*Content-?\w+\:\s.*/g;
var re = /^.*?[\r|\n]{2}/;


  app.set('port', process.env.PORT || 3000);


app.get(script_name, function(req, res){
      var count=0;
      perl(script,req,null,function(err,data){
       var header = {'Content-Type':'text/html'};
                 
			   if(err){
                console.log(err);
				}
                 res.header(header);
                 res.write(data);
                 res.end();
				});                    
   });

app.post(script_name, function(req, res){
         var count=0;
       perl(script,req,null,function(err,data){
		 var content,header = {'Content-Type':'text/html'};
       if(err){              
                console.log(err);
				}                
                 res.header(header);
                 res.write(data);
                 res.end();
       });
   });
 
http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
