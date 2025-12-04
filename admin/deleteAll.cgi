#!/usr/bin/ruby

$stdout.sync = true
$stderr.reopen $stdout

print "content-type: text/html\r\n\r\n"

require 'cgi'
require 'stringio'
require 'mysql2'

cgi = CGI.new("html5")

puts "<html>"
puts "<head>"
puts "<link rel='stylesheet'; href='styles.css'>"

db = Mysql2::Client.new(:host=>'10.20.3.4',:username=> 'dbms_cg',:password => 'cg_27_levan', :database=> 'dbms_cg_dbA')

if cgi['decision'] == 'yes'
    db.query("DELETE FROM Passengers;")
    db.query("DELETE FROM Boarding_Info;")
    puts "<meta http-equiv='refresh' content='3;url=admin.cgi'>"
    puts "<title>DELETED</title></head>"
    puts "<body>"
    puts "<h2>ALL ROWS DELETED</h2>"
elsif cgi['decision'] == 'no'
    puts "<meta http-equiv='refresh' content='0;url=admin.cgi'>"
else
    puts "<title>Delete All</title></head>"
    puts "<body>"
    puts "<header class='header'>"
    puts "<h1>DELETE ALL</h1>"
    puts "</header>"
    puts "<div class='content3'>"
    puts "<form method='post' action='deleteAll.cgi'>"
    puts "<legend>Are you sure you want to Delete Everything in our Database?</legend><br>"
    puts "<input type='radio' name='decision' value='no' checked> No, nevermind <br>"
    puts "<input type='radio' name='decision' value='yes' > Yes <br><br>"
    puts "<input type='submit'>"
    puts "</form>"
end
puts "</body>"
puts "</html>"