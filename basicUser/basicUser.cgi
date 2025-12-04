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
puts "<title>Options</title>"
puts "</head>"
puts "<body>"
puts "<header class='header'>"
puts "<h1>Basic Options</h1>"
puts "<h2>Titanic Tables</h2>"
puts "</header>"
puts "<div class='content2'>"
puts "<form method='post' action='basicUser.cgi'>"
puts "<legend>What type of query would you like to make?</legend><br>"
puts "<a href='select.cgi'> Select </a><br>"
puts "<a href='viewAll.cgi'> View Current Database State </a><br>"
puts "</form>"
puts "</div>"
puts "</body>"
puts "</html>" 