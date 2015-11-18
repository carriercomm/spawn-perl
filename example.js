var Perlcgi = require('./index').spawnPerlCGI;
var express = require('express')
  ,http = require('http')
  ,url = require('url')
  ,path = require('path');
var app = express();
var script_name = '/cgi-bin/guest.cgi';

var script = path.join(__dirname, '/cgi-bin/guest.cgi');

  app.set('port', process.env.PORT || 3000);


app.get(script_name, function(req, res){
      var perl = new Perlcgi(script,req,null,function(err,data){
       
       
                 
			   if(err){
                console.log(err);
				}
                 //console.log(perl.getHeader());
                 res.header(perl.getHeader());
                 res.write(data);
                 res.end();
				});                    
   });

app.post(script_name, function(req, res){
       var perl = new Perlcgi(script,req,null,function(err,data){
		 
       if(err){              
                console.log(err);
				}                
                 res.header(perl.getHeader());
                 res.write(data);
                 res.end();
       });
   });
 
http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});
