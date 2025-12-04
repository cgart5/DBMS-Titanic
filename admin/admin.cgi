#!/usr/bin/ruby
#file sends user to the operation that they would like to make

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
puts "<h1>Admin Options</h1>"
puts "<h2>Titanic Tables</h2>"
puts "</header>"
puts "<div class='content2'>"
puts "<form method='post' action='admin.cgi'>"
puts "<legend>What type of query would you like to make?</legend><br>"
puts "<a href='select.cgi'> Select </a><br>"
puts "<a href='calculations.cgi'> Find Total, Sums, and Averages </a><br>"
puts "<a href='insert.cgi'> Insert Single Row </a><br>"
puts "<a href='insertFile.cgi'> Insert File </a><br>"
puts "<a href='update.cgi'> Update </a><br>"
puts "<a href='deleteRow.cgi'> Delete Row </a><br>"
puts "<a href='deleteRows.cgi'> Delete Multiple Rows </a><br>"
puts "<a href='deleteAll.cgi'> Delete All </a><br>"
puts "<a href='viewAll.cgi'> View Current Database State </a><br>"
puts "</form>"
puts "</div>"
puts "</body>"
puts "</html>" 